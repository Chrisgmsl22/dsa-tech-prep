"""
    Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

    The overall run time complexity should be O(log (m+n)).

    

    Example 1:

    Input: nums1 = [1,3], nums2 = [2]
    Output: 2.00000
    Explanation: merged array = [1,2,3] and median is 2.
    Example 2:

    Input: nums1 = [1,2], nums2 = [3,4]
    Output: 2.50000
    Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

"""

"""
    Brainstorm: Median is the middle value of a sorted list of numbers, IF the array size is even, then its the sum of the 2 middle ones divided by 2
    - Need to calculate the median
    - the two arrays are already sorted
    - Need to merge the arrays (and keep the order)
    - Result might be an integer or a float, so it should be float just in case
    - Will we need to iterate over the collection? (for / while loops)
"""

"""
    Plain english
    array1, array2 = param1, param2
    merged_array = array1 + array2
    sort(merged_array)
    result = 0
    
    #check the size of the merged array (is it even or odd)
    if merged array size is odd
        then middle one can be its length divided by 2
        result = middle one
    if merged array size is even
        then middle one will consist of two values (don't know yet how to obtain this)
        result = (middle1 + middle2) / 2
        
    return result
    
"""
def merge_two_sorted_arrays(arr1: list[int], arr2: list[int]) -> list[int]:
    merged_array = []
    
    while (len(arr1) != 0 or len(arr2) != 0):
        if len(arr1) == 0 and len(arr2) > 0:
            merged_array = merged_array + arr2
            break
        if len(arr1) > 0 and len(arr2) == 0:
            merged_array = merged_array + arr1
            break
        
        if arr1[0] < arr2[0]:
            merged_array.append(arr1[0])
            arr1.remove(arr1[0])
        else:
            merged_array.append(arr2[0])
            arr2.remove(arr2[0])
        
        
    return merged_array
a_1 = [4]
a_2 = [7, 9]
print(f"Calling function: {merge_two_sorted_arrays(a_1, a_2)}") # [1, 2, 3, 5, 6]


def calculate_median_of_two_sorted_arrays(arr1: list[int], arr2: list[int]) -> float:
    merged_array = merge_two_sorted_arrays(arr1, arr2)
    merged_array_length = len(merged_array)
    result = 0
   
    is_merged_array_even = True if merged_array_length % 2 == 0 else False

    if is_merged_array_even:
        right_index = merged_array_length // 2
        right_side = merged_array[right_index]
        left_side = merged_array[right_index - 1]
        result = float((left_side + right_side) / 2)
    else:
        middle_index = merged_array_length // 2
        result = float(merged_array[middle_index])
    
    return result
    

test_input1 = [1,3]
test_input2 = [2]

first_arr = [1, 2]
second_arr = [3, 4]

res = calculate_median_of_two_sorted_arrays(first_arr, second_arr)
#print(f"FINAL RESULT: {res}")


test = [1, 2, 3, 4, 5, 6] # Median is (3 + 4) / 2
test_two = [1, 2, 3, 4] # Median is then (2 + 3) / 2
test_three = [1, 2] # Median is then (1 + 2) / 2
"""
    6 / 2 = 3 -> index
    So, right_side = test[3] -> 4
    what if  left_side = test[3 - 1] -> 3
    return float(left_side + right_side) / 2
"""
middle = len(test) // 2
#print(middle, test[middle])