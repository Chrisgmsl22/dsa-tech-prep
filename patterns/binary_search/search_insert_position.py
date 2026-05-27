class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        pos = 0
        while left <= right:
            m = (left + right) // 2
            val = nums[m]

            if val == target: # if our target is already in array, then return index
                return m
            if val > target:
                right = m - 1
            if val < target:
                left = m + 1
            print("pos: ", pos)
        print("Final pos: ", pos)         
        return left
        # [1, 3, 5, 6], t = 2
        #.    l.       
        #. r  

sol = Solution()
inp = [1, 3, 5, 6]
t = 2

res = sol.searchInsert(inp, t)
print(res)
"""
    NOTES:
    - Input: an array of unique numbers sorted in ascending order, and a target
    - Output: A number, which represents the index where we would place the value if
    we were inserting it in order

    This means that if our array already contains the value, we just return its index
    If our number is not found, then this is where the challenge happens

    We can define a binary search approach.
    We start from a given range of data
    But we also need to track our possible best guess for the location in which we should return our object
    if our current number is less than the target found, we store this as a possible value

"""