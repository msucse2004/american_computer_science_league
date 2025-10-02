import re

from utils.unicodes import UNICODE_MULTIPLIER, SUPERSCRIPT_NUMBERS, UNICODE_DIVISION, UNICODE_PRODUCT, \
    identify_token_type


class Expression:
    # Define operator precedence: higher number means higher precedence
    _PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '÷': 2,
        '/': 2,
        '^': 3,
    }

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

        output = []  # To store the postfix expression
        operator_stack = []  # To store operators and parentheses

        # Use the new tokenizer function to get tokens
        tokens = self.tokenize_expression(infix_expression_string)
        max_nested_depth = 0
        curr_nested_depth = 0

        for token in tokens:
            # Check if the token is a number (e.g., '11', '123') or an alphanumeric operand (e.g., 'A', 'xyz')
            if token.isalnum() or all(re.fullmatch(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]', char) for char in token):
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
            elif token in self._PRECEDENCE:  # If it's an operator
                # Pop operators from stack to output if their precedence is
                # greater than or equal to the current token's precedence
                # and it's not a left parenthesis
                while (operator_stack and operator_stack[-1] != '(' and
                       ((self._PRECEDENCE[operator_stack[-1]] > self._PRECEDENCE[token]) or
                        (self._PRECEDENCE[operator_stack[-1]] == self._PRECEDENCE[token] and token != '^'))):
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

    def infix_to_prefix(self, infix_expression_string) -> str:

        # 1. 토큰화 및 문자열 반전
        tokens = self.tokenize_expression(infix_expression_string)

        # 괄호를 반전시키고 토큰 리스트를 반전시킵니다.
        reversed_tokens = []
        for token in reversed(tokens):
            if token == '(':
                reversed_tokens.append(')')
            elif token == ')':
                reversed_tokens.append('(')
            else:
                reversed_tokens.append(token)

        output = []  # Prefix 표현식의 반전 결과를 저장
        operator_stack = []

        # **3. Infix to Postfix와 유사한 처리 (단, 반전된 식에 대해)**
        for token in reversed_tokens:
            if token.isalnum() or all(re.fullmatch(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]', char) for char in token):  # 피연산자
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # '(' 제거
                else:
                    return "Error: Mismatched parentheses in prefix conversion."
            elif token in self._PRECEDENCE:  # 연산자
                # Infix to Postfix에서 사용하는 precedence >= 조건을 그대로 사용
                while (operator_stack and operator_stack[-1] != '(' and
                       ((self._PRECEDENCE[operator_stack[-1]] > self._PRECEDENCE[token]) or
                        (self._PRECEDENCE[operator_stack[-1]] == self._PRECEDENCE[token] and token == '^'))):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                return f"Error: Invalid token '{token}' in prefix conversion."

        # 스택에 남은 연산자 처리
        while operator_stack:
            if operator_stack[-1] == '(':
                return "Error: Mismatched parentheses in prefix conversion."
            output.append(operator_stack.pop())

        # 4. 최종 결과 반전 및 반환
        return " ".join(reversed(output))

    def prefix_to_infix(self, prefix_expression_string) -> str:

        tokens = prefix_expression_string.split()
        stack = []  # Infix 부분식을 저장할 스택

        # Prefix는 오른쪽에서 왼쪽으로 읽어들입니다.
        for token in reversed(tokens):
            if token.isalnum() or all(re.fullmatch(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]', char) for char in token):
                # 피연산자는 그대로 스택에 푸시합니다.
                stack.append(token)
            elif token in self._PRECEDENCE:
                if len(stack) < 2:
                    return "Error: Invalid prefix expression, not enough operands."

                left = stack.pop()  # 우측 피연산자 (Op2)
                right = stack.pop()  # 좌측 피연산자 (Op1)

                # new_infix = f"({operand2} {token} {operand1})" # 원래의 올바른 순서
                new_infix = f"({left} {token} {right})"  # Prefix는 연산자-Operand1-Operand2 순서 (읽는 순서 기준)

                stack.append(new_infix)
            else:
                return f"Error: Invalid token '{token}' in prefix expression."

        if len(stack) != 1:
            return "Error: Invalid prefix expression, too many operands remaining."

        # 최외곽 괄호를 제거하고 반환합니다.
        result = stack.pop()
        # if result.startswith('(') and result.endswith(')'):
        #     return result[1:-1]
        return result

    def postfix_to_infix(self, postfix_expression_string) -> str:
        """
        Postfix 표현식 문자열을 Infix 표현식 문자열로 변환합니다.
        (최소한의 괄호 포함)

        Args:
            postfix_expression_string (str): Space-separated Postfix 표현식 문자열.

        Returns:
            str: Infix 표현식 문자열 (적절한 괄호로 묶인 형태).
        """
        tokens = postfix_expression_string.split()
        stack = []  # (Infix 부분식, 해당 식의 외부 연산자 우선순위)를 저장할 스택

        for token in tokens:
            if token.isalnum() or all(re.fullmatch(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]', char) for char in token):
                # 피연산자는 우선순위 4 (가장 높음, 임의 지정)로 스택에 푸시
                stack.append((token, 4))
            elif token in self._PRECEDENCE:
                if len(stack) < 2:
                    return "Error: Invalid postfix expression, not enough operands."

                # Postfix: Operand1 Operand2 Operator
                operand2_expr, operand2_prec = stack.pop()
                operand1_expr, operand1_prec = stack.pop()

                current_prec = self._PRECEDENCE[token]

                # 괄호 추가 로직:
                # 1. 현재 연산자보다 피연산자의 외부 연산자 우선순위가 더 낮으면 괄호 추가 (ex: 1 + (2*3))
                # 2. 현재 연산자와 피연산자의 외부 연산자 우선순위가 같고, 현재 연산자가
                #    좌측 결합(+, *, /)인데 Op2이거나, 우측 결합(^)인데 Op1이면 괄호 추가

                # Op1 (좌측 항) 괄호 처리
                if operand1_prec < current_prec or \
                        (operand1_prec == current_prec and token == '^'):  # 우측 결합 연산자(^): Op1이 같은 우선순위면 괄호 추가
                    op1_formatted = f"({operand1_expr})"
                else:
                    op1_formatted = operand1_expr

                # Op2 (우측 항) 괄호 처리
                # 좌측 결합 연산자(+, -, *, /, ÷)는 Op2가 같은 우선순위면 괄호 추가
                if operand2_prec < current_prec or \
                        (operand2_prec == current_prec and token != '^'):
                    op2_formatted = f"({operand2_expr})"
                else:
                    op2_formatted = operand2_expr

                new_infix = f"{op1_formatted} {token} {op2_formatted}"
                stack.append((new_infix, current_prec))

            else:
                return f"Error: Invalid token '{token}' in postfix expression."

        if len(stack) != 1:
            return "Error: Invalid postfix expression, too many operands remaining."

        # 최종 결과의 인픽스 식만 반환합니다.
        return stack[0][0]

    def evaluate_infix(self, infix):
        postfix = self.infix_to_postfix(infix)
        return self.evaluate_postfix(postfix)

    def evaluate_prefix(self, prefix):
        infix = self.prefix_to_infix(prefix)
        return self.evaluate_infix(infix)

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

    def _infix_to_unicode_format(self, expression: str) -> str:

        infix_notation = expression
        prefix_expression = self.infix_to_prefix(expression)
        postfix_expression = self.infix_to_postfix(expression)
        if "Error:" in prefix_expression:
            return prefix_expression  # 오류 메시지를 그대로 반환

        tokens = prefix_expression.split()

        current_index = 0
        while len(tokens) > 1:
            if current_index + 2 >= len(tokens):
                current_index = 0
                if len(tokens) > 1 and current_index + 2 < len(tokens):
                    continue
                else:
                    break
            token1 = tokens[current_index]
            token2 = tokens[current_index + 1]
            token3 = tokens[current_index + 2]
            # find pattern
            if identify_token_type(token1) == "Operator" and identify_token_type(token2) != "Operator" and identify_token_type(token3) != "Operator":
                operator = token1
                left_term = token2
                right_term = token3
                if operator == "^":
                    print(f"infix: {expression}, prefix: {prefix_expression}, l: {left_term}, r: {right_term}")
                    if identify_token_type(left_term) == "Unknown":
                        new_term = f"({left_term}){SUPERSCRIPT_NUMBERS[right_term]}"
                    else:
                        if identify_token_type(right_term) == "Number" and any(c in SUPERSCRIPT_NUMBERS.values() for c in right_term):
                            new_term = f"({left_term}{SUPERSCRIPT_NUMBERS[right_term[0]]}){right_term[1:]}"
                        else:
                            new_term = f"{left_term}{SUPERSCRIPT_NUMBERS[right_term]}"
                elif operator == "*":
                    new_term = f"({left_term} {UNICODE_MULTIPLIER} {right_term})"
                elif operator == "/":
                    new_term = f"({left_term} {UNICODE_DIVISION} {right_term})"
                else:
                    new_term = f"({left_term} {operator} {right_term})"

                tokens[current_index] = new_term
                del tokens[current_index + 2]
                del tokens[current_index + 1]
                current_index = 0
            else:
                current_index = current_index + 1
        if not tokens:
            return "Error: no expression found."

        final_result = tokens[0]

        if final_result.startswith('(') and final_result.endswith(')'):
            return final_result[1:-1]

        return final_result
