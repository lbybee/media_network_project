from pymongo import MongoClient
from datetime import datetime
import pickle


client = MongoClient()
db = client["StreamingDb"]
collection = db["StreamingCollection"]

output = []
output_f = "test.pkl"


i = 0
for obs in collection.find():
    output.append(obs)
    i += 1
    if i == 50:
        break

output_d = open(output_f, "wb")
pickle.dump(output, output_d)
output_d.close()
