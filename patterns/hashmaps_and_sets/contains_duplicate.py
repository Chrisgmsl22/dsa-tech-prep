class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        numsMap: dict[int, int] = {}

        for n in nums:
            #print(n, numsMap, numsMap[n])
            numsMap[n] = numsMap.get(n, 0) + 1
            
            if numsMap[n] > 1:
                return True
        
        return False
    def containsDuplicate2(self, nums: list[int]) -> bool:
        return len(nums) != len(set(nums))


""""
    NOTES:
    - Input: an integer array nums
    - Output: A boolean value indicating if the collection contains a duplicate number

    Keep in mind that our nums array can contain 1 value and up to 10^5 (see if performance is affected)

    How would I approach:
        We need to know either the frequency of the elements (using a frequency count)
        Or we can use a different data structure called sets. Which in theirn nature they do not contain duplicates

        So we can iterate over the whole collection and create a frequency count
        THen iterate over this hashMap and see if at least one value is > 1, then return true, otherwise continue
        and in the end return false

"""

sol = Solution()

print(sol.containsDuplicate2([1, 2, 3, 1]))