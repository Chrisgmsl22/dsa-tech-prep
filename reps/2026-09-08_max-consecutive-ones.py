class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        n = len(nums)
        maxConsec = float("-inf")
        l = 0
        flipsUsed = 0 # We can use 2
        # [1,1,1,0,0,0,1,1,1,1,0]
        #          l
        #            r
        # max: 4
        # flips: 2
        for r in range(n):
            if nums[r] == 0:
                # If zero has been found, use one from our stock
                flipsUsed += 1

            # Shrink condition
            while flipsUsed > k: 
                if nums[l] == 0:
                    # Not only are we going to shrink, we are also going to reduce the 0 we flipped
                    flipsUsed -= 1
                l += 1
            
            windowSize = (r - l) + 1
            maxConsec = max(maxConsec, windowSize)

        return maxConsec


"""
    NOTES:
    - Input: a binary array (only 1s and 0s), and an integer k
    - Output: a number, which represents the longest subarray that contains all 1s IF WE FLIF
    AT MOST K ZEROS, meaning we can treat k zeros as 1 and increase our window size.

    Our goal here is to construct the biggest subarray, and keep track of how long it is, ideally, at the end of our code we can simply return it
    since we are constructing a subarray, we can use a sliding window approach.

    Now, when we're told we can flip at most k zeros, most of the time we are not needed to flip them. So lets instead use them
    as a way to simply treat them as a zero, and keep growing our window

    Still need to define proper constrains for our sliding window, such as how to shrink our window or something along those lines.

"""