# ui/components/tree_viewer.py

def build_json_tree(tree, parent, value):

    if isinstance(value, dict):
        for key, val in value.items():
            node = tree.insert(parent, "end", text=str(key))
            build_json_tree(tree, node, val)

    elif isinstance(value, list):
        for index, item in enumerate(value):
            node = tree.insert(parent, "end", text=f"[{index}]")
            build_json_tree(tree, node, item)

    else:
        tree.insert(parent, "end", text=str(value))
