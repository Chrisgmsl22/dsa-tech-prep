class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        n = len(nums)
        L, R = 0, n - 1

        # Typical binary search
        # [1, 3, 5, 6]
        #  
        while L <= R:
            M = (R + L) // 2 # Confirm this is correct 
            candidate = nums[M]

            if candidate == target:
                return M
            elif candidate > target:
                R = M - 1
            else:
                L = M + 1
        
        #
        return L


"""
    NOTES:
    - Input: A sorted array of numbers, and a target 5
    - Output: Number, which represents the index of the current target number in the array
    Note: If no number was found in array, we should return the index of the position where it should be

    Okay, this is definitely a binary search problem, since the array is already sorted, we need to perform 
    our search on both ends, and keep iterating,

    Best case scenario: We find out number, we return the currnent index
    Worst case scenario: Number is not found, so we return the index of where it is supposed to be
    Still need to figure out how to work this one our, but I feel like we can reuse our pointers
    
    Our pointers are going to tell us when the closest answer was found, maybe we could do some math there

"""