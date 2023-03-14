# if you can read this, this meant you use code from Ubot | Ram Project
# this code is from somewhere else
# please dont hestitate to steal it
# because Ubot and Ram doesn't care about credit
# at least we are know as well
# who Ubot and Ram is
#
#
# kopas repo dan hapus credit, ga akan jadikan lu seorang developer
# ©2023 Ubot | Ram Team
import random
import time
import traceback
from sys import version as pyver
from datetime import datetime
import os
import shlex
import textwrap
import asyncio 
from gc import get_objects

from pyrogram import __version__ as pyrover
from pyrogram.enums import ParseMode
from pyrogram import *
from pyrogram.types import *
from ubotlibs.ubot.helper.data import Data
from ubotlibs.ubot.helper.inline import inline_wrapper, paginate_help
from Ubot.core.db import *
from ubotlibs.ubot.database.accesdb import *
from pyrogram.raw.functions import Ping
from ubotlibs import BOT_VER
from Ubot import CMD_HELP, StartTime, app, ids, cmds


WHITE = [1970636001, 902478883, 2067434944, 1947740506, 1897354060, 1694909518, 5077932806]

BLACK = [951454060, 2099942562]


def support():
    buttons = [
        [
            InlineKeyboardButton(text="Support", url=f"https://t.me/kynansupport"),
            InlineKeyboardButton(text="Deploy", url=f"t.me/ProjectUbot?start"),
        ],
    ]
    return buttons

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time
    

async def alive_function(message, answers):
    users = 0
    group = 0
    async for dialog in message._client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            users += 1
        elif dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            group += 1
    if message._client.me.id in BLACK:
        status = "OWNER"
    elif message._client.me.id in WHITE:
        status = "ADMINS"
    else:
        status = "MEMBER"
    start = datetime.now()
    buttons = support()
    ex = await message._client.get_me()
    user = len(ids)
    user_active_time = await get_active_time(ex.id)
    remaining_days = (expired_date - datetime.now()).days
    await message._client.invoke(Ping(ping_id=0))
    ping = (datetime.now() - start).microseconds / 1000
    uptime = await get_readable_time((time.time() - StartTime))
    expired_date = await get_expired_date(user_id)
    if expired_date is None:
        expired_date = "Belum di tetapkan"
    else:
        remaining_days = (expired_date - datetime.now()).days
    msg = (
        f"<b>NEW UBOT</b>\n"
        f"   <b> Status : {status} </b>\n"
        f"   <b> Users :</b> <code>{user}</code>\n"
        f"   <b> Ping DC :</b> <code>{ping} ms</code>\n"
        f"   <b> Users Count :</b> <code>{users} users</code>\n"
        f"   <b> Groups Count :</b> <code>{group} group</code>\n"
        f"   <b> Expired :</b> <code>{remaining_days}</code>\n"
        f"   <b> Uptime :</b> <code>{uptime}</code>\n")
    answers.append(
        InlineQueryResultArticle(
            title="Alive",
            description="Check Bot's Stats",
            thumb_url="https://telegra.ph/file/8254768833ab62009c125.jpg",
            input_message_content=InputTextMessageContent(
                msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            ),
            reply_markup=InlineKeyboardMarkup(buttons)))
    return answers


async def help_function(answers):
    bttn = paginate_help(0, CMD_HELP, "helpme")
    answers.append(
        InlineQueryResultArticle(
            title="Help Article!",
            input_message_content=InputTextMessageContent(
                Data.text_help_menu.format(len(CMD_HELP))
            ),
            reply_markup=InlineKeyboardMarkup(bttn),
        )
    )
    return answers


@app.on_inline_query()
# @inline_wrapper
async def inline_query_handler(client: Client, query):
    try:
        text = query.query.strip().lower()
        string_given = query.query.lower()
        answers = []
        if text.strip() == "":
            return
        elif string_given.startswith("helper"):
            answers = await help_function(answers)
            await client.answer_inline_query(query.id, results=answers)
        elif text.split()[0] == "alive":
            m = [obj for obj in get_objects() if id(obj) == int(query.query.split(None, 1)[1])][0]
            answers2 = await alive_function(m, answers)
            await client.answer_inline_query(query.id, results=answers2)
    except Exception as e:
        e = traceback.format_exc()
        print(e, "InLine")
      
