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

for i, name in enumerate(names):
    print(f"[{i+1}/{len(names)}] Fetching UUID for {name}")
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

full_data["dev"] = sorted(full_data["dev"], key=lambda v: v["id"])

with open("dev_capes.json", "w") as f:
    json.dump(full_data, f, indent=4)
