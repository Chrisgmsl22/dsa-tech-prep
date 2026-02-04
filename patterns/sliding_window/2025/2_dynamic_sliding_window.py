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

# Helper function to check when a window is  valid
def is_window_valid(current_window_map: dict, target_map: dict) -> bool:
    for char in target_map:
        if current_window_map.get(char, 0) < target_map[char]:
            return False
    return True


# "ADOBECODEBANC"
#  ADOBEC is the first occurence
def min_window_substring(s: str, target: str) -> str:
    # YOUR CODE HERE
    # Hint: Use HashMap to count characters, expand until valid, then shrink
    left = 0
    target_char_map = {}
    min_substring = ""
    for char in target:
        if char not in target_char_map:
            target_char_map[char] = 1
        else:
            target_char_map[char] += 1
        
    #print(target_char_map)
    
    # INCREASE to become valid
    window_map = {} # This will keep count of my current characters
    for right in range(len(s)):
        current_char = s[right]
        window_map[current_char] = 1 if current_char not in window_map else window_map[current_char] + 1

      
        if is_window_valid(window_map, target_char_map):
            # Then it means all characters from target are contained in window map
            current_minimum = s[left : right + 1]
            
            print('current minimum: ', current_minimum)
            if min_substring is None or len(current_minimum) < len(min_substring):
                min_substring = current_minimum
    
        #SHRINK until it valid
        while not is_window_valid(window_map, target_char_map):
            # Shrink by moving the left pointer a little bit to the right
            window_map[s[left]] -= 1
            if window_map[s[left]] == 0:
                del window_map[s[left]]

            left += 1
    
    #CHECK
    
    #UPDATE
    return min_substring
    
    
   
   
input = "ADOBECODEBANC"
t = "ABC"

res = min_window_substring(input, t)
print(f"Final result: {res}")