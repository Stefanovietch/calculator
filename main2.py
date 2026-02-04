import argparse
parser = argparse.ArgumentParser()
parser.add_argument("first", type=int)
parser.add_argument("+", action="store")
parser.add_argument("-", action="store")
args = parser.parse_args()
print(args)

def add(self, x, y):
    """Adds numbers
    >>> add(1,2)
    3
    >>> add(-1,9)
    8
    """
    return x + y

def minus(self,x, y):
    """Subtract numbers
    >>> minus(1,2)
    -1
    >>> minus(-1,9)
    -10
    """
    return x - y