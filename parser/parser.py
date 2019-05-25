import re

import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.url = 'http://radm.gtn.ru'
        self.news_url = self.url + '/events'
        self.html = self.__get_html(self.news_url)

    def __get_html(self, url):
        response = requests.get(url)
        return response.text

    def __get_news_data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('div', class_='inCenter')
        title = content.find('h1', class_='padd_b20').text
        text = content.find('div', class_='F17').text
        return title, text

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
        return self.__get_news_data(self.__get_html(link))

    def get_all_news(self):
        links = self.__get_all_links(self.html)
        for link in links:
            yield self.__get_news_data(self.__get_html(link))
