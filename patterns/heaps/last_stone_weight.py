""""
    You are given an array of integers stones where stones[i] is the weight of the ith stone.

    We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:

    If x == y, both stones are destroyed, and
    If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.
    At the end of the game, there is at most one stone left.

    Return the weight of the last remaining stone. If there are no stones left, return 0.



"""
import heapq
class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        # Build a max heap using a min heap
        for i in range(len(stones)):
            stones[i] = -stones[i]
        heapq.heapify(stones)

        while len(stones) > 1:
            # Get 2 largest values
            firstLargest = -(heapq.heappop(stones))
            secondLargest = -(heapq.heappop(stones))

            if firstLargest != secondLargest:
                diff = firstLargest - secondLargest
                heapq.heappush(stones, -diff)
        
        if len(stones) == 1:
            return -(heapq.heappop(stones))
        else:
            return 0
    
sol = Solution()

inputData = [2,7,4,1,8,1]

res = sol.lastStoneWeight(inputData)
print("Final ans: ", res)