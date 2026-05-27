"""
2. Sum of Array (Easy)
Problem: Find sum of all elements in an array using recursion
Example: sum([1, 2, 3, 4]) = 10
Think:

Base case: Empty array = 0
Recursive: First element + sum of rest

Try This:
"""
def sum_array(arr):
    # Always start with the base case, when dealing with recursion
    if len(arr) == 0: return 0
    
    topElement = arr[-1]
    rest = arr[ : -1]
    
    return topElement + sum_array(rest)

# Test: sum_array([1, 2, 3, 4]) should return 10
print(sum_array([1, 2, 3, 4]))