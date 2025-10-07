#from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem
from utils.number_bases import convert_to_base
from utils.unicodes import SUBSCRIPT_NUMBERS, UNICODE_MULTIPLIER, SUPERSCRIPT_NUMBERS
import random
import os
import sys
from utils import pdf

class ExpandedForm():

    def __init__(self):
        #super().__init__()
        self._title = "Expanded Form"
        self._target_base = "Decimal"
        pass
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
    def target_base(self):
        return self._target_base

    @target_base.setter
    def target_base(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Target base must be a non-empty string.")
        self._target_base = value

    def generate_number_base(self)->tuple[int, str]:

        init_number = random.randint(1, 1000000)
        if self._target_base == "Decimal":
            target_base = 10
        else:
            target_base = random.randint(2, 16)

        converted_nuber = convert_to_base(10, target_base, str(init_number))
        return target_base, converted_nuber

    def convert_to_expanded_form(self, base: int, number: str) -> str:

        # Character set for digits, including A-F for bases > 10
        DIGITS = "0123456789ABCDEF"

        expanded_parts = []
        num_length = len(number)

        # Iterate through the number string from left to right
        for i in range(num_length):
            digit = number[i].upper()
            # Get the integer value of the digit
            digit_value = DIGITS.index(digit)

            # Calculate the power of the base
            power = num_length - 1 - i

            # Format the current term as a string
            term = f"{digit_value}{UNICODE_MULTIPLIER}{base}{SUPERSCRIPT_NUMBERS[str(power)]}"
            expanded_parts.append(term)

        # Join all the parts with " + "
        return " + ".join(expanded_parts)

    def get_problem_answer(self) -> (str, str):
        base, number = self.generate_number_base()
        expanded_form = self.convert_to_expanded_form(base, number)

        problem_text = f"Express the following number in expanded form {number} {SUBSCRIPT_NUMBERS[str(base)]} = "
        answer_text = expanded_form
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
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=1, row_spacing=70)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

#자신을 부모 클래스 레지스트리에 등록
#ComputerNumberSystem.register_child('ExpandedForm', ExpandedForm)

def main():
    topic_instance = ExpandedForm()
    topic_instance.title = "Expanded Form - Decimal (마루)"
    topic_instance.target_base = "Decimal"
    topic_instance.generate_practice(10)

    topic_instance.title = "Expanded Form - Various"
    topic_instance.target_base = "All"
    topic_instance.generate_practice(10)

if __name__ == "__main__":
    main()