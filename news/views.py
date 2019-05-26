import geocoder
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat
from chat.views import get_address_from_coordinates
from news.models import News


class NewsUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        result = []
        new_news = News.objects.filter(is_new=True)
        for news in new_news:
            links = []
            if news['address']:
                for address in new_news['address']:
                    geocode_yandex = geocoder.yandex(
                        address,
                        method='reverse',
                        kind='house',
                        lang='RU',
                        key='7bb41e4d-5a27-4b8c-a856-ee56d3284019'
                    )
                    lat = geocode_yandex.lat
                    lng = geocode_yandex.lng
                    adrs = get_address_from_coordinates([lat, lng])
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
                'title': news['title'],
                'text': news['text'],
                'chat_links': links,
            })

        return Response(result)
