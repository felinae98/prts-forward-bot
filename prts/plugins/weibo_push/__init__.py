import nonebot

from .config import Config
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

from . import sina
from . import send

from nonebot import require
from nonebot.adapters.cqhttp import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot.log import logger

scheduler: AsyncIOScheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('interval', seconds=30, id='check_weibo')
async def check_weibo():
    if bot_list := list(nonebot.get_bots().values()):
        bot: Bot = bot_list[0]
    else:
        logger.warning('no bot detected')
        return
    new_posts = await sina.fetch_new_post()
    logger.info('fectch new weibo')
    for parsed_text, detail_url, pic_urls in new_posts:
        logger.debug('sending {}'.format(detail_url))
        await send.send_msg(bot, parsed_text, detail_url, pic_urls)
