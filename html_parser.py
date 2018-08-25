import re
from logger import record_logger


def movie_parser(url, html):
    try:
        title = re.findall('<h1 class="postli-1">(.*?)</h1>', html)[0]
    except IndexError:
        return False

    try:
        movie_name = re.findall('\[(.*?)\]', title)[0]
    except IndexError:
        movie_name = 'null'

    try:
        movie_category = re.findall('类型(.*?)<br', html)[0]
        movie_category = movie_category.replace(':', '').strip()
        movie_category = movie_category.replace('：', '').strip()
    except IndexError:
        movie_category = 'null'

    try:
        movie_score = re.findall('豆瓣(.*?)分', title)[0]
    except IndexError:
        movie_score = 'null'

    record = [movie_name, movie_category, movie_score, title, url]
    record = [e.replace(',', '-') for e in record]
    record = ','.join(record)
    record_logger.info(record)
    return True


if __name__ == '__main__':
    import requests
    page = requests.get(r'https://www.btdx8.com/torrent/lzdw_2018.html').text
    print(movie_parser(page))
