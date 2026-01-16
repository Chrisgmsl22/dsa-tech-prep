class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        sortedNums = sorted(nums)# Get the numbers in the correct order first
        n = len(nums)
        allPermutations, currPermutation = [], []
        def backtrack():
            # What is going to be our base case?
            if len(currPermutation) == n:
                allPermutations.append(currPermutation[ : ])
                return # Stop current recursive call
            
            for num in sortedNums:
                if num not in currPermutation:
                    # If we have not used it before
                    currPermutation.append(num)
                    backtrack()
                    currPermutation.pop()
        
        backtrack()
        #print(allPermutations, len(allPermutations))
        # I can go over the permutations array to try to find my target
        print(f"nums before: {nums}")
        target = []
        for i in range(len(allPermutations)):
            print(i, allPermutations[i])
            if nums == allPermutations[i]:
                if i == len(allPermutations) - 1: # Then we go back to the first one
                    target = allPermutations[0][:]
                    break
                else:
                    target = allPermutations[i + 1][:]
                    break
        print(f"target: {target}")
        for i in range(len(nums)):
            nums[i] = target[i]
        print(f"nums after: {nums}")
        
        



problem = Solution()
print(problem.nextPermutation([1, 2, 3]))




"""
    Notes:
    - input: an array of numbers (can be unsorted, can contain duplicates)
    - output: NONE, the idea is to generate all permutations first. then find the correct order for all permutations. Find current number combination, and return the next permutation.
        Since we cannot return anything, we need to modify nums instead. I am thinkint on finding my next permutation and just replace it with =
    
"""
