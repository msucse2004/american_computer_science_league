#from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem
import random
import utils
from utils import pdf
from utils.expression import tokenize_expression, infix_to_postfix, evaluate_postfix
from utils.number_bases import convert_to_base
from utils.unicodes import SUBSCRIPT_NUMBERS
import os
import sys

NUM_PROBLEM_GENERATION = 10
NUM_NESTED = 2


class AdditionAndSubtraction():
    def __init__(self):
        #super().__init__()
        self.title = "Addition and Subtraction"

    def generate_number_base(self) -> (int, str, str, str):

        op1 = random.randint(1000, 100000)
        op2 = random.randint(1000, 100000)
        # target_base = random.choice([2, 16])
        target_base = random.randint(2, 16)
        op = random.choice(['+', '-'])

        converted_op1 = convert_to_base(10, target_base, str(op1))
        converted_op2 = convert_to_base(10, target_base, str(op2))
        return target_base, converted_op1, converted_op2, op
        pass


    def convert_base_of_expression(self, expression: str, base: int) -> str:
        tockens = tokenize_expression(expression)
        new_expression = []
        for tocken in tockens:
            if tocken.isdigit():
                converted_num = convert_to_base(10, base, tocken)
                new_expression.append(f"{converted_num}{SUBSCRIPT_NUMBERS[str(base)]}")
            else:
                new_expression.append(tocken)

        return " ".join(new_expression)

    @staticmethod
    def generate_random_expression(depth=0):
        """
        중첩 깊이가 2를 넘지 않는 무작위 수식을 생성합니다.

        Args:
            depth (int): 현재 재귀 호출의 깊이. 기본값은 0입니다.

        Returns:
            str: 생성된 무작위 수식 문자열.
        """
        # operators = ['+', '-', '*', '/']
        # operators = ['+', '-', '*', '÷']
        operators = ['+', '-']

        # 중첩 깊이가 2를 초과하면 숫자를 반환합니다.
        if depth >= NUM_NESTED:
            return str(random.randint(1, 1000))

        # 50% 확률로 숫자를 반환하여 수식의 복잡도를 조절합니다.
        # if random.choice([True, False]):
        #    return str(random.randint(1, 100))
        # 30% 확률로 숫자를 반환합니다.
        if random.random() < 0.2:  # 0.0에서 1.0 사이의 무작위 값
            return str(random.randint(1, 10))

        # 재귀적으로 새로운 수식 부분을 생성합니다.
        left_part = AdditionAndSubtraction.generate_random_expression(depth + 1)
        right_part = AdditionAndSubtraction.generate_random_expression(depth + 1)
        operator = random.choice(operators)

        # 괄호를 사용하여 중첩을 표현합니다.
        # 중첩 깊이가 0일 때는 가장 바깥쪽 괄호를 생략합니다.
        if depth == 0:
            return f"{left_part} {operator} {right_part}"
        else:
            # return f"({left_part} {operator} {right_part})"
            return f"{left_part} {operator} {right_part}"

    def get_problem_answer(self) -> (str, str):
        while True:
            random_expression = self.generate_random_expression()
            postfix = infix_to_postfix(random_expression)
            evaluation_result = evaluate_postfix(postfix)

            print(tokenize_expression(random_expression))
            target_base = random.randint(2, 16)

            if isinstance(evaluation_result, int):
                problem_text = self.convert_base_of_expression(random_expression, target_base)
                answer_text = f"{convert_to_base(10, target_base, str(evaluation_result))}{SUBSCRIPT_NUMBERS[str(target_base)]}"

                print(f"{random_expression} = {evaluation_result}")
                print(f"returning: {problem_text} {answer_text}")
                break

        return f"{problem_text} = ", answer_text

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
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=2, row_spacing=70)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

#자신을 부모 클래스 레지스트리에 등록
#ComputerNumberSystem.register_child('AdditionAndSubtraction', AdditionAndSubtraction)

def main():
    AdditionAndSubtraction().generate_practice(5)

if __name__ == "__main__":
    main()