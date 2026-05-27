"""
    3. Longest Substring Without Repeating Characters
Solved
Medium
Topics
premium lock icon
Companies
Hint
Given a string s, find the length of the longest substring without duplicate characters.

 

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.
Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

"""
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        L = 0
        longest = 0
        freqCount: dict[str, int] = {}
        n = len(s)

        for R in range(n):
            currChar = s[R]
            freqCount[currChar] = freqCount.get(currChar, 0) + 1

            # While my set contains a counter greater than 1, we know its a repeated char, so we shrink
            while freqCount[currChar] > 1:
                leftmostChar = s[L]
                freqCount[leftmostChar] -= 1
                if freqCount[leftmostChar] == 0:
                    del freqCount[leftmostChar]
                
                L += 1 # Increase L so the window changes shape

            #After thats done, we end up with a valid window
            windowSize = (R - L) + 1
            longest = max(longest, windowSize)

        return longest


sol = Solution()
s = "abcabcbb"

res = sol.lengthOfLongestSubstring(s)
print(res)
