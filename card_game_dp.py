def b_zero(r):
    return 0


def r_zero(b):
    return b


def expect(r, b, ex=0):

    if r < 1 and b < 1:
        ex = 0

    elif r < 1 and b > 0:
        ex = r_zero(b)
        b -= 1

    elif r > 0 and b < 1:
        ex = b_zero(r)
        r -= 1
    else:
        if b <= r:
            ex += expect(r-1,b)
        else:
            ex += expect(r, b - 1)
    return ex



