import itertools
import re

import pandas as pd

from elementary_division.boolean_algebra.evaluate_algebra.evaluate_algebra import EvaluateAlgebra
from utils.unicodes import UNICODE_BITWISE_XOR, UNICODE_BITWISE_NOT, UNICODE_BITWISE_AND, UNICODE_BITWISE_OR


class TruthTable:
    VARIABLES = ['A', 'B']
    def __init__(self, expression=None):
        self._title = "Truth Table"
        self._expression = expression
        self._python_expression = None
        self._truth_table_df = None
        self._initialize_internal_variables()

    def _initialize_internal_variables(self, expression=None):
        if expression is None:
            return
        self._expression = expression
        self._python_expression = self._translate_expression(expression)
        self.generate_truth_table()

    def _translate_expression(self, expression: str) -> str:
        if not expression:
            return ""

        modified_expression = "".join(expression.split())

        modified_expression = modified_expression.replace('XOR', ' ^ ')  # 키워드
        modified_expression = modified_expression.replace('NOT', 'not ')
        modified_expression = modified_expression.replace('AND', ' and ')
        modified_expression = modified_expression.replace('OR', ' or ')

        # 비트연산 기호 → 논리 연산자
        modified_expression = modified_expression.replace('^', ' ^ ')  # 심볼
        modified_expression = modified_expression.replace('~', 'not ')
        modified_expression = modified_expression.replace('*', ' and ')
        modified_expression = modified_expression.replace('+', ' or ')

        # 공백 정리
        while '  ' in modified_expression:
            modified_expression = modified_expression.replace('  ', ' ')

        return modified_expression.strip()

    def _create_converted_expression(self, expression: str, style='keyword') -> str:
        """
        주어진 논리식을 지정된 스타일(keyword, arithmetic, symbol)로 변환하는 헬퍼 함수.
        """
        if not expression:
            return ""

        # 1. 모든 공백 제거
        modified_expression = self._translate_expression(expression)

        # 2. 치환 맵 정의
        # 맵은 치환 순서를 보장하지 않으므로, 아래에서 직접 치환 순서를 제어합니다.
        if style == 'keyword':
            replace_xor = ' XOR '
            replace_not = ' NOT '
            replace_and = ' AND '
            replace_or = ' OR '
            replace_unary_not = 'NOT '  # 단항 연산자는 뒤에만 공백
        elif style == 'arithmetic':
            replace_xor = f' {UNICODE_BITWISE_XOR} '
            replace_not = f' {UNICODE_BITWISE_NOT} '
            replace_and = f' {UNICODE_BITWISE_AND} '
            replace_or = f' {UNICODE_BITWISE_OR} '
            replace_unary_not = '~'
        else:  # symbol style
            replace_xor = ' ^ '
            replace_not = '~ '
            replace_and = ' & '
            replace_or = ' | '
            replace_unary_not = 'not '


        modified_expression = modified_expression.replace('not', replace_not)
        modified_expression = modified_expression.replace('^', replace_xor)
        modified_expression = modified_expression.replace('and', replace_and)
        modified_expression = modified_expression.replace('or', replace_or)


        # 3. 공백 및 괄호 주변 정리 ( eval() 안전성 확보 )
        modified_expression = modified_expression.replace('( ', '(').replace(' )', ')')

        # 단항 연산자 뒤에 괄호 분리 (필요한 경우)
        if 'not ' in replace_unary_not:
            modified_expression = modified_expression.replace('not(', 'not (')
        if 'NOT ' in replace_unary_not:
            modified_expression = modified_expression.replace('NOT(', 'NOT (')
        if '~' in replace_unary_not:
            modified_expression = modified_expression.replace('~(', '~ (')

        # 4. 연속된 공백을 단일 공백으로 정규화
        while '  ' in modified_expression:
            modified_expression = modified_expression.replace('  ', ' ')

        return modified_expression.strip()


    def get_bitwise_keyword_expression(self,  expression: str) -> str:
        return self._create_converted_expression(expression, style='keyword')

    def get_bitwise_arithmetic_expression(self, expression: str) -> str:
        return self._create_converted_expression(expression, style='arithmetic')

    def get_bitwise_symbol_expression(self, expression: str) -> str:
        return self._create_converted_expression(expression, style='symbol')

    def _validate_expression(self):
        """Checks for common non-Python boolean syntax and variable presence."""
        if 'AND' in self._expression or 'OR' in self._expression or 'NOT' in self._expression:
            raise ValueError(
                "Expression must use Python's boolean operators: '&' for AND, "
                "'|' for OR, and '~' or 'not ' for NOT. "
                "Example: (A & B) | (~A)"
            )
        # Simple check for required variables
        for var in self.VARIABLES:
            if var not in self._expression:
                print(f"Warning: Variable '{var}' is not used in the expression.")

    def evaluate_expression(self, A: bool, B: bool) -> bool:
        if not self._python_expression:
            return False

        # Create a dictionary to map variable names in the string to their values
        context = {'A': A, 'B': B}

        # Use eval() to calculate the result of the expression string
        return eval(self._python_expression, context)

    def generate_truth_table(self) -> pd.DataFrame:
        """
        Generates the full truth table.

        Returns:
            A pandas DataFrame representing the truth table.
        """
        table_data = []

        # itertools.product generates all combinations of (True, False) for 2 variables
        # i.e., (F, F), (F, T), (T, F), (T, T)
        for A, B in itertools.product([False, True], repeat=len(self.VARIABLES)):
            # Evaluate the expression for the current combination
            result = self.evaluate_expression(A, B)

            # Add the row data: [A, B, Result]
            # Convert bools to 1/0 for cleaner table presentation if desired
            table_data.append([A, B, result])

        # Define column names for the DataFrame
        columns = self.VARIABLES + [self._expression]

        # Create the DataFrame
        df = pd.DataFrame(table_data, columns=columns)
        self._truth_table_df = df
        return df

    def _get_table(self):
        if self._truth_table_df is None:
            return self.generate_truth_table()
        return self._truth_table_df

    def count_true_results(self) -> int:
        """결과가 True인 행의 개수를 반환합니다."""
        df = self._get_table()
        result_column = self._expression
        return df[result_column].sum()  # True는 1로 계산되므로 sum()을 사용합니다.

    def count_false_results(self) -> int:
        """결과가 False인 행의 개수를 반환합니다."""
        df = self._get_table()
        result_column = self._expression
        # False는 0으로 계산되므로, Not(True)의 합계를 구하거나 전체 개수에서 True 개수를 뺍니다.
        return len(df) - df[result_column].sum()

    def get_true_variable_combinations(self) -> list[tuple[bool, bool]]:
        """결과가 True일 때의 (A, B) 값 튜플 리스트를 반환합니다."""
        df = self._get_table()
        result_column = self._expression

        # 결과 컬럼이 True인 행만 필터링합니다.
        true_rows = df[df[result_column] == True]

        true_rows_int = true_rows[['A', 'B']].astype(int)

        # A, B 컬럼만 선택하여 튜플 리스트로 변환합니다.
        return list(true_rows_int[['A', 'B']].itertuples(index=False, name=None))

    def get_false_variable_combinations(self) -> list[tuple[bool, bool]]:
        """결과가 False일 때의 (A, B) 값 튜플 리스트를 반환합니다."""
        df = self._get_table()
        result_column = self._expression

        # 결과 컬럼이 False인 행만 필터링합니다.
        false_rows = df[df[result_column] == False]

        false_rows_int = false_rows[['A', 'B']].astype(int)

        # A, B 컬럼만 선택하여 튜플 리스트로 변환합니다.
        return list(false_rows_int[['A', 'B']].itertuples(index=False, name=None))

def main():
    #expression = "~A * ~B + A * B"
    expression = "(NOT B AND (A AND B)) OR ((A OR B) XOR (NOT A))"

    print(f"--- Truth Table Analysis for: {expression} ---")
    ttg = TruthTable(expression)
    ttg._initialize_internal_variables(expression)

    print(f"Keyword Style: {ttg.get_bitwise_keyword_expression(expression)}")
    print(f"Arithmetic Style:  {ttg.get_bitwise_arithmetic_expression(expression)}")
    print(f"Symbol Style:  {ttg.get_bitwise_symbol_expression(expression)}")

    # 1. 진리표 생성 및 출력
    table = ttg.generate_truth_table()

    print("\n[1] Truth Table")
    print(table)

    # 2. 분석 함수 호출
    print("\n[2] 분석 결과")
    print(f"True 결과 개수: {ttg.count_true_results()}")
    print(f"False 결과 개수: {ttg.count_false_results()}")
    print(f"True일 때의 (A, B) 조합: {ttg.get_true_variable_combinations()}")
    print(f"False일 때의 (A, B) 조합: {ttg.get_false_variable_combinations()}")

    print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()


