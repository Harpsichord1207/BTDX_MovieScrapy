import re
from logger import record_logger


def movie_parser(html):
    try:
        title = re.findall('<h1 class="postli-1">(.*?)</h1>', html)[0]
        movie_name = re.findall('\[(.*?)\]', title)[0]
        movie_category = re.findall('类型(.*?)<br', html)[0]
        movie_category = movie_category.replace(':', '').strip()
        movie_category = movie_category.replace('：', '').strip()
        movie_score = re.findall('豆瓣(.*?)分', title)
        if movie_score:
            movie_score = movie_score[0]
        else:
            movie_score = 'null'
        record = ','.join([movie_name, movie_category, movie_score, title])
        record_logger.info(record)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    import requests
    page = requests.get(r'https://www.btdx8.com/torrent/lzdw_2018.html').text
    print(movie_parser(page))