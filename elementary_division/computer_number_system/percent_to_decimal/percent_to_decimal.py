import os
import random
import sys

# Allow running this file directly (without requiring the project root on PYTHONPATH).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils import pdf


class PercentToDecimal:
    """
    Percent (%) -> Decimal conversion practice.
    - easy: 1% ~ 100%
    - medium: 1% ~ 1000%
    - hard: -1000% ~ 1000% (includes 0%)
    """

    def __init__(self, difficulty: str = "easy"):
        self.title = "Percent to Decimal"
        self.difficulty = difficulty

    @staticmethod
    def _normalize_difficulty(difficulty: str) -> str:
        if not isinstance(difficulty, str):
            raise ValueError("difficulty must be a string: 'easy', 'medium', or 'hard'")
        d = difficulty.strip().lower()
        if d not in {"easy", "medium", "hard"}:
            raise ValueError("difficulty must be 'easy', 'medium', or 'hard'")
        return d

    @property
    def difficulty(self) -> str:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: str):
        self._difficulty = self._normalize_difficulty(value)

    def _pick_percent(self) -> int:
        if self.difficulty == "easy":
            return random.randint(1, 100)
        if self.difficulty == "medium":
            return random.randint(1, 1000)
        # hard
        return random.randint(-1000, 1000)

    @staticmethod
    def _percent_to_decimal(p: int) -> str:
        """
        Returns decimal representation of p%.
        p% = p/100
        Examples: 25% = 0.25, 150% = 1.5, -50% = -0.5, 0% = 0
        """
        decimal_value = p / 100.0
        # Format to remove trailing zeros, but keep at least one decimal place if needed
        if decimal_value == int(decimal_value):
            return str(int(decimal_value))
        # Format to reasonable precision (up to 2 decimal places for most cases)
        formatted = f"{decimal_value:.10f}".rstrip('0').rstrip('.')
        return formatted

    def get_problem_answer(self) -> tuple[str, str]:
        p = self._pick_percent()
        decimal_str = self._percent_to_decimal(p)
        problem_text = f"Convert {p}% to a decimal: "
        answer_text = decimal_str
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
            label = f"{self.title} ({self.difficulty.title()})"
            pdf.generate_pdf_files(f"{label} Problems", problem_list, num_column=2, row_spacing=70, output_dir=output_dir)
            # Answers: 7 columns to fit more solutions per page
            pdf.generate_pdf_files(f"{label} Answers", answer_list, num_column=7, row_spacing=30, output_dir=output_dir)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")


def main():
    PercentToDecimal(difficulty="medium").generate_practice(50)


if __name__ == "__main__":
    main()



