class Solution:
    def isAnagram(self, s: str, t: str) -> bool: # or we could use a counter as well
        sMap: dict[str, int] = {}
        tMap: dict[str, int] = {}

        for char in s:
            sMap[char] = sMap.get(char, 0) + 1

        for char in t:
            tMap[char] = tMap.get(char, 0) + 1

        if len(tMap) != len(sMap):
            return False

        # Now that we have out counters done, we go over our objective (t), and start comparing it to s
        for k in tMap.keys():
            if k not in sMap:
                return False # If key isnt even present, we alreay know its not valid
            if tMap[k] != sMap[k]:
                return False

        return True

"""
    NOTES:
    - Input: 2 strings, which contain english lower case characters with possibly repeated characters
    - Output: boolean, which represent the comparison of checking of T is an anagram of S.
    How do we know when a string is an anagram?, when their re arranged latters form another word.

    Our goal is to check if those comparisons help check if T is an anagram of S.

    How do we check this?
    we need to compare character by character basically if we have sufficient words.
    And not only that, I think the exact number of words need to match.

    We could generate a Key, which would be our basic form for any string, we can achieve this by sorting the input.
    And then we create the key for T, and compare the 2, both should match.

    or we use a frequency counter hashMap for both, then start comparing if the count number for each character of t equals s.
    As soon as its not valid, we can stop of iterations and simply return False


    ADDITIONAL NOTES: TIL that you can compare hashMaps

"""
