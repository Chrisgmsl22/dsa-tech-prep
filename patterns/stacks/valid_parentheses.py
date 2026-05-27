class Solution:
    def isValidUglyVersion(self, s: str) -> bool:
        tempStack = []
        def isOpeningBracket(char: str):
            return char == "(" or char == "{" or char == "["
        def doesOpeningBracketMatchClosing(top: str, char: str):
            return (topVal == "(" and char == ")") or (topVal == "{" and char == "}") or (topVal == "[" and char == "]")

        for char in s:
            if isOpeningBracket(char) or not tempStack:
                tempStack.append(char)
            else: # Then is closing bracket 
                topVal = tempStack[-1]
                # If closing matches exactly opening
                if doesOpeningBracketMatchClosing(topVal, char):
                    tempStack.pop()
                else:
                    tempStack.append(char)
            #print(tempStack)
        
        return not tempStack
    def isValid(self, s: str) -> bool:
        validMap = { ")": "(", 
                    "}": "{", 
                    "]": "["  }
        temp = []
        # ()[]{}
        # (
        for char in s:
            if char not in validMap:
                # If its an opening bracket
                temp.append(char)
            else:
                if not temp:
                    return False
                # It is a closing bracket
                topVal = temp[-1]
                if topVal == validMap[char]:
                    temp.pop()
                else:
                    return False
        
        return len(temp) == 0

sol = Solution()
print(sol.isValid("]"))
""" 
    NOTES:
    - Input: A string containig parentheses brackets 
    - Output: A boolean, indicating if the given string contains valid parentheses
        A parentheses is valid if every close bracket has a corresponding open bracket of the same type 

        Keep in mind that our string might contain at least 1 character
        And we can assume that the characters within our string contain only parentheses

        Brainstorming:
        We need to go through the collection linearly (regular iteration)
        We need to collec these characters one by one
        Since there is a chance a closing bracket might appear later in the string, we cant just compare parentheses that are together, we need to build something else

        We can start building a stack which contains these opening characters, and if the current character is a closing bracket AND the top one is its corresponding opening bracket, then we pop the top

        If the current char is opening, we just append it
        By the time our iteration fininshes, we will either end up with a full or empty list, if its empty, then the parentheses is valid, if not, then is False

""" 