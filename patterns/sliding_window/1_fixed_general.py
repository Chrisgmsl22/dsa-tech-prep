def max_average_subarray(nums: list[int], k: int) -> float:
    left = 0
    window_sum = 0
    max_average = float('-inf')
    
    
    # [1, 12, -5, -6, 50, 3] 
    #  l          r
    #  0           3
    for right in range(len(nums)):
        # Expand window
        window_sum += nums[right]
        
        # Check when window size matches the given k size
        print(right, left, right - left + 1)
        if (right + 1) - left == k:
            print("Window sum: ", window_sum)
            current_average = window_sum / k
            max_average = max(max_average, current_average)
            
            # Move left one position to the right
            window_sum -= nums[left] # We need to remove its left element because we will build a new window with the same size, so it does not need this left value anymore
            left += 1
            
    return max_average
            
            
            
nums = [1, 12, -5, -6, 50, 3] 
k = 4

res = max_average_subarray(nums, k)
# print(f"FINAL RESULT: {res}")