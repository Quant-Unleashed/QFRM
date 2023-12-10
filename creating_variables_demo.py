import sys
import time
import ctypes
import gc
import string

# variable
a = [1, 2, 3]
b = a
# memory address
id(a)

a_add = id(a)

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

list1 = [1,2,3]
id(list1)
list1.append(4)
list1
id(list1)


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

# Beware of mutable object as optional parameter
def add_item(name, quantity, unit, grocery_list=[]):
    item_fmt = "{0} ({1} {2})".format(name, quantity, unit)
    grocery_list.append(item_fmt)
    return grocery_list

store_1 = add_item('bananas', 2, 'units')
add_item('grapes', 1, 'bunch', store_1)
store_1
store_2 = add_item('milk', 1, 'gallon')
print(store_2)


def add_item(name, quantity, unit, grocery_list=None):
    if not grocery_list:
        grocery_list = []
    item_fmt = "{0} ({1} {2})".format(name, quantity, unit)
    grocery_list.append(item_fmt)
    return grocery_list

store_1 = add_item('bananas', 2, 'units')
add_item('grapes', 1, 'bunch', store_1)
store_2 = add_item('milk', 1, 'gallon')
store_2


# Mutable as favourable optional parameter
def factorial(n):
    if n < 1:
        return 1
    else:
        print('calculating {0}!'.format(n))
        return n * factorial(n-1)

factorial(3)
factorial(4)
factorial(3)

def factorial(n, cache={}):
    if n < 1:
        return 1
    elif n in cache:
        return cache[n]
    else:
        print('calculating {0}!'.format(n))
        result = n * factorial(n-1)
        cache[n] = result
        return result


factorial(3)
factorial(5)
factorial(4)
factorial(7)


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

# unpacking iterables
a, b, c = [2, 3, 4]
print(a, b, c)
a, b = b, a
print(a, b, c)

# Unpacking sets and dictionaries. order may not be the same
x, y, z, a, b, c = {7: 'a', 0: 'z', 4: 'x', 2: 'b', 9: 'v', 1: 'c'}
print(x, y, z, a, b, c)


# Keywords and Positional parameters, *, *args and **kwargs ()
def func(a, b, *args):
    print(a, b, args)


func(1, 2, 'x', 'y', 'z')


def func1(a, b=2, *, c, d=4):
    print(a, b, c, d)


func1(c=3, a=1, b=2, d=4)
func1(c=3, a=1)


def func2(a, b, *, c, d=4, **kwargs):
    print(a, b, c, d, kwargs)


func2(x=100, y=200, z=300, c=3, b=2, a=1)

# Print also has *object
def func_print(name):
    '''    This is my first docString    '''

    print(name, "Hi!", sep='-', end=' *** ')
    print("I didn't know print has *args and more parameters")


func_print('Aman')

help(func_print)








