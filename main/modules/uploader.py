import asyncio

import os
from string import ascii_letters, digits
import time
import random
import pixeldrain

import aiohttp

import requests

import aiofiles

from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator, get_messages, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from main.modules.anilist import get_anime_name

from main.modules.anilist import get_anime_img

from main.modules.db import present_user, add_user, is_fid_in_db, save_file_in_db

from main.modules.thumbnail import generate_thumbnail

from config import UPLOADS_ID

from pyrogram import Client, filters, enums

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument

from main.modules.progress import progress_for_pyrogram

from os.path import isfile

import os

import time

from main import app, status

from pyrogram.errors import FloodWait

from main.inline import button1



async def upload_video(msg: Message, img, file, id, tit, name, ttl, main, subtitle, nyaasize, audio_info, alink):
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            size = get_filesize(file)
            ep_num = get_epnum(name)
            print(ep_num)
            rest = tit
            filed = os.path.basename(file)
            print('filed: ', filed)
            filed = filed.replace("[1080p Web-DL]", "[Web][720p x265 10Bit][Opus][Erai-raws]")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001895203720
            gay_id = 1159872623
            upid = int(main.id)
            print(upid)
            x = await app.edit_message_media(
                chat_id=kayo_id,
                message_id=upid,
                media=InputMediaDocument(file),
                file_name=filed
            )
            await asyncio.sleep(3)
            hash = "".join([random.choice(ascii_letters + digits) for n in range(50)])
            save_file_in_db(filed, hash, subtitle, img, audio_info, tit, alink, upid)
            print(hash)
            gcaption = f"`📺 {filed}`\n\n`🔗 EP - {ep_num}:  https://anidl.ddlserverv1.me.in/beta/{hash}`" + "\n\n" + f"🔠 __{tit}__" + "\n" + "\n" + f"📝 `{subtitle}`"
            dl_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔗 Download Link", url=f"https://anidl.ddlserverv1.me.in/beta/{hash}")
                    ]
                ]
            )
            await app.edit_message_caption(
                chat_id=kayo_id,
                message_id=upid,
                caption=gcaption
            )
            await asyncio.sleep(3)
            await app.edit_message_reply_markup(
                chat_id=kayo_id,
                message_id=upid,
                reply_markup=dl_markup
            )
            await asyncio.sleep(3)
            anidl_id=-1001234112068
            anidlcap = f"<b>{anidltitle}</b>\n<i>({tit})</i>\n\n<blockquote><b>• Source:</b> <code>Erai-raws</code>\n<b>• Video:</b> <code>720p x265 10Bit CRF@22</code>\n<b>• Audio:</b> <code>Japanese (OPUS)</code>\n<b>• Subtitle:</b> <code>{subtitle}</code></blockquote>"
            anidl_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔗 VISIT PAGE", url=f"https://anidl.org/airing-anime")
                    ]
                ]
            )
            await asyncio.sleep(3)
            await app.send_photo(anidl_id,photo=img,caption=anidlcap, reply_markup=anidl_markup, parse_mode=enums.ParseMode.HTML)
    except Exception:
        await app.send_message(kayo_id, text="Something Went Wrong!")


    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.id
