from thread_class import BtdxMovie
from collections import OrderedDict
import time

base_url = r'https://www.btdx8.com/'

all_url = OrderedDict()
used_url = set()
movie_url = set()
all_url[base_url] = [0, 0]
thread_list = []
treads_num = 20

while thread_list or all_url:
    for t in thread_list:
        if not t.is_alive():
            thread_list.remove(t)
    while len(thread_list) < treads_num and all_url:
        t = BtdxMovie(all_url, used_url, movie_url, 'Thread-{}'.format(time.time()))
        t.start()
        thread_list.append(t)
    time.sleep(0.1)


print(movie_url)
