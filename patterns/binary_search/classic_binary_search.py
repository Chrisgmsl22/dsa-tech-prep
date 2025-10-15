class BinarySearch:
    def binarySearch(self, nums, target):
        left, right = 0, len(nums) - 1
        
        while left <= right:
            # Get middle value
            middle = (left + right) // 2
            
            if nums[middle] == target:
                return middle # Keep in mind this is an index, not an actual value
            elif nums[middle] < target:
                left = middle + 1 # Everything on the left is useless for our search, so we advance our pointers the whole way
            else: # it is greater than the target, we decrease right
                right = middle - 1
                
        return -1
    
    
nums = [1, 3, 5, 6, 7, 8, 11, 20] # T = 3
#       l
#          m   
#             r
target = 3 # index 5

pattern = BinarySearch()
res = pattern.binarySearch(nums, target)
print(res)