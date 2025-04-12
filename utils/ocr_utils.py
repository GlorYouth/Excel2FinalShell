from PIL import ImageGrab
from paddleocr import PaddleOCR

from utils import box


class OCR:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    def get_txt_pos(self, text) -> box.Position:
        result = self.ocr.ocr("OCR.jpg", cls=True)

        for line in result:
            for detection in line:
                pos = detection[0][0]
                txt = detection[1][0]
                if txt == text:
                    return box.Position(pos[0], pos[1])

        # poslist = [detection[0][0] for line in result for detection in line]
        # txtlist = [detection[1][0] for line in result for detection in line]
        #
        # for i in range(len(poslist)):
        #     print(poslist[i], txtlist[i])
        #     if txtlist[i] == text:
        #         return box.Position(poslist[i][0], poslist[i][1])

        exit("Failed to find text")


    def capture(self, region: box.Box):
        image = ImageGrab.grab((region.region[0], region.region[1],region.region[2],region.region[3]))
        image.save("ocr.jpg")
        return self