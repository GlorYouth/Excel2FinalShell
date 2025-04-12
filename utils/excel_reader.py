import openpyxl

class Config:
    def __init__(self):
        self.name = ""
        self.host = ""
        self.port = 0
        self.username = ""
        self.password = ""

class ExcelReader:
    def __init__(self, path: str):
        self.df = openpyxl.open(path,True)
        self.sheet = self.df.worksheets[0]
        self.row_iter = self.sheet.iter_rows()
        next(self.row_iter)
        if self.df is None:
            exit("File doesn't exist")

    def read(self):
        config = Config()
        try:
            row = next(self.row_iter)
        except StopIteration:
            return None
        config.name = row[0].value
        config.host = row[1].value
        config.port = row[2].value
        config.username = row[3].value
        config.password = row[4].value
        return config

    def close(self):
        self.df.close()


def __test__():
    reader = ExcelReader("../ssh.xlsx")
    while True:
        row = reader.read()
        if row is None:
            break
        print(row.name,row.host,row.port,row.username,row.password)
