"""
    Problem 2: Power Function

Implement pow(x, n) that returns x^n.
Example: pow(2, 3) → 8

Hint:

Base case → anything to the power 0 is 1.

Recursive step → reduce n each time.

Bonus: Can you optimize it using n//2 (divide and conquer style recursion)?
"""
class Recursion:
    def powerTo(self, base, exp) -> int:
        # Identity base case
        # 2^3 ==> 2 * 2 * 2
        if exp == 0:
            return 1 # Any number to the power of 0 is 1
        elif exp == 1:
            return base # Any number to the power of 1 is the same number
        
        # Identify recursion case
        return base * self.powerTo(base, exp - 1)
    
solution = Recursion()

print(solution.powerTo(2, 3))