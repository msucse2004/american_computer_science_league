import os
import random
import sys

from elementary_division.boolean_algebra.evaluate_algebra.evaluate_algebra import EvaluateAlgebra
from utils import pdf


class BitwiseOperation():
    BITWISE_OPERATIONS = ['NOT', 'AND', 'OR', 'XOR']
    BITWISE_OPERATION_MAP = {
        'NOT': lambda x, y: not x,
        'AND': lambda x, y: x and y,
        'OR': lambda x, y: x or y,
        'XOR': lambda x, y: x != x,}

    def __init__(self):
        self._title = "Bitwise Operations"
        self._number_of_nested = 0
        self._algebra_instance = EvaluateAlgebra()

    @property
    def title(self):
        """Returns the title of the expression type."""
        return self._title

    @title.setter
    def title(self, value):
        """Sets the title of the expression type."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string.")
        self._title = value

    @property
    def number_of_nested(self):
        return self._number_of_nested

    @number_of_nested.setter
    def number_of_nested(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Number of nested operations must be an integer greater than 0.")
        self._number_of_nested = value

    def operate_bitwise_operation(self, op, x, y):
        op_func = self.BITWISE_OPERATION_MAP[op]
        return op_func(x, y)

    def generate_random_expression(self, depth=0):

        operators = self.BITWISE_OPERATIONS

        if depth >= self._number_of_nested:
            return self._algebra_instance.generate_problem()

        is_binary_structure = random.choice([True, False])


        left_part, left_answer = self.generate_random_expression(depth + 1)
        operator = random.choice(operators)
        if operator == 'NOT':
            expression = f"{operator}({left_part})"
            answer = self.operate_bitwise_operation(operator, left_answer, left_answer)
        else:
            right_part, right_answer = self.generate_random_expression(depth + 1)
            expression = f"({left_part}) {operator} ({right_part})"
            answer = self.operate_bitwise_operation(operator, left_answer, right_answer)

        # 괄호를 사용하여 중첩을 표현합니다.
        # 중첩 깊이가 0일 때는 가장 바깥쪽 괄호를 생략합니다.
        if depth == 0:
            return expression, answer
        else:
            return f"({expression})", answer

    def generate_problem(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        problem_text, answer_text = self.generate_random_expression()

        return problem_text, answer_text

    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        problem_text, answer_text = self.generate_problem()
        print(f"{problem_text} {answer_text}")

        return problem_text, answer_text

    def generate_practice(self, number_of_problems: int = 10):
        num_of_problems = 0
        problem_list = []
        answer_list = []

        while num_of_problems < number_of_problems:
            problem, answer = self.get_problem_answer()
            problem_list.append(problem)
            answer_list.append(answer)
            num_of_problems += 1

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        module_path = os.path.join(parent_dir, "pdf_handling")

        if module_path not in sys.path:
            sys.path.append(module_path)

        try:
            pdf.generate_pdf_files(f"{self._title} Problems", problem_list, num_column=1, row_spacing=60)
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=4)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

def main():
    topic_instance = BitwiseOperation()
    topic_instance.title = "Bitwise Operations"
    topic_instance.number_of_nested = 2
    topic_instance.generate_practice(5)


if __name__ == "__main__":
    main()