"""
    YOu have n pages of a book. Each day you can read k pages. What is the minimum k so that you can finish the book
    in d days
"""
import math

class BinarySearch:
    def findMinimumPages(self, numberOfPages: int, days: int) -> int:
        left = 1 # Tecnically, you read at least a page, not zero
        right = numberOfPages
        # book: 50 pages, 10 days (5 pages per day should be the answer)
        while left < right:
            mid = (left + right) // 2 # 25 pages in 2 days technically
            
            daysNeeded = math.ceil(numberOfPages / mid)
            
            if daysNeeded <= days: # then it is possible to finish
                right = mid
                print('Current minimum: ', mid, daysNeeded)
            else:
                # if the days needed is greater than the whole amount of days given, then remove the left block
                left = mid + 1
        
        return left
    

solution = BinarySearch()
print(solution.findMinimumPages(100, 8))  