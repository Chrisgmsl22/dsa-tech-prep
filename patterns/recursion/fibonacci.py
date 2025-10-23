"""
    Phase 2: Recursion with Multiple Branches
    These problems have the yoyo split into multiple yoyos going down!
    6. Fibonacci (You've Done This!)
"""
# 0, 1, 1, 2, 3, 5, 8, 13, 21
def fibonacci(n: int ) -> int:
    # always start with the base case
    memo = {}
    
    
    def dp_helper(i):
        if i < 2: return i
        if i in memo: return memo[i]
    
        operation = dp_helper(i - 2) + dp_helper(i - 1)
        memo[i] = operation
        return memo[i]
    
    
    return dp_helper(n)

def fibonacciTab(n: int) -> int:
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    for i in range(2, n + 1):
        currentVal = dp[i - 1] + dp[i - 2]
        dp[i] = currentVal
    print(dp)
    return dp[n]
    


print(fibonacciTab(5))