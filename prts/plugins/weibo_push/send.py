from . import plugin_config
from nonebot.adapters.cqhttp import Bot

async def do_send(bot: Bot, message):
    for group in plugin_config.target_group:
        await bot.call_api('send_group_msg', group_id=group, message=message)

async def send_msg(bot: Bot, text: str, url: str, pics: list[str]):
    text_to_send = "{}\n详情：{}".format(text, url)
    await do_send(bot, text_to_send)
    for pic in pics:
        pic_code = "[CQ:image,file={url}]".format(url=pic)
        await do_send(bot, pic_code)
