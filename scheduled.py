
import pymongo;
from datetime import datetime, timedelta
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["carNumbers"]
col = db["table"]
expirationDate = past = datetime.now() - timedelta(days=7)
now = datetime.now()
'''x = col.find({"end":{"$gt": now , "$lt": expirationDate }})'''

x = col.find({"end":{"$gt": "2023-09-01" , "$lt":"2023-09-30"}})

resList =list(x)

if (int(len(resList)) > 0):
    for item in resList:
        print (item['carNum'])
        print (item['end'])
        print(item['email'])
        if (expirationDate < past):
            print ("send email")