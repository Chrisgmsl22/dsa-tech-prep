from collections import Counter

def is_window_valid(window_map: dict, target_map: dict) -> bool:
    for char in target_map:
        if window_map.get(char, 0) < target_map[char]:
            return False
    return True

def min_window_substring(s: str, target: str) -> str:
    if not s or not target:
        return ""
    
    target_char_map = Counter(target)
    window_map = {}
    
    left = 0
    min_substring = None
    
    for right in range(len(s)):
        current_char = s[right]
        window_map[current_char] = window_map.get(current_char, 0) + 1

        # Try to shrink the window from the left while it's still valid
        while is_window_valid(window_map, target_char_map):
            current_window = s[left:right+1]
            
            # Update the result if it's the smallest so far
            if min_substring is None or len(current_window) < len(min_substring):
                min_substring = current_window
            
            # Shrink the window from the left
            left_char = s[left]
            window_map[left_char] -= 1
            if window_map[left_char] == 0:
                del window_map[left_char]
            left += 1
    
    return min_substring if min_substring is not None else ""



   
input = "ADOBECODEBANC"
t = "ABC"

res = min_window_substring(input, t)
print(f"Final result: {res}")