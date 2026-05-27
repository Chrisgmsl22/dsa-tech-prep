"""
    4. Count Digits (Easy)
Problem: Count number of digits in a number
Example: count_digits(12345) = 5
Think:

Base case: Number is 0
Recursive: 1 + count_digits(n // 10)
"""


def countDigits(number: int) -> int:
    # Always start with the base case
    number = abs(number)
    if number < 10: # So if its one digit, then return 1
        return 1
    # 12345
    
    remainingDigits = number // 10 # 1234
    
    operation = 1 + countDigits(remainingDigits)
    print(operation)
    return operation


print(countDigits(12345)) # Expected: 5
# 5 + (1234)
# 4 + 5 + (123)
# 3 + 4 + 5 + (12)
# 2 + 3 + 4 + 5 + 1