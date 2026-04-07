"""
    The Fibonacci numbers, commonly denoted F(n) form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1. That is,

F(0) = 0, F(1) = 1
F(n) = F(n - 1) + F(n - 2), for n > 1.
Given n, calculate F(n).




"""


class Solution:
    def fib(self, n: int) -> int:
        # Lets add memoization
        cache = {}

        def recurse(num: int) -> int:
            if num <= 1:
                return num
            
            if num in cache:
                return cache[num]
            

            combination = recurse(num - 1) + recurse(num - 2)
            # else
            cache[num] = combination
            return cache[num]
            
        return recurse(n)




sol = Solution()

print("Result: ", sol.fib(2))

# fib 4
# fib 2 + fib 3
# fib 0 + fib 1 + fib 1 + fib 2
# fib 0 + fib + + fib 1 + fib 0 + fib 1
# 0 1 1 0 1 = 1 + 1 + 1 = 3