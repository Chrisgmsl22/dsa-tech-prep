"""
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

 

Example 1:


Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation:
The distance between (1, 3) and the origin is sqrt(10).
The distance between (-2, 2) and the origin is sqrt(8).
Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].
Example 2:

Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: The answer [[-2,4],[3,3]] would also be accepted.
"""
import heapq
class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        res = []
        minHeap = []
        ORIGIN = [0, 0]
        
        for coordinate in points:
            # We calculate the distance.
            x1, x2 = coordinate[0], ORIGIN[0]
            y1, y2 = coordinate[1], ORIGIN[1]
            
            xOp = (x1 - x2) ** 2
            yOp = (y1 - y2) ** 2
            dist = (xOp + yOp) ** 0.5
            
            key: tuple[int, list[int, int]] = (-dist, [x1, y1])
            heapq.heappush(minHeap, key)

            if len(minHeap) > k:
                # THen we trim it until its back to valid size
                heapq.heappop(minHeap) # Pop the LARGEST distance, thats we we negated the val, to turn it into a maxHeap
        
        res = [arr for _, arr in minHeap ]
        return res
"""
    NOTES:
    - Input: an array of arrays, and an integer K
    - Output: An array of arrays, which represent the K coordinates that are the closest to the origin (0,0)
    - Our goal is to calculate which ones are closest to the origin, and we return K times that number.

    Assumptions: is my points array always going to contain 1 coordinate?, does it always contain 2 values (x, y)?

    How would I do this?
    We need to take into consideration the Euclidean distance formula, for this we calculare it for all elements in our array
    We need to store this somehow. Since we care about the CLOSEST to the origin, then we need to know the one with the SMALLEST
    value form the formula.

    Once we have our collection, we simply extract K times our values and add it to a result array. Lastly we can return the result

"""