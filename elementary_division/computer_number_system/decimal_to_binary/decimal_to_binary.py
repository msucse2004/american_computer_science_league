#from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem
from utils.number_bases import convert_to_base, NAME_OF_NUMBER_BASES
from utils.unicodes import SUBSCRIPT_NUMBERS, UNICODE_MULTIPLIER, SUPERSCRIPT_NUMBERS
import random
import os
import sys
from utils import pdf

class DecimalToBinary():
    def __init__(self):
        #super().__init__()
        self.title = "Decimal to Binary"
        pass

    def generate_number_base(self)->(int, str):

        init_number = random.randint(1, 15)
        # target_base = random.randint(2, 16)
        target_base = 10

        converted_nuber = convert_to_base(10, target_base, str(init_number))
        return target_base, converted_nuber

    def count_binary_digits(self, binary_number:str)-> (int, int):
        count_zero = binary_number.count('0')
        count_one = binary_number.count('1')
        return (count_zero, count_one)

    def make_simple_conversion_problem(self):
        base, number = self.generate_number_base()
        target_base = 2  # random.randint(2, 16)
        answer = convert_to_base(base, target_base, str(number))

        problem_text = f"{number} {SUBSCRIPT_NUMBERS[str(base)]} converts to base {target_base} ({NAME_OF_NUMBER_BASES[target_base]}) = "
        answer_text = f"{answer}{SUBSCRIPT_NUMBERS[str(target_base)]}"
        #print(
        #    f"{number} {SUBSCRIPT_NUMBERS[str(base)]} converts to base {target_base} = {answer}{SUBSCRIPT_NUMBERS[str(target_base)]}")
        return problem_text, answer_text

    def get_answer_for_digit_count_problem(self, comparision_choice: int, start_number: int, end_number: int) -> str:
        count = 0
        for number in range(start_number, end_number + 1):
            binary_representation = bin(number)[2:]  # Convert to binary and remove the '0b' prefix
            count_ones = binary_representation.count('1')
            count_zeros = binary_representation.count('0')

            # Check the condition based on the comparison choice
            if comparision_choice == 0:  # more 0s than 1s
                if count_zeros > count_ones:
                    count += 1
            elif comparision_choice == 1:  # more 1s than 0s
                if count_ones > count_zeros:
                    count += 1
            elif comparision_choice == 2:  # an equal number of 1s and 0s
                if count_ones == count_zeros:
                    count += 1

        return str(count)

    def make_digit_count_problem(self):
        comparision_map = {0: "more 0s than 1s", 1: "more 1s than 0s", 2: "an equal number of 1s and 0s"}
        comparision_choice = random.choice([0, 1, 2])
        start_number = random.randint(1, 100)
        range_value = random.randint(5, 10)

        problem_text = f"How many binary numbers have {comparision_map[comparision_choice]} in the range of numbers from {start_number} to {start_number + range_value}, inclusive in base 10?"
        answer_text = self.get_answer_for_digit_count_problem(comparision_choice, start_number, start_number + range_value)
        return problem_text, answer_text

    def generate_problem(self)->(str, str):

        simple_conversion_problem, simple_conversion_answer = self.make_simple_conversion_problem()
        digit_count_problem, digit_count_answer = self.make_digit_count_problem()

        problem_pool = [simple_conversion_problem,
                        digit_count_problem
                        ]
        answer_pool = [simple_conversion_answer,
                       digit_count_answer
                       ]

        #for problem, answer in zip(problem_pool, answer_pool):
        #    print(f"{problem} : {answer}")

        random_choice = random.randint(0, len(problem_pool)-1)
        return problem_pool[random_choice], answer_pool[random_choice]

    def get_problem_answer(self) -> (str, str):
        problem_text = f""
        answer_text = f""
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
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=2, row_spacing=100)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

def main():
    DecimalToBinary().generate_practice(5)

if __name__ == "__main__":
    main()