from requests import get
import json
url = "http://172.18.81.254:9002/basicbook/page-for-ml"


pageNum = 0
pageSize = 10
data = {
    "page":pageNum,
    "size":pageSize,
    "includeCategories":"keben-jiaofu"
}

while True:
    
    print(pageNum+1,data)
    re = get(url,params=data)
    

    
    reJson = re.json()
    if reJson["status"]==200:
        if len(reJson['data']['content']) < 1:
            break
        open("./bookJson/Book{:04d}.json".format(pageNum),'w').write(re.text)
    
    pageNum += 1
    data["page"] = pageNum

