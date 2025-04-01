from django.conf import settings
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stock_market_db_new"]

def get_model_metadata():
    collection = db['model_metadata']
    data = list(collection.find({}, {"_id": 0}))
    return data

def get_news(skip=0, limit=30):
    collection = db['news_data']
    newsData = list(collection.find({}, {"_id": 0}).skip(skip).limit(limit))
    return newsData

def get_user_watchlist(user_email):
    collection = db['user_watchlist']
    user_watchlist = collection.find_one({"userMailId": user_email}, {"_id": 0})
    return user_watchlist

def add_stock_to_watchlist(user_email, stock_data):
    collection = db['user_watchlist']
    stock_data["status"] = "Holding"
    result = collection.update_one(
        {"userMailId": user_email},
        {"$push": {"stock_symbol_list": stock_data}},
        upsert=True
    )
    return result.modified_count

def update_stock_in_watchlist(user_email, symbol, update_data):
    collection = db['user_watchlist']
    result = collection.update_one(
        {"userMailId": user_email, "stock_symbol_list.symbol": symbol},
        {"$set": {f"stock_symbol_list.$.{key}": value for key, value in update_data.items()}}
    )
    return result.modified_count

def mark_stock_as_sold(user_email, symbol):
    collection = db['user_watchlist']
    result = collection.update_one(
        {"userMailId": user_email, "stock_symbol_list.symbol": symbol},
        {"$set": {"stock_symbol_list.$.status": "Sold"}}
    )
    return result.modified_count