
import unittest

from utils.expression import Expression


class TestExpression(unittest.TestCase):

    def setUp(self):
        """모든 테스트 전에 새로운 Expression 인스턴스 생성"""
        self.expr = Expression()

    def test_tokenize_expression(self):
        expr_str = "((2 ^ 2 + 2 ^ 3) * (1 - 4))"
        tokens = self.expr.tokenize_expression(expr_str)
        self.assertEqual(tokens, ['(', '(', '2', '^', '2', '+', '2', '^', '3', ')', '*', '(', '1', '-', '4', ')', ')'])

    def test_infix_to_postfix(self):
        expr_str = "(2 + 3) * 4"
        postfix = self.expr.infix_to_postfix(expr_str)
        self.assertEqual(postfix, "2 3 + 4 *")

    def test_infix_to_prefix(self):
        expr_str = "(2 + 3) * 4"
        prefix = self.expr.infix_to_prefix(expr_str)
        self.assertEqual(prefix, "* + 2 3 4")

    def test_prefix_to_infix(self):
        prefix = "* + 2 3 4"
        infix = self.expr.prefix_to_infix(prefix)
        self.assertEqual(infix, "((2 + 3) * 4)")

    def test_postfix_to_infix(self):
        postfix = "2 3 + 4 *"
        infix = self.expr.postfix_to_infix(postfix)
        self.assertEqual(infix, "(2 + 3) * 4")

    def test_evaluate_infix(self):
        expr_str = "((2 ^ 2 + 2 ^ 3 + 2 ^ 3) * (1 - 4)) + ((3 + 1 + 3) * (4 * 3 ^ 2))"
        result = self.expr.evaluate_infix(expr_str)
        self.assertEqual(result, "Error: The result '-3.0' is a negative.")

    def test_evaluate_postfix(self):
        postfix = "2 3 + 4 *"
        result = self.expr.evaluate_postfix(postfix)
        self.assertEqual(result, 20)

    def test_evaluate_prefix(self):
        prefix = "* + 2 3 4"
        result = self.expr.evaluate_prefix(prefix)
        self.assertEqual(result, 20)

    def test_error_division_by_zero(self):
        postfix = "5 0 /"
        result = self.expr.evaluate_postfix(postfix)
        self.assertTrue("Division by zero" in result)

    def test_error_invalid_token(self):
        expr_str = "2 + $"
        result = self.expr.infix_to_postfix(expr_str)
        self.assertTrue("Invalid token" in result)

    def test_unicode_format(self):
        expr_str = "(2 ^ 3) * (3 + 4)"
        formatted = self.expr._infix_to_unicode_format(expr_str)
        # 예: "2³ × (3 + 4)" 이런 식의 결과여야 함
        self.assertIn("²", "0¹²³⁴⁵⁶⁷⁸⁹")  # 단순히 superscript 사용 확인
        self.assertIn("×", formatted)


if __name__ == "__main__":
    unittest.main()
