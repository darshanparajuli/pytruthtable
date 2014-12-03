# Written by Darshan Parajuli, 12/02/2014

# Binary Tree node
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

# Helper class to evaluate most basic proposition
class LogicEvaluator:
    @staticmethod
    def evaluate(op, a, b):
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

# Evaluate a given proposition in tree form 
class TreeEvaluator:
    def __init__(self):
        self.valueTable = None
        self.operands = None
        self.resultTable = {}

    # valueTable is a list of tuples in the form (T, T, F, ..., n)
    # each tuple holds a permutation of T,T,F,...,n
    # operands is a list of operands i.e. p, q, r, etc
    def setInitialValues(self, operands, valueTable):
        self.operands = operands
        self.valueTable = valueTable

    # evaluate the tree for each given list of truth values
    def evaluate(self, tree):
        result = []
        for v in self.valueTable:
            value = dict()
            i = 0
            while i < len(self.operands):
                value[self.operands[i]] = v[i]
                i += 1

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

        b = None
        if tree.right != None:
            b = self.evaluateHelper(tree.right, valuepair)
            
        op = tree.value
        
        return LogicEvaluator.evaluate(op, a, b)

operators = ['<>', '>', '|', '&', '!']

# check if user input has errors
def hasErrors(expression):
    for i in range(0, len(expression) - 1):
        currOp = expression[i]
        nextOp = expression[i + 1]
        if currOp in operators:
            if nextOp in operators:
                return "consecutive operators"
            
        if currOp not in operators and currOp != '(' and currOp != ')':
            if nextOp not in operators and nextOp != '(' and nextOp != ')':
                return "consecutive operands"

    import collections
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
        if i not in operators and i != '(' and i != ')':
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
        if i not in operators:
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
        if l < 5:
            l = 5;
        lengths.append(l + 5)
            
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
            output[j + 1] += str(result[i][j]).ljust(lengths[i + templen])
                
    for i in output:
        print(i)

# main function, program starts here
def main():
    print("*******************************************************************************************")
    print("*Operators u can use:                                                                     *")
    print("* !  -> not, please use parenthesis, i.e ( ! p )                                          *")
    print("* &  -> and                                                                               *")
    print("* |  -> or                                                                                *")
    print("* >  -> implication                                                                       *")
    print("* <> -> bidirectional implication                                                         *")
    print("*   ***Please put a space between operators and operands***                               *")
    print("*   ***Don't do this -> (p&q) <- the whole thing will be treated as single operand!***    *")
    print("*Proper input example: ( p & q ) | ( ! r )                                                *")
    print("*******************************************************************************************\n")

    inputPrompt = "Enter a propositional sentence (type 'quit' to quit): "
    
    userInput = input(inputPrompt)

    evaluator = TreeEvaluator()
    
    while userInput != "quit":
        expression = list(userInput.split())
        error = hasErrors(expression)
        
        if error != False:
            print("Error: " + error)
        else:
            postFix = convertToPostFix(expression)
            trees = convertPostFixToTree(postFix)
        
            operands = [i for i in postFix if i not in operators]
            operands = list(set(operands))
            operands.sort()

            import itertools
            table = list(itertools.product([True, False], repeat = len(operands)))
            evaluator.setInitialValues(operands, table)
            
            exp = []
            result = []
            for i in trees:
                a = []
                getExpression(i, a)
                b = evaluator.evaluate(i)
                exp.append(' '.join(a))
                result.append(b)

            displayResult(operands, table, exp, result)

        userInput = input(inputPrompt)

    print("Bye!")

if __name__ == "__main__":
    main()
