# !python3
# coding : utf-8
import requests
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client(MONGO_DB)

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print ("存储到mongdb成功",result)
        return  True
    return False


def get_page_index():
    data={
        'offset' : '0',
        'format' : 'json',
        'keyword' : '街拍',
        'autoload' : 'true',
        'count' : '20',
        'cur_ta': '1'
    }
