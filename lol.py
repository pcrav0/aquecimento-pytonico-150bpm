def Player(x, y):
    '''let over lambda'''

    def instance(method, *args, **kargs):
        match method:
            case "x":
                return x
            case "set-x":
                return Player(args[0], y)
            case "y":
                return y
            case "set-y":
                return Player(x, args[0])
    return instance


def Enemy(x, y):
    '''smart hash table'''

    return {
        "x": x,
        "y": y,
        "set-x": lambda n: Player(n, y),
        "set-y": lambda n: Player(x, n),
    }


p = Player(5, 6)
e = Enemy(3, 4)
