"""
    Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-231, 231 - 1], then return 0.

    Assume the environment does not allow you to store 64-bit integers (signed or unsigned).

    

    Example 1:

    Input: x = 123
    Output: 321
    Example 2:

    Input: x = -123
    Output: -321
    Example 3:

    Input: x = 120
    Output: 21
    
"""

"""
    Brainstorm:
        - unsigned int is always positive
        - signed can be either + or -
        - Reverse this number (the main goal)
        - How can I do this? can I turn the number into a string, then reverse it?
        - Can I turn the number into an array of individual numbers, then reverse the array?
        - How does the negative value takes place? (what differences does this cause).
        - This function takes in a number, and returns a number
        - Do I need iterations? (if so, what kind)
    
"""

"""
    human english pseudo code
    define function{

    }
"""
# REMINDER: DONT FORGET TO ADD CHECKS FOR EDGE CASES
def reverse_int(number: int) -> int:
    is_negative = number < 0
    number = abs(number)
    
    n = str(number)
    reversed_n = n[ : : -1]
    print(f"n: {n, type(n)}")

    return int(reversed_n) if not is_negative else -int(reversed_n)


test_input = 123
test_input_two = -123

res = reverse_int(test_input)
print(f"FINAL RESULTL {res}")