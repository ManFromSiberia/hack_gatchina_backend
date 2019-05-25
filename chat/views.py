from django.conf import settings
from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from telethon import TelegramClient, sync, utils, events
import geocoder

# [60.02833645805045, 30.250738203167884]
# [59.9698057, 30.316310699999995]
from chat.models import Chat
from chat.serializers import ChatDetailSerializer


def get_chats_by_address(address, is_private_house=None):
    chats = Chat.objects.all()
    if is_private_house:
        result = chats.filter(postal_code=address.get('postal'))
    else:
        result = chats.filter(street=address.get('street'), house_number=address.get('house'))
    return result


def get_address_from_coordinates(coordinates):
    geocode_yandex = geocoder.yandex(
        coordinates,
        method='reverse',
        kind='district',
        lang='RU',
        key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
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
        key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
    )

    yandex_address_array = geocode_yandex.address.split(',')
    street = yandex_address_array[-2].strip()
    house = yandex_address_array[-1].strip()
    city = yandex_address_array[1].strip()
    geocode_mapquest = geocoder.mapquest(
        coordinates,
        method='reverse',
        key='OXS9eKFyynkRwSMAaZDPMMJWcuKAZ9GP'
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


def create_chat(social_network):
    if social_network == 0:
        client = TelegramClient('allmemes_app', settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
        client.action()


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
            chat_identification = create_chat(social_network)

            print('Address', address)
            if not is_private_house:
                chat = Chat.objects.create(
                    social_network=social_network,
                    city=address.get('city'),
                    city_district=address.get('district'),
                    postal_code=address.get('postal'),
                    street=address.get('street'),
                    house_number=address.get('house'),
                    coordinates=Point(coordinates),
                    app_chat_identification='test_chat_identification'
                )
            else:
                chat = Chat.objects.create(
                    social_network=social_network,
                    city=address.get('city'),
                    city_district=address.get('district'),
                    postal_code=address.get('postal'),
                    coordinates=Point(coordinates),
                    is_private_house=is_private_house,
                    app_chat_identification='test_chat_identification'
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
