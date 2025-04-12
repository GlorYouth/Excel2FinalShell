from PIL import ImageGrab
from paddleocr import PaddleOCR
from utils import box


class OCR:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    def get_txt_pos(self, union: list[str] | str) -> box.Position:
        result = self.ocr.ocr("OCR.jpg", cls=True)

        for line in result:
            for detection in line:
                pos = detection[0][0]
                txt = detection[1][0]
                if txt in union:
                    return box.Position(pos[0], pos[1])

        exit("Failed to find text")

    def get_txt_list_pos(self, text_list:list[list[str] | str]) -> list[(str,box.Position)]:
        _list = []
        result = self.ocr.ocr("OCR.jpg", cls=True)

        for line in result:
            for detection in line:
                pos = detection[0][0]
                txt = detection[1][0]
                for union in text_list:
                    if txt in union:
                        print(txt)
                        _list.append((txt, box.Position(pos[0], pos[1])))
                        break

        return _list


    def capture(self, region: box.Box):
        image = ImageGrab.grab((region.region[0], region.region[1],region.region[2],region.region[3]))
        image.save("ocr.jpg")
        return self
