import os
import random
import sys

# Allow running this file directly (without requiring the project root on PYTHONPATH).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils import pdf


class DecimalPointMovement:
    """
    Decimal point movement practice (multiplication/division by powers of 10).
    - easy: Simple decimals * 10, 100 or / 10, 100
    - medium: More complex decimals * 10, 100, 1000 or / 10, 100, 1000
    - hard: Larger numbers and more complex operations
    """

    def __init__(self, difficulty: str = "easy"):
        self.title = "Decimal Point Movement"
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

    def _generate_problem(self) -> tuple[str, str, str]:
        """
        Returns (base_number_str, operation_str, answer_str)
        operation_str is like "* 10" or "/ 100"
        Second operand (multiplier/divisor) is random from 10 to 1000000.
        """
        if self.difficulty == "easy":
            # Simple decimals: 0.1 to 9.9
            base = round(random.uniform(0.1, 9.9), random.choice([1, 2]))
        elif self.difficulty == "medium":
            # More complex: 0.01 to 99.99
            base = round(random.uniform(0.01, 99.99), random.choice([1, 2]))
        else:  # hard
            # Larger numbers: 0.001 to 999.999
            base = round(random.uniform(0.001, 999.999), random.choice([1, 2, 3]))

        # Random operation: multiplication or division
        op_symbol = random.choice(["*", "/"])
        
        # Second operand: powers of 10 based on difficulty
        if self.difficulty == "easy":
            # Only positive powers: 10^1 to 10^6 (10 to 1000000)
            power = random.randint(1, 6)
            multiplier = 10 ** power
        elif self.difficulty == "medium":
            # Positive and negative powers: 10^-6 to 10^6
            # 10^-6=0.000001, 10^-5=0.00001, ..., 10^-1=0.1, 10^1=10, ..., 10^6=1000000
            power = random.randint(-6, 6)
            if power == 0:
                power = 1  # Avoid 10^0 = 1
            multiplier = 10 ** power
        else:  # hard
            # All powers of 10 (positive and negative), and also negative versions
            use_negative = random.choice([True, False])
            power = random.randint(-6, 6)
            if power == 0:
                power = 1
            multiplier = 10 ** power
            if use_negative:
                multiplier = -multiplier

        # Format base number to remove trailing zeros
        base_str = f"{base:.10f}".rstrip('0').rstrip('.')
        if base_str.startswith('.'):
            base_str = '0' + base_str

        # Calculate answer
        if op_symbol == "*":
            answer = base * multiplier
        else:  # "/"
            answer = base / multiplier

        # Format answer to remove trailing zeros
        answer_str = f"{answer:.10f}".rstrip('0').rstrip('.')
        if answer_str.startswith('.'):
            answer_str = '0' + answer_str
        if answer_str.startswith('-.'):
            answer_str = '-0' + answer_str[1:]

        # Convert operation symbols to mathematical symbols for display
        display_symbol = "×" if op_symbol == "*" else "÷"
        
        # Format multiplier for display (avoid scientific notation)
        if multiplier < 0:
            multiplier_str = f"-{abs(multiplier):.10f}".rstrip('0').rstrip('.')
        elif multiplier < 1:
            multiplier_str = f"{multiplier:.10f}".rstrip('0').rstrip('.')
        else:
            multiplier_str = str(int(multiplier)) if multiplier == int(multiplier) else f"{multiplier:.10f}".rstrip('0').rstrip('.')
        
        operation_str = f"{display_symbol} {multiplier_str}"

        return base_str, operation_str, answer_str

    def get_problem_answer(self) -> tuple[str, str]:
        base_str, operation_str, answer_str = self._generate_problem()
        problem_text = f"What is {base_str} {operation_str}?"
        return problem_text, answer_str

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
            # Answers: 5 columns to fit more solutions per page
            pdf.generate_pdf_files(f"{label} Answers", answer_list, num_column=5, row_spacing=30, output_dir=output_dir)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")


def main():
    DecimalPointMovement(difficulty="easy").generate_practice(50)


if __name__ == "__main__":
    main()

