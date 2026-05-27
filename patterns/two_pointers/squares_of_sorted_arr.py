class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [0] * n
        
        left = 0
        right = n - 1
        i = right # This will act as our point of reference for inserting values
        #  16 and 100
        # [ -4, -1, 0, 3, 10]
        #.   l 
        #           r
        # res = [0, 1, 9, 16, 100]
        while left <= right: # < or <= ???
            if abs(nums[left]) < abs(nums[right]):
                # Then insert right
                res[i] = nums[right] ** 2
                right -= 1
            else:
                # Then insert left
                res[i] = nums[left] ** 2
                left += 1
            
            i -= 1
        
        return res 

sol = Solution()

print(sol.sortedSquares([-4,-1,0,3,10]))

"""
    NOTES:
    - Input: an integer array (which can contain duplicates)
    - Output: an integer array which contains each element in the array squared and also sorted
    in ascending order

        Lets keep in mind that the array given has at least one value
        And that the value of each element can also be very big
    
    Brainstorm.
        First thing I can think of is to go over the entire array, square the current element
        then sort the entire array. But the problem does not really want this

        Something important to note is that the array we're given is already sorted.
        We need to calculate the square of each number and also return it in an increasing order

        We can use a two pointer approach, this way it will serve as a way to know if our current number is greater than the number at the very end.

        This will require to be constantly comparing each sides, if left is bigger, then assign it there, if right is bigger, move bigger. Something like that.

        Once we finish the whole iteration, then technically we would be done

"""