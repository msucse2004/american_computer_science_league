"""
Computer Number System 문제 풀이 생성 스크립트
RGB_Coding_Solution_2_5.html과 동일한 형식으로 풀이를 생성합니다.
"""
import os
import sys
import re
import math

# Allow running this file directly
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils.number_bases import convert_to_base, NAME_OF_NUMBER_BASES
from utils.unicodes import SUBSCRIPT_NUMBERS, SUPERSCRIPT_NUMBERS, UNICODE_MULTIPLIER
from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem


def html_escape(text):
    """HTML 특수 문자 이스케이프"""
    return (text.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def format_subscript(text):
    """Unicode subscript를 HTML <sub> 태그로 변환"""
    result = text
    for num, sub in SUBSCRIPT_NUMBERS.items():
        result = result.replace(sub, f'<sub>{num}</sub>')
    return result


def format_superscript(text):
    """Unicode superscript를 HTML <sup> 태그로 변환"""
    result = text
    for num, sup in SUPERSCRIPT_NUMBERS.items():
        result = result.replace(sup, f'<sup>{num}</sup>')
    return result


def parse_base_number(text):
    """진수 표기에서 숫자와 진수 추출 (예: "28₁₃" -> (28, 13))"""
    # Unicode subscript를 일반 숫자로 변환
    # 큰 숫자부터 변환해야 함 (예: ₁₆을 _16으로 변환, _1_6이 아닌)
    # 키를 숫자로 변환해서 정렬
    def get_numeric_key(item):
        key = item[0]
        try:
            return int(key)
        except ValueError:
            return 0
    
    sorted_subs = sorted(SUBSCRIPT_NUMBERS.items(), key=get_numeric_key, reverse=True)
    for num, sub in sorted_subs:
        text = text.replace(sub, f'_{num}')
    
    # 패턴: 숫자_진수
    match = re.match(r'([0-9A-Fa-f]+)_(\d+)', text)
    if match:
        number_str = match.group(1)
        base = int(match.group(2))
        return number_str, base
    
    # 패턴: 숫자 (진수) 또는 숫자 converts to base X
    match = re.search(r'(\d+)\s*\((\d+)\)', text)
    if match:
        number_str = match.group(1)
        base = int(match.group(2))
        return number_str, base
    
    return None, None


def solve_addition_subtraction(problem_text, answer_text):
    """진수 덧셈/뺄셈 문제 풀이 생성"""
    steps = []
    
    # 문제에서 두 숫자와 진수 추출
    # 예: "28₁₃ + 25₁₃ ="
    parts = problem_text.split('=')
    if len(parts) < 1:
        return steps
    
    expression = parts[0].strip()
    
    # 연산자 찾기
    if '+' in expression:
        operator = '+'
        op_parts = expression.split('+')
    elif '-' in expression:
        operator = '-'
        op_parts = expression.split('-')
    else:
        return steps
    
    if len(op_parts) != 2:
        return steps
    
    num1_text = op_parts[0].strip()
    num2_text = op_parts[1].strip()
    
    num1_str, base1 = parse_base_number(num1_text)
    num2_str, base2 = parse_base_number(num2_text)
    
    if not num1_str or not num2_str or base1 != base2:
        return steps
    
    base = base1
    
    # base가 11 이상일 때는 직접 해당 진수로 덧셈/뺄셈 수행
    if base >= 11 and operator == '+':
        # 16진수 직접 덧셈
        # 숫자를 오른쪽 정렬
        max_len = max(len(num1_str), len(num2_str))
        num1_padded = num1_str.upper().rjust(max_len, '0')
        num2_padded = num2_str.upper().rjust(max_len, '0')
        
        result_digits = []
        carry = 0
        addition_steps = []
        
        # 오른쪽부터 왼쪽으로 덧셈
        for i in range(max_len - 1, -1, -1):
            d1 = num1_padded[i]
            d2 = num2_padded[i]
            
            # 자릿수를 10진수로 변환
            if '0' <= d1 <= '9':
                val1 = int(d1)
            else:
                val1 = ord(d1) - ord('A') + 10
            
            if '0' <= d2 <= '9':
                val2 = int(d2)
            else:
                val2 = ord(d2) - ord('A') + 10
            
            # 덧셈
            total = val1 + val2 + carry
            new_carry = total // base
            remainder = total % base
            
            # 결과 자릿수
            if remainder >= 10:
                result_digit = chr(ord('A') + remainder - 10)
            else:
                result_digit = str(remainder)
            
            result_digits.insert(0, result_digit)
            
            # 설명 생성 (세로 계산 형식)
            # 16진수 자릿수를 10진수로 변환하는 설명 추가
            d1_desc = ''
            d2_desc = ''
            
            if d1 >= 'A':
                d1_desc = f'{d1}는 {base}진수이고, 이를 10진수로 변환하면 {val1}'
            else:
                d1_desc = f'{d1}는 10진수 {val1}'
            
            if d2 >= 'A':
                d2_desc = f'{d2}는 {base}진수이고, 이를 10진수로 변환하면 {val2}'
            else:
                d2_desc = f'{d2}는 10진수 {val2}'
            
            # 결과를 16진수로 변환하는 설명
            result_desc = ''
            if remainder >= 10:
                result_desc = f'{total}는 10진수이고, 이를 다시 {base}진수로 변환하면 {result_digit}'
            else:
                result_desc = f'{total}는 10진수'
            
            if carry > 0:
                step_desc = f'{d1} + {d2} + {carry}(올림): {d1_desc}. {d2_desc}. {val1} + {val2} + {carry} = {total} ({result_desc}). {total} = {new_carry}×{base} + {remainder} → 올림 {new_carry}, 현재 자리 {result_digit}'
            else:
                step_desc = f'{d1} + {d2}: {d1_desc}. {d2_desc}. {val1} + {val2} = {total} ({result_desc}). {total} = {new_carry}×{base} + {remainder} → 올림 {new_carry}, 현재 자리 {result_digit}'
            
            addition_steps.append(step_desc)
            carry = new_carry
        
        # 마지막 올림이 있으면 추가
        if carry > 0:
            result_digits.insert(0, str(carry) if carry < 10 else chr(ord('A') + carry - 10))
            addition_steps.append(f'마지막 올림: {carry}')
        
        result_base = ''.join(result_digits)
        
        # 세로 계산 형식 생성
        base_name = NAME_OF_NUMBER_BASES.get(base, f'base {base}')
        vertical_calc = f'''
            <div style="font-family: 'Courier New', monospace; text-align: right; margin: 20px 0;">
                <div style="margin-bottom: 5px;">&nbsp;&nbsp;{num1_str.upper()}<sub>{base}</sub></div>
                <div style="margin-bottom: 5px;">+&nbsp;{num2_str.upper()}<sub>{base}</sub></div>
                <div style="border-top: 2px solid #333; padding-top: 5px; margin-top: 5px;">&nbsp;&nbsp;{result_base}<sub>{base}</sub></div>
            </div>
        '''
        
        steps.append({
            'title': f'1단계: {base}진수({base_name})로 직접 덧셈하기',
            'content': f'''
                <p>오른쪽부터 왼쪽으로 각 자릿수를 더합니다 (1의 자리, 10의 자리 순서):</p>
                {vertical_calc}
                <div class="formula">
                    <strong>계산 과정:</strong><br>
                    {'<br>'.join(addition_steps)}
                </div>
                <p>결과: <span class="highlight">{result_base}<sub>{base}</sub></span></p>
            '''
        })
        
        # 10진수로 변환한 값도 확인용으로 표시 (선택사항)
        num1_decimal = 0
        for i, digit in enumerate(reversed(num1_str.upper())):
            if '0' <= digit <= '9':
                digit_val = int(digit)
            else:
                digit_val = ord(digit) - ord('A') + 10
            num1_decimal += digit_val * (base ** i)
        
        num2_decimal = 0
        for i, digit in enumerate(reversed(num2_str.upper())):
            if '0' <= digit <= '9':
                digit_val = int(digit)
            else:
                digit_val = ord(digit) - ord('A') + 10
            num2_decimal += digit_val * (base ** i)
        
        result_decimal = num1_decimal + num2_decimal
        
    else:
        # 기존 방식: 10진수로 변환 후 계산
        # 1단계: 각 숫자를 10진수로 변환
        steps.append({
            'title': f'1단계: 각 숫자를 10진수로 변환하기',
            'content': f'<p>먼저 각 숫자를 10진수로 변환합니다:</p>'
        })
        
        # num1을 10진수로
        num1_decimal = 0
        num1_parts = []
        for i, digit in enumerate(reversed(num1_str.upper())):
            if '0' <= digit <= '9':
                digit_val = int(digit)
            else:
                digit_val = ord(digit) - ord('A') + 10
            power = len(num1_str) - 1 - i
            value = digit_val * (base ** power)
            num1_decimal += value
            num1_parts.append(f'{digit_val} × {base}<sup>{power}</sup> = {value}')
        
        # num2를 10진수로
        num2_decimal = 0
        num2_parts = []
        for i, digit in enumerate(reversed(num2_str.upper())):
            if '0' <= digit <= '9':
                digit_val = int(digit)
            else:
                digit_val = ord(digit) - ord('A') + 10
            power = len(num2_str) - 1 - i
            value = digit_val * (base ** power)
            num2_decimal += value
            num2_parts.append(f'{digit_val} × {base}<sup>{power}</sup> = {value}')
        
        steps[-1]['content'] += f'''
            <div class="formula">
                <strong>{num1_str}<sub>{base}</sub>:</strong><br>
                {' + '.join(num1_parts)}<br>
                = <span class="highlight">{num1_decimal}</span><sub>10</sub>
            </div>
            <div class="formula">
                <strong>{num2_str}<sub>{base}</sub>:</strong><br>
                {' + '.join(num2_parts)}<br>
                = <span class="highlight">{num2_decimal}</span><sub>10</sub>
            </div>
        '''
        
        # 2단계: 10진수로 계산
        if operator == '+':
            result_decimal = num1_decimal + num2_decimal
            steps.append({
                'title': '2단계: 10진수로 덧셈하기',
                'content': f'''
                    <div class="formula">
                        {num1_decimal}<sub>10</sub> + {num2_decimal}<sub>10</sub> = {result_decimal}<sub>10</sub>
                    </div>
                '''
            })
        else:
            result_decimal = num1_decimal - num2_decimal
            steps.append({
                'title': '2단계: 10진수로 뺄셈하기',
                'content': f'''
                    <div class="formula">
                        {num1_decimal}<sub>10</sub> - {num2_decimal}<sub>10</sub> = {result_decimal}<sub>10</sub>
                    </div>
                '''
            })
        
        # 3단계: 결과를 원래 진수로 변환
        result_base = convert_to_base(10, base, str(result_decimal))
        
        # 변환 과정 설명
        conversion_steps = []
        temp = result_decimal
        max_iterations = 100  # 안전장치
        iteration = 0
        while temp > 0 and iteration < max_iterations:
            remainder = temp % base
            quotient = temp // base
            if remainder >= 10:
                remainder_str = chr(ord('A') + remainder - 10)
            else:
                remainder_str = str(remainder)
            conversion_steps.append(f'{temp} ÷ {base} = {quotient} ... 나머지 {remainder_str}')
            temp = quotient
            iteration += 1
        
        steps.append({
            'title': f'3단계: 결과를 {base}진수로 변환하기',
            'content': f'''
                <p>10진수 {result_decimal}을 {base}진수로 변환합니다:</p>
                <div class="formula">
                    {'<br>'.join(conversion_steps[::-1])}<br>
                    나머지를 아래에서 위로 읽으면: <span class="highlight">{result_base}<sub>{base}</sub></span>
                </div>
            '''
        })
    
    return steps


def solve_base_conversion(problem_text, answer_text):
    """진수 변환 문제 풀이 생성"""
    steps = []
    
    # Unicode subscript를 일반 숫자로 변환
    problem_text_normalized = problem_text
    for num, sub in sorted(SUBSCRIPT_NUMBERS.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0, reverse=True):
        problem_text_normalized = problem_text_normalized.replace(sub, f'_{num}')
    
    # 문제에서 숫자와 진수 추출
    # 예: "What is the base8 (Octal) equivalent for 95₁₂?"
    # 또는 "95₁₂ converts to base 8 (Octal) ="
    
    # 패턴 1: "What is the baseX equivalent for Y_baseZ?"
    match = re.search(r'base\s*(\d+).*?for\s+([0-9A-Fa-f]+)[_\(](\d+)', problem_text_normalized, re.IGNORECASE)
    if match:
        target_base = int(match.group(1))
        number_str = match.group(2)
        source_base = int(match.group(3))
    else:
        # 패턴 2: "Y_baseZ converts to base X"
        match = re.search(r'([0-9A-Fa-f]+)[_\(](\d+).*?base\s*(\d+)', problem_text_normalized, re.IGNORECASE)
        if match:
            number_str = match.group(1)
            source_base = int(match.group(2))
            target_base = int(match.group(3))
        else:
            return steps
    
    # 1단계: 소스 진수를 10진수로 변환 (또는 expanded form으로 표현)
    num_decimal = 0
    conversion_parts = []
    expanded_parts = []
    
    # 순서대로 처리 (왼쪽부터 오른쪽으로)
    for i, digit in enumerate(number_str.upper()):
        if '0' <= digit <= '9':
            digit_val = int(digit)
        else:
            digit_val = ord(digit) - ord('A') + 10
        power = len(number_str) - 1 - i
        value = digit_val * (source_base ** power)
        num_decimal += value
        conversion_parts.append(f'{digit_val} × {source_base}<sup>{power}</sup> = {value}')
        expanded_parts.append(f'{digit_val}×{source_base}<sup>{power}</sup>')
    
    # source_base가 10일 때는 expanded form으로 표현
    if source_base == 10:
        # expanded form 계산 (순서대로)
        expanded_parts_ordered = []
        expanded_values_ordered = []
        for i, digit in enumerate(number_str):
            if '0' <= digit <= '9':
                digit_val = int(digit)
            else:
                digit_val = ord(digit.upper()) - ord('A') + 10
            power = len(number_str) - 1 - i
            value = digit_val * (10 ** power)
            expanded_parts_ordered.append(f'{digit_val}×10<sup>{power}</sup>')
            expanded_values_ordered.append(str(value))
        
        steps.append({
            'title': f'1단계: 10진수를 expanded form으로 표현하기',
            'content': f'''
                <div class="formula">
                    {number_str}<sub>10</sub> = {' + '.join(expanded_parts_ordered)}<br>
                    = {' + '.join(expanded_values_ordered)}<br>
                    = <span class="highlight">{num_decimal}</span><sub>10</sub>
                </div>
            '''
        })
    else:
        # expanded form 형식으로 표시
        expanded_form_parts = []
        expanded_values = []
        for i, digit in enumerate(number_str.upper()):
            if '0' <= digit <= '9':
                digit_val = int(digit)
            else:
                digit_val = ord(digit) - ord('A') + 10
            power = len(number_str) - 1 - i
            value = digit_val * (source_base ** power)
            expanded_form_parts.append(f'{digit_val} × {source_base}<sup>{power}</sup>')
            expanded_values.append(str(value))
        
        steps.append({
            'title': f'1단계: {source_base}진수를 10진수로 변환하기',
            'content': f'''
                <div class="formula">
                    {number_str}<sub>{source_base}</sub> = {' + '.join(expanded_form_parts)}<br>
                    = {' + '.join(expanded_values)}<br>
                    = <span class="highlight">{num_decimal}</span><sub>10</sub>
                </div>
            '''
        })
    
    # 2단계: 10진수를 타겟 진수로 변환 (같은 진수거나 이미 10진수면 생략)
    if source_base == target_base:
        # 같은 진수이므로 변환 불필요
        steps.append({
            'title': '결과',
            'content': f'''
                <p>{source_base}진수를 {target_base}진수로 변환하는 것이므로 변환할 필요가 없습니다.</p>
                <div class="formula">
                    결과: <span class="highlight">{num_decimal}<sub>{target_base}</sub></span>
                </div>
            '''
        })
    elif target_base == 10:
        # 이미 10진수로 변환했으므로 추가 변환 불필요
        steps.append({
            'title': '결과',
            'content': f'''
                <p>이미 10진수로 변환되었으므로 추가 변환이 필요 없습니다.</p>
                <div class="formula">
                    결과: <span class="highlight">{num_decimal}<sub>10</sub></span>
                </div>
            '''
        })
    else:
        result_base = convert_to_base(10, target_base, str(num_decimal))
        
        conversion_steps = []
        temp = num_decimal
        max_iterations = 100  # 안전장치
        iteration = 0
        while temp > 0 and iteration < max_iterations:
            remainder = temp % target_base
            quotient = temp // target_base
            if remainder >= 10:
                remainder_str = chr(ord('A') + remainder - 10)
            else:
                remainder_str = str(remainder)
            conversion_steps.append(f'{temp} ÷ {target_base} = {quotient} ... 나머지 {remainder_str}')
            temp = quotient
            iteration += 1
        
        target_base_name = NAME_OF_NUMBER_BASES.get(target_base, f'base {target_base}')
        
        steps.append({
            'title': f'2단계: 10진수를 {target_base}진수({target_base_name})로 변환하기',
            'content': f'''
                <p>10진수 {num_decimal}을 {target_base}진수로 변환합니다:</p>
                <div class="formula">
                    {'<br>'.join(conversion_steps)}<br>
                    나머지를 아래에서 위로 읽으면: <span class="highlight">{result_base}<sub>{target_base}</sub></span>
                </div>
            '''
        })
    
    return steps


def solve_rgb_color(problem_text, answer_text):
    """RGB 색상 코드 문제 풀이 생성"""
    steps = []
    
    # 패턴 1: "A color has a red value of X, green value of Y, blue value of Z. What is its hexadecimal color code?"
    match = re.search(r'red value of (\d+).*?green value of (\d+).*?blue value of (\d+)', problem_text, re.IGNORECASE)
    if match:
        red = int(match.group(1))
        green = int(match.group(2))
        blue = int(match.group(3))
        
        steps.append({
            'title': '1단계: 주어진 RGB 값 확인하기',
            'content': f'''
                <div class="formula">
                    Red (R) = {red}<sub>10</sub><br>
                    Green (G) = {green}<sub>10</sub><br>
                    Blue (B) = {blue}<sub>10</sub>
                </div>
                <p>각 값을 16진수로 변환해야 합니다.</p>
            '''
        })
        
        # 각 값을 16진수로 변환
        red_hex = f"{red:02X}"
        green_hex = f"{green:02X}"
        blue_hex = f"{blue:02X}"
        
        # 변환 과정
        rgb_values = [
            ('Red', red, red_hex),
            ('Green', green, green_hex),
            ('Blue', blue, blue_hex)
        ]
        
        conversion_details = []
        for name, value, hex_val in rgb_values:
            if value == 0:
                conversion_details.append(f'<strong>{name}:</strong> {value}<sub>10</sub> = 00<sub>16</sub>')
            else:
                conversion_steps = []
                temp = value
                max_iterations = 100  # 안전장치
                iteration = 0
                while temp > 0 and iteration < max_iterations:
                    remainder = temp % 16
                    quotient = temp // 16
                    if remainder >= 10:
                        remainder_str = chr(ord('A') + remainder - 10)
                    else:
                        remainder_str = str(remainder)
                    conversion_steps.append(f'{temp} ÷ 16 = {quotient} ... 나머지 {remainder_str}')
                    temp = quotient
                    iteration += 1
                conversion_details.append(f'''
                    <strong>{name}:</strong> {value}<sub>10</sub><br>
                    <div style="margin-left: 20px;">
                        {'<br>'.join(conversion_steps)}<br>
                        = {hex_val}<sub>16</sub>
                    </div>
                ''')
        
        steps.append({
            'title': '2단계: 각 RGB 값을 16진수로 변환하기',
            'content': f'''
                <div class="formula">
                    {'<br><br>'.join(conversion_details)}
                </div>
            '''
        })
        
        steps.append({
            'title': '3단계: 16진수 색상 코드 조합하기',
            'content': f'''
                <div class="formula">
                    RGB({red}, {green}, {blue}) = RGB({red_hex}<sub>16</sub>, {green_hex}<sub>16</sub>, {blue_hex}<sub>16</sub>)<br>
                    색상 코드 = <span class="highlight">#{red_hex}{green_hex}{blue_hex}</span>
                </div>
                <div style="margin-top: 15px;">
                    <span class="color-box" style="background-color: #{red_hex}{green_hex}{blue_hex};"></span>
                    <span style="margin-left: 15px; vertical-align: middle;">이 색상입니다</span>
                </div>
            '''
        })
    
    # 패턴 2: "In the color #XXXXXX, what is the binary value for the X component?"
    match = re.search(r'color (#[0-9A-Fa-f]{6}).*?(\w+)\s+value.*?(\w+)\s+component', problem_text, re.IGNORECASE)
    if match:
        color_code = match.group(1)
        base_type = match.group(2)  # binary, decimal, etc.
        component = match.group(3)  # red, green, blue
        
        # 색상 코드에서 RGB 값 추출
        hex_color = color_code[1:]  # # 제거
        red_hex = hex_color[0:2]
        green_hex = hex_color[2:4]
        blue_hex = hex_color[4:6]
        
        red = int(red_hex, 16)
        green = int(green_hex, 16)
        blue = int(blue_hex, 16)
        
        component_map = {'red': (red, red_hex), 'green': (green, green_hex), 'blue': (blue, blue_hex)}
        component_value, component_hex = component_map.get(component.lower(), (0, '00'))
        
        steps.append({
            'title': f'1단계: 색상 코드에서 {component} 구성 요소 추출하기',
            'content': f'''
                <div class="formula">
                    {color_code} = RGB({red_hex}<sub>16</sub>, {green_hex}<sub>16</sub>, {blue_hex}<sub>16</sub>)<br>
                    = RGB({red}<sub>10</sub>, {green}<sub>10</sub>, {blue}<sub>10</sub>)
                </div>
                <p><strong>{component}</strong> 구성 요소: {component_hex}<sub>16</sub> = {component_value}<sub>10</sub></p>
            '''
        })
        
        if base_type.lower() == 'binary':
            # 2진수로 변환
            binary_value = convert_to_base(10, 2, str(component_value))
            conversion_steps = []
            temp = component_value
            max_iterations = 100  # 안전장치
            iteration = 0
            while temp > 0 and iteration < max_iterations:
                remainder = temp % 2
                quotient = temp // 2
                conversion_steps.append(f'{temp} ÷ 2 = {quotient} ... 나머지 {remainder}')
                temp = quotient
                iteration += 1
            
            steps.append({
                'title': f'2단계: {component} 값을 2진수로 변환하기',
                'content': f'''
                    <p>{component_value}<sub>10</sub>을 2진수로 변환합니다:</p>
                    <div class="formula">
                        {'<br>'.join(conversion_steps)}<br>
                        나머지를 아래에서 위로 읽으면: <span class="highlight">{binary_value}<sub>2</sub></span>
                    </div>
                '''
            })
    
    # 패턴 3: "What is the sum of the X and Y components for the color #XXXXXX in decimal?"
    match = re.search(r'sum of the (\w+)\s+and\s+(\w+).*?components.*?color (#[0-9A-Fa-f]{6})', problem_text, re.IGNORECASE)
    if match:
        component1 = match.group(1)
        component2 = match.group(2)
        color_code = match.group(3)
        
        # 색상 코드에서 RGB 값 추출
        hex_color = color_code[1:]
        red_hex = hex_color[0:2]
        green_hex = hex_color[2:4]
        blue_hex = hex_color[4:6]
        
        red = int(red_hex, 16)
        green = int(green_hex, 16)
        blue = int(blue_hex, 16)
        
        component_map = {'red': red, 'green': green, 'blue': blue}
        val1 = component_map.get(component1.lower(), 0)
        val2 = component_map.get(component2.lower(), 0)
        sum_val = val1 + val2
        
        steps.append({
            'title': '1단계: 색상 코드에서 RGB 값 추출하기',
            'content': f'''
                <div class="formula">
                    {color_code} = RGB({red_hex}<sub>16</sub>, {green_hex}<sub>16</sub>, {blue_hex}<sub>16</sub>)<br>
                    = RGB({red}<sub>10</sub>, {green}<sub>10</sub>, {blue}<sub>10</sub>)
                </div>
            '''
        })
        
        # component 이름을 한글로 변환
        component_names = {'red': '빨간색', 'green': '녹색', 'blue': '파란색'}
        component1_kr = component_names.get(component1.lower(), component1)
        component2_kr = component_names.get(component2.lower(), component2)
        
        steps.append({
            'title': f'2단계: {component1_kr}과 {component2_kr} 구성 요소의 합 계산하기',
            'content': f'''
                <div class="formula">
                    {component1_kr}: {val1}<sub>10</sub><br>
                    {component2_kr}: {val2}<sub>10</sub><br>
                    합계: {val1} + {val2} = <span class="highlight">{sum_val}</span><sub>10</sub>
                </div>
            '''
        })
    
    # 패턴 4: "If you increase/decrease the X component of the color #XXXXXX by Y%, what is the new hexadecimal color code?"
    match = re.search(r'(increase|decrease|rise|grow|expand|reduce|fall|decline|drop|shrink).*?(\w+).*?component.*?color (#[0-9A-Fa-f]{6}).*?by\s+(\d+)%', problem_text, re.IGNORECASE)
    if match:
        trend = match.group(1).lower()
        component = match.group(2)
        color_code = match.group(3)
        percent = int(match.group(4))
        
        # 색상 코드에서 RGB 값 추출
        hex_color = color_code[1:]
        red_hex = hex_color[0:2]
        green_hex = hex_color[2:4]
        blue_hex = hex_color[4:6]
        
        red = int(red_hex, 16)
        green = int(green_hex, 16)
        blue = int(blue_hex, 16)
        
        component_map = {'red': (red, red_hex), 'green': (green, green_hex), 'blue': (blue, blue_hex)}
        original_value, original_hex = component_map.get(component.lower(), (0, '00'))
        
        steps.append({
            'title': f'1단계: 색상 코드에서 {component} 구성 요소 추출하기',
            'content': f'''
                <div class="formula">
                    {color_code} = RGB({red_hex}<sub>16</sub>, {green_hex}<sub>16</sub>, {blue_hex}<sub>16</sub>)<br>
                    = RGB({red}<sub>10</sub>, {green}<sub>10</sub>, {blue}<sub>10</sub>)
                </div>
                <p><strong>{component}</strong> 구성 요소: {original_hex}<sub>16</sub> = {original_value}<sub>10</sub></p>
            '''
        })
        
        # 퍼센트 계산
        if trend in ['increase', 'rise', 'grow', 'expand']:
            new_value = original_value * (100 + percent) // 100
            operation = f'{original_value} × (100% + {percent}%) = {original_value} × {100 + percent}% = {original_value * (100 + percent) // 100}'
        else:
            new_value = original_value * (100 - percent) // 100
            operation = f'{original_value} × (100% - {percent}%) = {original_value} × {100 - percent}% = {original_value * (100 - percent) // 100}'
        
        if new_value > 255:
            new_value = 255
        
        steps.append({
            'title': f'2단계: {component} 값을 {percent}% {trend}시키기',
            'content': f'''
                <div class="formula">
                    {operation}<br>
                    새로운 {component} 값 = <span class="highlight">{new_value}</span><sub>10</sub>
                </div>
            '''
        })
        
        # 새로운 색상 코드 조합
        new_red = red
        new_green = green
        new_blue = blue
        
        if component.lower() == 'red':
            new_red = new_value
        elif component.lower() == 'green':
            new_green = new_value
        else:
            new_blue = new_value
        
        new_color_code = f"#{new_red:02X}{new_green:02X}{new_blue:02X}"
        
        steps.append({
            'title': '3단계: 새로운 16진수 색상 코드 조합하기',
            'content': f'''
                <div class="formula">
                    새로운 RGB 값: RGB({new_red}, {new_green}, {new_blue})<br>
                    = RGB({new_red:02X}<sub>16</sub>, {new_green:02X}<sub>16</sub>, {new_blue:02X}<sub>16</sub>)<br>
                    새로운 색상 코드 = <span class="highlight">{new_color_code}</span>
                </div>
                <div style="margin-top: 15px;">
                    <span class="color-box" style="background-color: {color_code};"></span>
                    <span style="margin: 0 20px;">→</span>
                    <span class="color-box" style="background-color: {new_color_code};"></span>
                </div>
            '''
        })
    
    return steps


def solve_find_number(problem_text, answer_text):
    """가장 작은/큰 수 찾기 문제 풀이 생성"""
    steps = []
    
    # 문제에서 옵션 추출
    # 예: "Which of the following is the smallest number? [1401₇, 4111₅, ...]"
    match = re.search(r'(the smallest|the second smallest|the largest|the second largest)', problem_text, re.IGNORECASE)
    if not match:
        return steps
    
    option = match.group(1).lower()
    
    # 숫자 리스트 추출
    # 대괄호 안의 내용 찾기
    bracket_match = re.search(r'\[(.*?)\]', problem_text)
    if not bracket_match:
        return steps
    
    numbers_text = bracket_match.group(1)
    
    # 각 숫자 파싱
    numbers = []
    # 쉼표나 다른 구분자로 분리
    parts = re.split(r'[,，]', numbers_text)
    for part in parts:
        part = part.strip().strip("'\"")
        num_str, base = parse_base_number(part)
        if num_str and base:
            # 10진수로 변환 (순서대로 처리)
            num_decimal = 0
            for i, digit in enumerate(num_str.upper()):
                if '0' <= digit <= '9':
                    digit_val = int(digit)
                else:
                    digit_val = ord(digit) - ord('A') + 10
                power = len(num_str) - 1 - i
                num_decimal += digit_val * (base ** power)
            numbers.append((part, num_str, base, num_decimal))
    
    if not numbers:
        return steps
    
    steps.append({
        'title': f'1단계: 각 숫자를 10진수로 변환하기',
        'content': '<p>모든 숫자를 10진수로 변환하여 비교합니다:</p>'
    })
    
    conversion_table = []
    for original, num_str, base, decimal in numbers:
        conversion_parts = []
        for i, digit in enumerate(num_str.upper()):
            if '0' <= digit <= '9':
                digit_val = int(digit)
            else:
                digit_val = ord(digit) - ord('A') + 10
            power = len(num_str) - 1 - i
            value = digit_val * (base ** power)
            conversion_parts.append(f'{digit_val} × {base}<sup>{power}</sup> = {value}')
        
        conversion_table.append(f'''
            <tr>
                <td style="padding: 10px; text-align: center;">{format_subscript(original)}</td>
                <td style="padding: 10px; text-align: center;">{' + '.join(conversion_parts)}</td>
                <td style="padding: 10px; text-align: center; font-weight: bold;">{decimal}<sub>10</sub></td>
            </tr>
        ''')
    
    steps[-1]['content'] += f'''
        <table style="width: 100%; margin: 15px 0; border-collapse: collapse;">
            <tr style="border-bottom: 2px solid #333;">
                <th style="padding: 10px; text-align: center; background-color: #e3f2fd;">원래 숫자</th>
                <th style="padding: 10px; text-align: center; background-color: #e3f2fd;">변환 과정</th>
                <th style="padding: 10px; text-align: center; background-color: #e3f2fd;">10진수 값</th>
            </tr>
            {''.join(conversion_table)}
        </table>
    '''
    
    # 정렬
    sorted_numbers = sorted(numbers, key=lambda x: x[3])
    
    # 옵션에 따라 선택
    if 'smallest' in option:
        if 'second' in option:
            selected = sorted_numbers[1]
        else:
            selected = sorted_numbers[0]
    else:  # largest
        if 'second' in option:
            selected = sorted_numbers[-2]
        else:
            selected = sorted_numbers[-1]
    
    steps.append({
        'title': f'2단계: {option.replace("the ", "").title()} 찾기',
        'content': f'''
            <p>10진수 값으로 정렬: {", ".join([f"{n[3]}" for n in sorted_numbers])}</p>
            <p><strong>{option.replace("the ", "").title()}</strong>는 <span class="highlight">{format_subscript(selected[0])}</span>입니다.</p>
            <p>(10진수 값: {selected[3]})</p>
        '''
    })
    
    # answer_text 파싱하여 정답과 10진수 값들 추출
    # 형식: "정답, [10진수값1, 10진수값2, ...]"
    answer_parts = answer_text.split(',', 1)
    if len(answer_parts) == 2:
        answer_number = answer_parts[0].strip()
        decimal_values_text = answer_parts[1].strip()
        # 대괄호 제거하고 숫자 추출
        decimal_values = re.findall(r'\d+', decimal_values_text)
        # 문제 순서대로 10진수 값 매핑
        problem_decimal_values = [str(n[3]) for n in numbers]
        # 정답 형식: "정답, [문제순서대로 10진수값들]"
        formatted_answer = f"{answer_number}, [{', '.join(problem_decimal_values)}]"
    else:
        formatted_answer = answer_text
    
    # formatted_answer를 steps에 저장 (나중에 사용)
    steps.append({
        'title': '_answer_format',
        'content': formatted_answer
    })
    
    return steps


def solve_expanded_form(problem_text, answer_text):
    """전개형 문제 풀이 생성"""
    steps = []
    
    # 문제에서 숫자와 진수 추출
    # 예: "Express the following number in expanded form 13₁₀ ="
    match = re.search(r'([0-9A-Fa-f]+)[_\(](\d+)', problem_text)
    if not match:
        return steps
    
    number_str = match.group(1)
    base = int(match.group(2))
    
    steps.append({
        'title': f'1단계: 각 자릿수의 값 계산하기',
        'content': f'<p>{number_str}<sub>{base}</sub>의 각 자릿수를 분석합니다:</p>'
    })
    
    expanded_parts = []
    for i, digit in enumerate(number_str.upper()):
        if '0' <= digit <= '9':
            digit_val = int(digit)
        else:
            digit_val = ord(digit) - ord('A') + 10
        
        power = len(number_str) - 1 - i
        expanded_parts.append(f'{digit_val} × {base}<sup>{power}</sup>')
    
    steps[-1]['content'] += f'''
        <div class="formula">
            {number_str}<sub>{base}</sub> = {' + '.join(expanded_parts)}
        </div>
    '''
    
    return steps


def generate_solution_html(problem_num, problem_text, answer_text, problem_type):
    """문제 풀이 HTML 생성"""
    
    # 문제 유형에 따라 풀이 생성
    steps = []
    if problem_type == 'AdditionAndSubtraction':
        steps = solve_addition_subtraction(problem_text, answer_text)
    elif problem_type == 'TransformNumberBases':
        steps = solve_base_conversion(problem_text, answer_text)
    elif problem_type == 'RGBCoding':
        steps = solve_rgb_color(problem_text, answer_text)
    elif problem_type == 'FindNumber':
        steps = solve_find_number(problem_text, answer_text)
    elif problem_type == 'ExpandedForm':
        steps = solve_expanded_form(problem_text, answer_text)
    
    # HTML 생성
    html = f'''
        <h2>문제 {problem_num}번</h2>
        <div class="problem">
            <strong>문제:</strong> {html_escape(problem_text)}
        </div>
        
        <div class="solution">
    '''
    
    # answer_format 찾기
    answer_format = answer_text
    for step in steps:
        if step['title'] == '_answer_format':
            answer_format = step['content']
            break
    
    for i, step in enumerate(steps, 1):
        if step['title'] == '_answer_format':
            continue  # answer_format은 HTML에 표시하지 않음
        html += f'''
            <div class="step">
                <div class="step-title">{step['title']}</div>
                {step['content']}
            </div>
        '''
    
    html += f'''
            <div class="answer">
                <strong>정답: {format_subscript(html_escape(answer_format))}</strong>
            </div>
        </div>
    '''
    
    return html


def generate_solutions_from_problems(problems_with_answers):
    """생성된 문제와 답으로부터 풀이 HTML 생성"""
    cns = ComputerNumberSystem()
    problems = []
    
    print(f"총 {len(problems_with_answers)}개 문제의 풀이를 생성합니다...")
    
    for problem_num, (problem, answer) in enumerate(problems_with_answers, 1):
        # 문제 유형 판별 (문제 텍스트 패턴 분석)
        problem_type = None
        
        # RGBCoding: color, #, rgb, hexadecimal color code 등
        if any(keyword in problem.lower() for keyword in ['color', 'rgb', 'hexadecimal', '#']):
            problem_type = 'RGBCoding'
        # FindNumber: smallest, largest 등
        elif any(keyword in problem.lower() for keyword in ['smallest', 'largest', 'which of the following']):
            problem_type = 'FindNumber'
        # ExpandedForm: expanded form
        elif 'expanded form' in problem.lower():
            problem_type = 'ExpandedForm'
        # TransformNumberBases: converts to base, equivalent for
        elif any(keyword in problem.lower() for keyword in ['converts to base', 'equivalent for', 'base']):
            problem_type = 'TransformNumberBases'
        # AdditionAndSubtraction: + 또는 - 연산자
        elif '+' in problem or ' + ' in problem:
            problem_type = 'AdditionAndSubtraction'
        else:
            # 기본값: 첫 번째 챕터로 할당
            problem_type = cns.chapter[0] if cns.chapter else 'Unknown'
        
        problems.append((problem_num, problem, answer, problem_type))
        
        if problem_num % 30 == 0:
            print(f"진행 중... {problem_num}/{len(problems_with_answers)} 문제 완료")
    
    # HTML 생성 및 저장
    _generate_html_file(problems)


def main():
    """메인 함수: 문제 생성 및 풀이 HTML 생성 (독립 실행용)"""
    
    # 문제 생성
    cns = ComputerNumberSystem()
    
    # PDF와 동일한 방식으로 문제 생성 (30 set × 5문제 = 150문제)
    problems = []
    problem_set_count = 30
    
    print(f"총 {problem_set_count}개 set의 문제를 생성합니다...")
    
    for set_num in range(1, problem_set_count + 1):
        problem_list, answer_list = cns.get_problem_answer()
        
        if not problem_list:
            print(f"Set {set_num}: 문제 생성 실패")
            continue
        
        # 각 문제에 대한 풀이 정보 추가
        # get_problem_answer는 챕터를 섞어서 반환하므로, 문제 텍스트로 유형 판별
        for i, (problem, answer) in enumerate(zip(problem_list, answer_list)):
            # 문제 유형 판별 (문제 텍스트 패턴 분석)
            problem_type = None
            
            # RGBCoding: color, #, rgb, hexadecimal color code 등
            if any(keyword in problem.lower() for keyword in ['color', 'rgb', 'hexadecimal', '#']):
                problem_type = 'RGBCoding'
            # FindNumber: smallest, largest 등
            elif any(keyword in problem.lower() for keyword in ['smallest', 'largest', 'which of the following']):
                problem_type = 'FindNumber'
            # ExpandedForm: expanded form
            elif 'expanded form' in problem.lower():
                problem_type = 'ExpandedForm'
            # TransformNumberBases: converts to base, equivalent for
            elif any(keyword in problem.lower() for keyword in ['converts to base', 'equivalent for', 'base']):
                problem_type = 'TransformNumberBases'
            # AdditionAndSubtraction: + 또는 - 연산자
            elif '+' in problem or ' + ' in problem:
                problem_type = 'AdditionAndSubtraction'
            else:
                # 기본값: 챕터 순서로 할당
                problem_type = cns.chapter[i % len(cns.chapter)]
            
            problem_num = (set_num - 1) * len(problem_list) + i + 1
            problems.append((problem_num, problem, answer, problem_type))
        
        if set_num % 5 == 0:
            print(f"진행 중... {set_num}/{problem_set_count} set 완료")
    
    # HTML 생성 및 저장
    _generate_html_file(problems)


def _generate_html_file(problems):
    """문제 리스트로부터 HTML 파일 생성"""
    # HTML 헤더
    html_content = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Computer Number System 문제 풀이</title>
    <style>
        body {
            font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-left: 5px solid #3498db;
            padding-left: 15px;
        }
        .problem {
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #e74c3c;
        }
        .solution {
            background-color: #e8f5e9;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #4caf50;
        }
        .step {
            margin: 15px 0;
            padding: 15px;
            background-color: #fff3e0;
            border-radius: 5px;
            border-left: 3px solid #ff9800;
        }
        .step-title {
            font-weight: bold;
            color: #e65100;
            margin-bottom: 10px;
        }
        .formula {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            text-align: left;
        }
        .color-box {
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 2px solid #333;
            border-radius: 5px;
            margin: 10px;
            vertical-align: middle;
        }
        .answer {
            background-color: #fff9c4;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border: 2px solid #fbc02d;
            font-size: 1.2em;
            text-align: center;
        }
        .highlight {
            background-color: #fff59d;
            padding: 2px 5px;
            border-radius: 3px;
        }
        code {
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        sub {
            font-size: 0.75em;
            vertical-align: sub;
            line-height: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #e3f2fd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Computer Number System 문제 풀이</h1>
        <p style="text-align: right; color: #7f8c8d;">상세 풀이</p>
'''
    
    # 각 문제에 대한 풀이 추가
    for problem_num, problem, answer, problem_type in problems:
        solution_html = generate_solution_html(problem_num, problem, answer, problem_type)
        html_content += solution_html
    
    # HTML 푸터
    html_content += '''
        <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #ddd; text-align: center; color: #7f8c8d;">
            <p>Computer Number System 문제 풀이 완료</p>
        </div>
    </div>
</body>
</html>
'''
    
    # HTML 파일 저장
    output_path = os.path.join(_THIS_DIR, 'Computer_Number_System_Solutions.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n풀이 HTML 파일이 생성되었습니다: {output_path}")
    print(f"총 {len(problems)}개 문제의 풀이가 포함되어 있습니다.")
    print(f"각 문제 유형별 통계:")
    
    # 문제 유형별 통계
    type_counts = {}
    for _, _, _, problem_type in problems:
        type_counts[problem_type] = type_counts.get(problem_type, 0) + 1
    
    for problem_type, count in sorted(type_counts.items()):
        print(f"  - {problem_type}: {count}개")


if __name__ == "__main__":
    main()
