
import cv2
import numpy as np
from paddleocr import PaddleOCR


class OCR:
    def __init__(self):
        # self.ocr = PaddleOCR(use_angle_cls=True)
        self.ocr = {
            # "en":PaddleOCR(lang="en"),
            "ch":PaddleOCR(lang="ch")
        }
        self.drop_scores = 0.5
    def predictOCR(self, img_path,lang='ch'):
        #去水印
        ocr = self.ocr[lang]
        img = None
        if isinstance(img_path,str):
            img = cv2.imread(img_path)
        else:
            img = img_path
        img = np.clip(2.0*img-160, 0, 255).astype(np.uint8)
        result = ocr.ocr(img)
        # boxes = [line[0] for line in result]
        # txts = [line[1][0] for line in result]
        # scores = [line[1][1] for line in result]
        return ' '.join([ line[1][0]  for line in result if line[1][1]>self.drop_scores ])

if __name__ == "__main__":
    ocr = OCR()
    txts = ocr.predictOCR('test.jpg')
    # print(boxes)
    print(txts)
    # print(scores)