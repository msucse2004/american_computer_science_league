MIN_INT_VAL = 0
MAX_INT_VAL = 500
NEGATIVE = "No"

def infix_to_postfix(infix_expression_string):
    """
    Converts an infix mathematical expression string to a postfix (Reverse Polish Notation) string.

    Args:
        infix_expression_string (str): The infix expression, e.g., "A + B * C - (D / E)" or "A+(B*C)".

    Returns:
        str: The postfix expression, e.g., "A B C * + D E / -".
             Returns an error message string if the expression is invalid.
    """

    # Define operator precedence: higher number means higher precedence
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '÷': 2,
        '/': 2
    }

    output = []  # To store the postfix expression
    operator_stack = []  # To store operators and parentheses

    # Use the new tokenizer function to get tokens
    tokens = tokenize_expression(infix_expression_string)
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

def evaluate_postfix(postfix_expression_string):
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
            elif token == '*':
                result = operand1 * operand2
            # elif token == '/':
            elif token == '÷':
                if operand2 == 0:
                    return "Error: Division by zero."
                result = operand1 / operand2
            else:
                return f"Error: Invalid operator '{token}'."

            # 여기서 float 타입인지 확인하고 에러를 발생시킵니다.
            if isinstance(result, float) and result % 1 != 0:
                return f"Error: The result '{result}' is a float."

            if NEGATIVE == "No" and result < 0:
                return f"Error: The result '{result}' is a negative."
            # 결과가 정수이면 int로 변환하여 스택에 넣습니다.
            if result < MIN_INT_VAL or result > MAX_INT_VAL:
                return f"Error: calculation hit the boundary value : {operand1} {token} {operand2} = {result}"
            operand_stack.append(int(result))

    if len(operand_stack) != 1:
        return "Error: Invalid postfix expression, too many operands."

    # Return the final result
    final_result = operand_stack.pop()
    return final_result

def tokenize_expression(expression_string):
    """
    Splits the infix expression string into a list of individual tokens
    (numbers, single-letter variables, operators, and parentheses),
    handling cases where there are no spaces between them.
    """
    tokens = []
    current_operand = ""
    for char in expression_string:
        if char.isspace():
            if current_operand:
                tokens.append(current_operand)
                current_operand = ""
            continue
        elif char.isdigit() or char.isalpha():  # Handles multi-digit numbers and single/multi-char variables
            current_operand += char
        else:  # Operator or parenthesis
            if current_operand:
                tokens.append(current_operand)
                current_operand = ""
            tokens.append(char)  # Add operator/parenthesis as a separate token
    if current_operand:  # Add any remaining operand at the end of the string
        tokens.append(current_operand)
    return tokens