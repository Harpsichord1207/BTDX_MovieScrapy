from thread_class import BtdxMovie
from collections import OrderedDict
from logger import dingding_alert
import time


def main(max_treads_num=20):
    dingding_alert('===Program starts===')

    # URL entrance
    base_url = r'https://www.btdx8.com/'

    # The URLs which need to crawl
    all_url = OrderedDict()

    # The URLs which have been crawled
    used_url = dict()

    # The URLs which are move page
    movie_url = set()

    # The key of all_url is url, and value is [depth, retry]
    all_url[base_url] = [0, 1]

    thread_list = []
    thread_id = 0

    def get_info():
        info = ('ALL:', str(len(all_url)), 'USED:', str(len(used_url)), 'MOV:', str(len(movie_url)))
        return info

    while thread_list or all_url:
        for t in thread_list:
            if not t.is_alive():
                thread_list.remove(t)
        while len(thread_list) < max_treads_num and all_url:
            thread_id += 1
            t = BtdxMovie(all_url, used_url, movie_url, 'Thread-{}'.format(str(thread_id).zfill(2)))
            t.start()
            thread_list.append(t)
        time.sleep(0.1)
        if movie_url and len(movie_url) % 1000 == 0:
            dingding_alert(get_info())

    dingding_alert('===Finished===')
    dingding_alert(get_info())


if __name__ == '__main__':
    main(10)
