# id1: 326528494
# name1: Erez Avrahami
# username1: erezavrahami
# id2: 326283264
# name2: Omer Lemel
# username2: lemel

import time
import math

"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.successor = None
        self.predecessor = None
        self.height = -1
        self.bf = 0

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.height != -1


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """

    def __init__(self, is_avl):
        self.root = None
        self.is_avl = is_avl
        self.tsize = 0
        self.virtual_node = AVLNode(None, None)

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        if self.root == None: # Empty tree -> search_time = 1
            return None, 1
        search_time = 0 # Initialize seach_time
        node = self.root
        while node.is_real_node():
            if node.key == key: return node, search_time + 1
            elif key < node.key: # Add 1 to search_time for every node we visited
                node = node.left
                search_time += 1
            else: 
                node = node.right
                search_time += 1
        return None, search_time + 1 # If the search failed, search_time += 2. We already added 1 for the empty node we visited, so we're adding 1 and not 2

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int,int)
    @returns: a 4-tuple (x, search_time, rotations, height_changes), where x is the new node
    and the other 3 return values are as defined and explained in the assignment.
    """

    def insert(self, key, val):
        if self.root == None:
            self.tsize += 1
            t0 = time.time()
            self.root = AVLNode(key, val)
            self.root.height = 0
            self.root.successor = self.virtual_node
            self.root.predecessor = self.virtual_node
            self.root.parent = self.virtual_node
            self.update_virtual_sons(self.root)
            return self.root,time.time()-t0,-1,-1
        
        if self.search(key)[0] == None:
            self.tsize += 1
            t0 = time.time()
            leftNode = True
            parent = None
            node = self.root
            while node.is_real_node():
                parent = node
                parent.height += 1
                if key > node.key: node = node.right  
                else: node = node.left
            
            if key < parent.key:
                parent.left = AVLNode(key, val)
                parent.left.parent = parent
            else:
                parent.right = AVLNode(key, val)
                parent.right.parent = parent
                leftNode = False

            resNode = parent.left if leftNode else parent.right
            resNode.height += 1
            self.update_virtual_sons(resNode)
            self.update_bf(resNode)
            self.update_relations(resNode, "insertion")
            
            node = resNode
            made_rolls = False
            while node.is_real_node() and not made_rolls:
                made_rolls = self.rolls(node, "insertion")
                node = node.parent
            
            return resNode, time.time()-t0, -1, -1
        return None, -1, -1, -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        parent = node.parent
        if self.num_children(node) < 2:
            child = self.get_childeren(node)[0] #if len(self.get_childeren(node)) != 0 else self.virtual_node
            self.update_relations(node, "deletion")
            if parent is self.virtual_node: self.root = child
            elif node.key < parent.key: parent.left = child
            else: parent.right = child
        else:
            succ = node.successor
            succ_parent = succ.parent
            succ_child = self.get_childeren(succ)[0] #if len(self.get_childeren(node)) != 0 else self.virtual_node ##
            self.update_relations(node, "deletion")
            
            print(succ.key,succ_parent.key,succ_child.key)
            succ_parent.left = succ_child
            succ_child.parent = succ_parent
            succ.left = node.left
            succ.right = node.right
            succ.parent = parent
            if parent is self.virtual_node: self.root = succ
            elif node.key < parent.key: parent.left = succ
            else: parent.right = succ



            

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        def rec_avl_to_list(node, ls):
            if not node.is_real_node(): # Goes to the end of the left tree
                return []
            rec_avl_to_list(node.left, ls)
            ls.append((node.key, node.value)) # Adds the node into the list
            rec_avl_to_list(node.right, ls) # Continues to the right tree
            return ls
        return rec_avl_to_list(self.root, [])

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.tsize

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        return self.root.height if self.root != None else -1 # If the tree is empty, the function will return -1

    def update_height(self, node):
        while node.is_real_node():
            node.height = max(node.left.height, node.right.height) + 1
            node = node.parent
    
    def update_bf(self, node):
        while node.is_real_node():
            node.bf = node.left.height - node.right.height
            node = node.parent
    
    def update_virtual_sons(self, node):
        node.left = self.virtual_node
        node.right = self.virtual_node
    

    def get_childeren(self, node):
        ls = []
        if node.left.is_real_node(): ls.append(node.left)
        if node.right.is_real_node(): ls.append(node.right)
        if len(ls) == 0: ls.append(self.virtual_node)
        return ls
    
    def num_children(self, node):
        return len(self.get_childeren(node))
    
    """returns the successor of a node

    @pre: node in AVLTree
    @rtype: AVLnode
    """
    def find_succ(self, node):
        successor = node
        if node.right.is_real_node():
            successor = successor.right
            while successor.left.is_real_node():
                successor = successor.left
            return successor
        
        else:
            parent = successor.parent
            while parent.is_real_node():
                if successor.key < parent.key:
                    successor = parent
                    break
                else:
                    successor = parent
                    parent = successor.parent
            return successor if parent.is_real_node() else self.virtual_node
    
    """returns the predecessor of a node

    @pre: node in AVLTree
    @rtype: AVLnode
    """
    def find_pred(self, node):
        predecessor = node
        if node.left.is_real_node():
            predecessor = predecessor.left
            while predecessor.right.is_real_node():
                predecessor = predecessor.right
            return predecessor
        
        else:
            parent = predecessor.parent
            while parent.is_real_node():
                if predecessor.key > parent.key:
                    predecessor = parent
                    break
                else:
                    predecessor = parent
                    parent = predecessor.parent
            return predecessor if parent.is_real_node() else self.virtual_node
    
    
    def update_relations(self, node, op):
        if self.tsize <= 1:
            pass
        
        elif op == "insertion":
            succ = self.find_succ(node)
            pred = self.find_pred(node)  
            node.successor = succ
            node.predecessor = pred
            if succ.is_real_node(): succ.predecessor = node
            if pred.is_real_node(): pred.successor = node
        
        elif op == "deletion":
            if node.successor.is_real_node(): node.successor.predecessor = node.predecessor
            if node.predecessor.is_real_node(): node.predecessor.successor = node.successor

    
    def one_roll(self, node): # the "easy" roll where its big->mid->small or opposite
        parent = node.parent
        if node.bf == 2:
            left = node.left
            right = left.right

            node.left = right
            right.parent = node
            left.right = node
            left.parent = parent
            node.parent = left
            
            if parent.is_real_node(): # we need to update the parent fields
                if node.key > parent.key:
                    parent.right = left
                else:
                    parent.left = left
            else: self.root = left # parent was None meaning the right is now the root

        elif node.bf == -2:
            right = node.right
            left = right.left

            node.right = left
            left.parent = node
            right.left = node
            right.parent = parent
            node.parent = right
            if parent.is_real_node(): # we need to update the parent fields
                if node.key > parent.key:
                    parent.right = right
                else: 
                    parent.left = right
            else: self.root = right # parent was None meaning the right is now the root
        
        self.update_height(node)
        self.update_bf(node)
        return True

    def two_rolls(self, node, op):
        parent = node.parent
        if node.bf == 2:
            left = node.left
            right = left.right
            if (left.bf == 1 and op == "insertion") or (left.bf >= 0 and op == "deletion"):
                return self.one_roll(node)
            
            
            node.left = right
            right.parent = node
            left.right = right.left
            right.left.parent = left
            right.left = left
            left.parent = right
            return self.one_roll(node)

        elif node.bf == -2:
            right = node.right
            right = right.left
            if (right.bf == -1 and op == "insertion") or (right.bf <= 0 and op == "deletion"):
                return self.one_roll(node)
            
            
            node.right = left
            left.parent = node
            right.left = left.right
            left.right.parent = right
            left.right = right
            right.parent = left
            return self.one_roll(node)
        
        self.update_height(node)
        self.update_bf(node)
        return True

    def rolls(self, node, op):
        if abs(node.bf) == 2:
                self.two_rolls(node, op)
        return False


    def __repr__(self): 
        print("the format of a node is x,y,z where x:key, y:height, z:bf") #added explantion of printed values
        def printree(root):
            if not root.is_real_node():
                return ["#"]

            node_info = str(root.key)+","+str(root.height)+","+str(root.bf) # edited
            left, right = printree(root.left), printree(root.right)

            lwid = len(left[-1])
            rwid = len(right[-1])
            nodewid = len(node_info) # edited

            result = [(lwid + 1) * " " + node_info + (rwid + 1) * " "] # edited

            ls = len(left[0].rstrip())
            rs = len(right[0]) - len(right[0].lstrip())
            result.append(ls * " " + (lwid - ls) * "_" + "/" + nodewid * " " + "\\" + rs * "_" + (rwid - rs) * " ") # edited

            for i in range(max(len(left), len(right))):
                row = ""
                if i < len(left):
                    row += left[i]
                else:
                    row += lwid * " "
                    
                row += (nodewid + 2) * " "  # edited

                if i < len(right):
                    row += right[i]
                else:
                    row += rwid * " "

                result.append(row)

            return result

        return '\n'.join(printree(self.root))