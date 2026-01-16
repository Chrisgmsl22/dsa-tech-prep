class Solution:
    def findClosestNumber(self, nums: list[int]) -> int:
        closest = float("inf")

        # [-4, -2, 1, 4, 8]
        #  n
        for num in nums:
            if abs(num) < abs(closest):
                closest = num
            elif abs(num) == abs(closest):
                # How can I check which one is the largest?
                closest = max(num, closest)
        
        return closest

"""
    NOTES:
    - Input: an array of numbers with at least one value (can contain negatives)
    - Output: A number, which represents the number (not index) that is closest to zero
        Keep in mind if there are multiple answers, we return the value with the LARGEST VAL (perhaps a max function?)

    Brainstorming:
        We need to iterate over the array.
        We need to keep track of a final result, which will be updated as we go.
        It does not really matter the sign, positive or negative we need its abs val
        We ask ourselves if our abs val of our current number is greater than our current max
        if so, we update, and we continue

        When it says we might have multiple answers, I think this refers to having the same
        value, just in positive vs negative?, if thats the case we can maybe return the positive one

"""