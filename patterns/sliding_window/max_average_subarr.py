class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        n = len(nums)
        left = 0
        maxx = float("-inf")
        currSum = 0
        # nums = [1, 12, -5, -6, 50, 3], k = 4
        #            l
        #                        r
        for right in range(n): # Right will increase no matter what
            windowSize = (right - left) + 1
            currSum += nums[right]

            if windowSize < k: 
                continue
            elif windowSize > k:
                currSum -= nums[left]
                left += 1

            avg = currSum / k
            maxx = max(maxx, avg)
            
        return maxx
            
                
    def findMaxAverage2(self, nums: list[int], k: int) -> float:
        res = float('-inf')
        left = 0
        currSum = 0

        # We start our window
        for right in range(len(nums)):
            # Build up your sum
            currSum += nums[right]
            windowSize = (right - left) + 1

            if windowSize == k:
                currAvg = currSum / k
                res = max(res, currAvg)

                # Since our window's fixed size is K, when we reach k size, it will become
                # In our next iteration, so we need to subtract the leftmost value
                currSum -= nums[left]
                left += 1
            
        return res
    
    def findMaxOptimal(self, nums: list[int], k: int) -> float:
        currSum = sum(nums[ : k])
        maxSum = currSum

        for i in range(k, len(nums)):
            currentNumber = nums[i]
            leftmostNumber = nums[i - k]
            currSum = currSum - leftmostNumber + currentNumber 

            maxSum = max(maxSum, currSum)
            
        
        return maxSum / k
            

sol = Solution()
inp = [1,12,-5,-6,50,3]
k = 4

res = sol.findMaxOptimal(inp, k)
print(res)
        

"""
    NOTES:
    - Input: An array of numbers (may contain negatives), and a target k
    - Output: A float value, which represents the MAXIMUM possible average from a subarray who's length is EQUAL to k

    So, this means we need to build contiguous subarrays (elements need to be together).
    Once we reach a length of K, we calculate the average and update a maxx variable.
    Since we can have different subarrays, it is important to adjust the maxx

    By the time we are done with the iterations, we then return our maxx val

    How?, this does seems like a sliding window problem. Where we form our window using
    left and right pointers, and we adjust it as we go.

"""