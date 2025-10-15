def length_of_longest_substring_optimized(s: str) -> int:
    """
    OPTIMIZED VERSION: Use HashMap to jump directly to the right position
    Instead of removing one by one, we jump left pointer directly!
    """
    print(f"String: '{s}'")
    print("=" * 50)
    
    char_index = {}    # Maps character -> its most recent index
    left = 0          # Left boundary of window
    max_length = 0    # Longest valid substring found so far
    
    for right in range(len(s)):
        current_char = s[right]
        print(f"\nStep {right + 1}: Processing s[{right}] = '{current_char}'")
        
        # Check if we've seen this character before AND it's in our current window
        if current_char in char_index and char_index[current_char] >= left:
            old_position = char_index[current_char]
            print(f"  ❌ Found duplicate! '{current_char}' was last seen at index {old_position}")
            print(f"  Current window: s[{left}:{right}] = '{s[left:right]}'")
            
            # JUMP: Move left pointer to just after the duplicate
            left = old_position + 1
            print(f"  🚀 JUMPING left pointer to {left} (right after the duplicate)")
            print(f"  New window starts at: s[{left}:{right}] = '{s[left:right]}'")
        else:
            if current_char in char_index:
                print(f"  '{current_char}' seen before at index {char_index[current_char]}, but outside current window")
            else:
                print(f"  ✅ '{current_char}' is new!")
        
        # Update the character's position
        char_index[current_char] = right
        
        # Calculate current window
        current_window = s[left:right+1]
        window_length = right - left + 1
        print(f"  Current window: '{current_window}' (length: {window_length})")
        
        # Update max length
        if window_length > max_length:
            max_length = window_length
            print(f"  🎉 New maximum length: {max_length}")
        
        print(f"  Character positions: {char_index}")
    
    print(f"\nFinal Answer: {max_length}")
    return max_length


test_input = "abcabc"
res = length_of_longest_substring_optimized(test_input)