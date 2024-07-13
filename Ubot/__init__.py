import asyncio
import logging
import sys
import time
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict
from aiohttp import ClientSession
from pyrogram.types import Message
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Chat, User
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gpytranslate import Translator
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from Ubot.get_config import get_config

from pyrogram import (
    Client,
    __version__,
    enums
)
from Ubot.logging import LOGGER
from config import *
cmds = None
cmd_help = {}
clients = []
ids = []
sudo_user=[]

trl = Translator()
aiosession = ClientSession()
CMD_HELP = {}
scheduler = AsyncIOScheduler()
StartTime = time.time()
START_TIME = datetime.now()
TEMP_SETTINGS: Dict[Any, Any] = {}
TEMP_SETTINGS["PM_COUNT"] = {}
TEMP_SETTINGS["PM_LAST_MSG"] = {}

LOOP = asyncio.get_event_loop_policy()
event_loop = LOOP.get_event_loop()
asyncio.set_event_loop(event_loop)


BOT_WORKERS = int(get_config("BOT_WORKERS", "4"))
COMMM_AND_PRE_FIX = get_config("COMMM_AND_PRE_FIX", "/")
START_COMMAND = get_config("START_COMMAND", "deploy")
SESI_COMMAND = get_config("SESI_COMMAND", "tampil")
SESIID_COMMAND = get_config("SESI_COMMAND", "cari")
LOG_FILE_ZZGEVC = get_config("LOG_FILE_ZZGEVC", "Ubot.log")

AKTIFSESI = {}
# /start message when other users start your bot
SESI_OTHER_USERS_TEXT = get_config(
    "SESI_OTHER_USERS_TEXT",
    (
        """
        TAMPIL SESI : 
        """
    )
)
AKTIFSESIID = {}
# /start message when other users start your bot
SESIID_OTHER_USERS_TEXT = get_config(
    "SESI_OTHER_USERS_TEXT",
    (
        """
        Fitur ini untuk cari sesi string yang sudah menggunakan bot ini
        """
    )
)
AKTIFPERINTAH = {}
START_OTHER_USERS_TEXT = get_config(
    "START_OTHER_USERS_TEXT",
    (
        f"""
        👋 **Halo Saya Adalah Wildan-Userbot**
        """
    )
)
INPUT_PHONE_NUMBER = get_config("INPUT_PHONE_NUMBER", (
    "Masukan nomor akun telegram anda dengan diawali +, Contoh +62xxxx"
))
RECVD_PHONE_NUMBER_DBP = get_config("RECVD_PHONE_NUMBER_DBP", (
    "Mohon periksa pesan masuk anda, dan masukkan kode yang ada dengan menggunakan spasi setiap kode\n Contoh : 1 2 3 4 5"
))
ALREADY_REGISTERED_PHONE = get_config("ALREADY_REGISTERED_PHONE", (
    "Mencoba mengirikan kode OTP"
))
CONFIRM_SENT_VIA = get_config("CONFIRM_SENT_VIA", (
    "Mohon periksa pesan masuk anda, dan masukkan semua kode 𝗱𝗶𝗺𝗮𝗻𝗮 𝗼𝘁𝗽 𝗮𝗻𝗴𝗸𝗮 𝗱𝗶𝗱𝗮𝗵𝘂𝗹𝘂𝗸𝗮𝗻 𝗱𝗮𝗻 𝗱𝗶𝗯𝗲𝗿𝗶 𝘀𝗽𝗮𝘀𝗶 𝗱𝗶𝘁𝗮𝗺𝗯𝗮𝗵 𝘀𝗲𝗹𝘂𝗿𝘂𝗵 𝗸𝗼𝗱𝗲 𝘀𝘁𝗿𝗶𝗻𝗴 𝘁𝗮𝗻𝗽𝗮 𝘀𝗽𝗮𝘀𝗶\n Contoh : 3 0 0 5 7"
))
RECVD_PHONE_CODE = get_config("RECVD_PHONE_CODE", (
    "Mencoba mengirikan kode OTP"
))
NOT_REGISTERED_PHONE = get_config("NOT_REGISTERED_PHONE", (
    "Maaf Nomor Yang Anda Masukkan Belum Terdaftar"
))
PHONE_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode yang anda masukkan salah, coba masukin kembali atau mulai dari awal"
)
TFA_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode yang anda masukkan salah, coba masukin kembali atau mulai dari awal"
)
ACC_PROK_WITH_TFA = get_config("ACC_PROK_WITH_TFA", (
    "Verifikasi 2 Langkah Diaktifkan, Mohon Masukkan Verifikasi 2 Langkah Anda."
))
SESSION_GENERATED_USING = get_config("SESSION_GENERATED_USING", (
    "Ubot sudah aktif, Hubungi Admins Untuk MeRestart Bot ..."
))

class Bot(Client):
    """ modded client for SessionMakerBot """

    def __init__(self):
        super().__init__(
            name="ubot",
            api_hash=API_HASH,
            api_id=API_ID,
            bot_token=BOT_TOKEN,
            plugins={
                "root": "Ubot/modules/bot"
            },
            workers=BOT_WORKERS,
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = self.me
        self.LOGGER(__name__).info(
            f"@{usr_bot_me.username} based on Pyrogram v{__version__} "
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")

app = Bot()


bot1 = (
    Client(
        name="bot1",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION1,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION1
    else None
)

bot2 = (
    Client(
        name="bot2",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION2,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION2
    else None
)

bot3 = (
    Client(
        name="bot3",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION3,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION3
    else None
)

bot4 = (
    Client(
        name="bot4",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION4,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION4
    else None
)

bot5 = (
    Client(
        name="bot5",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION5,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION5
    else None
)
bot6 = (
    Client(
        name="bot6",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION6,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION6
    else None
)

bot7 = (
    Client(
        name="bot7",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION7,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION7
    else None
)

bot8 = (
    Client(
        name="bot8",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION8,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION8
    else None
)

bot9 = (
    Client(
        name="bot9",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION9,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION9
    else None
)

bot10 = (
    Client(
        name="bot10",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION10,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION10
    else None
)

bot11 = (
    Client(
        name="bot11",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION11,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION11
    else None
)

bot12 = (
    Client(
        name="bot12",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION12,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION12
    else None
)

bot13 = (
    Client(
        name="bot13",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION13,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION13
    else None
)

bot14 = (
    Client(
        name="bot14",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION14,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION4
    else None
)

bot15 = (
    Client(
        name="bot15",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION15,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION15
    else None
)

bot16 = (
    Client(
        name="bot16",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION16,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION16
    else None
)

bot17 = (
    Client(
        name="bot17",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION17,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION17
    else None
)

bot18 = (
    Client(
        name="bot18",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION18,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION18
    else None
)

bot19 = (
    Client(
        name="bot19",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION19,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION19
    else None
)

bot20 = (
    Client(
        name="bot20",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION20,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION20
    else None
)
bot21 = (
    Client(
        name="bot21",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION21,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION21
    else None
)

bot22 = (
    Client(
        name="bot22",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION22,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION22
    else None
)

bot23 = (
    Client(
        name="bot23",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION23,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION23
    else None
)

bot24 = (
    Client(
        name="bot24",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION24,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION24
    else None
)

bot25 = (
    Client(
        name="bot25",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION25,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION25
    else None
)

bot26 = (
    Client(
        name="bot26",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION26,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION26
    else None
)

bot27 = (
    Client(
        name="bot27",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION27,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION27
    else None
)

bot28 = (
    Client(
        name="bot28",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION28,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION28
    else None
)

bot29 = (
    Client(
        name="bot29",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION29,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION29
    else None
)

bot30 = (
    Client(
        name="bot30",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION30,
        plugins=dict(root="Ubot/modules"),
        in_memory=True,
    )
    if SESSION30
    else None
)

bot31 = (
    Client(
        name="bot31",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION31,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION31
    else None
)

bot32 = (
    Client(
        name="bot32",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION32,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION32
    else None
)

bot33 = (
    Client(
        name="bot33",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION33,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION33
    else None
)

bot34 = (
    Client(
        name="bot34",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION34,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION34
    else None
)

bot35 = (
    Client(
        name="bot35",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION35,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION35
    else None
)

bot36 = (
    Client(
        name="bot36",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION36,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION36
    else None
)

bot37 = (
    Client(
        name="bot37",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION37,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION37
    else None
)

bot38 = (
    Client(
        name="bot38",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION38,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION38
    else None
)

bot39 = (
    Client(
        name="bot39",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION39,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION39
    else None
)

bot40 = (
    Client(
        name="bot40",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION40,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION40
    else None
)

bot41 = (
    Client(
        name="bot41",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION41,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION41
    else None
)

bot42 = (
    Client(
        name="bot42",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION42,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION42
    else None
)

bot43 = (
    Client(
        name="bot43",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION43,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION43
    else None
)

bot44 = (
    Client(
        name="bot44",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION44,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION44
    else None
)

bot45 = (
    Client(
        name="bot45",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION45,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION45
    else None
)
bot46 = (
    Client(
        name="bot46",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION46,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION46
    else None
)

bot47 = (
    Client(
        name="bot47",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION47,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION47
    else None
)

bot48 = (
    Client(
        name="bot48",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION48,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION48
    else None
)

bot49 = (
    Client(
        name="bot49",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION49,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION49
    else None
)

bot50 = (
    Client(
        name="bot50",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION50,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION50
    else None
)

bot51 = (
    Client(
        name="bot51",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION51,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION51
    else None
)

bot52 = (
    Client(
        name="bot52",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION52,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION52
    else None
)

bot53 = (
    Client(
        name="bot53",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION53,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION53
    else None
)

bot54 = (
    Client(
        name="bot54",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION54,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION54
    else None
)

bot55 = (
    Client(
        name="bot55",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION55,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION55
    else None
)
bot56 = (
    Client(
        name="bot56",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION56,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION56
    else None
)
bot57 = (
    Client(
        name="bot57",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION57,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION57
    else None
)
bot58 = (
    Client(
        name="bot58",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION58,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION58
    else None
)
bot59 = (
    Client(
        name="bot59",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION59,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION59
    else None
)
bot60 = (
    Client(
        name="bot60",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION60,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION60
    else None
)

bot61 = (
    Client(
        name="bot61",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION61,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION61
    else None
)

bot62 = (
    Client(
        name="bot62",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION62,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION62
    else None
)

bot63 = (
    Client(
        name="bot63",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION63,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION63
    else None
)

bot64 = (
    Client(
        name="bot64",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION64,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION64
    else None
)

bot65 = (
    Client(
        name="bot65",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION65,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION65
    else None
)
bot66 = (
    Client(
        name="bot66",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION66,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION66
    else None
)
bot67 = (
    Client(
        name="bot67",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION67,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION67
    else None
)
bot68 = (
    Client(
        name="bot68",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION68,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION68
    else None
)
bot69 = (
    Client(
        name="bot69",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION69,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION69
    else None
)
bot70 = (
    Client(
        name="bot70",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION70,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION70
    else None
)

bot71 = (
    Client(
        name="bot71",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION71,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION71
    else None
)

bot72 = (
    Client(
        name="bot72",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION72,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION72
    else None
)

bot73 = (
    Client(
        name="bot73",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION73,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION73
    else None
)

bot74 = (
    Client(
        name="bot74",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION74,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION74
    else None
)

bot75 = (
    Client(
        name="bot75",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION75,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION75
    else None
)
bot76 = (
    Client(
        name="bot76",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION76,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION76
    else None
)
bot77 = (
    Client(
        name="bot77",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION77,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION77
    else None
)
bot78 = (
    Client(
        name="bot78",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION78,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION78
    else None
)
bot79 = (
    Client(
        name="bot79",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION79,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION79
    else None
)
bot80 = (
    Client(
        name="bot80",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION80,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION80
    else None
)

bot81 = (
    Client(
        name="bot81",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION81,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION81
    else None
)

bot82 = (
    Client(
        name="bot82",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION82,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION82
    else None
)

bot83 = (
    Client(
        name="bot83",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION83,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION83
    else None
)

bot84 = (
    Client(
        name="bot84",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION84,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION84
    else None
)

bot85 = (
    Client(
        name="bot85",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION85,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION85
    else None
)
bot86 = (
    Client(
        name="bot86",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION86,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION86
    else None
)
bot87 = (
    Client(
        name="bot87",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION87,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION87
    else None
)
bot88 = (
    Client(
        name="bot88",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION88,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION88
    else None
)
bot89 = (
    Client(
        name="bot89",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION89,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION89
    else None
)
bot90 = (
    Client(
        name="bot90",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION90,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION90
    else None
)

bot91 = (
    Client(
        name="bot91",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION91,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION91
    else None
)

bot92 = (
    Client(
        name="bot92",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION92,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION92
    else None
)

bot93 = (
    Client(
        name="bot93",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION93,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION93
    else None
)

bot94 = (
    Client(
        name="bot94",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION94,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION94
    else None
)

bot95 = (
    Client(
        name="bot95",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION95,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION95
    else None
)
bot96 = (
    Client(
        name="bot96",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION96,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION96
    else None
)
bot97 = (
    Client(
        name="bot97",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION97,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION97
    else None
)
bot98 = (
    Client(
        name="bot98",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION98,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION98
    else None
)
bot99 = (
    Client(
        name="bot99",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION99,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION99
    else None
)
bot100 = (
    Client(
        name="bot100",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION100,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION100
    else None
)



bots = [bot for bot in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9, bot10, bot11, bot12, bot13, bot14, bot15, bot16, bot17, bot18, bot19, bot20, bot21, bot22, bot23, bot24, bot25, bot26, bot27, bot28, bot29, bot30, bot31, bot32, bot33, bot34, bot35, bot36, bot37, bot38, bot39, bot40, bot41, bot42, bot43, bot44, bot45, bot46, bot47, bot48, bot49, bot50, bot51, bot52, bot53, bot54, bot55, bot56, bot57, bot58, bot59, bot60, bot61, bot62, bot63, bot64, bot65, bot66, bot67, bot68, bot69, bot70, bot71, bot72, bot73, bot74, bot75, bot76, bot77, bot78, bot79, bot80, bot81, bot82, bot83, bot84, bot85, bot86, bot87, bot88, bot89, bot90, bot91, bot92, bot93, bot94, bot95, bot96, bot97, bot98, bot99, bot100] if bot]

for bot in bots:
    if not hasattr(bot, "group_call"):
        setattr(bot, "group_call", GroupCallFactory(bot).get_group_call())
