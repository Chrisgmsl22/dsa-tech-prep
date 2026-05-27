"""
    You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

    Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

    You may assume that you have an infinite number of each kind of coin.
"""

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        coins.sort()
        # Top down DP
        memo = {0 : 0}
        
        def minCoins(x: int):
            if x in memo: return memo[x] # This is standard for memoization problems
            
            minn = float('inf')
            
            for coin in coins:
                diff = x - coin
                if diff < 0: # A negative number
                   break # Number will get more and more negative
                
                minn = min(minn, 1 + minCoins(diff))
            memo[x] = minn
            return memo[x]
        
        result = minCoins(amount)
        if result < float('inf'):
            return result
        else:
            return -1

problem = Solution()
testData = [1, 2, 5]
amount = 11

print(problem.coinChange(testData, amount))