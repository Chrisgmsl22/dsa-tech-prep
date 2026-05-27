"""
    3. Reverse a String (Easy)
Problem: Reverse a string using recursion
Example: reverse("hello") = "olleh"
Think:

Base case: Empty string or single character
Recursive: Last character + reverse of everything else

Try This:
"""
def reverse_string(s):
    # Always start with the base case
    if len(s) == 1:
        return s
    
    topChar = s[-1]
    remainingChars = s[ : -1]
    
    return topChar + reverse_string(remainingChars)

# Test: reverse_string("hello") should return "olleh"
print(reverse_string("hello"))