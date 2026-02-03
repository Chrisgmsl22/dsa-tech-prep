class Solution:
    def search(self, nums: list[int], target: int) -> int:
        n = len(nums)
        left = 0
        right = n - 1

        while left <= right: # While these 2 pointers do not meet, iterate
            m = (left + right) // 2
            val = nums[m]

            if val == target:
                return m
            if val > target:
                right = m - 1
            if val < target:
                left = m + 1
        
        return -1

sol = Solution()

nums = [-1, 10, 22, 35, 100]
t = 100

res = sol.search(nums, t)
print(res)
        


"""
    NOTES:
    This is an essential algorithm for DSA.
    The point of this is to use a collection of data (or a given range)
    with SORTED values.
    We define 2 pointers, LEFT and RIGHT, where left points at the very start of 
    the collection and right points at the end of the collection

    Once we know our ranges, we find our middle (by adding L and R and dividing it into 
    2)

    Of the value is exaxtly there, return the current index.
    If not:
        If our current number is way to big, we need to reduce (right --)
        If our current number is way to small, we need to increase (left ++)
    
    we iterate until we either find the result
    If no result is found by the time l and r meet, we return -1 indicating that no number was found

"""