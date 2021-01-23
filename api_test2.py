from requests import get
import shutil
import os
import json
import time
url="http://172.18.81.254:9002/basicbook/get-for-ml/"

root = './bookJson'
outroot = "./books_hasBeen_download"

bookJsonInfoPath = './jsonInfo'
for jsonflie in os.listdir(root):
    jsonpath= os.path.join(root,jsonflie)
    try:
        with open(jsonpath,'r') as f:

            data = json.load(f)
        print(jsonpath)
        for book in data['data']['content']:
            
            downloadJson = os.path.join(bookJsonInfoPath,str(book['id'])+'.json')
            if os.path.exists(downloadJson):
                continue
            print(downloadJson)
            re = get(url+str(book['id']))
            # open(downloadJson,'w').write(re.text)
            with open(downloadJson,'w') as f:
                json.dump(re.json(),f,ensure_ascii=False)
        outPath = os.path.join(outroot,jsonflie)
        shutil.move(jsonpath,outPath)
        time.sleep(7)
    except Exception as e:
        print(e)
        continue



