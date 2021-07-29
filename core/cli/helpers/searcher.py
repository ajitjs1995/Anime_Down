"""
All the search algorithms for all the providers available in AnimDL.
"""

import re

import lxml.html as htmlparser

from ...config import *

NINEANIME_URL_SEARCH = NINEANIME + "search"

ANIME1_SEARCH_AJAX = ANIME1 + "/home/default/"

ANIMEPAHE_URL_CONTENT = ANIMEPAHE + "anime/%s"
ANIMEPAHE_URL_SEARCH_AJAX = ANIMEPAHE + "api"

ANIMEOUT_URL_SEARCH_AJAX = ANIMEOUT + "wp-admin/admin-ajax.php"

ANIMIX_URL_SEARCH_API = "https://cdn.animixplay.to/api/search"

ANIMIX_URL_SEARCH_POST = "https://v1.zv5vxk4uogwdp7jzbh6ku.workers.dev/"
ANIMIX_URL_CONTENT = ANIMIXPLAY.rstrip('/')

GOGOANIME_URL_SEARCH = GOGOANIME + "/search.html?"

TENSHI_URL_SEARCH_POST = TENSHI + "anime/search"

TWIST_URL_CONTENT_API = "https://api.twist.moe/api/anime"
TWIST_URL_CONTENT = TWIST + "a/"

WAF_TOKEN = re.compile(r"(\d{64})")
WAF_SEPARATOR = re.compile(r"\w{2}")


def search_9anime(session, query):
    with session.get(NINEANIME) as cloudflare_page:
        waf_token = ''.join(chr(int(c, 16)) for c in WAF_SEPARATOR.findall(
            WAF_TOKEN.search(cloudflare_page.text).group(1)))

    with session.get(NINEANIME_URL_SEARCH, params={'keyword': query}, headers={'cookie': 'waf_cv=%s' % waf_token}) as nineanime_results:
        parsed = htmlparser.fromstring(nineanime_results.text)

    for results in parsed.xpath(
            '//ul[@class="anime-list"]/li/a[@class="name"]'):
        yield {'anime_url': NINEANIME.rstrip('/') + results.get('href'), 'name': results.text_content()}


def search_animepahe(session, query):
    with session.get(ANIMEPAHE_URL_SEARCH_AJAX, params={'q': query, 'm': 'search'}) as animepahe_results:
        content = animepahe_results.json()

    for results in content.get('data', []):
        yield {'anime_url': ANIMEPAHE_URL_CONTENT % results.get('session'), 'name': results.get('title')}


def search_animeout(session, query):
    with session.get(ANIMEOUT, params={'s': query}) as animeout_results:
        content = htmlparser.fromstring(animeout_results.text)

    for result in content.xpath('//h3[@class="post-title entry-title"]/a'):
        yield {'anime_url': result.get('href'), 'name': result.text_content()}


def search_animixplay(session, query):
    with session.get(GOGOANIME_URL_SEARCH, params={'keyword': query}) as gogoanime_results:
        parsed = htmlparser.fromstring(gogoanime_results.text)

    for results in parsed.xpath('//p[@class="name"]/a'):
        yield {'anime_url': ANIMIXPLAY + "v1" + results.get('href')[9:], 'name': results.get('title')}


def search_gogoanime(session, query):
    with session.get(GOGOANIME_URL_SEARCH, params={'keyword': query}) as gogoanime_results:
        parsed = htmlparser.fromstring(gogoanime_results.text)

    for results in parsed.xpath('//p[@class="name"]/a'):
        yield {'anime_url': GOGOANIME.strip('/') + results.get('href'), 'name': results.get('title')}


def search_twist(session, query):
    with session.get(TWIST_URL_CONTENT_API, headers={'x-access-token': '0df14814b9e590a1f26d3071a4ed7974'}) as content:
        animes = content.json()

    def searcher(
        q, content): return any(
        [
            q.lower() in (
                content.get('title') or '').lower(), q.lower() in (
                    content.get('alt_title') or '').lower(), q.lower() in (
                        content.get(
                            'slug', {}).get('slug') or '').lower(), ])

    for anime in animes:
        if searcher(query, anime):
            yield {'anime_url': TWIST_URL_CONTENT + anime.get('slug', {}).get('slug'), 'name': anime.get('title', '')}


def search_anime1(session, query):
    with session.get(ANIME1_SEARCH_AJAX, params={'query': query}, headers={'x-requested-with': 'XMLHttpRequest'}, verify=False) as api_content:
        results = api_content.json()

    for slug, name in zip(results.get('data'), results.get('suggestions')):
        yield {'anime_url': ANIME1 + "watch/" + slug, 'name': name}


def search_tenshi(session, query):
    with session.get(TENSHI) as tenshi_page:
        session_id = tenshi_page.cookies.get('tenshimoe_session')
        token = htmlparser.fromstring(tenshi_page.text).xpath(
            '//meta[@name="csrf-token"]')[0].get('content')

    with session.post(TENSHI_URL_SEARCH_POST, data={'q': query}, headers={'x-requested-with': 'XMLHttpRequest', 'x-csrf-token': token, 'referer': 'https://tenshi.moe/', 'cookie': 'tenshimoe_session={}'.format(session_id)}) as ajax_content:
        results = ajax_content.json()

    for result in results:
        yield {'name': result.get('title'), 'anime_url': result.get('url')}


link = {
    '9anime': search_9anime,
    'anime1': search_anime1,
    'animepahe': search_animepahe,
    'animeout': search_animeout,
    'animixplay': search_animixplay,
    'gogoanime': search_gogoanime,
    'tenshi': search_tenshi,
    'twist': search_twist,
}

get_searcher = link.get
