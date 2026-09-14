class Solution:
    def isValid(self, s: str) -> bool:
        stck = []
        pTypes: dict[str, str] = {
            ")": "(",
            "]": "[",
            "}": "{"
        }

        for par in s:
            if par not in pTypes: # It is an opening
                stck.append(par)
            elif stck and pTypes[par] == stck[-1]:
                stck.pop()
            else:
                return False
            #print(stck)

        return len(stck) == 0


"""
    NOTES:
    - Input: a string, which contains parentheses only.
    - Output: Boolean, which represents the result of checking if the string is a valid parentheses.
    How do we know a string is a valid parentheses?
    We need to check if the open brackets are closed with the same type of brackets
        If they are not, we can immediately return false.

    There's a chance that we have nested opening brackets, which is valid, whats important here is that we clone the inner with the outer ones.
    They must match.

    So, we need to store our current inputs, otherwise we are not going to be able to tell
    As we add items to our stack we need to constantly check if they are valid parentheses.

    We need to pair each parentheses (opening with their closing)
    We can do this using a hashMap.
    If the parentheses is opening, we can simply add it, it is then it is a closing type where we need to check if we can pop

"""