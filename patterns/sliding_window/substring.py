"""
    Given a string s, find the length of the longest substring without duplicate characters.

 

    Example 1:

    Input: s = "abcabcbb"
    Output: 3
    Explanation: The answer is "abc", with the length of 3.
    Example 2:

    Input: s = "bbbbb"
    Output: 1
    Explanation: The answer is "b", with the length of 1.
    Example 3:

    Input: s = "pwwkew"
    Output: 3
    Explanation: The answer is "wke", with the length of 3.
    Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
    
    s consists of English letters, digits, symbols and spaces.
"""

"""
    Brainstorm: we're dealing with strings (string methods needed??), we will deal with a numeric value as the result. if we're moving through each character, then we will need some sort of pointers, ()indices, to keep track of these. DO WE NEED A SET? no
    
    a string, is an array, (array methods)?
    
    ...
"""

"""
    Plain english on how to build this solution:
    
    we define the function:
    
    define pointers (l, r)
    define a place to store the possible longest substring X
    
    iterate from l to right**
        X = first character
        is X in the map? CANCEL : ADD IT and continue
        add X to a map to keep track of if
        
    return X
    
"""

def find_longest_substring(word: str) -> int:
    longest_substring = ""
  
    for left in range(len(word)):
        map = {}
        current_substring = ""
        for i in range(left, len(word)):
            #print(f"current character: {i, word[i]}")
            character = word[i]
            
            if character in map: 
                break
            
            map[character] = character
            current_substring += character
            
            if len(current_substring) > len(longest_substring):
                # We do the swap
                longest_substring = current_substring
            #print(f"current substring: {current_substring}")
       
        
    
    print(f"Longest substring: {longest_substring}")
    return len(longest_substring)
   

test_input = "abcabcbb"
test_two = "pwwkew" # "wke"
t = "bbbbb"
test_three = "pwxywkew" # xywke ------------
test_four = "pwxwkew"
test_five = "wxywkew"
w = ""
res = find_longest_substring(test_three)

print(f"RESULT: {res}")