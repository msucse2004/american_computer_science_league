import os
import random
import sys
from fractions import Fraction

from elementary_division.expressions.order_of_operations.order_of_operations import OrderOfOperations
from utils import pdf
from utils.expression import Expression


class MathmaticalExpressionToInfixNotation(Expression):
    def __init__(self):
        super().__init__()
        self._title = 'MathmaticalExpressionToInfixNotation'
        self._operation_instance = OrderOfOperations()
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

    def evaluate_infix_as_fraction(self, infix_expression: str) -> str:
        """infix 표현식을 분수로 계산하여 분수 형태 문자열로 반환"""
        try:
            # infix를 postfix로 변환
            postfix = self._operation_instance.infix_to_postfix(infix_expression)
            if isinstance(postfix, str) and postfix.startswith("Error"):
                return None
            
            # postfix를 분수로 계산
            stack = []
            tokens = postfix.split()
            
            for token in tokens:
                try:
                    # 숫자는 Fraction으로 변환
                    stack.append(Fraction(int(token), 1))
                except ValueError:
                    # 연산자 처리
                    if len(stack) < 2:
                        return None
                    
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    
                    if token == '+':
                        result = operand1 + operand2
                    elif token == '-':
                        result = operand1 - operand2
                    elif token == '*' or token == '×':
                        result = operand1 * operand2
                    elif token == '/' or token == '÷':
                        if operand2 == 0:
                            return None
                        result = operand1 / operand2
                    elif token == '^':
                        # 지수는 정수만 허용
                        if operand2.denominator != 1 or operand2.numerator > 5:
                            return None
                        exp = operand2.numerator
                        if operand1.denominator == 1:
                            result = Fraction(operand1.numerator ** exp, 1)
                        else:
                            # 분수의 거듭제곱
                            result = Fraction(operand1.numerator ** exp, operand1.denominator ** exp)
                    else:
                        return None
                    
                    stack.append(result)
            
            if len(stack) != 1:
                return None
            
            fraction_result = stack[0]
            
            # 결과가 -1000과 1000 사이에 있는지 확인
            result_value = float(fraction_result)
            if result_value < -1000 or result_value > 1000:
                return None
            
            # 분자와 분모가 각각 1000을 넘지 않는지 확인
            if abs(fraction_result.numerator) > 1000 or fraction_result.denominator > 1000:
                return None
            
            # 분수를 문자열로 변환 (기약분수 형태)
            if fraction_result.denominator == 1:
                return str(fraction_result.numerator)
            else:
                return f"{fraction_result.numerator}/{fraction_result.denominator}"
                
        except Exception:
            return None

    def generate_problem(self) -> tuple[str, str]:
        problem_text, answer_text = None, None

        self._operation_instance.number_of_nested = 2
        self._operation_instance.difficulty_level = 0.2
        self._operation_instance.frequency_exponential = 0.3

        # rule_negation, allowed_operators는 setter를 통해 문자열로 설정 가능
        self._operation_instance.rule_negation = "Yes"
        self._operation_instance.allowed_operators = '+-*/^'

        # rule_lower_upper_limit는 setter가 튜플을 받도록 정의되어 있으므로 튜플로 할당
        self._operation_instance.rule_lower_upper_limit = (-1000, 1000)

        problem_choice = random.choice(["infix", "mathmetics"])
        
        # 결과가 -1000과 1000 사이에 나올 때까지 반복
        max_attempts = 200
        attempt = 0
        infix_notation = None
        calculation_result = None
        
        while attempt < max_attempts:
            infix_notation = self._operation_instance.generate_random_expression()
            calculation_result = self.evaluate_infix_as_fraction(infix_notation)
            
            if calculation_result is not None:
                # 결과가 범위 내에 있는지 확인
                try:
                    if '/' in calculation_result:
                        num, den = map(int, calculation_result.split('/'))
                        if den == 0:
                            attempt += 1
                            continue
                        result_value = num / den
                        # 분자와 분모가 각각 1000을 넘지 않는지 확인
                        if abs(num) > 1000 or den > 1000:
                            calculation_result = None
                            attempt += 1
                            continue
                    else:
                        result_value = int(calculation_result)
                    
                    # 범위 체크: -1000 <= result <= 1000
                    if -1000 <= result_value <= 1000:
                        break
                    else:
                        # 범위를 벗어나면 None으로 설정하여 다시 시도
                        calculation_result = None
                except (ValueError, ZeroDivisionError):
                    calculation_result = None
            
            attempt += 1
        
        if problem_choice == "infix":
            problem_text = f"Convert to Mathematiccal Expression and calculate. {infix_notation} ="
            unicode_format = self._operation_instance._infix_to_unicode_format(infix_notation)
            if calculation_result is not None:
                answer_text = f"{unicode_format} = {calculation_result}"
            else:
                answer_text = unicode_format
        else:
            problem_text = f"Conver to Infix notation and calculate. {self._operation_instance._infix_to_unicode_format(infix_notation)} ="
            if calculation_result is not None:
                answer_text = f"{infix_notation} = {calculation_result}"
            else:
                answer_text = infix_notation
        return problem_text, answer_text

    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = None, None
        problem_text, answer_text = self.generate_problem()
        print(f"{problem_text} = {answer_text}")

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
            pdf.generate_pdf_files(f"{self._title} Problems", problem_list, num_column=1, row_spacing=60, output_dir=current_dir)
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=2, output_dir=current_dir)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

def main():
    infix_notation = "(9 - 5 + 5) + (5 ^ 3 + 4 + 7) / (4 ^ 2 ^ 2)"
    #infix_notation = "(4 ^ 2 ^ 2)"
    #infix_notation = "(9 - 5 + 5)"
    topic_instance = MathmaticalExpressionToInfixNotation()
    print(topic_instance._infix_to_unicode_format(infix_notation))
    topic_instance.generate_practice(58)


if __name__ == "__main__":
    main()