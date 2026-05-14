"""
You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.

 

Example 1:

Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.
Example 2:

Input: s = "AABABBA", k = 1
Output: 4
Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
The substring "BBBB" has the longest repeating letters, which is 4.
There may exists other ways to achieve this answer too.


"""
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        L = 0
        freqCount: dict[str, int] = {}
        longest = 0
        maxFreq = 0
        # A A B A B B A ==> K = 1
        # L
        #         R
        # {A: 3, B: 2}, maxFreq = 3
        # longest = 2
        for R in range(len(s)):
            curr = s[R]
            freqCount[curr] = freqCount.get(curr, 0) + 1
            maxFreq = max(maxFreq, freqCount[curr])

            while ((R - L) + 1) - maxFreq > k:
                leftChar = s[L]
                # if freqCount[leftChar] == maxFreq:
                #     maxFreq -= 1
                
                freqCount[leftChar] -= 1
                if freqCount[leftChar] == 0:
                    del freqCount[leftChar]
                
                L += 1
                

            windowSize = (R - L) + 1
            longest = max(longest, windowSize)

        return longest



sol = Solution()

s = "AABABBA"
k = 1

res = sol.characterReplacement(s, k)
print("Final result: ", res)