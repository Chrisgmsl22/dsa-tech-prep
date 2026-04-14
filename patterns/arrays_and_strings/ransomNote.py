"""
Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.

Each letter in magazine can only be used once in ransomNote.

 

Example 1:

Input: ransomNote = "a", magazine = "b"
Output: false
Example 2:

Input: ransomNote = "aa", magazine = "ab"
Output: false
Example 3:

Input: ransomNote = "aa", magazine = "aab"
Output: true


"""
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        rMap: dict[str, int] = {} # We will point to this
        mMap: dict[str, int] = {} # We will use this

        # Let's build up our frequency counts
        for char in ransomNote:
            rMap[char] = rMap.get(char, 0) + 1
        
        for char in magazine:
            mMap[char] = mMap.get(char, 0) + 1
        
        print(f"rMap: {rMap}, mMap: {mMap}")
        # r = aa -> {a: 2}
        # m = aab -> {a: 2, b: 1}
        for rKey in rMap:
            # Check if rKey is present in mMap, and if the counter is enough
            isKeyPresent = rKey in mMap
            if not isKeyPresent: return False
            
            isCounterNotEnough = mMap[rKey] < rMap[rKey]
            if isKeyPresent and isCounterNotEnough:
                return False

        return True



""" 
    NOTES:
    - Input: 2 strings which are english letters in lowercase
    - Output: Boolean, which represents the result of checking if each letter in magazine can be used in ransomNote.
    - Assumptions: both strings are english and lowercase. Our string length can be at least 1 character and up to 10p5, which is very large.

    Given that we care about the total number of elements in our strings, we can ignore their relative positions, meaning we do not necesarily need to iterate over the strings.

    What we need to do is build up our frequency counter hashMaps, which will allow us constant lookup so we can check if the number of characters from a, is at least present inside magazine, otherwise we can return false

"""