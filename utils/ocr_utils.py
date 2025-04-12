from PIL import ImageGrab
from paddleocr import PaddleOCR
from utils import box


class OCR:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True)  # need to run only once to download and load model into memory
    def get_txt_pos(self, text:str) -> box.Position:
        result = self.ocr.ocr("OCR.jpg", cls=True)

        for line in result:
            for detection in line:
                pos = detection[0][0]
                txt = detection[1][0]
                if txt == text:
                    return box.Position(pos[0], pos[1])

        exit("Failed to find text")

    def get_txt_list_pos(self, text_list:list[str]) -> list[box.Position]:
        _list = []
        result = self.ocr.ocr("OCR.jpg", cls=True)

        for line in result:
            for detection in line:
                pos = detection[0][0]
                txt = detection[1][0]
                if txt in text_list:
                    _list.append(box.Position(pos[0], pos[1]))

        if len(_list) != len(text_list):
            exit("Failed to find all text")

        return _list

    def get_txt_one_of_list_pos(self, text_list:list[str]) -> box.Position:
        _list = []
        result = self.ocr.ocr("OCR.jpg", cls=True)

        for line in result:
            for detection in line:
                pos = detection[0][0]
                txt = detection[1][0]
                if txt in text_list:
                    return box.Position(pos[0], pos[1])

        exit("Failed to find all text")


    def capture(self, region: box.Box):
        image = ImageGrab.grab((region.region[0], region.region[1],region.region[2],region.region[3]))
        image.save("ocr.jpg")
        return self