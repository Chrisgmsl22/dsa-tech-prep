class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        self.head = Node(value)
        self.tail = self.head
        self.length = 1

    def append(self, value):
        """Add a new node at the right of the list."""
        new_node = Node(value)
        
        self.tail.next = new_node
        self.tail = new_node
        self.length += 1
        
    def prepend(self, value):
        new_node = Node(value)
        
        new_node.next = self.head
        self.head = new_node
        self.length += 1

    def display(self):
        """Print the linked list elements."""
        arr = []
        current_node = self.head
        while current_node is not None:
            arr.append(current_node.value)
            current_node = current_node.next
        print(f"Display linked list: {arr}")
        return arr

# Create the linked list
ll = LinkedList(2)
ll.append(10)
ll.append(20)
ll.prepend(30)

# Display the list
ll.display()
