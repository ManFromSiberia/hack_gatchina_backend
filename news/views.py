import geocoder
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat
from news.models import News


class NewsUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        result = []
        new_news = News.objects.filter(is_new=True)
        for news in new_news:
            links = []
            if news.address:
                for address in news.address:
                    if 'ул' in address:
                        try:
                            geocode_yandex = geocoder.yandex(
                                address,
                                method='reverse',
                                kind='house',
                                lang='RU',
                                key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
                            )
                            lat = float(geocode_yandex.lat)
                            lng = float(geocode_yandex.lng)
                            adrs = get_address_from_coordinates([lat, lng], False)
                        except ValueError:
                            continue
                    else:
                        geocode_yandex = geocoder.yandex(
                            address,
                            method='reverse',
                            kind='locality',
                            lang='RU',
                            key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
                        )
                        lat = float(geocode_yandex.lat)
                        lng = float(geocode_yandex.lng)
                        adrs = get_address_from_coordinates([lat, lng], True)
                    chats = Chat.objects.all()
                    try:
                        link = chats.filter(city=adrs.get('city'), street=adrs.get('street'),
                                            house_number=adrs.get('house'))
                    except:
                        link = chats.filter(city=adrs.get('city'))
                    links.extend(link)
            if not links:
                links = Chat.objects.all()
            result.append({
                'title': news.title,
                'text': news.text,
                'chat_links': links,
            })
            news.is_new = False
            news.save()

        return Response(result)


def get_address_from_coordinates(coordinates, is_city):
    if is_city:
        geocode_yandex = geocoder.yandex(
            coordinates,
            method='reverse',
            kind='locality',
            lang='RU',
            key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
        )
        yandex_address_array = geocode_yandex.address.split(',')
        locality = yandex_address_array[2]
        street = ''
        house = ''
    else:
        geocode_yandex = geocoder.yandex(
            coordinates,
            method='reverse',
            kind='house',
            lang='RU',
            key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
        )
        yandex_address_array = geocode_yandex.address.split(',')
        locality = yandex_address_array[2]
        street = yandex_address_array[3]
        house = yandex_address_array[4]
    return {
        'city': locality,
        'street': street,
        'house': house,
    }
