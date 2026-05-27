# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:
def isBadVersion(num: int) -> bool:
    pass

class Solution:
    def firstBadVersion(self, n: int,) -> int:
        L, R = 0, n
        temp = 0 # Will act as our final result
        # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 
        #     l
        #               M
        #.                           r
        while L <= R:
            # We need a middle pointer
            M = (R + L) // 2 # Please confirm this is the correct approach

            if (isBadVersion(M)):
                # If it is, store it and shrink search (look left)
                temp = M
                R = M - 1
            else:
                # If its not, grow right
                L = M + 1
        return temp
"""

    NOTES:
    - Input: a number, which represent the total versions. We can imagine this like an array that starts at 0 and ends at n. 
    - Output: integer, which represents the very first bad version of our total versions.
    The purpose is to find the very first version because it means that the rest of numbers to my "right" are always going to be bad versions.

    - Assumptions: We are given a versions number which is at least 1, and it can be
    very big, we are dealing with only numbers. Also, we can assume that isBadVersion is already defined and implemented for us, we dont need to worry about the implementation, so its ready to be used for us.

    Ok, so we need to see this number as a long list.
    We need to try our numbers from left to right
    for each number, check if its bad version.
    if it is, then we found our very first bad version, return our current number.
    Since our list can be very long, it means we would spend a lot of time doing this work.

    We can optimize this by using a binary search, because we have our numbers already sorted. We can do the lookup way faster.
    But, once we find a match we should not treat this as the definitive answer, because we might have more invalid values to our left, so we need to keep trying until we find a good version to our left. If we find this, then we know what our final result is going to look like. 

""" 