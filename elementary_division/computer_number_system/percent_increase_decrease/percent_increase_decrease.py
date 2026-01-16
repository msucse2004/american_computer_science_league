import math
import os
import random
import sys

# Allow running this file directly (without requiring the project root on PYTHONPATH).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils import pdf


class PercentIncreaseDecrease:
    def __init__(self, difficulty: str = "easy"):
        """
        difficulty:
          - "easy": 초3 수준(10단위 시작값, 10% 단위 퍼센트, 정답도 1000 이하)
          - "medium": 이전에 만들었던 버전(여러 유형 랜덤, 퍼센트 다양, 간단한 문장형)
        """
        self.title = "Percent Increase and Decrease"
        self.difficulty = difficulty

    @staticmethod
    def _normalize_difficulty(difficulty: str) -> str:
        if not isinstance(difficulty, str):
            raise ValueError("difficulty must be a string: 'easy' or 'medium'")
        d = difficulty.strip().lower()
        if d not in {"easy", "medium"}:
            raise ValueError("difficulty must be 'easy' or 'medium'")
        return d

    @property
    def difficulty(self) -> str:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: str):
        self._difficulty = self._normalize_difficulty(value)

    def _pick_percent(self) -> int:
        if self.difficulty == "easy":
            # 3rd-grade friendly: multiples of 10 from 10% to 200%.
            return random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200])
        # medium
        return random.choice([5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75])

    @staticmethod
    def _pick_context() -> tuple[str, str]:
        """
        Returns (thing, unit) for light word-problem variety.
        Keep unit empty for unit-less quantities.
        """
        contexts = [
            ("a price", "dollars"),
            ("a population", "people"),
            ("a file size", "MB"),
            ("a score", "points"),
            ("a quantity", ""),
        ]
        return random.choice(contexts)

    @staticmethod
    def _trend_word(is_increase: bool) -> str:
        return random.choice(
            ["increase", "rise", "grow", "go up"] if is_increase else ["decrease", "fall", "drop", "go down"]
        )

    @staticmethod
    def _apply_percent(value: int, percent: int, is_increase: bool) -> int:
        mult = 100 + percent if is_increase else 100 - percent
        return (value * mult) // 100

    @staticmethod
    def _required_multiple_for_new_value(percent: int, is_increase: bool) -> int:
        """
        Ensure original*(100±p) is divisible by 100 so the new value is an integer.
        """
        mult = 100 + percent if is_increase else 100 - percent
        g = math.gcd(100, mult)
        return 100 // g

    @staticmethod
    def _required_multiple_for_old_value(percent: int, is_increase: bool) -> int:
        """
        Ensure new*100/(100±p) is an integer. Let mult=(100±p).
        Need new divisible by mult/gcd(100,mult).
        """
        mult = 100 + percent if is_increase else 100 - percent
        g = math.gcd(100, mult)
        return mult // g

    def _make_new_value_problem_easy(self) -> tuple[str, str]:
        percent = self._pick_percent()
        is_increase = random.choice([True, False])

        # Requirements:
        # - starting number is a multiple of 10
        # - starting number <= 1000
        # - (for 3rd grade) keep the result <= 1000 as well
        # - answer must always be positive
        if is_increase:
            max_original = (1000 * 100) // (100 + percent)
            max_original = (max_original // 10) * 10  # round down to nearest 10
            if max_original < 10:
                is_increase = False
                max_original = 1000
            original = random.randrange(10, max_original + 1, 10)
        else:
            # For decrease: ensure answer is positive
            # new_value = original * (100 - percent) / 100 > 0
            # This means percent must be < 100, but we allow up to 200%
            # So we need to ensure: original * (100 - percent) / 100 > 0
            # If percent >= 100, this becomes negative or zero
            # Solution: only allow percent < 100 for decrease problems, OR ensure original is large enough
            if percent >= 100:
                # For percent >= 100, we need to force increase or limit percent
                # Let's limit decrease percent to max 90% to ensure positive results
                is_increase = True
                max_original = (1000 * 100) // (100 + percent)
                max_original = (max_original // 10) * 10
                if max_original < 10:
                    percent = 90  # fallback to 90% decrease
                    is_increase = False
                    max_original = 1000
                else:
                    original = random.randrange(10, max_original + 1, 10)
            else:
                # percent < 100, safe for decrease
                original = random.randrange(10, 1001, 10)
            
            if not is_increase:
                original = random.randrange(10, 1001, 10)
        
        new_value = self._apply_percent(original, percent, is_increase)
        
        # Double-check that answer is positive (shouldn't happen, but safety check)
        if new_value <= 0:
            # Force increase if result would be negative
            is_increase = True
            percent = self._pick_percent()
            max_original = (1000 * 100) // (100 + percent)
            max_original = (max_original // 10) * 10
            if max_original >= 10:
                original = random.randrange(10, max_original + 1, 10)
                new_value = self._apply_percent(original, percent, is_increase)
            else:
                # Fallback to smaller percent
                percent = 50
                original = random.randrange(10, 1001, 10)
                new_value = self._apply_percent(original, percent, is_increase)

        trend = self._trend_word(is_increase)
        problem_text = f"{original} {trend} by {percent}% = "
        answer_text = f"{new_value}"
        return problem_text, answer_text

    def _make_new_value_problem_medium(self) -> tuple[str, str]:
        thing, unit = self._pick_context()
        percent = self._pick_percent()
        is_increase = random.choice([True, False])

        multiple = self._required_multiple_for_new_value(percent, is_increase)
        original = multiple * random.randint(10, 400)  # keeps values reasonable
        new_value = self._apply_percent(original, percent, is_increase)

        trend = self._trend_word(is_increase)
        unit_suffix = f" {unit}" if unit else ""
        problem_text = (
            f"The value of {thing} is {original}{unit_suffix}. "
            f"If it {trend} by {percent}%, what is the new value?"
        )
        answer_text = f"{new_value}{unit_suffix}"
        return problem_text, answer_text

    def _make_old_value_problem_medium(self) -> tuple[str, str]:
        thing, unit = self._pick_context()
        percent = self._pick_percent()
        is_increase = random.choice([True, False])

        multiple = self._required_multiple_for_old_value(percent, is_increase)
        new_value = multiple * random.randint(10, 400)

        mult = 100 + percent if is_increase else 100 - percent
        original = (new_value * 100) // mult

        trend = self._trend_word(is_increase)
        unit_suffix = f" {unit}" if unit else ""
        problem_text = (
            f"The value of {thing} is now {new_value}{unit_suffix} after it {trend} by {percent}%. "
            f"What was the original value?"
        )
        answer_text = f"{original}{unit_suffix}"
        return problem_text, answer_text

    def _make_percent_change_problem_medium(self) -> tuple[str, str]:
        thing, unit = self._pick_context()
        percent = self._pick_percent()
        is_increase = random.choice([True, False])

        multiple = self._required_multiple_for_new_value(percent, is_increase)
        original = multiple * random.randint(10, 400)
        new_value = self._apply_percent(original, percent, is_increase)

        unit_suffix = f" {unit}" if unit else ""
        problem_text = (
            f"The value of {thing} changed from {original}{unit_suffix} to {new_value}{unit_suffix}. "
            f"What was the percent change?"
        )
        sign = "increase" if is_increase else "decrease"
        answer_text = f"{percent}% {sign}"
        return problem_text, answer_text

    def _make_successive_change_problem_medium(self) -> tuple[str, str]:
        thing, unit = self._pick_context()
        p1 = self._pick_percent()
        p2 = self._pick_percent()
        inc1 = random.choice([True, False])
        inc2 = random.choice([True, False])

        m1 = 100 + p1 if inc1 else 100 - p1
        m2 = 100 + p2 if inc2 else 100 - p2
        product = m1 * m2
        base_multiple = 10000 // math.gcd(10000, product)
        original = base_multiple * random.randint(5, 200)

        after_first = (original * m1) // 100
        final_value = (after_first * m2) // 100

        unit_suffix = f" {unit}" if unit else ""
        w1 = self._trend_word(inc1)
        w2 = self._trend_word(inc2)
        problem_text = (
            f"The value of {thing} starts at {original}{unit_suffix}. "
            f"It then {w1} by {p1}%, and then {w2} by {p2}%. "
            f"What is the final value?"
        )
        answer_text = f"{final_value}{unit_suffix}"
        return problem_text, answer_text

    def generate_problem(self) -> tuple[str, str]:
        if self.difficulty == "easy":
            return self._make_new_value_problem_easy()

        # medium: 이전 버전(여러 유형 랜덤)
        problem_generators = [
            self._make_new_value_problem_medium,
            self._make_old_value_problem_medium,
            self._make_percent_change_problem_medium,
            self._make_successive_change_problem_medium,
        ]
        return random.choice(problem_generators)()

    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = self.generate_problem()
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
            label = f"{self.title} ({self.difficulty.title()})"
            pdf.generate_pdf_files(
                f"{label} Problems",
                problem_list,
                num_column=2,
                row_spacing=70,
                output_dir=current_dir,
            )
            pdf.generate_pdf_files(
                f"{label} Answers",
                answer_list,
                num_column=2,
                output_dir=current_dir,
            )
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")


def main():
    # Default: easy
    PercentIncreaseDecrease(difficulty="easy").generate_practice(50)


if __name__ == "__main__":
    main()


