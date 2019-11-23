import requests
from bs4 import BeautifulSoup as bs
import os

from hackernews.models import Post

news_url = 'https://news.ycombinator.com/'
posts_api_limit = os.environ.get('POSTS_API_LIMIT', 5)
posts_db_limit = os.environ.get('POSTS_DB_LIMIT', None)


def delete_old_posts():
    current_count = Post.objects.count()
    if current_count + 30 > posts_db_limit:
        count_to_remove = current_count + 30 - posts_db_limit
        posts_to_remove = Post.objects.values_list('pk')[:count_to_remove]
        Post.objects.filter(pk__in=posts_to_remove).delete()


def scrap():
    responce = requests.get(news_url)
    if responce.status_code != 200:
        raise ConnectionError(f'{news_url} status code: {responce.status_code}')
    html = responce.content
    soup = bs(html, 'html.parser')
    posts = soup.find_all('a', class_='storylink')
    if not posts:
        raise ConnectionError(f'No posts found at page {news_url}')
    if not len(posts) == 30:
        raise ConnectionError(f'Page {news_url} contains only {len(posts)} posts of 30')

    if posts_db_limit:
        delete_old_posts()

    for post in reversed(posts):
        title = post.text
        url = post['href']
        Post.create(title, url)


def get(params):
    force = params.get('force')
    force = force is True or force == '1' or force == 'true' or force == 'True'

    if force or not Post.objects.exists():
        scrap()
    query = Post.objects

    if params.get('order'):
        query = query.order_by(params.get('order', 'created'))

    offset = int(params.get('offset', 0))
    limit = int(params.get('limit', posts_api_limit))
    limit = offset + limit

    return query.all()[offset:limit]
