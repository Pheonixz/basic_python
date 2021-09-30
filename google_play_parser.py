import json
import asyncio
import aiohttp
import bs4
import requests
from pprint import pprint


class AppSearch:

    def __init__(self, keyword):
        self.search_url = "https://play.google.com/store/search"
        self.main_url = "https://play.google.com"
        self.keyword = keyword

    def get_query_results(self):
        return requests.get(self.search_url, params={"q": self.keyword, "c": "apps"}).text

    def get_bs4_soup(self):
        return bs4.BeautifulSoup(self.get_query_results(), "html.parser")

    def get_apps_div_blocks(self):
        return self.get_bs4_soup().find_all("div", class_="mpg5gc")

    def get_apps_urls(self):
        urls = []

        for block in self.get_apps_div_blocks():
            a_href = block.find("div", class_="wXUyZd").find("a", class_="poRVub").get("href")
            urls.append(f"{self.main_url}{a_href}")

        return urls


class AppScrapper:

    def __init__(self, urls_list, keyword):
        self.urls_list = urls_list
        self.keyword = keyword
        self.queries_result_list = []
        self.resulting_apps = {}

    async def get(self, url, session):
        async with session.get(url=url, params={"h1": "ru"}) as resp:
            self.queries_result_list.append(
                f'<div class="url-for-parsing">{url}</div>{await resp.text(encoding="utf-8")}'
            )

    async def main(self):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.get(url, session) for url in self.urls_list])

    @staticmethod
    def get_parsing_done(soup):
        try:
            transitional_results = [
                soup.find("h1", class_="AHFaub").find("span").text.replace(u"\u202a", u""),
                soup.find("div", class_="url-for-parsing").text,
                soup.find("a", class_="hrTbp R8zArc").text,
                soup.find("a", class_="hrTbp R8zArc", itemprop="genre").text,
                soup.find("div", jsname="sngebd").text.replace(u"\xa0", u"").replace(u"\t", u""),
                soup.find("div", class_="BHMmbe").text,
                soup.find("span", class_="EymY4b").find("span", class_="").text,
                soup.find("span", class_="htlgb").text
            ]
        except AttributeError:
            transitional_results = ["По", "этому", "урлу", "возникла", "ошибка", "!"]

        return transitional_results

    def get_results_written(self, transitional_results):
        self.resulting_apps[transitional_results[0]] = {
            "Название": transitional_results[0],
            "url-страница": transitional_results[1],
            "автор": transitional_results[2],
            "категория": transitional_results[3],
            "описание": transitional_results[4],
            "средняя оценка": transitional_results[5],
            "количество оценок": transitional_results[6],
            "последнее обновление": transitional_results[7]
        }

    def get_results_filtered(self, app_info_list):
        for line in app_info_list:
            if self.keyword in line.lower():
                self.get_results_written(app_info_list)
                break

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.main())
        soups = [bs4.BeautifulSoup(html, "html.parser") for html in self.queries_result_list]
        transitional_results = [self.get_parsing_done(soup) for soup in soups]
        [self.get_results_filtered(result_list) for result_list in transitional_results]

        return json.dumps(self.resulting_apps, ensure_ascii=False)


if __name__ == "__main__":
    search_word = input("Введите слово для поиска >>>: ")
    pprint(AppScrapper(AppSearch(search_word).get_apps_urls(), search_word).run())