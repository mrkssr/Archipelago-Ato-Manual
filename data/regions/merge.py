import os
import json

base_json_path = 'regions_base.json'
transformed_json_path = '../regions.json'

regions = ["Blossom", "Crimson", "Fall", "Forbidden", "Hills", "Lake", "Pillar", "Swamp", "Temple"]
json_content = {}

with open(base_json_path) as base:
    json_content = json.load(base)

for key in regions:
    with open(f'{key}.json') as file:
        json_content = json_content | json.load(file)

with open(transformed_json_path, 'w') as file:
    json.dump(json_content, file, indent = 4, sort_keys=False)
