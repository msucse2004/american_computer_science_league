import os
import random
import sys

from utils import pdf
from utils.expression import Expression


class OrderOfOperations(Expression):
    _OPERATORS = ['+', '-', '*', '/', '^']

    def __init__(self):
        super().__init__()
        self._title = "Order of Operations"

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
    def allowed_operators(self):
        """수식 생성에 허용되는 연산자 리스트를 반환합니다. (+, -, *, /, ^)"""
        return self._allowed_operators

    @allowed_operators.setter
    def allowed_operators(self, operators):
        """
        수식 생성에 사용할 연산자 리스트를 설정합니다.
        문자열(쉼표, 공백, 연속) 또는 리스트를 입력받을 수 있습니다.

        Args:
            operators (list or str): 허용되는 연산자 (예: ['+', '*'], "+-", "+, *").
        """

        if isinstance(operators, str):
            # 1. 모든 공백 제거 (사용자가 "+, *"처럼 입력했을 때 공백을 제거)
            normalized_str = operators.replace(' ', '')

            if ',' in normalized_str:
                # 2. 쉼표가 포함된 경우: 쉼표를 기준으로 분리합니다. (예: "+,*-" -> ['+', '*-']는 아님, ['+', '*', '-']여야 함)
                # 쉼표를 기준으로 분리 후, 각 요소를 개별 문자로 다시 분리해야 할 필요성이 생길 수 있으므로,
                # 가장 안전하게는 쉼표를 기준으로 분리된 각 부분을 유효성 검사하는 것이 좋습니다.
                op_list = [op for sub_str in normalized_str.split(',') for op in sub_str if op]
            else:
                # 3. 쉼표가 없는 경우: 문자열을 개별 문자로 분리합니다. (예: "+-*^" -> ['+', '-', '*', '^'])
                op_list = list(normalized_str)

        elif isinstance(operators, list):
            # 리스트 입력 시, 문자열로 변환하고 양쪽 공백 제거
            op_list = [str(op).strip() for op in operators if str(op).strip()]
        else:
            raise TypeError("Allowed operators must be a list or a comma/space-separated string.")

        valid_ops = self._OPERATORS

        if not op_list:
            raise ValueError("The list of allowed operators cannot be empty.")

        # 모든 연산자가 유효한지 확인
        if not all(op in valid_ops for op in op_list):
            invalid_ops = [op for op in op_list if op not in valid_ops]
            raise ValueError(f"Invalid operator(s) found: {', '.join(invalid_ops)}. Allowed operators are: {valid_ops}")

        self._allowed_operators = op_list

    def generate_random_expression(self, depth=0):

        operators = self._allowed_operators

        if depth >= self.number_of_nested:
            if '^' in self._allowed_operators and random.random() < self.frequency_exponential:  # 0.0에서 1.0 사이의 무작위 값
                base = random.randint(2, 5)
                power = random.randint(2, 3)
                return f"{str(base)} ^ {str(power)}"
            else:
                return str(random.randint(1, 10))

        #if random.random() < self.difficulty_level:  # 0.0에서 1.0 사이의 무작위 값
            #print("!!! difficulty level down !!!")
        #    return str(random.randint(1, 10))


        if random.randint(1, 1000) % 2 == 0:
            left_part = self.generate_random_expression(depth + 1)
            operator = random.choice(operators)

            if operator == '^':
                right_part = str(random.randint(2, 3))
            else:
                right_part = self.generate_random_expression(depth + 1)

            expression = f"{left_part} {operator} {right_part}"
        else:
            operator1 = random.choice(operators)
            operator2 = random.choice(operators)
            left_part = self.generate_random_expression(depth + 1)
            if operator1 == '^':
                middle_part = str(random.randint(2, 3))
            else:
                middle_part = self.generate_random_expression(depth + 1)
            if operator2 == '^':
                right_part = str(random.randint(2, 3))
            else:
                right_part = self.generate_random_expression(depth + 1)

            expression = f"{left_part} {operator1} {middle_part} {operator2} {right_part}"

        # 괄호를 사용하여 중첩을 표현합니다.
        # 중첩 깊이가 0일 때는 가장 바깥쪽 괄호를 생략합니다.
        if depth == 0:
            return expression
        else:
            return f"({expression})"


    def generate_problem(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        while True:
            random_expression = self.generate_random_expression()
            postfix = self.infix_to_postfix(random_expression)
            if isinstance(postfix, str) and postfix.startswith("Error"):
                continue
            evaluation_result = self.evaluate_postfix(postfix)
            if isinstance(evaluation_result, int):
                problem_text = f"{self._format_expression_unicode(random_expression)} ="
                answer_text = str(evaluation_result)
                print(f"{random_expression} ==> {self._format_expression_unicode(random_expression)} = {evaluation_result}")
                break

        return problem_text, answer_text

    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        problem_text, answer_text = self.generate_problem()
        print(f"{problem_text} = {answer_text}")

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

    #expression = "((3 ^ 3) ^ 2) - ((8 * 4 ^ 3) + (7 - 3))"
    #unicode_expression = OrderOfOperations()._format_expression_unicode(expression)
    #print(unicode_expression)
    topic_instance = OrderOfOperations()
    topic_instance.title = "Order of Operations - 1"
    topic_instance.number_of_nested = 1
    topic_instance.difficulty_level = 0.2
    topic_instance.frequency_exponential = 0.3

    # rule_negation, allowed_operators는 setter를 통해 문자열로 설정 가능
    topic_instance.rule_negation = "No"
    topic_instance.allowed_operators = '+-*/'

    # rule_lower_upper_limit는 setter가 튜플을 받도록 정의되어 있으므로 튜플로 할당
    topic_instance.rule_lower_upper_limit = (-3000, 3000)

    topic_instance.generate_practice(5)

    topic_instance.title = "Order of Operations - 2"
    topic_instance.number_of_nested = 3
    topic_instance.allowed_operators = '+-*/'
    topic_instance.generate_practice(5)

    topic_instance.title = "Order of Operations - 3"
    topic_instance.number_of_nested = 1
    topic_instance.allowed_operators = '+-*/^'
    topic_instance.generate_practice(5)

    topic_instance.title = "Order of Operations - 4"
    topic_instance.number_of_nested = 3
    topic_instance.allowed_operators = '+-*/^'
    topic_instance.generate_practice(5)

if __name__ == "__main__":
    main()