"""
    Dado un arreglo ordenado de enteros numbers y un objetivo target, encuentra dos números cuya suma sea igual al target y devuelve sus índices (1-based).

    
    Input: numbers = [2,7,11,15], target = 9  
    Output: [1,2]  # 2 + 7 = 9
"""

class Solution:
    def __init__(self):
        pass
    
    def twoSum2(self, numbers: list[int], target: int) -> list[int]:
        leftPointer: int = 0
        rightPointer: int = len(numbers) - 1
        # Keep in mind this is a SORTED array, so all elements on the right, will be greater than the ones on the left
        # [2,7,11,15]
        #  l      r
        
        while leftPointer <= rightPointer:
            leftNumber = numbers[leftPointer]
            rightNumber = numbers[rightPointer]
            #print(leftNumber, rightNumber)
            possibleSum = leftNumber + rightNumber
            if possibleSum == target:
                return [leftPointer + 1, rightPointer + 1]
            
            if possibleSum > target:
                # Then our  value is too big, we need to shrink
                rightPointer -= 1
            else:
                # Then our value is too small, we need to increase
                leftPointer += 1
                
    def hasPairWithSum(self, arr: list[int], target: int) -> bool:
        left, right = 0, len(arr) - 1
        
        while left < right:
            possibleSum = arr[left] + arr[right]
            
            if possibleSum == target: return True
            
            if possibleSum > target: right -= 1
            
            if possibleSum < target: left += 1
            
        return False
            
        
        


solution = Solution()
inputData = [2,7,11,15]
target = 9

res = solution.twoSum2(inputData, target)
res2 = solution.hasPairWithSum(inputData, target)
print(res2)