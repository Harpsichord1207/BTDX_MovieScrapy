from threading import Thread
import requests
from logger import thread_info_logger
import re


class BtdxMovie(Thread):

    def __init__(self, all_url, used_url, movie_url, thread_name='MyThread'):
        super(BtdxMovie, self).__init__()
        self.all_url = all_url
        self.used_url = used_url
        self.movie_url = movie_url
        self.name = thread_name

    def run(self):
        while 1:
            try:
                url, info = self.all_url.popitem(last=False)
                depth, retry = info
                if depth > 10 or retry > 5:
                    continue
            except KeyError:
                continue
            info = '[{}] [Depth: {}]current url: '.format(self.name, depth) + url
            thread_info_logger.info(info)
            depth += 1
            try:
                html = requests.get(url).text
                new_url = re.findall('href="(https://.*?)"', html)
                for u in new_url:
                    if '#' in u:
                        u = u.split('#')[0]
                    if '?' in u:
                        u = u.split('?')[0]
                    if u in self.used_url or u in self.all_url:
                        continue
                    self.all_url[u] = [depth, retry]
                    if re.match('https://www.btdx8.com/torrent/.*?html', u):
                        self.movie_url.add(u)
                thread_info_logger.info('[{}] current url succeed.'.format(self.name))
            except Exception:
                thread_info_logger.info('[{}] current url failed for {} times.'.format(self.name, retry))
                self.all_url[u] = [depth-1, retry+1]
            self.used_url.add(url)
            info = ('[{}]'.format(self.name), 'ALL:', str(len(self.all_url)),
                    'USED:', str(len(self.used_url)), 'MOV:', str(len(self.movie_url)))
            info = ' '.join(info)
            thread_info_logger.info(info)
