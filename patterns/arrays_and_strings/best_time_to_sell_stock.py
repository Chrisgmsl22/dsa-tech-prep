class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        maxP = 0 # This could act as our default value 
        currStock = prices[0] # Start with a default value
        # [7, 1, 5, 3, 6, 4]
        #.       i 
        # curr = 1
        for i in range(1, n):
            currNum = prices[i]
            if currNum < currStock:
                # Swap curr stock, lower means we could potentially get a better value
                currStock = currNum
            else:
                # Dont swap, just store possible stock sold
                currProfit = currNum - currStock
                maxP = max(maxP, currProfit)
            # we should only sell when my next price is bigger than me
        return maxP


"""
    NOTES:
    - Input: An array of numbers, can contain zeros, and are not negatives
    - Output: A number, which represents the MAX profit we can achieve from buying and selling a stock on a later day

    We need to know what is the best profit we can make by buying and selling our stock.
    My first thought is that we need to generate all possible combinations, but the time our array grows, we'll hit TLE.

    We need to find a better approach.
    We care about the max profit, so we may not need to make all combinations.
    Instead, we need to consider the lowest prices first.
    If we run into 5 and immediately run into a smaller number, then its worth checking if we can switch.
    As for when to sell, we can always compute how much we would make if we sold at the next day and store it.
    Our current selection may change, but our max profix will still be the same.

    Now, this is an interesting problem because we need to find the pattern in which we can keep track of all operations.
    I still havent figured it out, but we can get started
"""