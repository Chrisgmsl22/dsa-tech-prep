# SLIDING WINDOW PRACTICE PROBLEMS
# Try to solve each one before looking at the solution!

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

# STATUS: SOLVED ✅
def max_average_subarray(nums, k):
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
            

# ========================================
# PROBLEM 2: MEDIUM - Variable Window
# ========================================
def problem_2():
    """
    Problem: Minimum Window Substring with all characters
    
    Find the smallest substring that contains ALL characters from a target string
    
    Example:
    s = "ADOBECODEBANC", target = "ABC"
    Answer: "BANC" (contains A, B, C)
    
    Your task: Implement min_window_substring(s, target)
    """
    pass

def min_window_substring(s, target):
    # YOUR CODE HERE
    # Hint: Use HashMap to count characters, expand until valid, then shrink
    pass

# ========================================
# PROBLEM 3: MEDIUM - Variable Window
# ========================================
def problem_3():
    """
    Problem: Longest Substring with At Most K Distinct Characters
    
    Example:
    s = "eceba", k = 2
    Answer: 3 (substring "ece")
    
    Your task: Implement longest_k_distinct(s, k)
    """
    pass

def longest_k_distinct(s, k):
    # YOUR CODE HERE
    # Hint: Use HashMap to count characters, shrink when > k distinct
    pass

# ========================================
# PROBLEM 4: MEDIUM - Variable Window
# ========================================
def problem_4():
    """
    Problem: Subarray Product Less Than K
    
    Count number of subarrays where product of all elements < k
    
    Example:
    nums = [10, 5, 2, 6], k = 100
    Answer: 8 
    Subarrays: [10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]
    
    Your task: Implement subarray_product_less_than_k(nums, k)
    """
    pass

def subarray_product_less_than_k(nums, k):
    # YOUR CODE HERE
    # Hint: When window is valid, ALL subarrays ending at right are valid
    pass

# ========================================
# PROBLEM 5: HARD - Variable Window
# ========================================
def problem_5():
    """
    Problem: Minimum Window Substring with Character Frequency
    
    Find shortest substring that contains ALL characters of target 
    with AT LEAST the same frequency
    
    Example:
    s = "ADOBECODEBANC", target = "AABC"
    Answer: "ADOBECODEBA" (contains 2 A's, 1 B, 1 C)
    
    Your task: Implement min_window_frequency(s, target)
    """
    pass

def min_window_frequency(s, target):
    # YOUR CODE HERE
    # Hint: Track required vs actual character counts
    pass

# ========================================
# PROBLEM 6: MEDIUM - Binary (0s and 1s)
# ========================================
def problem_6():
    """
    Problem: Max Consecutive Ones III
    
    Find length of longest subarray of 1s after flipping at most k zeros
    
    Example:
    nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
    Answer: 6 (flip the two zeros: [0,0,0,1,1,1,1,0] -> [1,1,1,1,1,1])
    
    Your task: Implement longest_ones_with_k_flips(nums, k)
    """
    pass

def longest_ones_with_k_flips(nums, k):
    # YOUR CODE HERE
    # Hint: Count zeros in window, shrink when zeros > k
    pass

# ========================================
# PROBLEM 7: EASY - Character Replacement
# ========================================
def problem_7():
    """
    Problem: Longest Repeating Character Replacement
    
    Find length of longest substring with same character after 
    replacing at most k characters
    
    Example:
    s = "ABAB", k = 2
    Answer: 4 (replace both B's with A's: "AAAA")
    
    Your task: Implement character_replacement(s, k)
    """
    pass

def character_replacement(s, k):
    # YOUR CODE HERE
    # Hint: Track most frequent char, others need to be replaced
    pass

# ========================================
# SOLUTIONS (Don't peek until you try!)
# ========================================

def solution_1_max_average(nums, k):
    """Solution for Problem 1"""
    if len(nums) < k:
        return 0
    
    # Calculate first window sum
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i-k] + nums[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum / k

def solution_2_min_window(s, target):
    """Solution for Problem 2"""
    if not s or not target:
        return ""
    
    # Count characters needed
    target_count = {}
    for char in target:
        target_count[char] = target_count.get(char, 0) + 1
    
    left = 0
    formed = 0  # Number of unique chars in window with desired frequency
    required = len(target_count)
    
    window_counts = {}
    min_len = float('inf')
    min_window = ""
    
    for right in range(len(s)):
        # Add character from right
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if frequency matches
        if char in target_count and window_counts[char] == target_count[char]:
            formed += 1
        
        # Try to shrink until not valid
        while left <= right and formed == required:
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_window = s[left:right + 1]
            
            # Remove from left
            char = s[left]
            window_counts[char] -= 1
            if char in target_count and window_counts[char] < target_count[char]:
                formed -= 1
            left += 1
    
    return min_window

def solution_3_k_distinct(s, k):
    """Solution for Problem 3"""
    if k == 0:
        return 0
    
    left = 0
    char_count = {}
    max_length = 0
    
    for right in range(len(s)):
        # Add character
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink if too many distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

def solution_4_product_less_than_k(nums, k):
    """Solution for Problem 4"""
    if k <= 1:
        return 0
    
    left = 0
    product = 1
    count = 0
    
    for right in range(len(nums)):
        product *= nums[right]
        
        # Shrink window while product >= k
        while product >= k:
            product //= nums[left]
            left += 1
        
        # All subarrays ending at right are valid
        count += right - left + 1
    
    return count

# Test functions
def run_tests():
    """Test all solutions"""
    print("Testing Solutions:")
    print("=" * 50)
    
    # Test 1
    result1 = solution_1_max_average([1,12,-5,-6,50,3], 4)
    print(f"Problem 1: {result1} (expected: 12.75)")
    
    # Test 2
    result2 = solution_2_min_window("ADOBECODEBANC", "ABC")
    print(f"Problem 2: '{result2}' (expected: 'BANC')")
    
    # Test 3
    result3 = solution_3_k_distinct("eceba", 2)
    print(f"Problem 3: {result3} (expected: 3)")
    
    # Test 4
    result4 = solution_4_product_less_than_k([10,5,2,6], 100)
    print(f"Problem 4: {result4} (expected: 8)")

if __name__ == "__main__":
    print("SLIDING WINDOW PRACTICE PROBLEMS")
    print("=" * 50)
    print("Try to solve each problem before looking at solutions!")
    print("Problems are ordered from easy to hard.")
    print("\nRun run_tests() to see expected outputs.")
    print("\nHints for each problem are in the docstrings.")
    
    run_tests()