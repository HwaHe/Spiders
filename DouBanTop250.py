# @Time    : 2020/4/12 23:37
# @Author  : hwa
# @File    : DouBanTop250.py
# Crawl Douban top250 movies with requests and re
import json
import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool

pattern_str = ('<li.*?item.*?<em class="">(\d+)</em>.*?href="(.*?)".*?src="(.*?)".*?title">(.*?)</span>.*?'
               'bd.*?class="">(.*?)<br>(.*?)</p>.*?average">(.*?)</span>.*?inq">(.*?)</span>.*?</li>')
headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/80.0.3987.163 Safari/537.36'),
}


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("Crawl failed when crawling a page")
        return None


def parse_one_page(html):
    pattern = re.compile(pattern_str, re.S)
    results = re.findall(pattern, html)
    for result in results:
        yield {
            'rank': result[0],
            'link': result[1],
            'img_src': result[2],
            'title': result[3],
            'info': result[4].strip().replace("&nbsp;", " ") + "\n" + result[5].strip().replace("&nbsp;", " "),
            'score': result[6],
            'abstract': result[7]
        }


def write_to_file(item):
    print(item)
    with open("Datas/DouBanTop250.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main(offset):
    url = "https://movie.douban.com/top250?start=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == "__main__":
    # pool = Pool()
    # pool.map(main, [x*25 for x in range(10)])
    for i in range(10):
        main(i*25)
