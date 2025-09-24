
from elementary_division.elementary_division import ElementaryDivision
import random
import os
import sys
from utils import pdf
from utils.number_bases import convert_to_base
from utils.unicodes import SUBSCRIPT_NUMBERS

from elementary_division.computer_number_system.addition_and_subtraction.addition_and_subtraction import AdditionAndSubtraction
from elementary_division.computer_number_system.binary_and_hexadecimal.binary_and_hexadecimal import BinaryAndHexadecimal
from elementary_division.computer_number_system.decimal_to_binary.decimal_to_binary import DecimalToBinary
from elementary_division.computer_number_system.expanded_form.expanded_form import ExpandedForm
from elementary_division.computer_number_system.find_number.find_number import FindNumber
from elementary_division.computer_number_system.rgb_coding.rgb_coding import RGBCoding
from elementary_division.computer_number_system.transforming_number_bases.transforming_number_bases import TransformNumberBases


class ComputerNumberSystem(ElementaryDivision):

    def __init__(self):
        super().__init__()

        self.title = "Computer Number System"

        self.chapter_classes = {'ExpandedForm': ExpandedForm(),
                                'TransformNumberBases': TransformNumberBases(),
                                'DecimalToBinary': DecimalToBinary(),
                                'BinaryAndHexadecimal': BinaryAndHexadecimal(),
                                'FindNumber': FindNumber(),
                                'AdditionAndSubtraction': AdditionAndSubtraction(),
                                'RGBCoding': RGBCoding()
                                }
        self.chapter = list(self.chapter_classes.keys())


    def get_problem_answer(self, start_chapter: str = None, end_chapter: str = None) -> tuple[list[str], list[str]]:

        if start_chapter and end_chapter:
            try:
                start_index = self.chapter.index(start_chapter)
                end_index = self.chapter.index(end_chapter)
                selected_chapters = self.chapter[start_index:end_index+1]
            except ValueError:
                print(f"Error: Invalid chapter name provided. '{start_chapter}', '{end_chapter}'")
                return [], []
        else:
            selected_chapters = self.chapter

        if not selected_chapters:
            print("Error: The specific chapter range is empty.")
            return [], []

        random.shuffle(selected_chapters)
        problem_set = []
        answer_set = []

        for chapter_name in selected_chapters:
            chapter_instance = self.chapter_classes.get(chapter_name)

            if chapter_instance:
                try:
                    problem, answers = chapter_instance.get_problem_answer()
                    problem_set.append(problem)
                    answer_set.append(answers)
                except Exception as e:
                    print(f"Error generating problem for chapter '{chapter_name}': {e}")
            else:
                print(f"Error: Chapter '{chapter_name}' not found in registry.")

        print(f"Problem set: {len(problem_set)}")
        print(f"Answers set: {len(answer_set)}")
        return problem_set, answer_set

    def generate_practice(self, start_chapter: str = None, end_chapter: str = None, problem_set: int = 1):
        num_of_problems = 0
        problem_list = []
        answer_list = []

        while num_of_problems < problem_set:
            problem, answer = self.get_problem_answer(start_chapter, end_chapter)

            # Check if the returned lists are not empty
            if not problem:
                print("No problems were generated in the current set. Stopping.")
                break

            problem_list.extend(problem)
            answer_list.extend(answer)
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


def main():
    # self.chapter = ['ExpandedForm', 'TransformNumberBases', 'DecimalToBinary', 'BinaryAndHexadecimal', 'FindNumber', 'AdditionAndSubtraction', 'RGBCoding']
    ComputerNumberSystem().generate_practice(None, None, 2)

if __name__ == "__main__":
    main()