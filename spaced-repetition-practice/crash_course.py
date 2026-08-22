"""
CRASH COURSE — blind template dump.

RULES
  - 3 minutes per function. Nothing looked up. Nothing pasted.
  - If it will not come, write a comment saying what you cannot remember,
    then MOVE ON. The gap is the useful information.
  - Add the time/space complexity as a comment on every one you finish.
  - Run the file often. `None` in the output means "not done yet".

TIER 1 is the test's stated topic list. Do all of TIER 1 before any of TIER 2.
Stop when the timer stops, not when the file is finished.
"""

from collections import Counter, deque


class ListNode:
    """Minimal linked-list node for the list templates."""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


class CrashCourse:
    # =========================================================================
    # DONE — your working code, left as-is
    # =========================================================================

    def reverseList(self, arr: list[int], lo: int, hi: int) -> list[int]:
        while lo <= hi:
            # We're going to swap and move on
            arr[lo], arr[hi] = arr[hi], arr[lo]
            lo += 1
            hi -= 1
        return arr

    def reverseArr(self, arr: list[int]) -> list[int]:
        l, r = 0, len(arr) - 1  # needs to point at the very last position
        while l <= r:
            arr[l], arr[r] = arr[r], arr[l]
            l += 1
            r -= 1
        return arr

    # =========================================================================
    # TIER 1 — do these first
    # =========================================================================

    def removeElement(self, nums: list[int], val: int) -> int:
        """Two pointers, SAME direction (in-place compaction).

        Remove every occurrence of `val` from `nums` in place. Return the new
        length. Elements past the returned length do not matter.

        [3, 2, 2, 3], val=3  ->  returns 2, nums starts [2, 2, ...]
        [1, 2, 3],    val=9  ->  returns 3, nums unchanged
        [3, 3, 3],    val=3  ->  returns 0

        Target: O(n) time, O(1) space.
        """
        l, r = 0, len(nums) - 1
        while l <= r:
            # Need to check if r is a valid disposal place
            if nums[r] == val:
                # Shrink R
                r -= 1
            # Now, we compare
            if nums[l] == val:
                # Swap them with curr Rs position
                nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

    def twoSumSorted(self, nums: list[int], target: int) -> list[int]:
        """Two pointers, OPPOSITE ends.

        `nums` is sorted ascending. Return the two 0-based indices whose values
        add up to `target`. Exactly one answer exists.

        [2, 7, 11, 15], target=9   ->  [0, 1]
        [-3, 1, 4, 8],  target=5   ->  [1, 2]

        Target: O(n) time, O(1) space. Do NOT use a hash map here — the point
        of this template is that sortedness replaces the extra space.
        """
        l, r = 0, len(nums) - 1
        while l <= r:
            leftVal = nums[l]
            rightVal = nums[r]
            possibleSum = leftVal + rightVal

            if possibleSum == target:
                return [l, r]
            elif possibleSum < target:
                # aim higher
                l += 1
            elif possibleSum > target:
                # aim lower
                r -= 1
            

    def maxSumFixedWindow(self, nums: list[int], k: int) -> int:
        """Sliding window, FIXED size.

        Return the largest sum of any contiguous subarray of exactly length k.
        Assume 1 <= k <= len(nums). Values may be negative.

        [1, 12, -5, -6, 50, 3], k=4  ->  41   (-5 + -6 + 50 + 3)
        [5], k=1                     ->  5

        Target: O(n) time, O(1) space. If you call sum() inside the loop you
        have written the O(n*k) version — that is the TLE you already hit once.
        """
        # Sliding window
        l = 0 
        maxSum = float('-inf')
        n = len(nums)
        summ = 0
        for r in range(n):
            summ += nums[r]
            windowSize = (r - l) + 1
            if windowSize == k: # Valid window, compute and store
                # Calculate current max Sum
                maxSum = max(maxSum, summ)
                summ -= nums[l]
                l += 1
        return maxSum
    def longestUniqueSubstring(self, s: str) -> int:
        """Sliding window, VARIABLE size.

        Return the length of the longest substring with no repeated character.

        "abcabcbb"  ->  3   ("abc")
        "bbbbb"     ->  1
        ""          ->  0
        "pwwkew"    ->  3   ("wke")

        Target: O(n) time. Needs one auxiliary structure — pick it deliberately.
        """
        l = 0 
        longest = float('-inf') # Really big value
        wordMap: dict[str, int] = {}
        # {a: 2, b: 1, c: 1} # 3
        for r in range(len(nums)):
            currChar = s[r]
            # First thing we do, add curr char to map, to make sure we have a unique place
            wordMap[currChar] = wordMap.get(currChar, 0) + 1
            
            while wordMap[currChar] > 1: # While there is a repetated one, shrink
                wordMap[currChar] -= 1
                if wordMap[currChar] == 0:
                    del wordMap[currChar]
                l += 1

            # Compute max
            windowSize = (r - l) + 1
            longest = max(longest, windowSize)
        return longest


    def isAnagram(self, s: str, t: str) -> bool:
        """Frequency map.

        True if `t` is a rearrangement of `s`.

        "anagram", "nagaram"  ->  True
        "rat", "car"          ->  False
        "a", "ab"             ->  False

        Write it TWICE: once building the counts by hand with a dict, then a
        second version using Counter. Know both — the manual one is what an
        interviewer sometimes asks for.

        Target: O(n) time, O(1) space if the alphabet is fixed.
        """
        # Anagram is when 2 words contain the same number of chars
        sMap: dict[str, int] = {}
        tMap: dict[str, int] = {}

        for char in s:
            sMap[char] = sMap.get(char, 0) + 1
        for char in t:
            tMap[char] = tMap.get(char, 0) + 1
        
        return sMap == tMap

    def hasDuplicate(self, nums: list[int]) -> bool:
        """Set — membership in O(1).

        True if any value appears more than once.

        [1, 2, 3, 1]  ->  True
        [1, 2, 3]     ->  False
        []            ->  False

        Target: O(n) time, O(n) space. Then answer this in a comment: what is
        the O(1)-space version, and what does it cost you?
        """
        seen = set()
        for num in nums:
            if num in seen:
                return True
            else:
                seen.add(num)
        return False

    def isValidParentheses(self, s: str) -> bool:
        """Stack — matching pairs.

        `s` contains only ()[]{}. True if every bracket is closed by the right
        type, in the right order.

        "()[]{}"  ->  True
        "(]"      ->  False
        "([)]"    ->  False
        "{[]}"    ->  True
        ""        ->  True

        Watch the two failure modes: a closer arriving on an empty stack, and
        leftovers on the stack at the end.

        Target: O(n) time, O(n) space.
        """
        closingPar: dict[str, str] = {
            '}': "{",
            ')': "(",
            ']': '['
        }
        stk = []
        for char in s:
            if char not in closingPar:
                stk.append(s)
            elif stk[-1] == closingPar[char]:
                stk.pop()
        return not stk


    def neighbors(self, grid: list[list[int]], r: int, c: int) -> list[tuple[int, int]]:
        """Bounds-checked neighbor walk — the most reused piece in any matrix
        problem. Get this one automatic.

        Return the in-bounds 4-directional neighbors of (r, c) as (row, col).

        On a 3x3 grid: (0, 0) -> [(1, 0), (0, 1)] in some order
                       (1, 1) -> 4 neighbors

        Write the directions as a named constant, not four if-statements.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # UP, DOWN, LEFT, RIGHT
        return directions

    def countIslands(self, grid: list[list[str]]) -> int:
        """Grid DFS — flood fill / connected components.

        "1" is land, "0" is water. Return the number of islands. Land connects
        4-directionally.

        [["1","1","0"],        ->  2
         ["0","1","0"],
         ["0","0","1"]]

        [["0","0"],            ->  0
         ["0","0"]]

        Decide deliberately: do you mark cells visited in a set, or mutate the
        grid? Say which you chose and why, in a comment.

        Target: O(rows * cols) time.
        """
        pass

    def minStepsBFS(self, grid: list[list[int]], start: tuple[int, int],
                    goal: tuple[int, int]) -> int:
        """Grid BFS — fewest steps. Level by level, with a deque.

        0 is open, 1 is a wall. Return the fewest 4-directional moves from
        `start` to `goal`, or -1 if unreachable. Count moves, not cells.

        [[0, 0, 0],       start=(0,0) goal=(2,2)  ->  4
         [1, 1, 0],
         [0, 0, 0]]

        [[0, 1],          start=(0,0) goal=(1,1)  ->  -1
         [1, 0]]

        The two classic bugs: marking visited when you POP instead of when you
        PUSH, and forgetting the start == goal case.

        Target: O(rows * cols) time.
        """
        pass

    # =========================================================================
    # TIER 2 — only after every TIER 1 runs green
    # =========================================================================

    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        """Matrix traversal in an order. Named explicitly in your test's topics.

        Return all values in clockwise spiral order.

        [[1, 2, 3],        ->  [1, 2, 3, 6, 9, 8, 7, 4, 5]
         [4, 5, 6],
         [7, 8, 9]]

        [[1, 2, 3, 4]]     ->  [1, 2, 3, 4]     (single row)
        [[1], [2], [3]]    ->  [1, 2, 3]        (single column)

        The single-row and single-column cases are where this one breaks. Test
        them before you believe it.
        """
        rows, cols = len(matrix), len(matrix[0])
        UP = 0
        RIGHT = cols - 1
        DOWN = rows - 1
        LEFT = 0
        result: list[int] = []
        # Need to traverse
        while UP <= DOWN and LEFT <= RIGHT:
            # Traverse top
            for i in range(LEFT, RIGHT + 1):
                num = matrix[UP][i]
                result.append(num)
            UP += 1
            
            # traverse right
            for i in range(UP, DOWN + 1):
                num = matrix[i][RIGHT]
                result.append(num)
            RIGHT -= 1
            # Add a check to see if matrix is perfectly squared, non squared matrices will not be symmetrical
            
            if not (UP <= DOWN and LEFT <= RIGHT): break

            # traverse down
            for i in range(RIGHT, LEFT - 1, -1):
                num = matrix[DOWN][i]
                result.append(num)
            DOWN -= 1
            # traverse left
            for i in range(DOWN, UP - 1, -1):
                num = matrix[i][LEFT]
                result.append(num)
            LEFT += 1
        return result



    def rotateImage(self, matrix: list[list[int]]) -> None:
        """Rotate an n x n matrix 90 degrees clockwise, IN PLACE.

        [[1, 2, 3],        becomes  [[7, 4, 1],
         [4, 5, 6],                  [8, 5, 2],
         [7, 8, 9]]                  [9, 6, 3]]

        Returns nothing. Target: O(1) extra space — no second matrix.
        """
        pass

    def dailyTemperatures(self, temps: list[int]) -> list[int]:
        """Monotonic stack — "next greater element".

        For each day, how many days until a warmer temperature? 0 if none.

        [73, 74, 75, 71, 69, 72, 76, 73]  ->  [1, 1, 4, 2, 1, 1, 0, 0]
        [30, 40, 50]                      ->  [1, 1, 0]
        [50, 40, 30]                      ->  [0, 0, 0]

        What do you push on the stack — the temperature, or the index? Answer
        that before you write a line.

        Target: O(n) time.
        """
        pass

    def reverseLinkedList(self, head: ListNode | None) -> ListNode | None:
        """Linked list, in place. Return the new head.

        1 -> 2 -> 3 -> None   becomes   3 -> 2 -> 1 -> None
        None                  ->        None
        1 -> None             ->        1 -> None

        Three names, and the order of the reassignments is the whole trick.

        Target: O(n) time, O(1) space.
        """
        pass

    def mergeTwoSorted(self, a: ListNode | None, b: ListNode | None) -> ListNode | None:
        """Linked list + dummy head.

        Merge two sorted lists into one sorted list. Return its head.

        1->3->5  and  2->4     ->  1->2->3->4->5
        None     and  1->2     ->  1->2
        None     and  None     ->  None

        The dummy head is what removes the "is this the first node?" branch.

        Target: O(m + n) time, O(1) extra space.
        """
        pass


# =============================================================================
# HARNESS — `None` means not implemented yet. Expected values are in comments.
# =============================================================================

def build(vals: list[int]) -> ListNode | None:
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def unbuild(node: ListNode | None) -> list[int]:
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


c = CrashCourse()
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print("--- done ---")
print("reverseList:", c.reverseList(arr[:], 0, 2))      # [3,2,1,4,5,6,7,8,9]
print("reverseArr: ", c.reverseArr(arr[:]))             # [9,8,7,6,5,4,3,2,1]

print("--- tier 1 ---")
nums = [3, 2, 2, 3]
print("removeElement:", c.removeElement(nums, 3), nums)  # 2, [2,2,...]
print("twoSumSorted:", c.twoSumSorted([2, 7, 11, 15], 9))          # [0,1]
print("maxSumFixedWindow:", c.maxSumFixedWindow([1, 12, -5, -6, 50, 3], 4))  # 41
print("longestUniqueSubstring:", c.longestUniqueSubstring("pwwkew"))  # 3
print("isAnagram:", c.isAnagram("anagram", "nagaram"), c.isAnagram("rat", "car"))  # True False
print("hasDuplicate:", c.hasDuplicate([1, 2, 3, 1]), c.hasDuplicate([1, 2, 3]))   # True False
print("isValidParentheses:", c.isValidParentheses("{[]}"), c.isValidParentheses("([)]"))  # True False
print("neighbors:", c.neighbors([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0))  # 2 of them
print("countIslands:", c.countIslands([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]))  # 2
print("minStepsBFS:", c.minStepsBFS([[0, 0, 0], [1, 1, 0], [0, 0, 0]], (0, 0), (2, 2)))  # 4
print("minStepsBFS blocked:", c.minStepsBFS([[0, 1], [1, 0]], (0, 0), (1, 1)))  # -1

print("--- tier 2 ---")
print("spiralOrder:", c.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # [1,2,3,6,9,8,7,4,5]
print("spiralOrder row:", c.spiralOrder([[1, 2, 3, 4]]))                 # [1,2,3,4]
m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
c.rotateImage(m)
print("rotateImage:", m)   # [[7,4,1],[8,5,2],[9,6,3]]
print("dailyTemperatures:", c.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))  # [1,1,4,2,1,1,0,0]
print("reverseLinkedList:", unbuild(c.reverseLinkedList(build([1, 2, 3]))))  # [3,2,1]
print("mergeTwoSorted:", unbuild(c.mergeTwoSorted(build([1, 3, 5]), build([2, 4]))))  # [1,2,3,4,5]
