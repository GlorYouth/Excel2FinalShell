class Box:
    def __init__(self, region: [int,int,int,int]):
        self.region = region

    def add_offset(self, offset:[int,int,int,int]):
        return Box([a + b for a, b in zip(offset, self.region)])

    def x(self):
        return self.region[0]

    def y(self):
        return self.region[1]

    def position(self):
        return Position(self.x(), self.y())

    def as_tuple(self):
        return self.region


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, pos: (int,int)):
        return Position(self.x + pos.x, self.y + pos.y)

    def as_tuple(self) -> (int,int):
        return self.x, self.y