import json
import httpx
import asyncio
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
from nonebot.log import logger
from . import plugin_config

EXIST_POST = set()

async def get_user_post_list(weibo_id: str):
    async with httpx.AsyncClient() as client:
        params = { 'containerid': '107603' + weibo_id}
        res = await client.get('https://m.weibo.cn/api/container/getIndex?', params=params)
        return res.text

def get_user_post_list_sync(weibo_id: str):
    params = { 'containerid': '107603' + weibo_id}
    res = httpx.get('https://m.weibo.cn/api/container/getIndex?', params=params)
    return res.text

def filter_weibo(weibo_raw_text, init=False):
    weibo_dict = json.loads(weibo_raw_text)
    weibos = weibo_dict['data']['cards']
    res = []
    for weibo in weibos:
        if weibo['card_type'] != 9:
            continue
        info = weibo['mblog']
        if init:
            EXIST_POST.add(info['id'])
            continue
        if info['id'] in EXIST_POST:
            continue
        created_time = datetime.strptime(info['created_at'], '%a %b %d %H:%M:%S %z %Y')
        if time.time() - created_time.timestamp() > 60 * 60 * 2:
            continue
        res.append(parse_weibo(weibo))
    return res

def parse_weibo(weibo_dict):
    info = weibo_dict['mblog']
    parsed_text = bs(info['text'], 'html.parser').text
    pic_urls = [img['large']['url'] for img in info.get('pics', [])]
    EXIST_POST.add(info['id'])
    detail_url = 'https://weibo.com/{}/{}'.format(info['user']['id'], info['bid'])
    return parsed_text, detail_url, pic_urls


def init():
    post_list = get_user_post_list_sync(plugin_config.weibo_id)
    filter_weibo(post_list, True)
    logger.info('weibo posts init done')
    logger.info('posts: {}'.format(EXIST_POST))

async def fetch_new_post():
    post_list = await get_user_post_list(plugin_config.weibo_id)
    return filter_weibo(post_list)

if __name__ == '__main__':
    async def test():
        raw_weibo = await get_user_post_list('2152886087')
        filter_weibo(raw_weibo, True)
        for _ in range(100):
            raw_weibo = await get_user_post_list('2152886087')
            filter_weibo(raw_weibo)
            await asyncio.sleep(10)
            print('13')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()

else:
    init()
