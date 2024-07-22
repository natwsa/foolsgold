from random import *

def get_move(query, humanity):
    if humanity == 0:
        return raw_input(query)
    else:
        if query in ["Where do you play, Green? ", "Where do you play, Blue? ", "Which miner do you remove, Green? ", "Which miner do you remove, Blue? "]:
            return randrange(0,9)
        if query[:13] == "How many fool" or query in ["What card do you play, Green? ", "What card do you play, Blue? "]:
            return randrange(0,3)
        if query in ["Do you pay off a debt, Green? ", "Do you pay off a debt, Blue? "]:
            return randrange(0,1)
        if query in ["What's your bid, Green? ", "What's your bid, Blue? "]:
            return randrange(-10, 15)


def inty(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return -11