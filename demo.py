""" Text based demo of parse tree generation for convex optimization expressions. """
from parser import Parser

def main():
    welcome()
    parser = Parser()
    parse_file(parser)
    explore_parse_trees(parser)

def welcome():
    print "This is a demo of parse tree navigation."

def get_filename():
    return raw_input('Name of the convex optimization script file: ')

def parse_file(filename, parser):
    while True:
        try:
            filename = get_filename()
            f = open(filename, 'r')
            break
        except Exception, e:
            print "Invalid filename"
    for line in f.readlines():
        try:
          parser.parse(line)
        except Exception, e:
          print "Error parsing " + line

def select_expression(expressions):
    for i in range(len(expressions)):
        print "Expression %i: %s" % (i, str(expressions[i]))

    index = int(raw_input('Select an expression by index: '))
    return expressions[index]

def explore_parse_trees(parser):
    exp = select_expression(parser.expressions)
    while True:
        display_root(exp)
        prev = exp
        exp = select_child(exp, prev)

def display_root(exp):
    pass

def select_child(exp, prev):
    pass

if __name__ == "__main__":
    main()