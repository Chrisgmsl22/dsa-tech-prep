"""
    The core idea for vertical scanning is that you check each character for each string, then the second, then the third and so on.
    
    As soon as a mismatch is found, then you return whatever you have up to that point. You don't need extra space since you can just use string ranges (aka, slicing)
    
    
    PROBLEM: Longest common prefix
    Write a function to find the longest common prefix string amongst an array of strings.

    If there is no common prefix, return an empty string "".

    

    Example 1:

    Input: strs = ["flower","flow","flight"]
    Output: "fl"

    Example 2:

    Input: strs = ["dog","racecar","car"]
    Output: ""
    Explanation: There is no common prefix among the input strings.

"""

def find_longest_common_prefix(strs: list[str]) -> str:
    if not strs: return ""
    
    firstWord = strs[0] # Technically speaking, the longest prefix could technically be the length of the first word
    # We need to iterate over the array one time
    for i in range(len(firstWord)):
        currentCharacter = firstWord[i]
        
        # We need to check if this character matches in the rest array elements
        for word in strs[1: len(strs)]:
            # Check if index is out of bounds or a mismatch has been found
            if i >= len(word) or word[i] != currentCharacter:
                return firstWord[0:i] # Return prefix before i (which is where the conditions are not met)
    
    # if we reach this part it means that technically the whole first  word is the common prefix, so we return in
    return firstWord

input = ["flower","flow","flight"]
res = find_longest_common_prefix(input)

print(f"Final result: {res}")