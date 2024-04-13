import re
import asyncio
from pyrogram import Client
from math import floor
import os
from main import queue, app
import cv2, random
from string import ascii_letters, ascii_uppercase, digits
from pyrogram.types import Message, MessageEntity
from pyrogram.errors import FloodWait
from base64 import standard_b64encode, standard_b64decode

def str_to_b64(__str: str) -> str:
    str_bytes = __str.encode('ascii')
    bytes_b64 = standard_b64encode(str_bytes)
    b64 = bytes_b64.decode('ascii')
    return b64


def b64_to_str(b64: str) -> str:
    bytes_b64 = b64.encode('ascii')
    bytes_str = standard_b64decode(bytes_b64)
    __str = bytes_str.decode('ascii')
    return __str

def get_duration(file):
    data = cv2.VideoCapture(file)
  
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    seconds = int(frames / fps)
    return seconds


def get_durationx(file):
    data = cv2.VideoCapture(file)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    seconds = int(frames / fps)
    minutes = floor(seconds/60)
    rem_seconds = round(seconds-(minutes*60))
    durationz = str(minutes) + " minutes " + str(rem_seconds) + " seconds"
    return durationz

FORWARD_AS_COPY = "True"

async def reply_forward(message: Message, file_id: int):
    try:
        await message.reply_text(
            f"**Here is Sharable Link of this file:**\n"
            f"https://t.me/zoroloverobot?start=animxt_{str_to_b64(str(file_id))}\n\n"
            f"__To Retrive the Stored File, just open the link!__",
            disable_web_page_preview=True, quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await reply_forward(message, file_id)
        
ky_id = -1001948444792
async def media_forward(bot, user_id: int, file_id: int):
    try:
        if FORWARD_AS_COPY is True:
            return await app.copy_message(chat_id=user_id, from_chat_id=ky_id,
                                          message_id=file_id)
        elif FORWARD_AS_COPY is False:
            return await app.forward_messages(chat_id=user_id, from_chat_id=ky_idL,
                                              message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return media_forward(bot, user_id, file_id)
    
async def send_media_and_reply(bot, user_id: int, file_id: int):
    sent_message = await media_forward(bot, user_id, file_id)
    await reply_forward(message=sent_message, file_id=file_id)
    await asyncio.sleep(2)


def get_screenshot(file):
    cap = cv2.VideoCapture(file)
    name = "./" + "".join(random.choices(ascii_uppercase + digits,k = 10)) + ".jpg"

    total_frames = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
    frame_num = random.randint(0,total_frames)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num-1)
    res, frame = cap.read()

    cv2.imwrite(name, frame)
    cap.release()
    #cv2.destroyAllWindows()
    return name

def get_filesize(file):
    x = os.path.getsize(file)
    x = round(x/(1024*1024))
    if x > 1024:
        x = str(round(x/1024,2)) + " GB"
    else:
        x = str(x) + " MBs"

    return x

def get_epnum(name):
    x = name.split(" - ")[-1].strip()
    x = x.split(" ")[0]
    x = x.strip()
    return x

def format_time(time):
    min = floor(time/60)
    sec = round(time-(min*60))

    time = str(min) + ":" + str(sec)
    return time

def format_text(text):
    ftext = ""
    for x in text:
        if x in ascii_letters or x == " " or x in digits:
            ftext += x
        else:
            ftext += " "
    
    while "  " in ftext:
        ftext = ftext.replace("  "," ")
    return ftext

def episode_linker(f,en,text,link):
    ent = en
    off = len(f) + 2
    length = len(text)
    new = MessageEntity(type="text_link",offset=off,length=length,url=link)
    ent.append(new)
    return ent

async def get_messages(bot, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await app.get_messages(
                chat_id=kayo_id,
                message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await app.get_messages(
                chat_id=kayo_id,
                message_ids=temb_ids
            )
        except:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages

def tags_generator(title):
    x = "#" + title.replace(" ","_")
    
    while x[-1] == "_":
        x = x[:-1]
    return x

async def status_text(text):
    stat = """
⭐️ **Status :** {}

⏳ **Queue :** 

{}
"""
    
    queue_text = ""
    for i in queue:
        queue_text += "📌 " + i["title"].replace(".mkv","").replace(".mp4","").strip() + "\n"

    if queue_text == "":
        queue_text = "Nothing to encode here uwu"
        
    return stat.format(
        text,
        queue_text
    )


def get_progress_text(sourcetext,status,completed,speed,total,enco=False):
    text = """Name: {}
{}: {}%
[{}]
{} of {}
Speed: {}
ETA: {}
    """

    text2 = """<blockquote><b>{}</b></blockquote>

<blockquote>
<b>STATUS</b>: <code>Encoding UwU!</code> ⚡️
<b>○ Engine</b>: <code>Azure</code>
<b>○ Precentage</b>: <code>{}%</code>
<b>○ Speed</b>: <code>{}</code>
<b>○ ETA</b>: <code>{}</code>
</blockquote>
    """


    if enco == False:
        total = str(total)
        completed = round(completed*100,2)
        size, forma = total.split(' ')
        if forma == "MiB":
            size = int(round(float(size)))
        elif forma == "GiB":
            size = int(round(float(size)*1024,2))

        percent = completed
        speed = round(float(speed)/1024) #kbps

        if speed == 0:
            speed = 0.1

        ETA = round((size - ((percent/100)*size))/(speed/1024))

        if ETA > 60:
            x = floor(ETA/60)
            y = ETA-(x*60)

            if x > 60:
                z = floor(x/60)
                x = x-(z*60)
                ETA = str(z) + " Hour " + str(x) + " Minutes"
            else:
                ETA = str(x) + " Minute " + str(y) + " Seconds"
        else:
            ETA = str(ETA) + " Second"  

        if speed > 1024:
            speed = str(round(speed/1024)) + " MB"
        else:
            speed = str(speed) + " KB"

        completed = round((percent/100)*size)

        if completed > 1024:
            completed = str(round(completed/1024,2)) + " GB"
        else:
            completed = str(completed) + " MB"

        if size > 1024:
            size = str(round(size/1024,2)) + " GB"
        else:
            size = str(size) + " MB"

        fill = " ▰ "
        blank = " ▱ "
        bar = ""

        bar += round(percent/10)*fill
        bar += round(((20 - len(bar))/2))*blank


        speed += "/sec"
        text = text.format(
            sourcetext,
            status,
            percent,
            bar,
            completed,
            size,
            speed,
            ETA
        )
        return text

    elif enco == True:
        speed = float(speed)
        if speed == 0:
            speed = 0.01

        remaining = floor(int(total)-completed)
        ETA = floor(remaining/float(speed))

        if ETA > 60:
            x = floor(ETA/60)
            y = ETA-(x*60)

            if x > 60:
                z = floor(x/60)
                x = x-(z*60)
                ETA = str(z) + " Hour " + str(x) + " Minutes"
            else:
                ETA = str(x) + " Minutes " + str(y) + " Seconds"
        else:
            ETA = str(ETA) + " Seconds"

        percent = round((completed/total)*100,2)

        fill = " ▰ "
        blank = " ▱ "
        bar = ""

        bar += round(percent/10)*fill
        bar += round(((20 - len(bar))/2))*blank
        
        speed = str(speed) + "x"
  
        text2 = text2.format(
            sourcetext,
            percent,
            str(speed),
            ETA
        )
        return text2


