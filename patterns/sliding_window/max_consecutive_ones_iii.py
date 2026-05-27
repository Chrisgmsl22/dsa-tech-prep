class Solution:
    def longestOnes(self, nums: list[int], k: int) -> int:
        maxRes = 0
        left = 0
        zerosInCurrWindow = 0

        # [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1] => k = 3
        #.         l
        #.                         r 
        #  zeros in window = 4
        # We build our sliding window
        for right in range(len(nums)):
            currentNumber = nums[right]
            #print("Current window size", windowSize, zerosInCurrWindow, maxRes)
            if currentNumber == 0: # See if you can flip
                zerosInCurrWindow += 1

            while zerosInCurrWindow > k:
                leftmostVal = nums[left]
                print('leftmostval', leftmostVal)
                if leftmostVal == 0:
                    zerosInCurrWindow -= 1
                left += 1

            windowSize = (right - left) + 1
            print("Current window size: ", maxRes, windowSize)
            maxRes = max(maxRes, windowSize)

        return maxRes

# Useful tip: My current window can contain at most k zeros
sol = Solution()
inp = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1]
k = 3

res = sol.longestOnes(inp, k)
print(res)
"""
    NOTES:
    - Input: an array of binary numbers (1s and 0s), and an integer k, which represent the amount of times
    we can flip a 0 to make it become a 1
    
    - Output: we return the length of the subarray that contains the most amount of 1s, after we fliped 0s 
    k amount of times at max

    This looks like a sliding window problem. For this we need to define a window size, which will be 
    dynamic. Our goal is to find the longest subarray (aka, longest window, keep track of it and return it).

    While we build our window we need to make sure our numbers are contiguous 1s. IF we find a zero
    We flip it (we can increase a counter or something like that), but if we run out of flip attempts
    then we can shrink the window size until we: Have a subarray with only 1s, and we have used less than
    or equal the amount of k zeros.

"""