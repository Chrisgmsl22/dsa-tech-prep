"""
     Ejercicio: Duplicados en arreglo ordenado
    Elimina duplicados in-place de un arreglo ordenado, y devuelve la longitud del arreglo con los valores únicos al frente.

    Input:  nums = [1,1,2]
    Output: 2, nums se modifica a [1,2,_]

    Input: nums = [0,0,1,1,1,2,2,3,3,4]
    Output: 5, nums se modifica a [0,1,2,3,4,...]
    📌 Nota: No debes usar espacio adicional significativo (O(1) extra), y los elementos únicos deben estar al principio del arreglo.


"""
"""
    Notes:
    - SORTED array, it means we will know the order in which these will be
    - Might go for the two pointers approach
    - In-place means we do not create extra memory, but we work with the existing array
    - we need to iterate
    - this function needs to return a number, which represents the length of the filtered array
"""

class DuplicatesSolution:
    def __init__(self):
        pass
    
    def eliminateDuplicatesInPlace(self, nums: list[int]) -> int:
        left, right = 0, 0
        
        # [0,0,1,1,1,2,2,3,3,4]
        #    l
        #        r
        while right < len(nums):
            uniqueValSoFar = nums[left]
            
            if nums[right] != uniqueValSoFar: # Then we just move one place
                left += 1
                nums[left] = nums[right]
            
            right += 1
        return left + 1
            
    
    
solution = DuplicatesSolution()
inputData = [1,1,2]
inputData2 = [0,0,1,1,1,2,2,3,3,4]
res = solution.eliminateDuplicatesInPlace(inputData2)

print(res)