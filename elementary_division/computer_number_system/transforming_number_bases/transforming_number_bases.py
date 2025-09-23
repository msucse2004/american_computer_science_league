#from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem
import random
import os
import sys
from utils import pdf
from utils.number_bases import convert_to_base
from utils.unicodes import SUBSCRIPT_NUMBERS


class TransformNumberBases():
    def __init__(self):
        #super().__init__()
        self.title = "Transform Number Bases"
        pass

    def generate_number_base(self)->(int, str):

        init_number = random.randint(1, 1000)
        target_base = random.randint(2, 16)

        converted_nuber = convert_to_base(10, target_base, str(init_number))
        return target_base, converted_nuber

    def get_problem_answer(self) -> (str, str):
        base, number = self.generate_number_base()
        # expanded_form = get_expanded_form(base, number)
        target_base = random.randint(2, 16)
        answer = convert_to_base(base, target_base, str(number))

        problem_text = f"{number} {SUBSCRIPT_NUMBERS[str(base)]} converts to base {target_base} "
        answer_text = f"{answer}{SUBSCRIPT_NUMBERS[str(target_base)]}"

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
#ComputerNumberSystem.register_child('TransformNumberBases', TransformNumberBases)

def main():
    TransformNumberBases().generate_practice(5)

if __name__ == "__main__":
    main()