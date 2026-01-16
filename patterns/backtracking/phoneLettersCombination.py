"""
    Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.

    A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.
"""
class Solution:
    phoneMap = {
        "2": ["a", "b", "c"],
        "3": ["d", "e", "f"],
        "4": ["g", "h", "i"],
        "5": ["j", "k", "l"],
        "6": ["m", "n", "o"],
        "7": ["p", "q", "r", "s"],
        "8": ["t", "u", "v"],
        "9": ["w", "x", "y", "z"]
    }
    def letterCombinations(self, digits: str) -> list[str]:
        n = len(digits)
        if n == 0: return []
        
        solution = []
        currentCombination = []
        
        def backtrack(i: int):
            # What is going to be our base case?
            if i == n:
                combinationString = "".join(currentCombination)
                solution.append(combinationString)
                return
            
            currentDigitArr = self.phoneMap[digits[i]]
            for letter in currentDigitArr:
                currentCombination.append(letter)
                backtrack(i + 1)
                
                # Backtrack
                currentCombination.pop()
        
        backtrack(0)
        return solution
    



solution = Solution()

inputData = "23"
res = solution.letterCombinations(inputData)

print(res)