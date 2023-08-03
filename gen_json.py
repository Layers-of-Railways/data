#!/usr/bin/python3
import urllib.request
import json

names = []

with open("dev_capes.txt") as f:
    for line in f:
        names.append(line.strip())

names = list(set(names))
names = [name for name in names if name != ""]

uuids = {}

for name in names:
    with urllib.request.urlopen("https://api.ashcon.app/mojang/v2/user/"+name) as f:
        dat = json.load(f)
        uuids[name] = dat["uuid"]


full_data = {
    "dev": [
        {
            "id": v,
            "name": k
        } for k, v in uuids.items()
    ]
}
with open("dev_capes.json", "w") as f:
    json.dump(full_data, f, indent=4)