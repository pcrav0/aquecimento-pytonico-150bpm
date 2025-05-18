class Node:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def next(self):
        if self.tail:
            return self.tail()

    def __eq__(self, other):
        if not other:
            return False

        return self.head == other.head and type(self.tail) == type(other.tail)

def sequence_reverse(end):
    if end == 0:
        return Node(end, None)

    return Node(end, lambda: sequence_reverse(end - 1))

def sequence(end, start=0):
    if start == end:
        return Node(start, None)

    return Node(start, lambda: sequence(end, start + 1))

zero = Node(0, None)
one = Node(0, lambda: Node(1, None))

assert sequence(0) == zero
assert sequence(1) == one
assert sequence(2) == Node(0, lambda: Node(1, lambda: Node(2, None)))
assert sequence(3) == Node(
    0,
    lambda: Node(
        1,
        lambda: Node(
            2,
            lambda: Node(
                3,
                None))))

# def take(node, n=None):
#     result = []
#     current = node

#     while current:
#         if n == 0: break
#         result.append(current.head)
#         current = current.next()
#         if not not n:
#             n -= 1

#     return result

def take(node, n=None, trace=None):
    if trace:
        print(node)

    if not node or n == 0:
        return []

    if not node.tail:
        return [node.head]

    return [node.head] + take(node.next(), n - 1 if n else None)


assert take(None) == []
assert take(zero) == [0]
assert take(one) == [0, 1]
assert take(sequence(2)) == [0, 1, 2]
assert take(sequence(3)) == [0, 1, 2, 3]
assert take(sequence(10), 5) == [0, 1, 2, 3, 4]

def inf(n):
    return Node(n, lambda: inf(n + 1))

assert inf(0).head == 0
assert inf(30).head == 30
assert inf(5).next().head == 6

def fil(node, predicate):
    if not node:
        return node

    if predicate(node.head):
        return Node(node.head, lambda: fil(node.next(), predicate))
    else:
        return fil(node.next(), predicate)


assert fil(None, lambda _: True) == None
assert fil(sequence(2), lambda _: True) == sequence(2)
assert fil(sequence(10), lambda _: True) == sequence(10)
assert fil(sequence(4), lambda n: n % 2 == 0) == Node(
    0,
    lambda: Node(
        2,
        lambda: Node(
            4,
            Node)))

def sieve(node):
    if not node:
        return node

    return Node(
        node.head,
        lambda: sieve(fil(node.next(), lambda n: n % node.head != 0)))

prime = sieve(inf(2))
