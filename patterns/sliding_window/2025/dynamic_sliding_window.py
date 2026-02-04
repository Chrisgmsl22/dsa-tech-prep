def longest_subarray_sum_k_detailed(arr: list[int], target: int) -> int:
    """
        Find length of longest subarray with sum equal to target
    """
    print(f"Array: {arr}. Target: {target}")
    print("=" * 50)
    
    left=  0 # Left boundary of window
    current_sum = 0 # Sum of elements in current window
    max_length = 0 # Length of longest valid subarray found so far
    
    for right in range(len(arr)):
        print(f"\nStep {right + 1}: right pointer at index {right} (value: {arr[right]})")
        
        # EXPAND: Add current element to window
        current_sum += arr[right]
        print(f"  Added arr[{right}] = {arr[right]} to window")
        print(f"  Window now: arr[{left}:{right+1}] = {arr[left:right+1]}")
        print(f"  Current sum: {current_sum}")
    
    
        # SHRINK: Remove elements from left while sum > target
        print(f"  Checking if sum ({current_sum}) > target ({target})")
        while current_sum > target and left <= right:
            print(f"    Sum {current_sum} > target {target}, so shrinking window")
            print(f"    Removing arr[{left}] = {arr[left]} from window")
            current_sum -= arr[left]
            left += 1
            print(f"    New window: arr[{left}:{right+1}] = {arr[left:right+1]}")
            print(f"    New sum: {current_sum}")
            
        # CHECK: If current sum equals target, then update max_length
        print(f"Final window sum: {current_sum}")
        if current_sum == target:
            window_length = (right - left) + 1
            print(f"  ✓ Found valid subarray! Length = {right} - {left} + 1 = {window_length}")
            max_length = max(max_length, window_length)
            print(f"  Max length so far: {max_length}")
        else:
            print(f"  Sum {current_sum} ≠ target {target}, continue searching")
    
    print(f"\nFinal Answer: {max_length}")
    return max_length
    
input = [1, 2, 3, 1, 1, 1, 1] # t: 4 (so, while the current sum is larger than the target, then shrink it)
#                 l           
#                          r
# Current sum: 4
# Current max: 2 (currentMax = len(arr[l:r + 1]))
# is my current sum the same as the target? Then set it as my current max 
# Length of range: 5
# 5 - 1 = 4 + 1 = 5
# 5 + 1 - 1

t = 4

res = longest_subarray_sum_k_detailed(input, t)