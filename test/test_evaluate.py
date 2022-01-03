from solver import *
import unittest


class TestSolver(unittest.TestCase):
    def test_node(self):
        node = Node(5)

        self.assertEqual(node.value, 5)
        self.assertEqual(node.left, None)
        self.assertEqual(node.right, None)

    def test_formulas(self):
        self.assertEqual(operators['+']['formula'](-5, 3), -2)
        self.assertEqual(operators['-']['formula'](-5, 3), -8)
        self.assertEqual(operators['*']['formula'](-5, 3), -15)
        self.assertAlmostEqual(operators['/']['formula'](-5, 3), -1.6666667)

    def test_is_integer(self):
        self.assertTrue(is_integer('5'))
        self.assertTrue(is_integer('-5'))

        self.assertFalse(is_integer('+5'))
        self.assertFalse(is_integer('5.15'))

    def test_normalise_expression(self):
        self.assertEqual(normalise_expression('   '), [])
        self.assertEqual(normalise_expression('+ 0 3'), ['3'])
        self.assertEqual(normalise_expression('( - 0 0 5 6 * 5 )'), ['(', '-56', '*', '5', ')'])
        self.assertEqual(normalise_expression('5 - 0 3 0'), ['5', '-', '30'])
        self.assertEqual(normalise_expression('+ ( 3 - 2 )'), ['(', '3', '-', '2', ')'])
        self.assertEqual(normalise_expression('- ( 3 - 2 )'), ['-1', '*', '(', '3', '-', '2', ')'])

    def test_validate_expression(self):
        self.assertTrue(validate_expression(['-5', '*', '(', '2', '+', '3', ')']))
        self.assertTrue(validate_expression(['-5']))
        self.assertTrue(validate_expression(['(', '-5', ')']))
        self.assertTrue(validate_expression(['(', '(', '-5', ')', ')']))
        self.assertTrue(validate_expression(['2', '+', '(', '-5', ')', '*' '10']))

        self.assertFalse(validate_expression([]))
        self.assertFalse(validate_expression(['*']))
        self.assertFalse(validate_expression([')', '(']))
        self.assertFalse(validate_expression(['(', ')']))
        self.assertFalse(validate_expression(['(', '(', ')']))
        self.assertFalse(validate_expression(['-5', '+']))
        self.assertFalse(validate_expression(['-5', '(', '2', '+', '3', ')']))

    def test_is_greater_precedence(self):
        self.assertTrue(is_greater_precedence('*', '+'))
        self.assertTrue(is_greater_precedence('/', '-'))
        self.assertTrue(is_greater_precedence('/', '/'))

        self.assertFalse(is_greater_precedence('+', '*'))
        self.assertFalse(is_greater_precedence('-', '/'))

    def test_build_tree(self):
        tree = build_tree(['(', '-5', '+', '3', ')'])

        self.assertEqual(tree.value, '+')
        self.assertEqual(tree.left.value, -5)
        self.assertEqual(tree.right.value, 3)

    def test_evaluate_expression_tree(self):
        tree = Node('+')
        tree.left = Node(-5)
        tree.right = Node(3)
        self.assertEqual(evaluate_expression_tree(tree), -2)

        tree_div_by_zero = Node('/')
        tree_div_by_zero.left = Node(-5)
        tree_div_by_zero.right = Node(0)
        self.assertRaises(ZeroDivisionError, evaluate_expression_tree, tree_div_by_zero)
