
from btree import BTree, BTreeNode

class Parser:
    def __init__(self):
        pass
            
    def parse_file(self, file_name):
        with open(file_name, "rb") as f:
            file = f.read()
            
            root_id, next_block_id = self.parse_header(file)
            
            if root_id == 0:
                return BTree([], 0, 0)
                
            to_parse = [root_id]
            nodes = []
            parsed = set()
            
            while to_parse:
                block_id = to_parse.pop()
                if block_id not in parsed:
                    node = self.parse_node(file, block_id)
                    nodes.append(node)
                    parsed.add(block_id)
                    to_parse.extend(child for child in node.children if child != 0)
            return BTree(nodes, root_id, next_block_id)
            
    def parse_header(self, file):
        header_data = file[:512]
        magic_number = header_data[:8]
        root_id = int.from_bytes(header_data[8:16], "big")
        next_block_id = int.from_bytes(header_data[16:24], "big")
        if magic_number != b"4337PRJ3":
            raise ValueError("Invalid magic number in header!")
        return root_id, next_block_id

    def parse_node(self, file, block_id):
        start = block_id * 512
        end = start + 512
        node_data = file[start:end]
        block_id = int.from_bytes(node_data[:8], "big")
        parent_id = int.from_bytes(node_data[8:16], "big")
        num_pairs = int.from_bytes(node_data[16:24], "big")
        keys = [int.from_bytes(node_data[24 + i * 8:24 + (i + 1) * 8], "big") for i in range(19)][:num_pairs]
        values = [int.from_bytes(node_data[176 + i * 8:176 + (i + 1) * 8], "big") for i in range(19)][:num_pairs]
        children = [int.from_bytes(node_data[328 + i * 8:328 + (i + 1) * 8], "big") for i in range(20)][:num_pairs + 1]
        return BTreeNode(block_id, parent_id, num_pairs, keys, values, children)
