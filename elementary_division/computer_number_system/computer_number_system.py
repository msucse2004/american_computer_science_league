
import random
import os
import sys

# Allow running this file directly (without requiring the project root on PYTHONPATH).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils import pdf
from utils.number_bases import convert_to_base
from utils.unicodes import SUBSCRIPT_NUMBERS

from elementary_division.computer_number_system.addition_and_subtraction.addition_and_subtraction import AdditionAndSubtraction
from elementary_division.computer_number_system.binary_and_hexadecimal.binary_and_hexadecimal import BinaryAndHexadecimal
from elementary_division.computer_number_system.decimal_to_binary.decimal_to_binary import DecimalToBinary
from elementary_division.computer_number_system.expanded_form.expanded_form import ExpandedForm
from elementary_division.computer_number_system.find_number.find_number import FindNumber
from elementary_division.computer_number_system.decimal_point_movement.decimal_point_movement import DecimalPointMovement
from elementary_division.computer_number_system.percent_increase_decrease.percent_increase_decrease import PercentIncreaseDecrease
from elementary_division.computer_number_system.percent_to_decimal.percent_to_decimal import PercentToDecimal
from elementary_division.computer_number_system.percent_to_fraction.percent_to_fraction import PercentToFraction
from elementary_division.computer_number_system.rgb_coding.rgb_coding import RGBCoding
from elementary_division.computer_number_system.transforming_number_bases.transforming_number_bases import TransformNumberBases


class ComputerNumberSystem():

    def __init__(self):

        self._title = "Computer Number System"

        self.chapter_classes = {'ExpandedForm': ExpandedForm(),
                                'TransformNumberBases': TransformNumberBases(),
                                
                                'FindNumber': FindNumber(),
                                'AdditionAndSubtraction': AdditionAndSubtraction(),
                                'RGBCoding': RGBCoding(),
                                }
        self.chapter = list(self.chapter_classes.keys())

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
        
        # Retry until all chapters succeed, or max attempts reached
        max_total_attempts = 10
        attempt = 0
        
        while attempt < max_total_attempts:
            problem_set = []
            answer_set = []
            failed_chapters = []
            
            for chapter_name in selected_chapters:
                chapter_instance = self.chapter_classes.get(chapter_name)

                if chapter_instance:
                    try:
                        problem, answers = chapter_instance.get_problem_answer()
                        problem_set.append(problem)
                        answer_set.append(answers)
                    except Exception as e:
                        # Collect failed chapters for retry
                        failed_chapters.append(chapter_name)
                else:
                    print(f"Error: Chapter '{chapter_name}' not found in registry.")
            
            # If all chapters succeeded, return the result
            if len(problem_set) == len(selected_chapters):
                print(f"Problem set: {len(problem_set)}")
                print(f"Answers set: {len(answer_set)}")
                return problem_set, answer_set
            
            # Otherwise, retry failed chapters
            attempt += 1
            if failed_chapters:
                print(f"Attempt {attempt}: Failed to generate problems for {len(failed_chapters)} chapter(s): {failed_chapters}. Retrying...")
        
        # If we exhausted all attempts, return what we have
        print(f"Warning: Could not generate problems for all chapters after {max_total_attempts} attempts.")
        print(f"Problem set: {len(problem_set)}/{len(selected_chapters)}")
        print(f"Answers set: {len(answer_set)}/{len(selected_chapters)}")
        return problem_set, answer_set

    def generate_practice(self, start_chapter: str = None, end_chapter: str = None, problem_set: int = 1):
        output_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Collect all problems and answers from all sets, with page breaks between sets
        problem_list = []
        answer_list = []

        for set_num in range(1, problem_set + 1):
            problem, answer = self.get_problem_answer(start_chapter, end_chapter)

            # Check if the returned lists are not empty
            if not problem:
                print(f"No problems were generated for set {set_num}. Skipping.")
                continue

            # Add problems for this set
            problem_list.extend(problem)
            answer_list.extend(answer)
            
            # Add page break marker (None) between sets (except after the last set)
            if set_num < problem_set:
                problem_list.append(None)  # Page break marker
                answer_list.append(None)   # Page break marker

        if not problem_list:
            print("No problems were generated. Cannot create PDF.")
            return

        # Calculate optimal spacing based on number of problems per set
        # Increase spacing to make problems more readable
        problems_per_set = len(self.chapter)  # Typically 5-7
        if problems_per_set <= 6:
            row_spacing_val = 85  # Increased from 70 to 85
        else:
            row_spacing_val = 80  # Increased from 65 to 80

        try:
            # Generate a single PDF containing all sets with page breaks between sets
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=2, row_spacing=row_spacing_val, output_dir=output_dir)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2, row_spacing=row_spacing_val, output_dir=output_dir)
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