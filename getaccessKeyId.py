'''
    获得accessKeyId,以及秘钥,有效期为一个小时
    将获得的accessKeyId 和 秘钥存储为accessKeyId.json文件
'''
from requests import get
import json
url='http://172.18.81.254:9004/aliyun/sts_token/get_oss/ml-test'
res = get(url)

dataJson = res.json()
with open('accessKeyId.json','w') as f:
    json.dump({
        "accessKeyId":dataJson["data"]["token"]["accessKeyId"],
        "accessKeySecret":dataJson["data"]["token"]["accessKeySecret"],
        "securityToken":dataJson["data"]["token"]["securityToken"],
        "createTime":dataJson["data"]["createTime"]
    },f)