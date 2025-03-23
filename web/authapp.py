import json
import os
data=dict()
dbdict=dict()
with open(f"{os.path.dirname(os.path.abspath(__file__))}\\db.json","r") as db:
    dbdict= json.load(db)
with open(f"{os.path.dirname(os.path.abspath(__file__))}\\pending.json","r") as file:
    data = json.load(file)

keys_to_remove = []
for key,value in data.items():
    print(key)
    choice = input("Accept? y/n:")
    if choice =="y":
        dbdict[key]=value
    keys_to_remove.append(key)
for key in keys_to_remove:
    data.pop(key)

with open(f"{os.path.dirname(os.path.abspath(__file__))}\\pending.json","w") as file:
    json.dump(data,file)
with open(f"{os.path.dirname(os.path.abspath(__file__))}\\db.json","w") as file:
    json.dump(dbdict,file)