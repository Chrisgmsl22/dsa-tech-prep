"""
Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given a roman numeral, convert it to an integer.



"""
class Solution:
    
    def romanToInt(self, s: str) -> int:
        romanNumbers: dict[str, int] = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

        sol = [] # Or could use it as a regular number?
        prev = 0
        # I V
        # 1 5
        for i in range(len(s)):
            currChar = s[i]
            romanNum = romanNumbers[currChar]
            print(currChar, romanNum, sol)

            if i > 0:
                if romanNum > prev: # Then its an edge case
                    sol[-1] = romanNum - prev
                    prev = romanNum
                    continue
            sol.append(romanNum)
            prev = romanNum
        
        print(sol)
        return sum(sol)
    def romanToInt2(self, s: str) -> int:
        romanNumbers: dict[str, int] = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

        sol = 0 # Or could use it as a regular number?
        i = 0
        # I V
        # 1 5
        while i < len(s):
            currChar = s[i]
            currNumber = romanNumbers[currChar]
            
            if i < len(s) - 1: # While there are at least 1 element after me
                nextNumber = romanNumbers[s[i + 1]]
                if currNumber < nextNumber: # Then this is an edge case
                    sol -= currNumber
                    i += 1
            sol += romanNumbers[s[i]] # Better to handle the index like this so it points to the next value
            i += 1

        return sol
s = "IV"
s2 = "MCMXCIV"
s3 = "III"
sol = Solution()
res = sol.romanToInt2(s2)

print(res)