import json
import shutil
import os
from requests import get

import numpy as np
import cv2
import oss2
import paddle
# import torch

from ocrApi import OCR
from model import shufflenetv2

def pil_loader(img):
    h,w,_ = img.shape
    if h >= w:
        if h > 512:
            new_h = 512
            new_w = int(w * (512 / h))
            img = cv2.resize(img,(new_w, new_h))
    else:
        if w > 512:
            new_w = 512
            new_h = int(h * (512 / w))
            img = cv2.resize(img,(new_w, new_h))
    return img


def rotate_bound(image,angle):
    #获取图像的尺寸
    #旋转中心
    (h,w) = image.shape[:2]
    (cx,cy) = (w/2,h/2)
    
    #设置旋转矩阵
    M = cv2.getRotationMatrix2D((cx,cy),-angle,1.0)
    cos = np.abs(M[0,0])
    sin = np.abs(M[0,1])
    
    # 计算图像旋转后的新边界
    nW = int((h*sin)+(w*cos))
    nH = int((h*cos)+(w*sin))
    
    # 调整旋转矩阵的移动距离（t_{x}, t_{y}）
    M[0,2] += (nW/2) - cx
    M[1,2] += (nH/2) - cy
    
    return cv2.warpAffine(image,M,(nW,nH))


# device = torch.device("cuda")

# model = shufflenetv2()
# model.to(device)
# model.load_state_dict(torch.load("/home/ldl/桌面/project/image_to_normal/log/adam100.pkl"))
# model.load_state_dict(torch.load("adam79.pkl"))
# model.train(False)

lang_label = "英语" 
ocr = OCR()
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
jsonDir = "jsonInfo"
outRoot = 'json_hasBeen_ocr'

imgNormalDir = "json_image_normal"#存放标记图片是否是阅读方向的标签

for jsonfileName in os.listdir(jsonDir):
    josnPath = os.path.join(jsonDir,jsonfileName)
    print(josnPath)
    with open(josnPath,'r') as f:
        info = json.load(f)


    # outPath = os.path.join(imgNormalDir,str(info['data']['id'])+"normal.json")
    # if os.path.exists(outPath):
    #     continue
    if info['data']['chapters'] is None:
        continue
    

    for chapterIndex,chapter in enumerate( info['data']['chapters']):
        if chapter['pages'] is None:
            continue
        for pageIndex,page in enumerate( chapter['pages']):
            try:

                file_likeObject= bucket.get_object(page["answerPicPath"])
                img = cv2.imdecode(np.array(bytearray(file_likeObject.read()),dtype='uint8'),cv2.IMREAD_UNCHANGED)
            except TypeError:
                print(page["answerPicPath"])
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
                
                file_likeObject= bucket.get_object(page["answerPicPath"])
                img = cv2.imdecode(np.array(bytearray(file_likeObject.read()),dtype='uint8'),cv2.IMREAD_UNCHANGED)

            # img = pil_loader(img)#数据预处理
            # img = np.array(img).astype(np.float32) / 128. - 1
            # result_images = torch.FloatTensor(img)
            # result_images = result_images.unsqueeze(0)
            # result_images = result_images.permute([0, 3, 1, 2])
            # result_images = result_images.to(device)
            
            # imgIsNormal = True

            # with torch.no_grad():
            #     # timeStart = time.time()
            #     forword = model(result_images)
            #     cls_scores = torch.nn.functional.softmax(forword, dim=1)
            #     scores, classes = torch.topk(cls_scores, k=1, dim=1)
            #     # timeEnd = time.time()
            #     print(scores,classes)
            #     if classes[0][0] == 0:
            #         info['data']["chapters"][chapterIndex]['pages'][pageIndex]["direction"] = 0
            #     elif classes[0][0] == 1:
            #         info['data']["chapters"][chapterIndex]['pages'][pageIndex]["direction"] = 1
            #     elif classes[0][0] == 2:
            #         info['data']["chapters"][chapterIndex]['pages'][pageIndex]["direction"] = 2
            #     else:
            #         info['data']["chapters"][chapterIndex]['pages'][pageIndex]["direction"] = 3

            if isinstance(page['attaches'],list):
                for questionIndex,question in enumerate(page['attaches']):
                    
                    img_cut = img[max(0,question["lty"]):question["lty"]+question["height"],
                        max(0,question["ltx"]):question["ltx"]+question["width"]]
                    # print(question["ltx"],question["lty"],question["width"],question["height"])
                    # if not imgIsNormal:
                    #     img_cut = rotate_bound(img_cut,270)
                    #img save 
                    # cv2.imwrite('imageCut/'+'{}_{}_{}_{}.jpg'.format(chapterIndex,pageIndex,questionIndex,question['id']),img_cut)
                    
                    try:    
                        ocr_text = ocr.predictOCR(img_cut)
                        print(chapterIndex,pageIndex,questionIndex,ocr_text)
                        info['data']["chapters"][chapterIndex]['pages'][pageIndex]['attaches'][questionIndex]['question']['ocr']=ocr_text
                    except Exception as e:
                        print("ocr Error "+ page["answerPicPath"])
                        info['data']["chapters"][chapterIndex]['pages'][pageIndex]['attaches'][questionIndex]['question']['ocr']=''
                    
            else:

                continue
            # break
    
    outPath = os.path.join(outRoot,str(info['data']['id'])+"ocr.json")
    open(outPath,'w').write(json.dumps(info))
    # break
    os.remove(josnPath)