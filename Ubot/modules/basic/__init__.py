from pyrogram import Client, filters
from Ubot import cmds
import os
import sys
from os import environ, execle, path, remove
from Ubot.modules.basic.help import
from ubotlibs import BOT_VER
from ubotlibs.ubot import Ubot, Devs
add_command_help = add_command_help

ADMINS = [5779185981]

BL_GCAST = [-1001678973384, -1002127258037,]


BL_UBOT = [-1001959439622]
DEVS = [5779185981]

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])
