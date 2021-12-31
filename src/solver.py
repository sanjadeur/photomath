import re
import sys
from typing import List


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


operators = {
    # Addition
    '+': {
        'precedence': 0,
        'formula': lambda a, b: a + b
    },
    # Subtraction
    '-': {
        'precedence': 0,
        'formula': lambda a, b: a - b
    },
    # Multiplication
    '*': {
        'precedence': 1,
        'formula': lambda a, b: a * b
    },
    # Division
    '/': {
        'precedence': 1,
        'formula': lambda a, b: a / b
    }
}


def is_integer(value: str) -> bool:
    return re.match("[-]?\d+$", value) is not None


def normalise_expression(expression: str) -> List[str]:
    symbols = [''] + expression.split() + ['']
    normalised_expression = []
    i = 1

    while i < len(symbols) - 1:
        symbol = symbols[i]
        left = symbols[i - 1]
        right = symbols[i + 1]

        # E.g. converts '+ 0 3' to ['3'], and '( - 0 0 5 6 * 5 )' to ['(', '-56', '*', '5', ')']
        if ((symbol == '+' or symbol == '-') and (left == '' or left == '(') and is_integer(right)) or (
                is_integer(symbol) and is_integer(right)):
            new_symbol = symbol + right
            i += 1
            right = symbols[i + 1]

            while is_integer(right):
                new_symbol += right
                i += 1
                right = symbols[i + 1]

            normalised_expression.append(str(int(new_symbol)))

        else:
            normalised_expression.append(symbol)

        i += 1

    return normalised_expression


def validate_expression(expression: List[str]) -> bool:
    if len(expression) == 0:
        return False

    symbols = [''] + expression + ['']
    brackets_counter = 0

    for i in range(1, len(symbols) - 1):
        symbol = symbols[i]
        left = symbols[i - 1]
        right = symbols[i + 1]

        # Check operator's surroundings
        if symbol in operators.keys():
            if not ((is_integer(left) or left == ')') and (is_integer(right) or right == '(')):
                return False

        # Check left bracket's surroundings
        elif symbol == '(':
            if is_integer(left) or left == ')':
                return False
            brackets_counter += 1

        # Check right bracket's surroundings
        elif symbol == ')':
            if is_integer(right) or left == '(':
                return False
            # Check that no right bracket appears before the left one
            brackets_counter -= 1
            if brackets_counter < 0:
                return False

    # Check that all brackets are closed
    return brackets_counter == 0


def is_greater_precedence(operator1: str, operator2: str) -> bool:
    return operators[operator1]['precedence'] >= operators[operator2]['precedence']


def build_tree(expression: List[str]) -> Node:
    stack = []
    tree_stack = []

    for i in expression:
        if i not in ['+', '-', '*', '/', '(', ')']:
            tree = Node(int(i))
            tree_stack.append(tree)

        elif i in operators.keys():
            if not stack or stack[-1] == '(':
                stack.append(i)

            elif is_greater_precedence(i, stack[-1]):
                stack.append(i)

            else:
                while stack and is_greater_precedence(stack[-1], i):
                    popped_item = stack.pop()
                    tree = Node(popped_item)
                    tree1 = tree_stack.pop()
                    tree2 = tree_stack.pop()
                    tree.right = tree1
                    tree.left = tree2
                    tree_stack.append(tree)
                stack.append(i)

        elif i == '(':
            stack.append('(')

        elif i == ')':
            while stack[-1] != '(':
                popped_item = stack.pop()
                tree = Node(popped_item)
                tree1 = tree_stack.pop()
                tree2 = tree_stack.pop()
                tree.right = tree1
                tree.left = tree2
                tree_stack.append(tree)
            stack.pop()

    while stack:
        popped_item = stack.pop()
        tree = Node(popped_item)
        tree1 = tree_stack.pop()
        tree2 = tree_stack.pop()
        tree.right = tree1
        tree.left = tree2
        tree_stack.append(tree)

    tree = tree_stack.pop()
    return tree


def evaluate_expression_tree(expression_tree: Node) -> str:
    left = expression_tree.left
    right = expression_tree.right

    if left and right:
        func = operators[expression_tree.value]['formula']
        return func(evaluate_expression_tree(left), evaluate_expression_tree(right))
    else:
        return expression_tree.value


def evaluate(expression: str) -> None:
    expression = normalise_expression(expression)

    if validate_expression(expression):
        expression_tree = build_tree(expression)

        try:
            print(f'Result: {evaluate_expression_tree(expression_tree)}')

        except ZeroDivisionError:
            sys.stderr.write('Division by zero is not allowed\n')

    else:
        sys.stderr.write('Math expression does not follow the infix notation\n')


if __name__ == '__main__':
    evaluate('- 0 3 + 4 * 2 / ( + 1 0 - 5 )')
