def length_of_longest_substring_detailed(s: str) -> int:
    """
    Find longest substring without repeating characters
    WITH STEP-BY-STEP EXPLANATION
    """
    print(f"String: '{s}'")
    print("=" * 50)
    
    
    char_set = set()
    left = 0 # Left boundary of my window
    max_length = 0 # Longest valid substring found so far
    
    for right in range(len(s)):
        current_char = s[right]
        char_set.add(current_char)
        print(f"\nStep {right + 1}: Processing s[{right}] = '{current_char}'")
        print(f"  Current window: s[{left}:{right}] = '{s[left:right]}'")
        print(f"  Characters in set: {sorted(char_set)}")
        
        # CHECK: if current character creates a duplicate
        if current_char in char_set:
            print(f"  ❌ '{current_char}' is already in our window! We have a duplicate!")
            print(f"  We need to shrink window from left until '{current_char}' is removed")
        else:
            print(f"  ✅ '{current_char}' is new, no duplicate yet")

        # SHRINK: Remove characters from left until no duplicate
        while current_char in char_set:
            char_being_removed = s[left]
            print(f"    Removing s[{left}] = '{char_being_removed}' from window and set")
            char_set.remove(char_being_removed)
            left += 1
            
            print(f"    New window start: left = {left}")
            print(f"    Characters in set now: {sorted(char_set)}")
            
            # Check if we still have the duplicate
            if current_char in char_set:
                print(f"    '{current_char}' still in set, continue removing...")
            else:
                print(f"    ✅ '{current_char}' no longer in set, we can add it!")
                
        # ADD: Add current character to set
        #char_set.add(current_char)
        current_window = s[left:right + 1]
        window_length = (right - left) + 1
        
        print(f"  Added '{current_char}' to set")
        print(f"  Current valid window: '{current_window}' (length: {window_length})")
        
        # UPDATE: Check if this is the longest window so far
        if window_length > max_length:
            max_length = window_length
            print(f"  🎉 New maximum length: {max_length}")
        else:
            print(f"  Max length remains: {max_length}")
        
    
test_input = "abcabc"
res = length_of_longest_substring_detailed(test_input)






def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.
    """
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        current_char = s[right]
        char_set.add(current_char)
        
        while current_char in char_set:
            char_set.remove(s[left])
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
test_input = "abcabc"
res = length_of_longest_substring(test_input)
print(res)