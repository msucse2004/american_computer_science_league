import os
import random
import sys

from utils import pdf
from utils.expression import Expression


class EvaluateAlgebra(Expression):
    _OPERATORS = ['+', '-', '*', '/']
    _EQUATIONS = ['=', '>', '<', '>=', '<=']

    def __init__(self):
        super().__init__()
        self._title = "Evaluate Algebra"

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

    def make_random_expression(self):
        choice = random.choice([True, False])
        if choice is True:
            left_term = random.randint(1, 10)
            right_term = random.randint(1, 10)
            operator = random.choice(EvaluateAlgebra._OPERATORS)
            expression = f"{left_term} {operator} {right_term}"
        else:
            left_term = random.randint(1, 10)
            middle_term = random.randint(1, 10)
            right_term = random.randint(1, 10)
            operator1 = random.choice(EvaluateAlgebra._OPERATORS)
            operator2 = random.choice(EvaluateAlgebra._OPERATORS)
            expression = f"{left_term} {operator1} {middle_term} {operator2} {right_term}"
        return expression


    def generate_problem(self) -> tuple[str, bool]:
        problem_text, answer_text = None, None

        while True:
            left = self.make_random_expression()
            answer = self.evaluate_infix(left)
            if isinstance(answer, int):
                break

        equality = random.choice(EvaluateAlgebra._EQUATIONS)

        decision_choice = random.choice([True, False])
        if decision_choice is True:
            if equality == '=':
                problem_text = f"{left} = {answer}"
            elif equality == '<' or equality == '<=':
                problem_text = f"{left} {equality} {random.randint(int(answer), int(answer)*2)}"
            elif equality == '>' or equality == '>=':
                problem_text = f"{left} {equality} {random.randint(int(answer)//2, int(answer)+1)}"
            answer_text = True
        else:
            if equality == '=':
                problem_text = f"{left} = {int(answer)+random.randint(1, 10)}"
            elif equality == '<' or equality == '<=':
                problem_text = f"{left} > {random.randint(int(answer)//2, int(answer))}"
            elif equality == '>' or equality == '>=':
                problem_text = f"{left} < {random.randint(int(answer)+1, int(answer)*2)}"
            answer_text = False


        return problem_text, answer_text

    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        problem_text, answer_text = self.generate_problem()
        print(f"{problem_text} {answer_text}")

        return problem_text, str(answer_text)

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
            pdf.generate_pdf_files(f"{self._title} Problems", problem_list, num_column=2, row_spacing=60)
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=4)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

def main():
    topic_instance = EvaluateAlgebra()
    topic_instance.generate_practice(5)


if __name__ == "__main__":
    main()