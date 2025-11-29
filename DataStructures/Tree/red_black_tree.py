import DataStructures.Tree.rbt_node as rbt 

def new_map():
    return {"root": None}

def default_compare(key, element):
    element_key = element["key"] if element is not None else None
    
    if key == element_key:
        return 0
    elif key > element_key:
        return 1
    else: 
        return -1


def size_tree(root):
    if root is None:
        return 0
    return root["size"]

def flip_node_color(node_rbt):
    if node_rbt is None:
        return None
    new_color = rbt.BLACK if rbt.is_red(node_rbt) else rbt.RED
    rbt.change_color(node_rbt, new_color) 
    
    return node_rbt 

def flip_colors(node_rbt):
    
    if node_rbt is None:
        return None
        
    flip_node_color(node_rbt) 
    
    
    if node_rbt["left"] is not None:
        flip_node_color(node_rbt["left"])
        
    
    if node_rbt["right"] is not None:
        flip_node_color(node_rbt["right"])
        
    return node_rbt

def rotate_left(node_rbt):
    
    if node_rbt is None or node_rbt["right"] is None:
        return node_rbt
        
    x = node_rbt
    y = x["right"]
    
    x["right"] = y["left"]
    y["left"] = x
    
    
    y["color"] = x["color"]
    x["color"] = rbt.RED 
    
    
    x["size"] = 1 + size_tree(x["left"]) + size_tree(x["right"])
    y["size"] = 1 + size_tree(y["left"]) + size_tree(y["right"])
    
    return y

def rotate_right(node_rbt):
    
    if node_rbt is None or node_rbt["left"] is None:
        return node_rbt
        
    x = node_rbt
    y = x["left"]
    
    x["left"] = y["right"]
    y["right"] = x
    
    
    y["color"] = x["color"]
    x["color"] = rbt.RED 
    
    x["size"] = 1 + size_tree(x["left"]) + size_tree(x["right"])
    y["size"] = 1 + size_tree(y["left"]) + size_tree(y["right"])
    
    return y

def insert_node(root, key, value):
 
    if root is None:
        return rbt.new_node(key, value) 

    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        
        root["value"] = value
        return root
    elif cmp < 0:
        
        root["left"] = insert_node(root["left"], key, value)
    else: 
        
        root["right"] = insert_node(root["right"], key, value)

    
    
    
    
    if rbt.is_red(root["right"]) and not rbt.is_red(root["left"]):
        root = rotate_left(root)
        
    
    if rbt.is_red(root["left"]) and rbt.is_red(root["left"]["left"]):
        root = rotate_right(root)
        
    
    if rbt.is_red(root["left"]) and rbt.is_red(root["right"]):
        flip_colors(root)
    
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])

    return root

def put(my_rbt, key, value):
    
    new_root = insert_node(my_rbt["root"], key, value)
    my_rbt["root"] = new_root
    
    rbt.change_color(my_rbt["root"], rbt.BLACK)
    
    return my_rbt

def size(my_rbt):
    return size_tree(my_rbt["root"])


def is_empty(my_rbt):
    return size(my_rbt) == 0
