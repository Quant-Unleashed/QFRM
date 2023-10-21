a = 1
b = 2
c = 3

class addition():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
    def summation(self):
        tot  = self.a + self.b + self.c
        return tot

asd = addition(a,b,c)
print(asd.summation())
