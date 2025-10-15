"""
    Given an array of positive integers and a number S, find the length of the smallest contiguous subarray whoce sum is greater than or equal to S. Return 0 if no such array exists
"""


def min_subarray_len(s: int, arr: list[int]) -> int:
    left = 0 # This will represent out left pointer, which will move to the right, when a condition is violated
    window_sum = 0
    min_length = float('inf')
    
    for right in range(len(arr)):
        current_number = arr[right]
        window_sum += current_number
        
        # When do we need to shrink? when we exceed the target amount
        while window_sum >= s:
            current_window = (right - left) + 1
            min_length = min(min_length, current_window)
            window_sum -= arr[left]
            left += 1
            
            
    final_res = min_length if min_length != float('inf') else 0
    return final_res
        
input_data = [2, 1, 5, 2, 3, 2]
s = 7
res = min_subarray_len(s=s, arr=input_data)
# Output should be 2 ([5,2])
print(f"Final result: {res}")