import geocoder
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat
from news.models import News
from settings import development as settings


class NewsUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        towns = ['Гатчина', 'Санкт-Петербург']
        result = []
        new_news = News.objects.filter(is_new=True)
        for news in new_news:
            links = []
            if news.address:
                for address in news.address:
                    if address == 'Гатчина':
                        link = Chat.objects.filter(city=address.strip()).values('chat_id')
                    else:
                        if towns[0] in address:
                            crd = get_coordinates_from_address_gtn(address)
                            adrs = get_address_from_coordinates_gtn(crd)
                        elif towns[1] in address:
                            crd = get_coordinates_from_address_spb(address)
                            adrs = get_address_from_coordinates_spb(crd)
                        chats = Chat.objects.all()
                        try:
                            link = chats.filter(city=adrs.get('city').strip(), street=adrs.get('street').strip(),
                                                house_number=adrs.get('house').strip()).values('chat_id')
                        except AttributeError:
                            link = chats.filter(city=adrs.get('city').strip()).values('chat_id')
                    for item in link:
                        if item:
                            links.append(item.get('chat_id'))
                    links = set(links)
                    links = list(links)
            else:
                link = news.chats.all().values('chat_id')
                for item in link:
                    if item:
                        links.append(item.get('chat_id'))
                links = set(links)
                links = list(links)
            result.append({
                'id': news.id,
                'title': news.title,
                'text': news.text,
                'chat_links': links,
            })
        return Response(result)


def get_coordinates_from_address_spb(address):
    kinds = ['house', 'district', 'locality']
    for kind in kinds:
        geocode_yandex = geocoder.yandex(
            address,
            method='reverse',
            kind=kind,
            lang='RU',
            key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
        )
        try:
            lat = float(geocode_yandex.lat)
            lng = float(geocode_yandex.lng)
        except:
            continue
        return [lat, lng]


def get_coordinates_from_address_gtn(address):
    kinds = ['house', 'locality']
    for kind in kinds:
        geocode_yandex = geocoder.yandex(
            address,
            method='reverse',
            kind=kind,
            lang='RU',
            key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
        )
        try:
            lat = float(geocode_yandex.lat)
            lng = float(geocode_yandex.lng)
        except:
            continue
        return [lat, lng]


def get_address_from_coordinates_gtn(crd):
    kinds = ['house', 'locality']
    for kind in kinds:
        geocode_yandex = geocoder.yandex(
            crd,
            method='reverse',
            kind=kind,
            lang='RU',
            key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
        )
        yandex_address_array = geocode_yandex.address.split(',')
        if len(yandex_address_array) > 3:
            result = {
                'city': yandex_address_array[2].strip(),
                'street': yandex_address_array[3].strip(),
                'house': yandex_address_array[4].strip(),
            }
        else:
            result = {
                'city': yandex_address_array[2].strip(),
            }
        return result


def get_address_from_coordinates_spb(crd):
    kinds = ['house', 'district', 'locality']
    result = {}
    for kind in kinds:
        geocode_yandex = geocoder.yandex(
            crd,
            method='reverse',
            kind=kind,
            lang='RU',
            key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
        )
        yandex_address_array = geocode_yandex.address.split(',')
        print(yandex_address_array)
        if len(yandex_address_array) == 4:
            result = {
                'city': yandex_address_array[1].strip(),
                'street': yandex_address_array[2].strip(),
                'house': yandex_address_array[3].strip(),
            }
            geocode_mapquest = geocoder.mapquest(
                crd,
                method='reverse',
                key=settings.MAPQUEST_MAP_KEY
            )
            result.update({'postal': geocode_mapquest.postal})
        else:
            result = {
                'city': yandex_address_array[1].strip(),
            }
    return result


class NewsPostCompleteView(APIView):
    def post(self, request, *args, **kwargs):
        news_id = kwargs.get('id')
        news = News.objects.get(id=news_id)
        news.is_new = False
        news.save()
        return Response('Ok', status=status.HTTP_200_OK)

