import itertools
import collections

# valid operators
OPERATORS = ['<>', '>', '|', '&', '!']

# Binary Tree node
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

# Evaluate a given proposition in tree form
class TreeEvaluator:
    def __init__(self):
        self.value_table = None
        self.operands = None

    # value_table is a list of tuples in the form (T, T, F, ..., n)
    # each tuple holds a permutation of T,T,F,...,n
    # operands is a list of operands i.e. p, q, r, etc
    def setInitialValues(self, operands, value_table):
        self.operands = operands
        self.value_table = value_table

    def evaluatePreposition(self, op, a, b):
        if op == '!':
            if a == None and b != None:
                return not b
            elif a != None and b == None:
                return not a
        elif op == '&':
            return a and b
        elif op == '|':
            return a or b
        elif op == ">":
            return (not a) or b
        elif op == "<>":
            return a == b
        else:
            return None

    # evaluate the tree for each given list of truth values
    def evaluate(self, tree):
        result = []
        for v in self.value_table:
            value = dict()
            for i in range(0, len(self.operands)):
                value[self.operands[i]] = v[i]

            a = self.evaluateHelper(tree, value)
            result.append(a)

        return result

    # recusively evaluate the expression
    def evaluateHelper(self, tree, valuepair):
        if tree.value in self.operands:
            return valuepair[tree.value]
        a = None
        if tree.left != None:
            a = self.evaluateHelper(tree.left, valuepair)
        b = self.evaluateHelper(tree.right, valuepair)
        op = tree.value
        return self.evaluatePreposition(op, a, b)

# check if user input has errors
def hasErrors(expression):
    for i in range(1, len(expression) - 1):
        prev = expression[i - 1]
        curr = expression[i]
        next = expression[i + 1]

        if curr == '!':
            if prev not in OPERATORS and prev != '(' and prev != ')':
                if next not in OPERATORS and next != '(' and next != ')':
                    return 'invalid use of !'

    for i in range(0, len(expression) - 1):
        currOp = expression[i]
        nextOp = expression[i + 1]
        nextNextOp = None

        if currOp in OPERATORS:
            if nextOp in OPERATORS:
                return "consecutive operators"

        if currOp not in OPERATORS and currOp != '(' and currOp != ')':
            if nextOp not in OPERATORS and nextOp != '(' and nextOp != ')':
                return "consecutive operands"

    if expression[-1] in OPERATORS:
        return 'invalid operator position'

    counter = collections.Counter(expression)

    if '(' in expression or ')' in expression:
        if counter['('] > counter[')']:
            return "closing parenthesis missing"
        elif counter['('] < counter[')']:
            return "opening parenthesis missing"

    return False

# converts the given infix expression to postfix expression, i.e. 3 + 4 -> 3 4 +
def convertToPostFix(expression):
    postFix = []
    stack = []

    order = ['(', '<>', '>', '|', '&', '!']

    for i in expression:
        if i not in OPERATORS and i != '(' and i != ')':
            postFix.append(i)
        elif i == '(':
            stack.append(i)
        elif i == ')':
            top = stack.pop()
            while top != '(':
                postFix.append(top)
                top = stack.pop()
        else:
            while len(stack) > 0 and order.index(stack[-1]) >= order.index(i):
                postFix.append(stack.pop())
            stack.append(i)

    while len(stack) > 0:
        postFix.append(stack.pop())

    return postFix

# build a tree for each column of the truth table with the given postfix expression
def convertPostFixToTree(postFix):
    stack = []
    trees = []

    for i in postFix:
        if i not in OPERATORS:
            stack.append(Node(i))
        else:
            a = stack.pop()
            b = None
            if i != '!':
                b = stack.pop()
            node = Node(i)
            node.right = a
            if b is not None:
                node.left = b

            stack.append(node)
            trees.append(node)

    return trees

# traverse the tree in-order so it displays the postfix data in infix i.e. 3 4 + -> 3 + 4
def getExpression(tree, exp):
    if tree == None:
        return;

    getExpression(tree.left, exp)
    exp.append(tree.value)
    getExpression(tree.right, exp)

# displays the final result in the table form
def displayResult(operands, table, exp, result):
    for i in range(0, len(operands)):
        exp.insert(0, operands[-(i + 1)])

    lengths = []
    for i in exp:
        l = len(i)
        if l < 2:
            l = 2;
        lengths.append(l + 2)

    output = []

    temp = ""
    for i in range(0, len(exp)):
        temp += exp[i].ljust(lengths[i])
    output.append(temp)


    for i in table:
        temp = ""
        for j in range(0, len(i)):
            temp += str(i[j]).ljust(lengths[j])
        output.append(temp)


    templen = len(table[0])
    for i in range(0, len(result)):
        for j in range(0, len(result[i])):
            output[j + 1] += str(int(result[i][j])).ljust(lengths[i + templen])


    for i in output:
        print(i)
    # print("Writing solution to solution.txt...", end = ' ')
    # f = None
    # try:
    #     f = open('solution.txt', 'a')
    #     for i in output:
    #         f.write('{}\n'.format(i))
    #     for i in output:
    #         f.write('{}'.format(len(i) * '#'))
    #         break
    #
    #     f.write('\n\n')
    # except Exception as e:
    #     print(str(e))
    # finally:
    #     if f != None:
    #         f.close()
    # print("done!")

def tokenize_input(user_input) -> list:
    user_input = user_input.strip().replace(' ', '')
    result = []
    size = len(user_input)
    i = 0
    while i < size:
        if i < size - 1:
            op = user_input[i:i+2]
            if op in OPERATORS:
                result.append(op)
                i = i + 1
            else:
                result.append(user_input[i])
        else:
            result.append(user_input[i])

        i = i + 1

    return result


def run(user_input, evaluator):
    expression = tokenize_input(user_input)
    error = hasErrors(expression)

    if error != False:
        print("Error: " + error)
    else:
        postFix = convertToPostFix(expression)
        # print('converted to postfix')

        # print(str(postFix))

        trees = convertPostFixToTree(postFix)
        # print('converted to postfix tree')

        operands = [i for i in postFix if i not in OPERATORS]
        operands = list(set(operands))
        operands.sort()

        table = list(itertools.product([1, 0], repeat = len(operands)))
        evaluator.setInitialValues(operands, table)
        # print('product complete')

        exp = []
        result = []
        for tree in trees:
            a = []
            getExpression(tree, a)
            # print('expression: {}'.format(a))
            b = evaluator.evaluate(tree)
            # print('evaluation complete')
            exp.append(' '.join(a))
            result.append(b)

        # print('done')
        # print("displaying results")
        displayResult(operands, table, exp, result)


# main function, program starts here
def main():
    print("*******************************************************************************************")
    print("*Operators u can use:                                                                     *")
    print("* !  -> not, please use parenthesis, i.e ( ! p )                                          *")
    print("* &  -> and                                                                               *")
    print("* |  -> or                                                                                *")
    print("* >  -> implication                                                                       *")
    print("* <> -> bidirectional implication                                                         *")
    print("*Proper input example: (p & q) | (!r)                                                *")
    print("*******************************************************************************************\n")

    input_prompt = "Enter a propositional sentence (enter 'exit' to quit): "

    evaluator = TreeEvaluator()

    while True:
        user_input = input(input_prompt).strip()
        if user_input == 'exit':
            break
        else:
            if len(user_input) > 0:
                run(user_input, evaluator)

    print("Bye!")

if __name__ == "__main__":
    # test_input = "a | b | c | d | e | f | g | h"
    # run(test_input, TreeEvaluator())
    main()
