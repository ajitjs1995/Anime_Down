import json
import re
from functools import partial

import lxml.html as htmlparser

from ....config import GOGOANIME
from ...helper import construct_site_based_regex

ANIME_RE = construct_site_based_regex(
    GOGOANIME, extra_regex=r"/([^&?/]+)-episode-\d+")

EPISODE_LOAD_AJAX = "https://ajax.gogo-load.com/ajax/load-list-episode"
SITE_URL = GOGOANIME

def get_episode_list(session, anime_id):
    """
    Fetch all the episodes' url from GogoAnime using.
    """
    with session.get(EPISODE_LOAD_AJAX, params={'ep_start': '0', 'ep_end': '2000', 'id': anime_id, }) as episode_page:
        content = htmlparser.fromstring(episode_page.text)

    for episode in content.xpath('//ul[@id="episode_related"]/li/a'):
        yield SITE_URL + episode.get('href', '').strip()


def get_anime_id(html_content):
    content = html_content.xpath('//input[@id="movie_id"]')
    assert content, "No GGA Anime ID found."
    return int(content[0].get('value', 0))


def convert_to_anime_page(url):
    match = ANIME_RE.search(url)
    if match:
        return SITE_URL + "/category/%s" % match.group(1)
    return url

def get_stream_url(session, episode_page_url):

    with session.get(episode_page_url) as response:
        content_parsed = htmlparser.fromstring(response.text)

    streaming = content_parsed.xpath(
        '//div[@class="play-video"]/iframe')[0].get('src')

    with session.get('https:%s' % streaming) as response:
        content = htmlparser.fromstring(response.text)

    url = content.xpath('//li[@data-provider="serverwithtoken"]')[0].get('data-video')

    with session.get(url) as server_load:
        return [{'quality': 'unknown', 'stream_url': urls.group(0), 'headers': {
            'referer': url}} for urls in re.finditer(
                        r"(?<=sources:\[{file: ')[^']+",
                            server_load.text)]

def fetcher(session, url, check):
    """
    Fetching algorithm from [here.](https://github.com/justfoolingaround/anime-radar/blob/master/radar/datacaller/gogoanime.py)
    """
    url = convert_to_anime_page(url)

    with session.get(url) as anime_page:
        content_id = get_anime_id(htmlparser.fromstring(anime_page.text))

    episodes = reversed([*get_episode_list(session, content_id)])

    for index, episode in enumerate(episodes, 1):
        if check(index):
            yield partial(get_stream_url, session, episode), index
