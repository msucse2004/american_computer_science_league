#from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem
from utils.number_bases import convert_to_base
from utils.unicodes import SUBSCRIPT_NUMBERS, UNICODE_MULTIPLIER, SUPERSCRIPT_NUMBERS
import random
import os
import sys
from utils import pdf


class FindNumber():
    def __init__(self):
        #super().__init__()
        self.title = "Find Number"
        pass

    def generate_number_list(self) -> list[int]:
        number_list = []
        for _ in range(0, 5):
            number_list.append(random.randint(100, 2000))
        return number_list

    def generate_random_base_number_list(self, number_list: list[int]) -> list[str]:
        random_base_number_list = []
        for i, number in enumerate(number_list):
            target_base = random.randint(2, 16)
            converted_num = convert_to_base(10, target_base, str(number))
            random_base_number_list.append(f"{converted_num}{SUBSCRIPT_NUMBERS[str(target_base)]}")
        return random_base_number_list

    def get_problem_answer(self) -> (str, str):
        selection_option = ['the smallest', 'the second smallest', 'the largest', 'the second largest']

        target_number = 0
        number_list = self.generate_number_list()
        option = random.choice(selection_option)
        converted_number_list = self.generate_random_base_number_list(number_list)

        sorted_number_list = sorted(number_list)

        if option == selection_option[0]:
            target_number = sorted_number_list[0]
        elif option == selection_option[1]:
            target_number = sorted_number_list[1]
        elif option == selection_option[2]:
            target_number = sorted_number_list[-1]
        elif option == selection_option[3]:
            target_number = sorted_number_list[-2]

        index = number_list.index(target_number)

        print(number_list, option, sorted_number_list, converted_number_list)
        print(index, converted_number_list[index])

        problem_text = f"Which of the following is {option} number? {converted_number_list}"
        answer_text = f"{converted_number_list[index]}, {number_list}"
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
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=2, row_spacing=70)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

#자신을 부모 클래스 레지스트리에 등록
#ComputerNumberSystem.register_child('FindNumber', FindNumber)

def main():
    FindNumber().generate_practice(5)

if __name__ == "__main__":
    main()