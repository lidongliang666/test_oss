import os
import json
import shutil

with open("json_info.json",'r') as f:
    data = json.load(f)

a = os.listdir("json_hasBeen_ocr")

n = 0
for i in a:
    print(i)
    if i not in data:
        n+=1
print(n)