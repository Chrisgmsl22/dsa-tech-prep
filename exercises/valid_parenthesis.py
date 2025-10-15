"""
    Brainstorm:
    - We are given a set of fixed values (which are the valid parenthesis)
    - We need to compare the whole string, so we go from start fo finish
    - If we do not have a valid pair, then we immediately know its not valid, so we return false
    - Do I possibly need a map function which contains the expected closing bracket??
    - Every closing bracket must be of the same type
    - ...
    - HINT: Use a stack of characters (so does that mean I need to pop values as I go?)
"""


def isValid(s: str) -> bool:
    possible_values = {")": "(", "]": "[", "}": "{"}
    valid_opening_brackets = ["(", "[", "{"]
    
    stack = []
    for i in range(len(s)):
        current_character = s[i]
        if current_character in valid_opening_brackets:
            stack.append(current_character)
        else:
            if len(stack) == 0: return False
            # We need to check if the closing bracket has the correct opening bracket
            if stack[-1] == possible_values[current_character]:
                # Then its a valid group, then we pop
                stack.pop()
            else:
                return False
    
    
    return len(stack) == 0
            
"""
    Stack:  [(]
"""

test_input = "()"
test_input_two = "()[]{}" # True
test_input_three = "(]"
test_input_four = "([])"
t = "){" # Should be False
res = isValid(t)
print(f"FINAL RESULT: {res}")

