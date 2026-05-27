"""
    Given two positive integers a and b, find the largest positive integer that divides both numbers evenly (with no remainder).

    if b divides a EVENLY, then b is the great common divisor
    GCD(a, b) == GCD(b, a%2)
  
"""
class Solution:
    def gcd(self, a: int, b: int) -> int:
        # What is our base case?, when the remainder of the division betwneen a and b is zero
        # GCD(a, 0) == a
        if b == 0: return a
        if a % b == 0: return b

        return self.gcd(b, a % b)



problem = Solution()

print(problem.gcd(5, 0))







"""
      Example 1:
Input: a = 48, b = 18
Output: 6
Explanation: 
- Divisors of 48: 1, 2, 3, 4, 6, 8, 12, 16, 24, 48
- Divisors of 18: 1, 2, 3, 6, 9, 18
- Common divisors: 1, 2, 3, 6
- Greatest common divisor: 6

Example 2:
Input: a = 54, b = 24
Output: 6
Explanation: Both 54 and 24 are divisible by 6

Example 3:
Input: a = 17, b = 19
Output: 1
Explanation: Both are prime numbers, only common divisor is 1

Example 4:
Input: a = 100, b = 50
Output: 50
Explanation: 50 divides both 100 and 50

Example 5:
Input: a = 0, b = 5
Output: 5
Explanation: Any number divides 0, so GCD(0, n) = n

"""