"""
    Given a number n, return the sum of its digits.
    Example: 1234 -> 1+2+3+4 = 10
"""

class RecursionClass:
    def sumDigits(self, n: int) -> int:
        # Identify base case (smallest possible value that can help us break the infinite loop)
        if n < 10:
            return n
        
        
        # Identify recursion
        lastDigit = n % 10
        allDigitsMinusLast = n // 10
        return lastDigit + self.sumDigits(allDigitsMinusLast)
        
    
        

inputData = 1234
solution = RecursionClass()
res = solution.sumDigits(inputData)

print(res)

print(f"test: {11 % 10}")