#from elementary_division.computer_number_system.computer_number_system import ComputerNumberSystem
from utils.number_bases import convert_to_base
from utils.unicodes import SUBSCRIPT_NUMBERS, UNICODE_MULTIPLIER, SUPERSCRIPT_NUMBERS
import random
import os
import sys
from utils import pdf

class RGB():
    def __init__(self):
        super().__init__()
        self.red = ""
        self.green = ""
        self.blue = ""
        self.red_decimal = 0
        self.green_decimal = 0
        self.blue_decimal = 0
        self.initialize_rgb()

    def get_rgb_string(self)->list[str]:
        return [self.red, self.green, self.blue]
    def get_rgb_decimal(self)->list[int]:
        return [self.red_decimal, self.green_decimal, self.blue_decimal]

    def get_rgb_code(self):
        return f"#{self.red}{self.green}{self.blue}"


    def set_rgb(self, red:str, green:str, blue:str):
        self.red = red
        self.green = green
        self.blue = blue

    def initialize_rgb(self):
        self.red_decimal = random.randint(0,255)
        self.green_decimal = random.randint(0,255)
        self.blue_decimal = random.randint(0,255)
        self.red = f"{self.red_decimal:02X}"
        self.green = f"{self.green_decimal:02X}"
        self.blue = f"{self.blue_decimal:02X}"
        print(f"({self.red_decimal}, {self.green_decimal}, {self.blue_decimal}) -> #{self.red}{self.green}{self.blue} generated RGB")


class RGBCoding(RGB):
    def __init__(self):
        super().__init__()
        self.title = "RGB Coding"
        self.rgb = RGB()
        pass

    def make_bitwise_operation_problem(self):
        bitwise_set = ['AND', 'OR', 'XOR', 'NOT']
        color_set = ['red', 'green', 'blue']

        #bitwise_choice = random.choice(bitwise_set)
        bitwise_choice = 'NOT'

        # Get the decimal values for each color component
        red_val, green_val, blue_val = self.rgb.get_rgb_decimal()
        color_map = {'red': red_val, 'green': green_val, 'blue': blue_val}

        answer = 0

        if bitwise_choice == 'NOT':
            color_choice = random.choice(color_set)
            problem_text = f"If you perform a bitwise '{bitwise_choice}' the {color_choice} component of {self.rgb.get_rgb_code()}, what is the resulting decimal value?"
            answer = ~color_map[color_choice]&0xff
        else:
            random_colors = random.sample(color_set, 2)
            color1, color2 = random_colors[0], random_colors[1]
            val1 = color_map[color1]
            val2 = color_map[color2]

            problem_text = (f"If you perform a bitwise '{bitwise_choice}' between the "
                            f"{color1} and the {color2} components of "
                            f"{self.rgb.get_rgb_code()}, what is the resulting decimal value?")

            # Calculate the answer based on the chosen operation
            if bitwise_choice == 'AND':
                answer = val1 & val2
            elif bitwise_choice == 'OR':
                answer = val1 | val2
            elif bitwise_choice == 'XOR':
                answer = val1 ^ val2

        answer_text = str(answer)

        return problem_text, answer_text

    def make_trend_word_problem(self)->(str, str):
        color_set = ['red', 'green', 'blue']
        trend_word_set = ['increase', 'rise', 'grow', 'expand', 'decrease', 'reduce', 'fall', 'decline', 'drop', 'shrink']
        delta = [10, 20, 30, 40, 50, 60, 70, 80, 90]

        color_choice = random.choice(color_set)
        trend_word_choice = random.choice(trend_word_set)
        delta_choice = random.choice(delta)

        problem_text = f"If you {trend_word_choice} the {color_choice} component of the color {self.rgb.get_rgb_code()} by {delta_choice}%, what is the new hexadecimal color code?"
        answer_text = f""
        answer = self.rgb.get_rgb_decimal()[color_set.index(color_choice)]
        if trend_word_choice == 'increase' or trend_word_choice == 'rise' or trend_word_choice == 'grow' or trend_word_choice == 'expand':
            answer = answer * (100 + int(delta_choice))//100
        else:
            answer = answer * (100 -int(delta_choice))//100
        if answer > 0xff :
            answer = 0xff
        print(f"trend word problem calculation: {color_choice}: {self.rgb.get_rgb_decimal()[color_set.index(color_choice)]} -> {answer}")

        if color_choice == 'red':
            answer_text = f"#{answer:02X}{self.rgb.green}{self.rgb.blue}"
        elif color_choice == 'green':
            answer_text = f"#{self.rgb.red}{answer:02X}{self.rgb.blue}"
        else:
            answer_text = f"#{self.rgb.red}{self.rgb.green}{answer:02X}"

        return problem_text, answer_text

    def make_color_value_problem(self)->(str, str):
        color_set = ['red', 'green', 'blue']
        base_set = ['binary', 'quaternary', 'octal', 'decimal', 'hexadecimal']
        base_map = {'binary': 2, 'quaternary': 4, 'octal': 8, 'decimal': 10, 'hexadecimal': 16}
        base_prefix_map = {'binary': '0b', 'quaternary': '0q', 'octal': '0o', 'decimal': '', 'hexadecimal': '0x'}

        color_choice = random.choice(color_set)
        base_choice = random.choice(base_set)

        problem_text = f"In the color {self.rgb.get_rgb_code()}, what is the {base_choice} value for the {color_choice} component?"

        # Get the decimal values for each color component
        red_val, green_val, blue_val = self.rgb.get_rgb_decimal()
        color_map = {'red': red_val, 'green': green_val, 'blue': blue_val}

        answer = color_map[color_choice]
        answer_text = f"{convert_to_base(10, base_map[base_choice], str(answer))}{SUBSCRIPT_NUMBERS[str(base_map[base_choice])]} or {base_prefix_map[base_choice]}{convert_to_base(10, base_map[base_choice], str(answer))}"
        return problem_text, answer_text

    def generate_problem(self)->(str, str):
        self.rgb.initialize_rgb()
        color_set = ['red', 'green', 'blue']
        color_choice = random.choice(color_set)
        random_colors = random.sample(color_set, 2)
        print(random_colors)
        color_value_problem, color_value_answer = self.make_color_value_problem()
        trend_problem, trend_answer = self.make_trend_word_problem()
        bitwise_problem, bitwise_answer = self.make_bitwise_operation_problem()
        problem_pool = [color_value_problem,
                        f"A color has a red value of {self.rgb.red_decimal}, a green value of {self.rgb.green_decimal}, and a blue value of {self.rgb.blue_decimal}. What is its hexadecimal color code?",
                        f"What is the sum of the {random_colors[0]} and {random_colors[1]} components for the color {self.rgb.get_rgb_code()} in decimal?",
                        trend_problem,
                        bitwise_problem,
                        ]

        answer_pool = [color_value_answer,
                       f"{self.rgb.get_rgb_code()}",
                       f"{self.rgb.get_rgb_decimal()[color_set.index(random_colors[0])] + self.rgb.get_rgb_decimal()[color_set.index(random_colors[1])]}",
                       trend_answer,
                       bitwise_answer,
                       ]

        for problem, answer in zip(problem_pool, answer_pool):
            print(f"{problem} : {answer}")

        random_choice = random.randint(0, len(problem_pool)-1)
        return problem_pool[random_choice], answer_pool[random_choice]

    def get_problem_answer(self) -> (str, str):

        problem_text = f""
        answer_text = f""
        problem_text, answer_text = self.generate_problem()
        print(f"{problem_text} {answer_text}")

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
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=2, row_spacing=70)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

#자신을 부모 클래스 레지스트리에 등록
#ComputerNumberSystem.register_child('RGBCoding', RGBCoding)

def main():
    RGBCoding().generate_practice(5)

if __name__ == "__main__":
    main()