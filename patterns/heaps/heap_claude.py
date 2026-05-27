class MinHeap:
      def __init__(self):
          self.data = []

      def push(self, val):
          self.data.append(val)
          self._bubble_up(len(self.data) - 1)

      def pop(self):
          if not self.data:
              raise IndexError("pop from empty heap")
          root = self.data[0]
          last = self.data.pop()
          if self.data:
              self.data[0] = last
              self._bubble_down(0)
          return root

      def peek(self):
          if not self.data:
              raise IndexError("peek from empty heap")
          return self.data[0]

      def _bubble_up(self, i):
          while i > 0:
              parent = (i - 1) // 2
              if self.data[i] < self.data[parent]:
                  self.data[i], self.data[parent] = self.data[parent], self.data[i]
                  i = parent
              else:
                  break

      def _bubble_down(self, i):
          n = len(self.data)
          while True:
              left = 2 * i + 1
              right = 2 * i + 2
              smallest = i

              if left < n and self.data[left] < self.data[smallest]:
                  smallest = left
              if right < n and self.data[right] < self.data[smallest]:
                  smallest = right

              if smallest != i:
                  self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
                  i = smallest
              else:
                  break

      def __len__(self):
          return len(self.data)