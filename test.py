from file_parser import Parser

def print_tree(tree, node_id=None, depth=0):
    if node_id is None:
        node_id = tree.root.block_id if tree.root else None
    if node_id is None or node_id not in tree.nodes:
        return
    node = tree.nodes[node_id]
    indent = "  " * depth
    print(f"{indent}Node ID: {node.block_id}")
    print(f"{indent}  Parent ID: {node.parent_id}")
    print(f"{indent}  Keys: {node.keys}")
    print(f"{indent}  Values: {node.values}")
    print(f"{indent}  Children: {node.children}")
    for child_id in node.children:
        if child_id != 0:
            print_tree(tree, child_id, depth + 1)

parser = Parser()
btree = parser.parse_file("sample.idx")

print_tree(btree)
