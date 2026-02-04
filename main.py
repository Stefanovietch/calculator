import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("string", action="store",  nargs='*')
args = parser.parse_args()
input_equation = " ".join(args.string)

class Operation:
    level = None
    def action(self, x, y):
        pass

class Add(Operation):
    def __init__(self):
        self.level = 4
    def action(self, x, y):
        """Adds numbers
        >>> Add().action(1,2)
        3
        >>> Add().action(-1,9)
        8
        """
        return x + y

class Minus(Operation):
    def __init__(self):
        self.level = 4
    def action(self, x, y):
        """Adds numbers
        >>> Minus().action(1,2)
        -1
        >>> Minus().action(-1,9)
        -10
        """
        return x - y

class Times(Operation):
    def __init__(self):
        self.level = 3
    def action(self, x, y):
        """Adds numbers
        >>> Times().action(1,2)
        2
        >>> Times().action(-1,9)
        -9
        """
        return x * y

class Division(Operation):
    def __init__(self):
        self.level = 3
    def action(self, x, y):
        """Adds numbers
        >>> Division().action(1,2)
        0.5
        >>> Division().action(-9,3)
        -3.0
        """
        return x / y

class Power(Operation):
    def __init__(self):
        self.level = 2
    def action(self, x, y):
        """Adds numbers
        >>> Power().action(1,2)
        1
        >>> Power().action(-9,2)
        81
        """
        return x ** y

class Root(Operation):
    def __init__(self):
        self.level = 2
    def action(self, x, y):
        """Adds numbers
        >>> Root().action(2,4)
        2.0
        >>> Root().action(3,27)
        3.0
        """
        return y ** (1/x)

class ClosingBracket(Operation):
    pass

class StartingBracket(Operation):
    pass

operators = {
    "+":Add(),
    "-":Minus(),
    "x":Times(),
    "/":Division(),
    "^":Power(),
    "r":Root(),
    "(":StartingBracket(),
    ")":ClosingBracket()
}

def text_parser(string):
    """Creates the equation from a string
    >>> text_parser("- 1 + 2.0 ")[0]
    -1.0
    >>> text_parser("15+8")[2]
    8.0
    >>> type(text_parser("     0+0.0000")[1]).__name__
    'Add'
    """
    string = string.replace(" ","")
    result = [x for x in re.split(r'([-+x/^r()]-?)', string) if x != ""]
    for i in range(len(result)):
        if re.match(r'[-+x/^r]-', result[i]):
            result[i] = result[i][0]
            result[i+1] = "-" + result[i+1]
    if len(result) > 1:
        if result[0] == "-":
            result[1] = "-" + result[1]
            del result[0]

    equation = []
    for elem in result:
        if elem in operators.keys():
            equation.append(operators[elem])
        else:
            try:
                equation.append(float(elem))
            except ValueError:
                print("Non number entered:", elem)
    return equation

def equation_parser(equation_list):
    """Calculates the equation from list
    >>> equation_parser([1,Add(),2])
    3
    >>> equation_parser([15,Add(),8,Minus(),21])
    2
    >>> equation_parser([2,Root(),2,Root(),81])
    3.0
    """
    if not equation_list:
        return None
    #print(equation_list)
    while True:
        ops = [x for x in equation_list if isinstance(x, Operation)]
        if not ops:
            break
        if not isinstance(ops, list):
            ops = [ops]
        o_brackets = [i for i, x in enumerate(equation_list) if isinstance(x, StartingBracket)]
        c_brackets = [i for i, x in enumerate(equation_list) if isinstance(x, ClosingBracket)]
        if c_brackets:
            first_close = c_brackets[0]
            first_open = max([b for b in o_brackets if b < first_close])
            equation_list[first_close] = equation_parser(equation_list[first_open+1:first_close])
            del equation_list[first_open:first_close]
            continue
        for level in range(0,6):
            opps_index = [i for i, x in enumerate(equation_list) if isinstance(x, Operation) if x.level == level]
            if not opps_index:
                continue
            opp_index = opps_index[-(level == 2)]
            cur_op = equation_list[opp_index]
            equation_list[opp_index+1] = cur_op.action(equation_list[opp_index-1],equation_list[opp_index+1])
            del equation_list[opp_index-1:opp_index+1]
            break

    return equation_list[0]

print(equation_parser(text_parser(input_equation)))

if __name__ == "__main__":
    import doctest
    doctest.testmod()

