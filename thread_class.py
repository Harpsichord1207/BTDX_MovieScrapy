import re
import requests
from threading import Thread
from html_parser import movie_parser
from logger import thread_info_logger
from config import max_depth, max_retry


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
                curr_depth, curr_retry = info
                if curr_depth > max_depth:
                    continue
            except KeyError:
                break
            info = '[{}] [Depth:{}] [Retry:{}]: '.format(self.name, curr_depth, curr_retry) + url
            thread_info_logger.info(info)
            curr_depth += 1
            try:
                html = requests.get(url).text
                if re.match('https://www.btdx8.com/torrent/.*?html', url):
                    if url not in self.movie_url:
                        if movie_parser(url, html):
                            self.movie_url.add(url)
                            info = '[{}] Movie url parse successfully: {}'.format(self.name, url)
                            thread_info_logger.info(info)
                        else:
                            info = '[{}] Movie url parse failed: {}'.format(self.name, url)
                            thread_info_logger.error(info)
                new_url = re.findall('href="(https://.*?)"', html)
                for u in new_url:
                    if not re.match('https://.*?btdx8.com', u):
                        continue
                    if '#' in u:
                        u = u.split('#')[0]
                    if u in self.used_url or u in self.all_url:
                        continue
                    self.all_url[u] = [curr_depth, 0]
                thread_info_logger.info('[{}] Succeed after {} times: {}.'.format(self.name, curr_retry, url))
                self.used_url[url] = 'Succeed'
            except Exception:
                if curr_retry < max_retry:
                    thread_info_logger.critical('[{}] Failed for {} times: {}.'.format(self.name, curr_retry, url))
                    self.all_url[url] = [curr_depth - 1, curr_retry + 1]
                else:
                    thread_info_logger.error('[{}] Totally failed after {} times: {}.'.format(self.name, curr_retry, url))
                    self.used_url[url] = 'Failed'
            info = ('[{}]'.format(self.name), 'ALL:', str(len(self.all_url)),
                    'USED:', str(len(self.used_url)), 'MOV:', str(len(self.movie_url)))
            info = ' '.join(info)
            thread_info_logger.info(info)
