"""
    Core functionality we need to consider in a heap.
    - left child: (2 * i) + 1
    - right child: (2 * i) + 2
    - parent: (i - 1) // 2

"""

class MinHeap:
    def __init__(self) -> None:
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2
    def left_child(self, i):
        return (i * 2) + 1
    def right_child(self, i):
        return (i * 2) * 2
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def push(self, val: int):
        # Complexity: O(log n)
        # Add to end
        self.heap.append(val)
        # Bubble up to maintain the order of a heap
        self.heapifyUp(len(self.heap) - 1)
    def _heapify_up(self, i):
          """Bubble element up until heap property is satisfied"""
          while i > 0:
              parent_idx = self.parent(i)
              # If current is smaller than parent, swap
              if self.heap[i] < self.heap[parent_idx]:
                  self.swap(i, parent_idx)
                  i = parent_idx
              else:
                  break

    def pop(self):
        """Remove and return minimum - O(log n)"""
        if len(self.heap) == 0:
            raise IndexError("pop from empty heap")

        if len(self.heap) == 1:
            return self.heap.pop()

        # Save min value
        min_val = self.heap[0]
        # Move last element to root
        self.heap[0] = self.heap.pop()
        # Bubble down to maintain heap property
        self._heapify_down(0)

        return min_val

    def _heapify_down(self, i):
        """Bubble element down until heap property is satisfied"""
        while True:
            smallest = i
            left = self.left_child(i)
            right = self.right_child(i)

            # Check if left child exists and is smaller
            if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
                smallest = left

            # Check if right child exists and is smaller
            if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
                smallest = right

            # If smallest is not current, swap and continue
            if smallest != i:
                self.swap(i, smallest)
                i = smallest
            else:
                break

    def peek(self):
        """Get minimum without removing - O(1)"""
        if len(self.heap) == 0:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def __len__(self):
        return len(self.heap)

    def __repr__(self):
        return f"MinHeap({self.heap})"
