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
        self.min_degree = 10
        self.max_keys = 2 * self.min_degree - 1
        self.max_children = 2 * self.min_degree
        self.nodes = {node.block_id: node for node in nodes}
        self.root = self.nodes.get(root_id, None)
        self.next_block_id = next_block_id

    def search(self, key):
        for node in self.nodes.values():
            if key in node.keys:
                idx = node.keys.index(key)
                return node.keys[idx], node.values[idx]
        return None

    def insert(self, key, value):
        if any(key in node.keys for node in self.nodes.values()):
            raise ValueError("Key already exists.")
        if not self.root:
            self.root = BTreeNode(1, 0, 0, [], [], [])
            self.nodes[self.root.block_id] = self.root
        if self.root.num_pairs < self.max_keys:
            self.insert_into_node(self.root, key, value)
        else:
            self.split_root(key, value)

    def insert_into_node(self, node, key, value):
        node.keys.append(key)
        node.values.append(value)
        node.num_pairs += 1
        sorted_keys_values = sorted(zip(node.keys, node.values))
        node.keys, node.values = map(list, zip(*sorted_keys_values))
        self.nodes[node.block_id] = node

    def split_root(self, key, value):
        old_root = self.root
        new_root_id = self.next_block_id
        self.next_block_id += 1

        new_root = BTreeNode(new_root_id, 0, 0, [], [], [])
        self.nodes[new_root_id] = new_root
        self.root = new_root

        left_child = BTreeNode(self.next_block_id, new_root_id, 0, [], [], [])
        self.next_block_id += 1
        right_child = BTreeNode(self.next_block_id, new_root_id, 0, [], [], [])
        self.next_block_id += 1

        middle_index = self.min_degree - 1
        middle_key = old_root.keys[middle_index]
        middle_value = old_root.values[middle_index]

        self.root.keys.append(middle_key)
        self.root.values.append(middle_value)
        self.root.children = [left_child.block_id, right_child.block_id]
        self.root.num_pairs = 1

        left_child.keys = old_root.keys[:middle_index]
        left_child.values = old_root.values[:middle_index]
        left_child.children = old_root.children[:self.min_degree]
        left_child.num_pairs = len(left_child.keys)

        right_child.keys = old_root.keys[middle_index + 1:]
        right_child.values = old_root.values[middle_index + 1:]
        right_child.children = old_root.children[self.min_degree:]
        right_child.num_pairs = len(right_child.keys)

        self.nodes[left_child.block_id] = left_child
        self.nodes[right_child.block_id] = right_child

        if key < middle_key:
            self.insert_into_node(left_child, key, value)
        else:
            self.insert_into_node(right_child, key, value)

    def serialize_header(self):
        root_id = self.root.block_id if self.root else 0
        header = (
            b"4337PRJ3"
            + root_id.to_bytes(8, "big")
            + self.next_block_id.to_bytes(8, "big")
            + b"\x00" * (512 - 24)
        )
        return header

    def serialize_node(self, node):
        def pad_list(lst, size):
            return lst + [0] * (size - len(lst))

        node_data = (
            node.block_id.to_bytes(8, "big")
            + node.parent_id.to_bytes(8, "big")
            + node.num_pairs.to_bytes(8, "big")
            + b"".join(k.to_bytes(8, "big") for k in pad_list(node.keys, self.max_keys))
            + b"".join(v.to_bytes(8, "big") for v in pad_list(node.values, self.max_keys))
            + b"".join(c.to_bytes(8, "big") for c in pad_list(node.children, self.max_children))
            + b"\x00" * (512 - 440)
        )
        return node_data

    def serialize(self):
        buffer = bytearray()
        buffer.extend(self.serialize_header())
        for node in self.nodes.values():
            buffer.extend(self.serialize_node(node))
        return bytes(buffer)
