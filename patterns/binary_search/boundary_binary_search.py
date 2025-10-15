class NewPattern:
    def findFirstOcurrence(self, nums, target):
        left = 0
        right = len(nums) - 1
        
        first = -1
        while left <= right:
            middleIndex = (right + left) // 2
            print('middle index on current iteration: ', middleIndex, left, right)
            # first occurence
            # [1, 2, 2, 2, 3 ,4]
            #.    l
            #.    m      
            #     r
            if nums[middleIndex] == target:
                first = middleIndex # For now, this is technically the first occurence
                right = middleIndex - 1
            elif nums[middleIndex] < target:
                left = middleIndex + 1
            else:
                right = middleIndex - 1
        
        return first

    def findLastOcurrence(self, nums, target):
        left = 0
        right = len(nums) - 1
        lastOcurrence = -1
        
        while left <= right:
            midIndex = (left + right) // 2
            
            if nums[midIndex] == target:
                # Update last occurence
                lastOcurrence = midIndex
                # Force the search to happen on the right (there might be another occurence, or not)
                left = midIndex + 1
            elif nums[midIndex] < target:
                left = midIndex + 1
            else:
                right = midIndex - 1
        
        return lastOcurrence
        

testData = [1, 2, 2, 2, 3, 4]
target = 2 # Expected outcome: 1 (index 1)

solution = NewPattern()
res = solution.findFirstOcurrence(testData, target)
resLast = solution.findLastOcurrence(testData, target)
print(f"target: {target}, ans: {res}")
print('last: ', resLast)