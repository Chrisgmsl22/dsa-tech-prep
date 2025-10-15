# ========================================
# PROBLEM 1: EASY - Fixed Window
# ========================================
def problem_1():
    """
    Problem: Find the maximum average of any subarray of length k
    
    Example:
    nums = [1, 12, -5, -6, 50, 3], k = 4
    Answer: 12.75 (subarray [12, -5, -6, 50])
    
    Your task: Implement max_average_subarray(nums, k)
    """
    pass

def max_average_subarray(nums: list[int], k: int) -> float:
    # We will start at [1, 12, -5, -6] and then move our way up
    nums_sum = sum(nums[:k])
    max_average = nums_sum / k
    
    
    # [1, 12, -5, -6, 50, 3]
    #              2  51  42
    # 2 + 50 - 1 = 51
    #                  n + i - startValue
    #
    # We start from the very end of the length 4, up to whats left
    for i in range(k, len(nums)):
        #print("->", nums[i], i)
        # we need [12, -5, -6, 50] = sum = 51
        right_value = nums[i]
        left_value = nums[i - k]
        #print(f"Right: {right_value}, Left: {left_value}")
        nums_sum = nums_sum + right_value - left_value
        #print(f"check sum built: ${nums_sum}")
        current_average = nums_sum / k
        max_average = max(max_average, current_average)
    return max_average
    
    

    
    
nums = [1, 12, -5, -6, 50, 3] 
k = 4

res = max_average_subarray(nums, k)
print(f"FINAL RESULT: {res}")
