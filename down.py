import json
import shutil
import os
from requests import get

import numpy as np
import cv2
import oss2


with open("accessKeyId.json","r") as f:
    keyJson = json.load(f)

access_key_id = keyJson["accessKeyId"]
access_key_secret = keyJson['accessKeySecret']
security_token = keyJson["securityToken"]

bucket_name = "test-zijinbook-2"
endpoint = 	"oss-cn-shenzhen-internal.aliyuncs.com"
auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

print("ok")
jsonDir = "downjson"
outRoot = 'image_math'


for jsonfileName in os.listdir(jsonDir):
    josnPath = os.path.join(jsonDir,jsonfileName)
    with open(josnPath,'r') as f:
        info = json.load(f)

    if info['data']['chapters'] is None:
        continue
    
    for chapterIndex,chapter in enumerate( info['data']['chapters']):
        if chapter['pages'] is None:
            continue
        for pageIndex,page in enumerate( chapter['pages']):
            try:
                file_likeObject= bucket.get_object(page["blankPicPath"])  # answerPicPath
                img = cv2.imdecode(np.array(bytearray(file_likeObject.read()),dtype='uint8'),cv2.IMREAD_UNCHANGED)
            except TypeError:
                print(page["blankPicPath"])
                continue
            except oss2.exceptions.ServerError :
                url='http://172.18.81.254:9004/aliyun/sts_token/get_oss/ml-test'
                res = get(url)
                dataJson = res.json()
                access_key_id=dataJson["data"]["token"]["accessKeyId"],
                access_key_secret=dataJson["data"]["token"]["accessKeySecret"],
                security_token=dataJson["data"]["token"]["securityToken"],
                # print(access_key_id,access_key_secret,security_token)
                print(dataJson)
                auth = oss2.StsAuth(*access_key_id, *access_key_secret, *security_token)
                bucket = oss2.Bucket(auth, endpoint, bucket_name)

                print("ok")
                
                file_likeObject= bucket.get_object(page["blankPicPath"])   #下载图片
                img = cv2.imdecode(np.array(bytearray(file_likeObject.read()),dtype='uint8'),cv2.IMREAD_UNCHANGED)
            
            #savePath = outRoot,str(info['data']['id'])
            #if os.path.exists( savePath ) == False: #
              #  os.mkdir(savePath)
            m = info['data']['id']
            n = page["pageNo"]
            cv2.imwrite('image_math/'+'{}_{}.jpg'.format(m,n),img)