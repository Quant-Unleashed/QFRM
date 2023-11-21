a = 1
b = 2
c = 3


class Addition():
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c

    def summation(self):
        tot = self.a + self.b + self.c
        return tot


asd = Addition(a, b, c)
print(asd.summation())
