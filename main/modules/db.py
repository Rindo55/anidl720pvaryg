import asyncio
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGO_DB_URI
print("[INFO]: STARTING MONGO DB CLIENT")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.autoanime720p
dbx = mongo_client["anidl"]
filesdb = dbx["files"]
animedb = db.animes
uploadsdb = db.uploads
user_data = db['users']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def get_animesdb(): 
    anime_list = []
    async for name in animedb.find():
        anime_list.append(name)
    return anime_list

async def save_animedb(name,data): 
    data = await animedb.insert_one({"name": name, "data": data})
    return
  
async def del_anime(name): 
    try:
        animesdb = db.animes
        result = await animesdb.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Successfully deleted anime: {name}")
        else:
            print(f"No anime found with the name: {name}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error deleting anime: {e}")

async def get_uploads(): 
    anime_list = []
    async for name in uploadsdb.find():
        anime_list.append(name)
    return anime_list

async def save_uploads(name):
    uploadb = db.uploads
    print("save_uploads: ", name)
    data = await uploadb.insert_one({"name": name})
    return

def is_fid_in_db(fid):
    data = filesdb.find_one({"fid": fid})
    if data:
        return data
    else:
        return None

def save_file_in_db(filed, hash, subtitle, img, audio_info, tit, alink, upid=None):
    filesdb.update_one(
        {
            "hash": hash,
            "fid": str(upid),
        },
        {"$set": {"filename": filed, "filenamex": filed, "code": hash, "msg_id": upid, "subtitle": subtitle, "image": img, "audio": audio_info, "etitle": tit, "alink": alink}},
        upsert=True,
    )
    return
    
def is_tit_in_db(bit):
    uploadeb = db.uploads
    data = uploadeb.find_one({"name": bit})
    if data:
        return True
    else:
        return False
