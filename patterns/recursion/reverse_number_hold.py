"""
    Problem 4: Reverse a Number

Given a number n, return its digits reversed.
Example: 1234 → 4321

Hint:

Base case → single digit number.

Recursive step → take last digit, recurse on the rest, and combine.


    1234
    
    4 + fn(123)
    3 + 4 + fn(12)
    2 + 3 + 4 + fn(1)
    1 + 2 + 3 + 4
    
    fn(123) + 4
    
"""
class Recursion:
    def reverseNum(self, num: int, starter = 0) -> int:
        # Identify base case
        if num < 10:
            return num # Because it is a single digit
            
        
        # Identify recursion case
        currentNumber = num % 10
        remainingNumbers = num // 10
        
        return starter * 10 + currentNumber + self.reverseNum(remainingNumbers)
    

inputData = 1234
solution = Recursion()

res = solution.reverseNum(inputData)
print(res)