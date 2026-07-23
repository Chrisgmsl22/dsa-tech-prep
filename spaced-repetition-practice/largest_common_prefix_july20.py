"""
Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".



Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"
Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.


Constraints:

1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] consists of only lowercase English letters if it is non-empty.
"""
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        smallestWord = min(strs, key=len)
        i = 0
        longestPrefix = ""

        while i < len(smallestWord):
            hasPassed = True
            char = smallestWord[i]
            for word in strs:
                currChar = word[i]
                if currChar != char:
                    print("Not valid anymore")
                    hasPassed = False
                    break

            if not hasPassed:
                return longestPrefix

            longestPrefix = smallestWord[ : i + 1]
            i += 1

        return longestPrefix

    def isPrefix(self, str: str, target: str) -> bool:
        possible = target[ : len(str)]
        return possible == str

sol = Solution()
#print(sol.isPrefix("al", "aliexpress"))
strs = ["flower","flow","flight"]
res = sol.longestCommonPrefix(strs)

print("FINAL RES: ", res)

"""
    NOTES:
        input: an array of strings
        output: A string, which represent the LONGEST common prefix

        A prefix is a portion of a string that happens at the beggining of the word
        A suffix is a portion of a string that happens at the end of the word

        Right out of the bath, I think we need to slice our word, otherwise we would not know how to make this happen.

        But also, notice how it needs to be a common prefix. So it has to apply to all the words in the array. Need to keep this in mind
"""
