class Solution:
    def fib(self, n: int) -> int:
        memo = {}
        
        def helper(x):
            if x <= 1:
                return x
            
            # If we already computed fib(x), then return it
            if x in memo: return memo[x]
            
            # Otherwise, compute and store it
            memo[x] = helper(x - 1) + helper(x - 2)
            return memo[x]
        
        return helper(n)