# id1: 326528494
# name1: Erez Avrahami
# username1: erezavrahami
# id2: 326283264
# name2: Omer Lemel
# username2: lemel


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
            search_time += 1 # Add 1 to search_time for every node we visited
            if node.key == key: return node, search_time
            elif key < node.key: node = node.left
            else: node = node.right
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
        self.tsize += 1
        if self.root == None:
            self.root = AVLNode(key, val)
            self.root.parent = self.virtual_node
            self.create_virtual_sons(self.root)
            self.update_node(self.root)
            return self.root, 1, 0, 0
        

        parent = None
        node = self.root
        resNode = AVLNode(key, val)
        self.create_virtual_sons(resNode)
        self.update_node(resNode)
        search_time = 0 # Initialize seach_time
        while node.is_real_node():
            search_time += 1
            parent = node
            if key > node.key: node = node.right  
            else: node = node.left
        
        if key < parent.key:
            parent.left = resNode
            resNode.parent = parent
        else:
            parent.right = resNode
            resNode.parent = parent

        roll_count = 0
        height_changes = 0
        tmpNode = resNode.parent # we get height_changes only from resNode.parent and up the tree
        while tmpNode.is_real_node() and roll_count == 0:
            tmp_height = tmpNode.height
            self.update_node(tmpNode)
            if tmp_height == tmpNode.height and tmpNode.height != 0: break # there was no change in height in tmpNode so there wont be changes upwards as well
            height_changes += 1
            if self.is_avl: 
                roll_count = self.rolls(tmpNode, "insertion", roll_count) # if a roll is made then made_rolls = True
            tmpNode = tmpNode.parent
        if roll_count != 0: height_changes -= 1 # if we made a roll then the roll replaces the height change
        return resNode, search_time+1, roll_count, height_changes


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        self.tsize -= 1
        if self.tsize == 0:
            self.root = None # root parent is virtual_node so we cant do self.root = self.root.parent
            return

        parent = node.parent
        if self.num_children(node) < 2:
            child = self.get_childeren(node)[0] # if len(self.get_childeren(node)) != 0 else self.virtual_node
            if parent is self.virtual_node: self.root = child
            elif node.key < parent.key: parent.left = child
            else: parent.right = child
            
            tmpNode = parent

        else:
            succ = self.find_succ(node)
            succ_parent = succ.parent
            succ_child = self.get_childeren(succ)[0]
            
            if succ_parent is not node: succ_parent.left = succ_child # if succ_parent is node then succ was node.right
            if succ_child.is_real_node(): 
                succ_child.parent = succ_parent if succ_parent is not node else succ # if succ_parent is node then succ_child.parent shouldn't change
            succ.left = node.left
            succ.left.parent = succ
            succ.right = node.right if node.right is not succ else succ.right # if node.right is succ then succ shifted up and succ.right stayed the same
            succ.right.parent = succ
            succ.parent = parent
            if parent is self.virtual_node: self.root = succ
            elif node.key < parent.key: parent.left = succ
            else: parent.right = succ   
            
            tmpNode = succ_parent if succ_parent is not node else succ
        
        while tmpNode.is_real_node():
            self.update_node(tmpNode)
            if self.is_avl: self.rolls(tmpNode, "deletion",0)
            tmpNode = tmpNode.parent

            

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        def rec_avl_to_list(node, ls):
            if not node.is_real_node():
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
        return self.root.height if self.root != None else -1 # if the tree is empty, the function will return -1
    
    def update_node(self, node):
        node.height = max(node.left.height, node.right.height) + 1
        node.bf = node.left.height - node.right.height
    
    def create_virtual_sons(self, node):
        node.left = self.virtual_node
        node.right = self.virtual_node
    
    def get_childeren(self, node):
        ls = []
        if node.left.is_real_node(): ls.append(node.left)
        if node.right.is_real_node(): ls.append(node.right)
        if len(ls) == 0: ls.append(self.virtual_node)
        return ls
    
    def num_children(self, node):
        res = self.get_childeren(node)
        return len(res) if res[0] is not self.virtual_node else 0
    
    """returns the successor of a node

    @pre: node in AVLTree
    @rtype: AVLnode
    """
    def find_succ(self, node):
        successor = node
        if node.right.is_real_node(): # if node has a right son then the successor is on the right sub-tree of node
            successor = successor.right
            while successor.left.is_real_node():
                successor = successor.left # the successor is the bottom-left (minimum) node the the right sub-tree 
            return successor
        
        else: # node has no right son
            parent = successor.parent
            while parent.is_real_node():
                if successor.key < parent.key: # if true both current successor and node are on the left sub-tree of parent
                    successor = parent
                    break
                else:
                    successor = parent
                    parent = successor.parent
            return successor if parent.is_real_node() else self.virtual_node
    

    def one_roll(self, node, roll_count): # the "easy" roll where its big->mid->small or opposite
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
            self.update_node(node)
            self.update_node(left)

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
            self.update_node(node)
            self.update_node(right)
        return roll_count+1

    def two_rolls(self, node, op, roll_count):
        if node.bf == 2:
            left = node.left
            right = left.right
            if (left.bf == 1 and op == "insertion") or (left.bf >= 0 and op == "deletion"):
                return self.one_roll(node, roll_count)
            
            
            node.left = right
            right.parent = node
            left.right = right.left
            right.left.parent = left
            right.left = left
            left.parent = right
            self.update_node(left)
            return self.one_roll(node, roll_count+1)

        elif node.bf == -2:
            right = node.right
            left = right.left
            if (right.bf == -1 and op == "insertion") or (right.bf <= 0 and op == "deletion"):
                return self.one_roll(node, roll_count)
            
            
            node.right = left
            left.parent = node
            right.left = left.right
            left.right.parent = right
            left.right = right
            right.parent = left
            self.update_node(right)
            return self.one_roll(node, roll_count+1)


    def rolls(self, node, op, roll_count):
        if abs(node.bf) == 2:
                return self.two_rolls(node, op, roll_count)
        return roll_count


    def __repr__(self): 
        print("the format of a node is x,y,z where x:key, y:height, z:bf") #added explantion of printed values
        def printree(root):
            if (root == None) or (not root.is_real_node()):
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