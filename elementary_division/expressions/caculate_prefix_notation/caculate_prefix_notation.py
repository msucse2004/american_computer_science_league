import os
import sys

from elementary_division.expressions.order_of_operations.order_of_operations import OrderOfOperations
from utils import pdf
from utils.expression import Expression


class CaculatePrefixNotation(Expression):
    def __init__(self):
        super().__init__()
        self._title = "Calculate Prefix Notation"
        self._operation_instance = OrderOfOperations()

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

    def generate_problem(self) -> tuple[str, str]:
        problem_text, answer_text = None, None

        self._operation_instance.number_of_nested = 3
        self._operation_instance.difficulty_level = 0.2
        self._operation_instance.frequency_exponential = 0.3

        # rule_negation, allowed_operators는 setter를 통해 문자열로 설정 가능
        self._operation_instance.rule_negation = "No"
        self._operation_instance.allowed_operators = '+-*/^'

        # rule_lower_upper_limit는 setter가 튜플을 받도록 정의되어 있으므로 튜플로 할당
        self._operation_instance.rule_lower_upper_limit = (-2000, 2000)

        while True:
            infix_notation = self._operation_instance.generate_random_expression()
            prefix_notation = self.infix_to_prefix(infix_notation)
            evaluation_prefix = self.evaluate_prefix(prefix_notation)
            if isinstance(evaluation_prefix, int):
                print(f"{infix_notation} -> {prefix_notation} = {evaluation_prefix}")
                problem_text = f"Calculate prefix notation. [{prefix_notation} =]"
                answer_text = str(evaluation_prefix)
                break

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
    topic_instance = CaculatePrefixNotation()
    topic_instance.generate_practice(5)

if __name__ == "__main__":
    main()