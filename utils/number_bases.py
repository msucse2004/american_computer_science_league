NAME_OF_NUMBER_BASES = {
    2: 'Binary',
    3: 'Ternary',
    4: 'Quaternary',
    5: 'Quinary',
    6: 'Senary',
    7: 'Septenary',
    8: 'Octal',
    9: 'Nonary',
    10: 'Decimal',
    11: 'Undecimal',
    12: 'Duodecimal',
    13: 'Tridecimal',
    14: 'Tetradecimal',
    15: 'Pentadecimal',
    16: 'Hexadecimal'
}

def convert_to_base(src_base: int, dst_base: int, number: str) -> str:
    if number == 0:
        return 0
    if number == 1:
        return 1
    if dst_base < 2:
        return 0

    # Character set for bases 2-16
    DIGITS = "0123456789ABCDEF"

    # --- Step 1: Convert the number to a decimal (base-10) integer ---

    decimal_value = 0
    power = 0

    # Iterate through the number string from right to left
    for digit in reversed(number.upper()):
        # Get the integer value of the digit (e.g., 'A' is 10, 'F' is 15)
        if '0' <= digit <= '9':
            digit_value = int(digit)
        else:
            digit_value = ord(digit) - ord('A') + 10

        # Add the place value to the total
        decimal_value += digit_value * (src_base ** power)
        power += 1

    # --- Step 2: Convert the decimal integer to the destination base ---

    # Handle the edge case where the input number is 0
    if decimal_value == 0:
        return "0"

    result = ""

    # Repeatedly divide the decimal number by the destination base
    while decimal_value > 0:
        remainder = decimal_value % dst_base
        # Prepend the corresponding digit from our DIGITS string
        result = DIGITS[remainder] + result
        # Integer division to get the next number to process
        decimal_value //= dst_base

    return result