from thread_class import BtdxMovie
from collections import OrderedDict
import time


def main(max_treads_num=20):
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


if __name__ == '__main__':
    main()
