import json

from django.conf import settings
from django.contrib.gis.geos import Point
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import asyncio
from telethon import TelegramClient
import geocoder
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest, EditAdminRequest
from telethon.tl.types import ChatAdminRights

from chat.models import Chat
from chat.serializers import ChatDetailSerializer


def get_chats_by_address(address, is_private_house=None):
    chats = Chat.objects.all()
    if is_private_house:
        result = chats.filter(postal_code=address.get('postal'))
    else:
        result = chats.filter(
            city=address.get('city'),
            street=address.get('street'),
            house_number=address.get('house')
        )
    return result


def get_address_from_coordinates(coordinates):
    geocode_yandex = geocoder.yandex(
        coordinates,
        method='reverse',
        kind='district',
        lang='RU',
        key=settings.YANDEX_MAP_KEY
    )
    yandex_address_array = geocode_yandex.address.split(',')
    district = ''
    locality = ''
    for address_item in yandex_address_array:
        if 'район' in address_item:
            district = address_item.replace('район', '').strip()
        elif 'муниципальный округ' in address_item:
            locality = address_item.replace('муниципальный округ', '').strip()

    geocode_yandex = geocoder.yandex(
        coordinates,
        method='reverse',
        kind='house',
        lang='RU',
        key=settings.YANDEX_MAP_KEY
    )

    yandex_address_array = geocode_yandex.address.split(',')
    street = yandex_address_array[-2].strip()
    house = yandex_address_array[-1].strip()
    if 'область' in yandex_address_array[1].strip():
        city = yandex_address_array[2].strip()
    else:
        city = yandex_address_array[1].strip()
    geocode_mapquest = geocoder.mapquest(
        coordinates,
        method='reverse',
        key=settings.MAPQUEST_MAP_KEY
    )
    postal = geocode_mapquest.postal
    return {
        'district': district,
        'locality': locality,
        'postal': postal,
        'street': street,
        'house': house,
        'city': city
    }


async def create_channel(chat_name):
    client = TelegramClient('allmemes_app', settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    # await client.start()
    await client.connect()
    channel = await client(CreateChannelRequest(
        chat_name,
        'Специально созданный чат для вас, сервисом Мой Двор\n'
        'По хештегу #жалоба вы можете написать свою претензию, которая будет направлена администрации',
        broadcast=False,
        megagroup=True
    ))
    goshan_bot = await client.get_input_entity('my_dvorbot')
    await client(InviteToChannelRequest(
        channel.chats[0].id,
        [goshan_bot]
    ))
    rights = ChatAdminRights(
        post_messages=True,
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        edit_messages=True
    )
    await client(EditAdminRequest(channel.chats[0].id, goshan_bot, rights))
    buff = await client.get_entity(channel.chats[0].id)
    await client.disconnect()
    response = requests.get(
        f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/exportChatInviteLink?chat_id=-100{buff.id}'
    )
    return {
        'chat_id': f'-100{buff.id}',
        'invite_link': json.loads(response.text).get('result')
    }


class ChatsFromCoordinatesView(APIView):
    def post(self, request, *args, **kwargs):
        coordinates = request.data.get('coordinates', None)
        is_private_house = request.data.get('is_private_house', None)

        if coordinates:
            address = get_address_from_coordinates(coordinates)
            chats = ChatDetailSerializer(get_chats_by_address(address, is_private_house), many=True).data
            return Response(chats)
        else:
            return Response(
                {'error': 'Предоставлены некорректные данные'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateNewChatView(APIView):
    def post(self, request, *args, **kwargs):
        coordinates = request.data.get('coordinates', None)
        is_private_house = request.data.get('is_private_house', None)
        social_network = request.data.get('social_network', -1)

        if coordinates and social_network != -1:
            address = get_address_from_coordinates(coordinates)

            if not is_private_house:
                chat_name = f"Чат {address.get('street')}, {address.get('house')}"
                chat_identifications = asyncio.new_event_loop().run_until_complete(create_channel(chat_name))

                chat = Chat.objects.create(
                    social_network=social_network,
                    city=address.get('city'),
                    city_district=address.get('district'),
                    postal_code=address.get('postal'),
                    street=address.get('street'),
                    house_number=address.get('house'),
                    coordinates=Point(list(reversed(coordinates))),
                    chat_invite_link=chat_identifications.get('invite_link'),
                    chat_id=chat_identifications.get('chat_id')
                )
            else:
                chat_name = f"Чат почтовый индекс {address.get('postal')}"
                chat_identifications = asyncio.new_event_loop().run_until_complete(create_channel(chat_name))

                chat = Chat.objects.create(
                    social_network=social_network,
                    city=address.get('city'),
                    city_district=address.get('district'),
                    postal_code=address.get('postal'),
                    coordinates=Point(list(reversed(coordinates))),
                    is_private_house=is_private_house,
                    chat_invite_link=chat_identifications.get('invite_link'),
                    chat_id=chat_identifications.get('chat_id')
                )
            return Response(ChatDetailSerializer(chat).data)
        else:
            return Response(
                {'error': 'Предоставлены некорректные данные'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChatLinkView(APIView):
    def get(self, request, *args, **kwargs):
        chat_id = int(kwargs.get('chat_id'))
        chat = Chat.objects.get(id=chat_id)
        return Response(ChatDetailSerializer(chat).data)
