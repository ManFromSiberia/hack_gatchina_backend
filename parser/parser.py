import re

import requests
from bs4 import BeautifulSoup
from natasha import AddressExtractor
from natasha.markup import show_markup, format_json


class Parser:
    def __init__(self):
        self.url = 'http://radm.gtn.ru'
        self.news_url = self.url + '/events'
        self.html = self.__get_html(self.news_url)

    def __get_html(self, url):
        response = requests.get(url)
        return response.text

    def __get_news_data(self, html, news_id):
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('div', class_='inCenter')
        title = content.find('h1', class_='padd_b20').text.strip()
        text = content.find('div', class_='F17').text.strip()
        adresses = self.__get_address(text)
        return {'title': title, 'text': text, 'news_id': news_id, 'addresses': adresses}

    def __get_last_link(self, html):
        soup = BeautifulSoup(html, 'lxml')
        news = soup.find('div', class_='newscont_l')
        last_news = news.find('div', class_='padd_t10 padd_b10')
        last_link = last_news.find('a').get('href')
        return self.url + last_link

    def __get_all_links(self, html):
        soup = BeautifulSoup(html, 'lxml')
        news = soup.find('div', class_='newscont_l')
        all_news = news.find_all(href=re.compile('/events/news/'))
        all_links = []
        for obj in all_news:
            link = obj.attrs['href']
            all_links.append(self.url + link)
        return all_links

    def get_last_news(self):
        link = self.__get_last_link(self.html)
        return self.__get_news_data(self.__get_html(link), self.__get_news_id(link))

    def get_all_news(self):
        links = self.__get_all_links(self.html)
        for link in links:
            yield self.__get_news_data(self.__get_html(link), self.__get_news_id(link))

    def __get_news_id(self, link):
        return link.split('=')[1]

    def __get_address(self, text):
        results = []
        number = re.compile('^\d+\w?$')
        word = re.compile('^[а-яА-Я]+')
        raw_text = text.split('ул. ')[1:]
        for text in raw_text:
            addresses = text.split(',')
            street = ''
            for part in addresses:
                part = part.strip()
                if re.findall(word, part):
                    street = part.split(' ')[0]
                    part = part.replace('д. ', 'д.')
                    results.append('ул. ' + part)
                elif re.findall(number, part):
                    results.append('ул. ' + street + ' д.' + part)
                elif '-' in part:
                    digits = part.split('-')
                    for i in range(int(digits[0]), int(digits[1]) + 1):
                        results.append('ул. ' + street + ' д.' + str(i))
        return results

    def test_nlp(self, text):
        lines = text.splitlines()
        extractor = AddressExtractor()
        for line in lines:
            matches = extractor(line)
            spans = [_.span for _ in matches]
            facts = [_.fact.as_json for _ in matches]
            show_markup(line, spans)
            print(format_json(facts))

    def demo(self):
        links = [
            '/events/news/?id=5183',
            '/events/news/?id=5184',
            '/events/news/?id=5185',
            '/events/news/?id=5186',
            '/events/news/?id=5187',
        ]
        for link in links:
            yield self.__get_news_data(self.__get_html(self.url + link), self.__get_news_id(link))
