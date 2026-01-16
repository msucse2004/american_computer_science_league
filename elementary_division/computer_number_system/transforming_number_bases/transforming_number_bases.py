#from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem
import random
import os
import sys

# Allow running this file directly (without requiring the project root on PYTHONPATH).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils import pdf
from utils.number_bases import convert_to_base, NAME_OF_NUMBER_BASES
from utils.unicodes import SUBSCRIPT_NUMBERS


class TransformNumberBases():
    def __init__(self):
        #super().__init__()
        self.title = "Transform Number Bases"
        pass

    def get_problem_answer_hex_to_decimal(self) -> (str, str):
        """
        Generate a problem converting hexadecimal (0x1 to 0xff) to decimal.
        """
        # Random number from 1 to 255 (0x1 to 0xff)
        decimal_value = random.randint(1, 255)
        hex_value = convert_to_base(10, 16, str(decimal_value)).upper()
        
        problem_text = f"0x{hex_value} converts to base 10 (decimal) = "
        answer_text = str(decimal_value)
        
        return problem_text, answer_text


    def generate_number_base(self)->(int, str):
        # Generate random base between 2 and 16
        init_number = random.randint(1, 15)
        target_base = random.randint(2, 16)

        converted_nuber = convert_to_base(10, target_base, str(init_number))
        return target_base, converted_nuber

    def get_problem_answer(self) -> (str, str):
        # Generate random source base (2-16)
        decimal_value = random.randint(1, 255)
        
        source_base = random.randint(2, 16)
        target_base = random.randint(2, 16)

        while target_base == source_base:
            target_base = random.randint(2, 16)

        source_number = convert_to_base(10, source_base, str(decimal_value))
        target_number = convert_to_base(source_base, target_base, str(source_number))

        problem_pool = [
            f"{source_number}{SUBSCRIPT_NUMBERS[str(source_base)]} converts to base {target_base} ({NAME_OF_NUMBER_BASES[target_base]}) = ",
            f"What is the base{target_base} ({NAME_OF_NUMBER_BASES[target_base]}) equivalent for {source_number}{SUBSCRIPT_NUMBERS[str(source_base)]}?"
        ]
        answer_pool = [
            f"{target_number}{SUBSCRIPT_NUMBERS[str(target_base)]}",
            f"{target_number}{SUBSCRIPT_NUMBERS[str(target_base)]}"
        ]
        # Randomly choose between two problem formats
        
        choice_index = random.randint(0, len(problem_pool)-1)

        problem_text = problem_pool[choice_index]
        answer_text = answer_pool[choice_index]
        
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

        output_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=2, row_spacing=70, output_dir=output_dir)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2, output_dir=output_dir)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

def main():
    topic_instance = TransformNumberBases()
    
    # Generate 100 problems: Hexadecimal to Decimal
    topic_instance.title = "Transform Number Bases"
    topic_instance.generate_practice(10)

if __name__ == "__main__":
    main()