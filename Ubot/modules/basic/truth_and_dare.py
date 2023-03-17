"""
Project [DarkWeb](https://github.com/TeamKillerX/DarkWeb) is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import random

import Ubot.modules.basic.truth_and_dare_string as tod

from . import *


# LU GABISA CODING LU KONTOL
# BELAJAR CODING DARI NOL


@Ubot("apakah", cmds)
async def apakah(client, message):
    cot = message.text.split(None, 1)[1]
    if not cot:
        return await message.reply("Berikan saya pertanyaan 😐")
    await message.reply(f"{random.choice(tod.AP)}")


@Ubot("kenapa", cmds)
async def kenapa(client, message):
    cot = message.text.split(None, 1)[1]
    if not cot:
        return await message.reply("Berikan saya pertanyaan 😐")
    await message.reply(f"{random.choice(tod.KN)}")


@Ubot("bagaimana", cmds)
async def bagaimana(client, message):
    cot = message.text.split(None, 1)[1]
    if not cot:
        return await message.reply("Berikan saya pertanyaan 😐")
    await message.reply(f"{random.choice(tod.BG)}")


@Ubot("dare", cmds)
async def dare(client, message):
    try:        
        await message.edit(f"{random.choice(tod.DARE)}")
    except BaseException:
        pass


@Ubot("truth", cmds)
async def truth(client, message):
    try:
        await message.edit(f"{random.choice(tod.TRUTH)}")
    except Exception:
        pass


add_command_help(
    "dare",
    [
        [f"dare", "Coba sendiri"],
        [f"truth", "Coba sendiri"],
        [f"apakah [pertanyaan]", "Coba sendiri"],
        [f"kenapa [pertanyaan]", "Coba sendiri"],
        [f"bagaimana [pertanyaan]", "Coba sendiri"],
    ],
)
        