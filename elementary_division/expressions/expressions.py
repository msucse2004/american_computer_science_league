import os
import random
import sys

from elementary_division.expressions.cacluate_infix_notation.calculate_infix_notation import CalculateInfixNotation
from elementary_division.expressions.caculate_prefix_notation.caculate_prefix_notation import CaculatePrefixNotation
from elementary_division.expressions.calculate_postfix_notation.calculate_postfix_notation import \
    CalculatePostfixNotation
from elementary_division.expressions.convert_infix_posfix.convert_infix_posfix import ConvertInfixPostfix
from elementary_division.expressions.convert_infix_prefix.convert_infix_prefix import ConvertInfixPrefix
from elementary_division.expressions.convert_prefix_postfix.convert_prefix_postfix import ConvertPrefixPostfix
from elementary_division.expressions.mathmatical_expression_to_infix_notation.mathmatical_expression_to_infix_notation import \
    MathmaticalExpressionToInfixNotation
from elementary_division.expressions.order_of_operations.order_of_operations import OrderOfOperations
from utils import pdf


class Expressions():
    def __init__(self):
        self._title = "Expressions"
        self.chapter_classes = {'OrderOfOperations': OrderOfOperations(),
                                'MathmaticalExpressionToInfixNotation': MathmaticalExpressionToInfixNotation(),
                                'CalculateInfixNotation': CalculateInfixNotation(),
                                'ConvertInfixPrefix': ConvertInfixPrefix(),
                                'ConvertInfixPostfix': ConvertInfixPostfix(),
                                'ConvertPrefixPostfix': ConvertPrefixPostfix(),
                                'CaculatePrefixNotation': CaculatePrefixNotation(),
                                'CalculatePostfixNotation': CalculatePostfixNotation()
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
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=1, row_spacing=70)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=1)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")


def main():
    # self.chapter = ['ExpandedForm', 'TransformNumberBases', 'DecimalToBinary', 'BinaryAndHexadecimal', 'FindNumber', 'AdditionAndSubtraction', 'RGBCoding']
    Expressions().generate_practice(None, None, 2)

if __name__ == "__main__":
    main()