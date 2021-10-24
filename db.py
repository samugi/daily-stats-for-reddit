import pymongo
import utils
import urllib
import ssl
import config_reader as config
from coin_and_count import CoinAndCount, Comment

USER = utils.get_env("DB_USER") or config.get('DB', 'USER')
password = utils.get_env("DB_PASSWORD") or config.get('DB', 'PASSWORD')
PASSWORD = urllib.parse.quote_plus(password)
DB_HOST = utils.get_env("DB_HOST") or config.get('DB', 'DB_HOST')
DB_NAME = utils.get_env("DB_NAME") or config.get('DB', 'DB_NAME')
DB_COLLECTION = utils.get_env("DB_COLLECTION") or config.get('DB', 'DB_COLLECTION')

# database configuration
URL = f"mongodb+srv://{USER}:{PASSWORD}@{DB_HOST}?retryWrites=true&w=majority"
client = pymongo.MongoClient(URL, ssl_cert_reqs=ssl.CERT_NONE)
db = client[DB_NAME]
coins_collection = db[DB_COLLECTION]

def store(coins_dict):
    r = coins_dict
    for k, v in r.items():
        if not isinstance(v, str):
            r[k] = v.__dict__
    try:
        coins_collection.insert_one(r)
    except pymongo.errors.InvalidDocument:
        n = {}
        for k, v in r.items():
            if isinstance(v, CoinAndCount):
                for va in v.comments:
                    if isinstance(va, Comment):
                        print(str(va.ups))
                        va.timestamp = str(va.timestamp).encode("utf-8")
                        va.ups = str(va.ups).encode("utf-8")
                        va.downs = str(va.downs).encode("utf-8")
                        va.total_awards_received = str(va.total_awards_received).encode("utf-8")
                        va.author_name = va.author_name.encode("utf-8")
            print(str(type(v)))
            n[k] = v
        coins_collection.insert_one(n)
    finally:
        print("Done.")