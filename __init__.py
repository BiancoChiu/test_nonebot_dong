import httpx
from nonebot import get_plugin_config, get_bot, on_command
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot_plugin_apscheduler import scheduler

from .config import Config
from .get_dong_puzzle import *

__plugin_meta__ = PluginMetadata(
    name="dong",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


dong = on_command('dong')

@dong.handle()
async def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "dong_puzzle.csv")
    article_url = pd.read_csv(file_path).iloc[0, -1]
    url = get_image_url(article_url)
    await dong.finish(MessageSegment.image(url))


GROUP_ID = [983876901, 1002183040]

@scheduler.scheduled_job("cron", hour=22, minute=35)
async def send_group_message():
    bot = get_bot()
    date, title, url = get_dong_puzzle()
    message = Message(
        MessageSegment.text(f"[{date}]{title}\n火冬老师更新咚咚谜啦～快和鸮鸮子一起尝试一下吧～") +  
        MessageSegment.image(url)
    )
    for group in GROUP_ID:
        await bot.send_group_msg(group_id=group, message=message)
        await bot.send_group_msg(group_id=group, message='ml')


TEST_GROUP_ID = [983876901]

# @scheduler.scheduled_job("cron", hour=17, minute=35)
# async def test_dong():
#     bot = get_bot()
#     date, title, url = get_dong_puzzle()
#     message = Message(
#         MessageSegment.text(f"[{date}]{title}\n火冬老师更新咚咚谜啦～快和鸮鸮子一起尝试一下吧～") +
#         MessageSegment.image(url)
#     )
#     for group in TEST_GROUP_ID:
#         await bot.send_group_msg(group_id=group, message=message)
#         await bot.send_group_msg(group_id=group, message='ml')
