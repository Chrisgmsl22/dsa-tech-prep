

from trees.utils.tree_node import TreeNode


class Solution:
    def countLeafNodes(self, root: TreeNode) -> int:
        if not root:
            return 0
        
        if not root.left and not root.right:
            return 1
        
        return self.countLeafNodes(root.left) + self.countLeafNodes(root.right)
