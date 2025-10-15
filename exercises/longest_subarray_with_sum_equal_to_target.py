def longest_subarray(arr: list[int], target: int):
    """
        Find length of longest subarray with sum equal to target (use dynamic sliding window)
    """
    left = 0
    current_sum = 0
    max_window_size = 0
    
    # right pointer will always run, left pointer WILL ONLY RUN when a condition is not valid
    for right in range(len(arr)):
        current_number = arr[right]
        
        current_sum += current_number
        
        
        # Condition to shrink
        while current_sum > target and left <= right:
            current_left_pointer_value = arr[left]
            # Then shrink the window size
            current_sum -= current_left_pointer_value
            # Increase left pointer to keep going until condition is not met
            left += 1
        
        # Check if current sum equals the target
        if current_sum == target:
            # Then get the current window size
            window_size = len(arr[left : right + 1])
            
            #update the max value
            max_window_size = max(max_window_size, window_size) # Assign which ever is larger
    
    return max_window_size


input = [1, 2, 3, 1, 1, 1, 1]

res = longest_subarray(input, 5)


print(f"Final result: {res}")
        