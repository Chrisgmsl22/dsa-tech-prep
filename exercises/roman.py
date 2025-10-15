"""
    Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

    Symbol       Value
"I": 1,
"V": 5,
"X": 10,
"L": 50,
"C": 100,
"D": 500,
"M": 1000,
    For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

    Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

    I can be placed before V (5) and X (10) to make 4 and 9. 
    X can be placed before L (50) and C (100) to make 40 and 90. 
    C can be placed before D (500) and M (1000) to make 400 and 900.
    Given a roman numeral, convert it to an integer.

    

    Example 1:

    Input: s = "III"
    Output: 3
    Explanation: III = 3.
    Example 2:

    Input: s = "LVIII"
    Output: 58
    Explanation: L = 50, V= 5, III = 3.
    Example 3:

    Input: s = "MCMXCIV"
    Output: 1994
    Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.

"""

"""
    Brainstorm:
    - I could use a map to store this "numerals" and I get to store its roman and integer equivalent
    - need to take into consideration when to use 4,9, 40, 90, 400 and 900
    - this function takes in a string
    - Can assume the roman number is correct
    - We need to return its number equivalent
    - need to consider all individual characters, (iteration? **) (a string, is an array)
    - translate all numbers 
    - sum all numbers
    - return final result (LEARN ABOUT REGEX)
    
    
    Plain english pseudocode:
    define function{
        create our map which contains all roman numbers
        
        final_result counter
        iterate over string{
            analyze each character
            I can use my map to access the roman number
            add this number to final_result
        }
        
        return final_result
    }
    
    IV # 4
    IX # 9
    1 | 10
    if 1 < 10, then 10 - 1
    1 | 5
    if 1 < 5, then 5 - 1
    
    CM # 900
    100 | 1000
    if 100 < 1000, then 1000 - 100 = 900
    
"""

# REMINDER: Dont forget to add checks for edge cases
def roman_to_integer(roman_number: str) -> int:
    roman_numbers_map = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }
    final_result = [] # this could be an int
    
    i = 0
    while i <= len(roman_number) - 1:
        print(f"Individual character: {roman_number[i]}")
        current_c = roman_number[i]
        next_c = None if i == len(roman_number) - 1 else roman_number[i + 1] 
        
        current_int = roman_numbers_map[current_c] # 5
        next_int = 0 if next_c is None else roman_numbers_map[next_c] # 0
        
        if current_int < next_int:
            # Swap and do substraction
            temp = next_int - current_int
            final_result.append(temp)
            i += 1
        else:
            final_result.append(current_int)
        i += 1
    
    print(final_result)
    # [500, 4, 5]
    return sum(final_result)    
test_input = "MCMXCIV" # 1994
res = roman_to_integer(test_input)
print(f"FINAL RESULT: {res}")