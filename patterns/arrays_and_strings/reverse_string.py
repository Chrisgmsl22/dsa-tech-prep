"""
    Create a function that reverses a string.
    
    Key points: we are talking about a function, it takes in a string, it returns a string as well
    
    Since we need to reverse the string, perhaps we might need to go over the whole string (iterate?)
    
    Are there any buil-in functions that could help me with this?
"""

# Initial approach
"""
    I would iterate over an array, store each value in a different array (also called list) and store it at the end, or at the start. This would help me ensure the content of the variable is not the same as the original argument
    
    Then we can print the result and see how this goes
"""

# Final approach
"""
    ...
"""

# Define the function
def reverse_string(input: str) -> str:
    # iterate over the whole world
    result = ""
    for char in input:
        result = char + result
        
    return result    
    
# Testing
word = 'Dog'
result = reverse_string(word)

print(f"Reverse a string: {result}") 

print("Hello"[::-1])