import os
import random
import sys

from utils import pdf
from utils.truth_table import TruthTable


class TruthTableKeywordOperation(TruthTable):
    BITWISE_OPERATIONS_KEYWORDS = ['NOT', 'AND', 'OR', 'XOR']
    BITWISE_OPERATIONS_SYMBOL = ['~', '*', '+', '^']
    def __init__(self):
        super().__init__()
        self._title = "Truth Table Text Operation"
        self._number_of_nested = 0

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
            operator = random.choice(operators)
            if operator == 'NOT':
                return f"({operator} {random.choice(["A", "B"])})"
            else:
                return f"(A {operator} B)"

        is_binary_structure = random.choice([True, False])

        left_part = self.generate_random_expression(depth + 1)
        operator = random.choice(operators)
        if operator == 'NOT':
            expression = f"{operator}({left_part})"

        else:
            right_part = self.generate_random_expression(depth + 1)
            expression = f"{left_part} {operator} {right_part}"

        # 괄호를 사용하여 중첩을 표현합니다.
        # 중첩 깊이가 0일 때는 가장 바깥쪽 괄호를 생략합니다.
        if depth == 0:
            return expression
        else:
            return f"({expression})"

    def generate_problem(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        problem_text = self.generate_random_expression()

        return problem_text, answer_text

    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        problem, _ = self.generate_problem()
        #print(f"gen problem: {problem}")
        self._initialize_internal_variables(problem)
        problem_printable = self.get_bitwise_keyword_expression(problem)

        problem_pool = [f"How many orderd pairs make the following statement TRUE? {problem_printable}",
                        f"How many orderd pairs make the following statement FALSE? {problem_printable}",
                        f"Determine which ordered pairs make the following statement TRUE? {problem_printable}",
                        f"Determine which ordered pairs make the following statement FALSE? {problem_printable}",
                        ]
        answer_pool = [f"{self.count_true_results()}",
                       f"{self.count_false_results()}",
                       f"{self.get_true_variable_combinations()}",
                       f"{self.get_false_variable_combinations()}",
                       ]

        #print(f"problems: {problem_pool}, answers: {answer_pool}")
        random_item = random.choice(problem_pool)
        random_index = problem_pool.index(random_item)

        problem_text = problem_pool[random_index]
        answer_text = answer_pool[random_index]

        print(f"{problem_text} {answer_text}")

        #print(f"True 결과 개수: {self.count_true_results()}")
        #print(f"False 결과 개수: {self.count_false_results()}")
        #print(f"True일 때의 (A, B) 조합: {self.get_true_variable_combinations()}")
        #print(f"False일 때의 (A, B) 조합: {self.get_false_variable_combinations()}")

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
    topic_instance = TruthTableKeywordOperation()
    topic_instance.title = "Bitwise Operations"
    topic_instance.number_of_nested = 1
    topic_instance.generate_practice(10)


if __name__ == "__main__":
    main()