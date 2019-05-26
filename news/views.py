import geocoder
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
                    if towns[0] in address:
                        crd = get_coordinates_from_address_gtn(address)
                        adrs = get_address_from_coordinates_gtn(crd)
                    elif towns[1] in address:
                        crd = get_coordinates_from_address_spb(address)
                        adrs = get_address_from_coordinates_spb(crd)
                    chats = Chat.objects.all()
                    try:
                        link = chats.filter(city=adrs.get('city'), street=adrs.get('street'),
                                            house_number=adrs.get('house')).values('chat_id')
                    except AttributeError:
                        link = chats.filter(city=adrs.get('city')).values('chat_id')
                    links = link
            result.append({
                'title': news.title,
                'text': news.text,
                'chat_links': links,
            })
            news.is_new = False
            news.save()

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
                'city': yandex_address_array[2],
                'street': yandex_address_array[3],
                'house': yandex_address_array[4],
            }
        else:
            result = {
                'city': yandex_address_array[2],
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
        if len(yandex_address_array) == 4:
            result = {
                'city': yandex_address_array[1],
                'street': yandex_address_array[2],
                'house': yandex_address_array[3],
            }
            geocode_mapquest = geocoder.mapquest(
                crd,
                method='reverse',
                key=settings.MAPQUEST_MAP_KEY
            )
            result.update({'postal': geocode_mapquest.postal})
        else:
            result = {
                'city': yandex_address_array[2],
            }
    return result
