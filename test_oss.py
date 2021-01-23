import json

import oss2
import cv2
import numpy as np

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

# 列举Bucket下10个Object，并打印它们的最后修改时间、文件名
# for i, object_info in enumerate(oss2.ObjectIterator(bucket)):
#     print("{0} {1}".format(object_info.last_modified, object_info.key))

#     if i >= 9:
#         break
# 上传一段字符串。Object名是motto.txt，内容是一段名言。
# bucket.put_object('motto.txt', 'Never give up. - Jack Ma')

# 下载到本地文件
# bucket.get_object_to_file('adv/wx57ddebee5ae12fbc/answerPage.json', '本地文件名.json')

# 删除名为motto.txt的Object
# bucket.delete_object('motto.txt')

# 确认Object已经被删除了
# assert not bucket.object_exists('motto.txt')

#类似于下载图片
file_likeObject= bucket.get_object("basicbook/1295/chapter/23880/page/84701_answerImg.jpg")
img = cv2.imdecode(np.array(bytearray(file_likeObject.read()),dtype='uint8'),cv2.IMREAD_UNCHANGED)
print(img.shape)
cv2.imwrite("test.jpg",img)