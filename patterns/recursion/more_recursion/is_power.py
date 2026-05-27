class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        # What is our base case?
        if n < 0: return False
    
        def recurse(number: int):
            if number == 0: return False
            if number == 1: return True
            if number % 2 != 0:
                return False
            
            # Recurse with a small portion
            return recurse(number // 2)
        
        result = recurse(n)
        return result
        
    def isPowerOfTwoCleaner(self, n: int) -> bool:
        # First, lets consider edge cases
        if n == 0: return False
        if n == 1: return True

        if n % 2 != 0: return False

        return self.isPowerOfTwoCleaner(n // 2)

solution = Solution()
res = solution.isPowerOfTwoCleaner(32)

print('Final res: ', res)


"""
    NOTES:
    - Input: A number, which represents the result of elevating 2 to the power of something
    - Outout: Boolean, which represents the outcome of checking if the number given is a result of elevating 2 to the power of something
    - Assumptions:
        n can be a really big negaitve number, or a really big positive number, its a 32bit integer (I think)

    - Brainstorm approach:
        We don't really care about what number exactly, we only care then the condition is met, IF we elevate to to the power of our CURRENT number and it equals n, then we return true, if not, we return false

        We cannot just start from zero and go to infinity, but we could maybe start from the current n, up until zero
"""

