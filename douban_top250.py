import re
import json
import requests
from multiprocessing import Pool, Lock
from requests.exceptions import RequestException


pattern_str = ('<li.*?item.*?<em class="">(\d+)</em>.*?href="(.*?)".*?src="(.*?)".*?title">(.*?)</span>.*?'
               'bd.*?class="">(.*?)<br>(.*?)</p>.*?average">(.*?)</span>(.*?)</li>')
abstract_str = '<span.*?inq">(.*?)</span>'

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
    abstract_pattern = re.compile(abstract_str, re.S)
    for result in results:
        abstract = re.search(abstract_pattern, result[7])
        yield {
            'rank': result[0],
            'link': result[1],
            'img_src': result[2],
            'title': result[3],
            'info': result[4].strip().replace("&nbsp;", " ") + "\n" + result[5].strip().replace("&nbsp;", " "),
            'score': result[6],
            'abstract': abstract.group(1) if abstract is not None else ''
        }


def write_to_file(item):
    lock.acquire()
    with open("datas/douban_top250.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    lock.release()


def main(offset):
    url = "https://movie.douban.com/top250?start=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


def init(g_lock):
    global lock
    lock = g_lock


if __name__ == "__main__":
    lock = Lock()
    pool = Pool(initializer=init, initargs=(lock,))
    pool.map(main, [x * 25 for x in range(10)])
    pool.close()
    pool.join()
    # for i in range(10):
    #     main(i * 25)
