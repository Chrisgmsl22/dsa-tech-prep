class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool: # We could also use Counter collection
        ransomNoteMap: dict[str, int] = {}
        magazineMap: dict[str, int] = {}

        for r in ransomNote:
            ransomNoteMap[r] = ransomNoteMap.get(r, 0) + 1

        for m in magazine:
            magazineMap[m] = magazineMap.get(m, 0) + 1

        # Now this is where we make sure that ransome note keys and counters are contained within magazine
        for key in ransomNoteMap.keys():
            if key not in magazineMap:
                return False
            if magazineMap[key] < ransomNoteMap[key]:
                return False


        return True



"""
    NOTES:
    - Input 2 strings, ransomNote which is our final target, and magazine, which represents our objective
    - Output: Boolean, which represents the result of checking if we can construct a by choosing the characters from magazine

    Important, we need to check if they can give us these characters in random order, if so, there is a chance we use a hashMap, so order doesnt matter

    If they will always give us the content in order, then we can simply use ransomNote as a fixed block and we check if that is present in magazine.

    Since there is a chance we might receive our characters in scrambled order, it makes sense to do the safer approach as a first round
"""
