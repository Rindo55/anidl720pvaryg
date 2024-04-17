
import asyncio
import time
import aiohttp
import requests
import aiofiles
import sys
from main.modules.compressor import compress_video
from pymediainfo import MediaInfo
from main.modules.utils import episode_linker, get_duration, get_epnum, status_text, get_filesize, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from main.modules.uploader import upload_video
from main.modules.thumbnail import generate_thumbnail

import os

from main.modules.db import del_anime, save_uploads, is_fid_in_db, is_tit_in_db

from main.modules.downloader import downloader

from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name

from config import INDEX_USERNAME, UPLOADS_USERNAME, UPLOADS_ID, INDEX_ID, PROGRESS_ID, LINK_ID

from main import app, queue, status

from pyrogram.errors import FloodWait

from pyrogram import filters, enums

from main.inline import button1

status: Message

async def tg_handler():

    while True:

        try:
            if len(queue) != 0:

                i = queue[0]  

                i = queue.pop(0)
                
                id, name, video = await start_uploading(i)
                print("Title: ", i["title"])
                await del_anime(i["title"])
                await save_uploads(i["title"])
                await asyncio.sleep(30)


            else:                

                if "Idle..." in status.text:

                    try:

                        await status.edit(await status_text("Idle..."))

                    except:

                        pass

                await asyncio.sleep(30)

                

        except FloodWait as e:

            flood_time = int(e.x) + 5

            try:

                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

            except:

                pass

            await asyncio.sleep(flood_time)

        except:

            pass


def get_audio_language(video_path):
    try:
        media_info = MediaInfo.parse(video_path)
        for track in media_info.tracks:
            if track.track_type == 'Audio':
                language = track.language
                language = language.replace("ja", "JP")
                return language
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        

def esl(video_file):
    media_info = MediaInfo.parse(video_file)
    
    subtitle_languages = []
    for track in media_info.tracks:
        if track.track_type == 'Text':
            subtitle_languages.append(f"[track.language]")
    
    return subtitle_languages

def replace_text_with_mapping(subtitle, mapping):
    for original_text, replacement_text in mapping.items():
        subtitle = subtitle.replace(original_text, replacement_text)
    return subtitle

# Define the mapping of text to be replaced
mapping = {
    "en": "ENG",
    "pt-BR": "POR-BR",
    "es-419": "SPA-LA",
    "es": "SPA",
    "ar": "ARA",
    "fr": "FRE",
    "de": "GER",
    "it": "ITA",
    "ru": "RUS",
    "ja": "JPN",
    "pt": "POR",
    "pl": "POL",
    "nl": "DUT",
    "nb": "NOB",
    "fi": "FIN",
    "tr": "TUR",
    "sv": "SWE",
    "el": "GRE",
    "he": "HEB",
    "ro": "RUM",
    "id": "IND",
    "th": "THA",
    "ko": "KOR",
    "da": "DAN",
    "zh": "CHI",
    "bg": "BUL",
    "vi": "VIE",
    "hi": "HIN",
    "te": "TEL",
    "uk": "UKR",
    "hu": "HUN",
    "cs": "CES",
    "hr": "HRV",
    "ms": "MAY",
    "sk": "SLK",
    "fil": "FIL"
}




print(" ".join(subtitle_languages))
async def start_uploading(data):

    try:

        title = data["title"]
        dbtit = data["title"]
        title = title.replace("Dr. Stone - New World", "Dr Stone New World")
        title = title.replace("Opus.COLORs", "Opus COLORs")
        title = title.replace(" Isekai wa Smartphone to Tomo ni. 2", " Isekai wa Smartphone to Tomo ni 2")
        title = title.replace("Stand My Heroes - Warmth of Memories - OVA", "Stand My Heroes Warmth of Memories - OVA")
        link = data["link"]
        size = data["size"]
        nyaasize = data["size"]
        name, ext = title.split(".")

        name += f" [AniDL]." + ext

        KAYO_ID =  -1001895203720
        uj_id = 1159872623
        DATABASE_ID = -1001895203720
        bin_id = -1002062055380
        name = name.replace(f" [AniDL].","").replace(ext,"").strip()
        id, img, tit = await get_anime_img(get_anime_name(title))
        msg = await app.send_photo(bin_id,photo=img,caption=title)

        print("Downloading --> ",name)
        img, caption, alink = await get_anilist_data(title)
        await asyncio.sleep(5)
        await status.edit(await status_text(f"Downloading {name}"),reply_markup=button1)
        file = await downloader(msg,link,size,title)

        await msg.edit(f"Download Complete : {name}")
        print("Encoding --> ",name)

        duration = get_duration(file)
        durationx = get_durationx(file)
        filed = os.path.basename(file)
        filed = filed.replace("Go.Go.Loser.Ranger.S01E01.We.Are.Justice.The.Dragon.Keepers.1080p.DSNP.WEB-DL.AAC2.0.H.264-VARYG", "[AniDL] Sentai Daishikkaku - 01 [Web][720p x265 10Bit][Opus][DSNP ~ Varyg]")
        filed = filed.replace("Go.Go.Loser.Ranger.S01E02.Go.Fighter.D.1080p.DSNP.WEB-DL.AAC2.0.H.264-VARYG", "[AniDL] Sentai Daishikkaku - 01 [Web][720p x265 10Bit][Opus][DSNP ~ Varyg]")
        filed = filed.replace("[1080p]", "[1080p Web-DL]")
        filed = filed.replace("2nd Season", "S2")
        filed = filed.replace("3rd Season", "S3")
        razo = filed.replace("[1080p Web-DL]", "[720p x265] @animxt")
        fpath = "downloads/" + filed
        ghostname = name
        ghostname = ghostname.replace("[1080p][Multiple Subtitle]", "")
        ghostname = ghostname.replace("[1080p]", "")
        ghostname = ghostname.replace("2nd Season", "S2")
        ghostname = ghostname.replace("3rd Season", "S3")    
    
        os.rename(file,"video.mkv")
        titlx = title.replace('[1080p][Multiple Subtitle]', '[Web][720p x265 10Bit][Opus][Erai-raws]')
        titm = f"**[AniDL] {titlx}**"
        tito = f"[AniDL] {titlx}"
        main = await app.send_photo(KAYO_ID,photo=img, caption=f"**{filed}**")
        video_path="video.mkv"
        
        audio_language = get_audio_language(video_path)
        if audio_language:
            print("Audio Track Language:", audio_language)
        else:
            print("Failed to get audio language.")
        subtitle_languages = esl(video_path)
        if subtitle_languages:
            print("Subtitle Track Language:", subtitle_languages)
        else:
            print("Failed to get subtitle language.")
        exsub = subtitle_laguages.replace("][", ", ")
        exsub = exsub.replace("[", "")
        exsub = exsub.replace("]", "")  
        subtitle = exsub
        msubtitle = replace_text_with_mapping(subtitle, mapping)
        print(msubtitle)
        compressed = await compress_video(duration,main,filed)
    

        if compressed == "None" or compressed == None:

            print("Encoding Failed Uploading The Original File")

            os.rename("video.mkv",fpath)

        else:

            os.rename("out.mkv",fpath)
  
        print("Uploading --> ",name)
        video = await upload_video(msg,img,fpath,id,tit,name,size,main,msubtitle,nyaasize,audio_language, alink)



        try:

            os.remove("video.mkv")

            os.remove("out.mkv")

            os.remove(file)

            os.remove(fpath)
        except:

            pass     

    except FloodWait as e:

        flood_time = int(e.x) + 5

        try:

            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

        except:

            pass

        await asyncio.sleep(flood_time)
        
    return id, name, video

    
