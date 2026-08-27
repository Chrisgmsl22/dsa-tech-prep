class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        L, R = 0, len(s) - 1

        while L < R:
            s[L], s[R] = s[R], s[L]
            L += 1
            R -= 1
        # print(s)




"""
    NOTES:
    - Input: an array of characters, ascii character, can contain repeated characters
    - Output: None, we modify our array in-place, meaning we do not use extra storage for it

    We need to reverse a array, our array could contain numbers even, so it makes us have to work with an array.
    Best way to start this is by using 2 pointers, one at each side of the array, and flip their values (a lives in B, and B lives in A), advance pointers and repeat until both pointers have crossed each other

"""
