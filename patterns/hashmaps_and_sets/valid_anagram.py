"""
Given two strings s and t, return true if t is an anagram of s, and false otherwise.

 

Example 1:

Input: s = "anagram", t = "nagaram"

Output: true

Example 2:

Input: s = "rat", t = "car"

Output: false

 

Constraints:

1 <= s.length, t.length <= 5 * 104
s and t consist of lowercase English letters.

"""
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        sMap: dict[str, int] = {}
        tMap: dict[str, int] = {}

        # Build up frequency counts (keep in mind I could also use Collections I think)
        for char in s:
            sMap[char] = sMap.get(char, 0) + 1
        for char in t:
            tMap[char] = tMap.get(char, 0) + 1
        
        return sMap == tMap


s = "anagram"
t = "nagaram"

sol = Solution()

print(sol.isAnagram(s, t))

"""
NOTES:
- Input: 2 string characters: s and t
- Output: Boolean, which represents the result of checking if t is an anagram of s
- Assumptions: s and t only contain english lowercase letters, our s and t length could be very large

Initial approach:
Our goal is to check if T is an anagram of S.
Correction: I do not need to check for a palinfrome, I need to check for an anagram, which is the construction of a word by using n amount of other characters.

Yes, we need a frequency count in this case. We build it up and simply check if the content match, if they do, then true.
False otherwise

"""