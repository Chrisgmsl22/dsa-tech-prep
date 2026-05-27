class Solution:
    def reverseStringRecursive(self, s: list[str]) -> None:
      

        def recurse(l: int, r: int):
            # Base case
            if l >= r:
                return
            
            # Then swap
            s[l], s[r] = s[r], s[l]
            return recurse(l + 1, r - 1)
        
        recurse(0, len(s) - 1)
        return s

    def reverseString(self, s: list[str]) -> None:
        l, r = 0, len(s) - 1

        while l < r:
            s[l], s[r] = s[r], s[l]
            l += 1
            r -= 1
        
        return s
"""
    NOTES:
    - Input: An array of characters 
    - Output: An array of characters with all of its content reversed
        We need to be careful with how much extra space we are using
        Because the goal of this exercise is to modify the array in-place
        (So this means using the same collection, not a new one )


    Brainstorm approach:
        This could be solved using the two pointer approach
        Because we need to flip the content of the first letter to be at the last place
        and the other way around.
        We need to have an L and R pointer (pointing to the start of the collection and at the end).

        While L < R, then we flip whatever content is there until we reach the middle point
"""
