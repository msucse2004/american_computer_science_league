import re

from utils.unicodes import UNICODE_MULTIPLIER, SUPERSCRIPT_NUMBERS, UNICODE_DIVISION


class Expression:
    def __init__(self):
        #self._title = "Expression"
        self._number_of_nested = 2
        self._difficulty_level = 0.2
        self._frequency_exponential = 0.5
        self._rule_negation = "No"
        self._rule_lower_limit = -1000
        self._rule_upper_limit = 1000



    @property
    def number_of_nested(self):
        return self._number_of_nested

    @number_of_nested.setter
    def number_of_nested(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Number of nested operations must be an integer greater than 0.")
        self._number_of_nested = value

    @property
    def difficulty_level(self):
        return self._difficulty_level

    @difficulty_level.setter
    def difficulty_level(self, value):
        if not isinstance(value, (int, float)) or not (0.0 <= value <= 1.0):
            raise ValueError("Difficulty level must be between 0.0 and 1.0.")
        self._difficulty_level = value

    @property
    def frequency_exponential(self):
        return self._frequency_exponential

    @frequency_exponential.setter
    def frequency_exponential(self, value):
        if not isinstance(value, (int, float)) or not (0.0 <= value <= 1.0):
            raise ValueError("Frequency exponential must be between 0.0 and 1.0.")
        self._frequency_exponential = value

    @property
    def rule_negation(self):
        return self._rule_negation

    @rule_negation.setter
    def rule_negation(self, value):
        if value not in ["Yes", "No"]:
            raise ValueError("Rule negation must be 'Yes' or 'No'.")
        self._rule_negation = value

    @property
    def rule_lower_upper_limit(self):
        return self._rule_lower_limit, self._rule_upper_limit

    @rule_lower_upper_limit.setter
    def rule_lower_upper_limit(self, values: tuple):
        """
        계산 결과의 하한과 상한을 한 번에 설정합니다.

        Args:
            values (tuple): (하한, 상한) 형태의 튜플.
        """
        if not isinstance(values, tuple) or len(values) != 2:
            raise ValueError("Limit values must be provided as a tuple of two integers: (lower, upper).")

        value_low, value_high = values

        # 1. 타입 검사
        if not isinstance(value_low, int) or not isinstance(value_high, int):
            raise ValueError("Both lower and upper limits must be integers.")

        # 2. 값의 유효성 검사: 하한이 상한보다 작아야 합니다.
        if value_low >= value_high:
            raise ValueError("Lower limit must be strictly less than the upper limit.")

        # 3. 값 설정
        self._rule_lower_limit = value_low
        self._rule_upper_limit = value_high

    def tokenize_expression(self, expression_string):
        """
        Splits the infix expression string into a list of individual tokens,
        ensuring operators and operands (including superscripts) are separated.

        FIX: Ensures multi-digit numbers are treated as a single token.
        """
        tokens = []
        current_operand = ""

        # 유니코드 윗첨자 정규식 패턴 (숫자, 알파벳, 유니코드 윗첨자만 허용)
        SUPERSCRIPT_PATTERN = r'[a-zA-Z0-9⁰¹²³⁴⁵⁶⁷⁸⁹]'

        for char in expression_string:
            if char.isspace():
                if current_operand:
                    tokens.append(current_operand)
                    current_operand = ""
                continue

            # 숫자, 알파벳, 유니코드 윗첨자로 구성된 피연산자를 처리
            # char.isalnum()이 '10'과 같은 문자열을 한 번에 캡처할 수 있도록 합니다.
            # char.isalnum()은 숫자(0-9)와 알파벳(a-z, A-Z)을 포함합니다.
            if char.isalnum() or re.fullmatch(SUPERSCRIPT_PATTERN, char):
                current_operand += char

            # 연산자나 괄호를 처리하며 current_operand가 있다면 먼저 토큰으로 추가
            elif char in ('(', ')', '+', '-', '*', '/', '^', UNICODE_MULTIPLIER, UNICODE_DIVISION):
                if current_operand:
                    tokens.append(current_operand)
                    current_operand = ""
                tokens.append(char)
            else:
                # 그 외의 문자 (오류 방지)
                if current_operand:
                    tokens.append(current_operand)
                    current_operand = ""
                tokens.append(char)  # 알 수 없는 문자도 하나의 토큰으로 처리

        if current_operand:
            tokens.append(current_operand)

        return tokens

    def infix_to_postfix(self, infix_expression_string)->str:

        # Define operator precedence: higher number means higher precedence
        precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '÷': 2,
            '/': 2,
            '^': 3,
        }

        output = []  # To store the postfix expression
        operator_stack = []  # To store operators and parentheses

        # Use the new tokenizer function to get tokens
        tokens = self.tokenize_expression(infix_expression_string)
        max_nested_depth = 0
        curr_nested_depth = 0

        for token in tokens:
            # Check if the token is a number (e.g., '11', '123') or an alphanumeric operand (e.g., 'A', 'xyz')
            if token.isalnum():
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
                curr_nested_depth += 1
                if curr_nested_depth > max_nested_depth:
                    max_nested_depth = curr_nested_depth
                # print(f"curr_nexted_depth : {curr_nested_depth}, max: {max_nested_depth}")
            elif token == ')':
                # Pop operators from stack to output until '(' is found
                curr_nested_depth -= 1
                # print(f"curr_nexted_depth decresed by 1: {curr_nested_depth}")
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Pop the '(' from the stack
                else:
                    return "Error: Mismatched parentheses."
            elif token in precedence:  # If it's an operator
                # Pop operators from stack to output if their precedence is
                # greater than or equal to the current token's precedence
                # and it's not a left parenthesis
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], 0) >= precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                return f"Error: Invalid token '{token}' in expression."

        # Pop any remaining operators from the stack to the output
        while operator_stack:
            if operator_stack[-1] == '(':
                return "Error: Mismatched parentheses."  # Unmatched left parenthesis
            output.append(operator_stack.pop())

        return " ".join(output)
    def evaluate_postfix(self, postfix_expression_string):
        """
        Evaluates a postfix expression string and returns the result.

        Args:
            postfix_expression_string (str): A space-separated postfix expression string.

        Returns:
            int: The result of the evaluation.
            str: An error message if the expression is invalid or if the result is a float.
        """
        operand_stack = []
        tokens = postfix_expression_string.split()

        for token in tokens:
            try:
                # If the token is a number, push it to the stack
                operand_stack.append(float(token))
            except ValueError:
                # If the token is an operator, pop two operands, perform the operation, and push the result
                if len(operand_stack) < 2:
                    return "Error: Invalid postfix expression, not enough operands."

                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()

                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == UNICODE_MULTIPLIER or token == '*':
                    result = operand1 * operand2
                elif token == '/' or token == '÷':
                    if operand2 == 0:
                        return "Error: Division by zero."
                    result = operand1 / operand2
                elif token == '^':
                    if operand2 > 5:
                        return f"Error: Exponent value is too large. {operand2} > 5."
                    result = operand1 ** operand2
                else:
                    return f"Error: Invalid operator '{token}'."

                # 여기서 float 타입인지 확인하고 에러를 발생시킵니다.
                if isinstance(result, float) and result % 1 != 0:
                    return f"Error: The result '{result}' is a float."

                if self.rule_negation == "No" and result < 0:
                    return f"Error: The result '{result}' is a negative."
                # 결과가 정수이면 int로 변환하여 스택에 넣습니다.
                if result < self._rule_lower_limit or result > self._rule_upper_limit:
                    return f"Error: calculation hit the boundary value : {operand1} {token} {operand2} = {result}"
                operand_stack.append(int(result))

        if len(operand_stack) != 1:
            return "Error: Invalid postfix expression, too many operands."

        # Return the final result
        final_result = operand_stack.pop()
        return final_result

    def _format_expression_unicode(self, expression: str) -> str:
        """
        주어진 infix expression 문자열을 후위 표기법(Postfix)을 사용하여
        사람이 읽기 좋은 수학적 표기(유니코드 연산자, 윗첨자)로 변환합니다.

        Args:
            expression (str): Infix 표현식 문자열.

        Returns:
            str: 유니코드로 포맷된 Infix 표현식 문자열.
        """
        # 1. 인픽스 표현식을 포스트픽스로 변환합니다.
        postfix_expression = self.infix_to_postfix(expression)

        if "Error:" in postfix_expression:
            return postfix_expression  # 오류 메시지를 그대로 반환

        tokens = postfix_expression.split()

        # 결과를 저장할 스택 (여기에 문자열 형태의 부분 표현식이 쌓입니다)
        # 스택의 각 요소는 부분적으로 포맷된 수식 문자열입니다.
        formatting_stack = []

        # 연산자 정의
        BINARY_OPERATORS = ['+', '-', '*', '/', '^', UNICODE_MULTIPLIER, UNICODE_DIVISION]

        for token in tokens:
            if token not in BINARY_OPERATORS:
                # 피연산자는 그대로 스택에 넣습니다.
                formatting_stack.append(token)

            # 2. 연산자 처리
            elif token in BINARY_OPERATORS:
                if len(formatting_stack) < 2:
                    return f"Error: Invalid postfix expression structure near operator '{token}'."

                # 후위 표기법: operand2가 우측 항, operand1이 좌측 항
                operand2 = formatting_stack.pop()
                operand1 = formatting_stack.pop()

                new_expr = ""

                # 2.1. 지수 연산자 처리 ('^')
                if token == '^':
                    # 지수(operand2)를 유니코드 윗첨자로 변환
                    superscript = "".join(SUPERSCRIPT_NUMBERS.get(ch, ch) for ch in operand2)

                    # 밑(operand1)에 괄호 추가 여부 결정: 복잡한 항(공백/연산자 포함)이거나 괄호가 없으면 추가
                    # 이전에 `( )²`와 같은 오류가 발생하지 않도록 괄호 처리 로직을 신중하게 적용합니다.

                    # 지수 연산자의 밑이 복합적인 연산(공백 포함)이지만,
                    # 아직 괄호로 감싸져 있지 않은 경우에만 괄호를 추가
                    is_complex_base = any(
                        op in operand1 for op in [' ', '+', '-', '*', UNICODE_MULTIPLIER, '/', UNICODE_DIVISION]
                        ) or re.search(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]', operand1)

                    if is_complex_base and not (operand1.startswith('(') and operand1.endswith(')')):
                        base = f"({operand1})"
                    else:
                        base = operand1

                    new_expr = f"{base}{superscript}"

                # 2.2. 곱셈/나눗셈 연산자 처리
                elif token in ('*', UNICODE_MULTIPLIER, '/', UNICODE_DIVISION):
                    new_op = UNICODE_MULTIPLIER if token in ('*', UNICODE_MULTIPLIER) else UNICODE_DIVISION

                    # 괄호 추가 규칙:
                    # 곱셈/나눗셈의 피연산자가 덧셈/뺄셈을 포함하는 복잡한 식인 경우 괄호로 감싸야 합니다.
                    # 이는 피연산자에 '+' 또는 '-'가 포함되거나 공백이 포함되어 복잡한 연산임을 나타낼 때 해당됩니다.

                    def add_parentheses(operand, op_token):
                        # 덧셈/뺄셈은 상위 연산자가 곱셈/나눗셈일 때 괄호 필요
                        if op_token in ('*', UNICODE_MULTIPLIER, '/', UNICODE_DIVISION):
                            # 항이 복잡하고(공백 포함) 이미 괄호로 감싸져 있지 않다면 괄호 추가
                            if ('+' in operand or '-' in operand or ' ' in operand) and \
                                    not (operand.startswith('(') and operand.endswith(')')):
                                return f"({operand})"
                        return operand

                    op1_formatted = add_parentheses(operand1, token)
                    op2_formatted = add_parentheses(operand2, token)

                    new_expr = f"{op1_formatted} {new_op} {op2_formatted}"

                # 2.3. 덧셈/뺄셈 연산자 처리
                elif token in ('+', '-'):
                    # 덧셈/뺄셈은 일반적으로 괄호가 필요 없지만, 스택의 내용을 연결하고 공백을 추가합니다.
                    new_expr = f"{operand1} {token} {operand2}"

                # 2.4. 결과 스택에 추가
                formatting_stack.append(new_expr)

            else:
                return f"Error: Invalid token '{token}' during formatting."

        # 3. 최종 결과 반환
        if len(formatting_stack) == 1:
            final_result = formatting_stack[0]

            return final_result

        else:
            return "Error: Postfix formatting failed, too many operands remaining."

