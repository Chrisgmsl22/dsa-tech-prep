class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        result: list[list[int]] = []
        n = len(nums)

        # [-2,0,1,1,2]
        #  x
        #       p1
        #.        p2
        nums.sort()
         
        for i in range(n):
            if i > 0 and nums[i] == nums[i - 1]:
                continue # Remove duplicates 
            if nums[i] > 0: break
            
            p1, p2 = i + 1, n - 1

            while p1 < p2:
                x, y, z = nums[i], nums[p1], nums[p2]
                summ = x + y + z 
                if summ == 0: # If sum does match, we have a valid candidate
                    result.append([x, y, z])
                    p1 += 1
                    p2 -= 1
                    
                    while p1 < p2 and nums[p1] == nums[p1 - 1]: # Skip duplicates
                        p1 += 1
                    while p1 < p2 and nums[p2] == nums[p2 + 1]:
                        p2 -= 1
                elif summ > 0: # too big, shrink
                    p2 -= 1
                else: # too small, grow
                    p1 += 1
        return result
""""
    NOTES:
    - Input: an array of integers, can contain negatives and repeated values
    - Output: An array of triplets, where each triplet contain unique indices, as well as all possible triples
    whose sum result in 0, if there are no triplets who's sum 

    Goal: Find all possible triplets, there may be none, 1 or many.
    What is a tripler?, an array of numbers (not indices) whose sum equals 0
    We can repeat numbers, but we CANNOT repeat indices, that is the main rule

    Okay, seems like we can duplicate indices per triplet
    A triplet cannot contain repeated indices
    And the solution cannot contain repeated triplets: This means we need to ignore the same combination (1, 1, -2) is the same as (-2, 1, 1), so we pick one

    Okay, what do we need to do:
    We need to formulate a proper strategy, we could simply make all possible combinations, then filter out repeated nums
    However, that would break under higher test data

    Instead, lets divide and conquer.
    Let's assume we already have 1 number, and now we simply turn this into 2 sum

    how can we know our combination is unique?
    we can sort the numbers to form a unique combination
    So if we have a valid combination, but its sorted form is already recorded, then we ignore it 


    How can I add a hashMap to speed this up?

"""