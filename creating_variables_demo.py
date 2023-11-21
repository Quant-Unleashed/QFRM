import sys
import time
import ctypes
import gc
import string

a = [1, 2, 3]

# Count number of references to the memory address of a variable using sys gives +1.
print(sys.getrefcount(a))
print(sys.getrefcount(a) - 1)


# Count number of references to the memory address of a variable
def ref_count(address: int):
    return ctypes.c_long.from_address(address).value


ref_count(id(a))


def object_by_id(object_id):
    for obj in gc.get_objects():
        if id(obj) == object_id:
            return "Object exists"
    return "Not found"


# Circular Refernce example
class A:
    def __init__(self):
        self.b = B(self)
        print('A: self: {0}, b: {1}'.format(hex(id(self)), hex(id(self.b))))


class B:
    def __init__(self, a):
        self.a = a
        print('B: self: {0}, a: {1}'.format(hex(id(self)), hex(id(self.a))))


gc.disable()

my_var = A()

gc.enable()

# function type
c = lambda x: x ** 2
print(c(2))


# Mutability vs immutability

tuple_1 = ([1,2], 'a')
print(id(tuple_1))

tuple_1[0].append(123)
print(id(tuple_1))


abc = [1,2,3,4]
xyz = abc
xyz.append(6)
print(abc)

abc.append(5)
print(xyz)


# is vs ==
a = [1,2,3]
b = [1,2,3]

print(a is b)
print(a == b)


# Singleton integer -5 to 256
a = 10
b = 10
print(a is b)

# In pycharm, for integers interning will work for all range when running together
c = 257
d = 257
print(c is d)

# String interning
def compare_using_equals(n):
    a = 'a b c d e f g h i j k l m n o p q r s t u v w x y z' * 2000
    b = 'a b c d e f g h i j k l m n o p q r s t u v w x y z' * 2000
    for i in range(n):
        if a == b:
            pass


def compare_using_interning(n):
    a = sys.intern('a b c d e f g h i j k l m n o p q r s t u v w x y z' * 2000)
    b = sys.intern('a b c d e f g h i j k l m n o p q r s t u v w x y z' * 2000)
    for i in range(n):
        if a is b:
            pass


start = time.perf_counter()
compare_using_equals(10000000)
end = time.perf_counter()
print('equality', end - start)
# equality 39.65362450003158


start = time.perf_counter()
compare_using_interning(10000000)
end = time.perf_counter()
print('interning', end - start)
# interning 0.20796779997181147

# Memory constants
print(compare_using_interning.__code__.co_consts)


char_list = list(string.ascii_letters)
char_tuple = tuple(string.ascii_letters)
char_set = set(string.ascii_letters)


def membership_test(n, container):
    for i in range(n):
        if 'z' in container:
            pass


start = time.perf_counter()
membership_test(100000000, char_list)
end = time.perf_counter()
print('list:', end - start)
# list: 25.494231599965133

start = time.perf_counter()
membership_test(100000000, char_tuple)
end = time.perf_counter()
print('tuple:', end - start)
# tuple: 26.66192039998714

start = time.perf_counter()
membership_test(100000000, char_set)
end = time.perf_counter()
print('set:', end - start)
# set: 3.0006126000080258

