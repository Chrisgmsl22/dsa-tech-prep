"""
Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers index1 and index2, each incremented by one, as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not use the same element twice.

Your solution must use only constant extra space.

 

Example 1:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
Example 2:

Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
Example 3:

Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

"""
class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        L, R = 0, len(numbers) - 1
        # Numbers is already sorted, if not, we could even sort it here
        # 2, 7, 11, 15
        # L
        #           R
        while L <= R: # As long as these 2 are separated, iterate
            leftmostNum = numbers[L]
            rightmostNum = numbers[R] # See if this works or if I should operate directly at numbers
            summ = leftmostNum + rightmostNum

            print(summ, L, R)
            # 1st case: sum is less than: GROW
            if summ < target:
                L += 1
            if summ > target: # SHRINK
                R -= 1
            if summ == target: # We found our answer
                return [L + 1, R + 1]


sol = Solution()

numbers = [3,24,50,79,88,150,345]
target = 200

res = sol.twoSum(numbers, target)

print(res)


""""
    NOTES:
    - Input: an array of numbers and an integer target
    - Output: An array of numbers, which represent the 1-indexes numbers that in the given array represent two numbers
    that add up to the target t.
    - Assumptions: There is always an answer (no -1 for invalid), index1 has to be smaller than index2. Our result array 
    is always going to have length of 2. There's only 1 answer?. For our answer we need to add the indices in the array added by 1

    initial approach:
        We are given a SORTED (asc) array of numbers, this is going to be useful for nagivating through the array.
        Since we are guaranteed to already have an answer, we need to navigate through the array
        Brute force: O(n squared) get all combinations, return the one that works?
        We can use a two pointer approach, we start from L and R and we shrink as we go.

        Ideally we need to check if our current combination is greater than the sum? shrink
            Is our current combination less than T? grow
        
        once we find the exact sum, we append L and R to the array, add 1 to their indices and stop iterating

"""