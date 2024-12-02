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
        if self.root.num_pairs < 19:
            self.insert_into_node(self.root, key, value)
        else:
            pass ## TODO - implement node splitting?

    def insert_into_node(self, node, key, value):
        node.keys.append(key)
        node.values.append(value)
        node.num_pairs += 1
        sorted_keys_values = sorted(zip(node.keys, node.values))
        node.keys, node.values = map(list, zip(*sorted_keys_values))
        self.nodes[node.block_id] = node

    def serialize_header(self):
        root_id = self.root.block_id if self.root else 0
        header = (
            b"4337PRJ3"
            + root_id.to_bytes(8, "big")
            + self.next_block_id.to_bytes(8, "big")
            + b"\x00" * (512 - 24)
        )
        return header
        
    def nodes_to_bytes(self, values, offset_size):
        return b"".join(v.to_bytes(8, "big") for v in values + [0] * (offset_size - len(values)))

    def serialize_node(self, node):
        node_data = (
            node.block_id.to_bytes(8, "big")
            + node.parent_id.to_bytes(8, "big")
            + node.num_pairs.to_bytes(8, "big")
            + nodes_to_bytes(node.keys, 19)
            + nodes_to_bytes(node.values, 19)
            + nodes_to_bytes(node.children, 20)
            + b"\x00" * (512 - 440)
        )
        return node_data

    def serialize(self):
        buffer = bytearray()
        
        root_id = self.root.block_id if self.root else 0
        header = (
            b"4337PRJ3"
            + root_id.to_bytes(8, "big")              
            + self.next_block_id.to_bytes(8, "big")     
            + b"\x00" * (512 - 24)                      
        )
        buffer.extend(header)

        for node in self.nodes.values():
            buffer.extend(self.serialize_node(node))
        
        return bytes(buffer)
