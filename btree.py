class BTreeNode:
    def __init__(self, block_id, parent_id, num_pairs, keys, values, children):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_pairs = num_pairs
        self.keys = keys
        self.values = values
        self.children = children


class BTree:
    def __init__(self, nodes, root_id, next_block_id):
        self.nodes = {node.block_id: node for node in nodes}
        self.root = self.nodes.get(root_id, None)
        self.next_block_id = next_block_id