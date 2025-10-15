class NewPattern:
    def binarySearch(self, low: int, high: int, condition):
        
        while low < high:
            mid = (low + high) // 2
            
            if condition(mid):
                # Try a smaller answer
                high = mid
            else:
                low = mid + 1
        
        return low # Or high