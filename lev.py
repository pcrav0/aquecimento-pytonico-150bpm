#from functools import cache
#@cache

cache = {}
def lev(a, b):
    if result := cache.get((a,b)):
        return result

    if len(b) == 0:
        result = len(a)
        cache[(a,b)] = result
        return result

    if len(a) == 0:
        result = len(b)
        cache[(a,b)] = result
        return result

    if a[0] == b[0]:
        result = lev(a[1:], b[1:])
        cache[(a,b)] = result
        return result

    remove = lev(a[1:], b)
    insert = lev(a, b[1:])
    replace = lev(a[1:], b[1:])
    result = 1 + min(remove, insert, replace)
    cache[(a,b)] = result
    return result


k = 'kitten'
assert lev(k, '') == len(k)
assert lev('', k) == len(k)
assert lev(k, k) == 0
assert lev(k, 'sitting') == 3
assert lev('apple', 'dapple') == 1

def lev_nocache(a, b):
    if len(b) == 0:
        return len(a)

    if len(a) == 0:
        return len(b)

    if a[0] == b[0]:
        return lev(a[1:], b[1:])

    remove = lev(a[1:], b)
    insert = lev(a, b[1:])
    replace = lev(a[1:], b[1:])
    return 1 + min(remove, insert, replace)

assert lev_nocache(k, '') == len(k)
assert lev_nocache('', k) == len(k)
assert lev_nocache(k, k) == 0
assert lev_nocache(k, 'sitting') == 3
assert lev_nocache('apple', 'dapple') == 1
