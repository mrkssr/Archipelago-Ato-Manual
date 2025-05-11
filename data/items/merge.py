import os
import json

base_json_path = 'items_base.json'
transformed_json_path = '../items.json'

regions = ["Shards", "Skills", "Runes", "Magic Bars", "Coins", "Talismans", "Checkpoints", "Events", "Filler"]
json_content = {}

with open(base_json_path) as base:
    json_content = json.load(base)

for key in regions:
    with open(f'{key}.json') as file:
        json_content["data"] = json_content["data"] + json.load(file)["data"]

with open(transformed_json_path, 'w') as file:
    json.dump(json_content, file, indent = 4, sort_keys=False)
