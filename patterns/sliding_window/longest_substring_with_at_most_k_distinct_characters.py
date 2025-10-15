"""
Given a string s and an integer k, return the length of the longest substring that contains at most k unique characters.

s = "eceba"
k = 3
print(longest_substring_k_distinct(s, k))  # Output: 4 ("eceb")
"""



def longestSubstringWithAtMostKUniqueCharacters(s: str, k: int) -> int:
    if k == 0 or not s: return 0
    left = 0
    charactersMapCount = {}
    longest_substring_length = float('-inf') # Smallest value possible
    
    
    for right in range(len(s)):
        currentCharacter = s[right]
        
        # Same as doing a for each iteration and adding the number manually for each time the key is or is not present 
        charactersMapCount[currentCharacter] = charactersMapCount.get(currentCharacter, 0) + 1
        print(charactersMapCount)
        
        # How do I build my substring?, is this a matter of ranges?
        # We need to shrink our window if a condition is not met
        
        while len(charactersMapCount) > k:
            # Then we shrink from the left
            # We first pop the left element
            print(f"Left value: {s[left]}")
            charactersMapCount[s[left]] -= 1
            if charactersMapCount[s[left]] == 0:
                del charactersMapCount[s[left]]
            
            # Move the left pointer
            left += 1
        
        
        # Window is already valid if we've passed the while condition
        current_window = (right - left) + 1
        longest_substring_length = max(longest_substring_length, current_window)
    
    return longest_substring_length


s = "eceba"
k = 3
res = (longestSubstringWithAtMostKUniqueCharacters(s, k))
print(f"Final result: {res}")