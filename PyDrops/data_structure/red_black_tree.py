#-*- coding: utf-8 -*-


class RBNode(object):
    red = False
    left = None
    right = None
    parent = None

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class RBTree(object):
    nil = RBNode(None)
    root = nil

    def insert(self, value):
        self._insert(RBNode(value))

    def _insert(self, node):
        nil = self.nil
        root = self.root
        while root != self.nil:
            nil = root
            if node.value < root.value:
                root = root.left
            else:
                root = root.right
        node.parent = nil
        if nil == self.nil:
            self.root = node
        elif node.value < nil.value:
            nil.left = node
        else:
            nil.right = node
        node.left = self.nil
        node.right = self.nil
        node.red = True
        self._fix_up_tree_after_insert(node)

    def _fix_up_tree_after_insert(self, node):
        while node.parent.red:
            if node.parent == node.parent.parent.left:
                tmp = node.parent.parent.right
                if tmp.red:
                    node.parent.red = False
                    tmp.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self._right_rotate(node.parent.parent)
            else:
                tmp = node.parent.parent.left
                if tmp.red:
                    node.parent.red = False
                    tmp.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self._left_rotate(node.parent.parent)
        self.root.red = False

    def _left_rotate(self, node):
        tmp = node.right
        node.right = tmp.left
        if tmp.left != self.nil:
            tmp.left.parent = node
        tmp.parent = node.parent
        if node.parent == self.nil:
            self.root = tmp
        elif node == node.parent.left:
            node.parent.left = tmp
        else:
            node.parent.right = tmp
        tmp.left = node
        node.parent = tmp

    def _right_rotate(self, node):
        tmp = node.left
        node.left = tmp.right
        if tmp.right != self.nil:
            tmp.right.parent = node
        tmp.parent = node.parent
        if node.parent == self.nil:
            self.root = tmp
        elif node == node.parent.right:
            node.parent.right = tmp
        else:
            node.parent.left = tmp
        tmp.right = node
        node.parent = tmp

    def min(self, subtree=False):
        frm = subtree or self.root
        minimal = frm

        while frm.left:
            minimal = frm
            frm = frm.left

        return minimal.value if not subtree else minimal

    def max(self):
        frm = self.root
        maximal = frm.value

        while frm.right:
            maximal = frm.value
            frm = frm.right

        return maximal

    def search(self, for_what):
        tmp = self.root
        while tmp:
            if tmp.value == for_what:
                return tmp
            tmp = tmp.left if tmp.value > for_what else tmp.right
        return None

    def delete(self, value):
        self._delete(self.search(value))

    def _delete(self, node):
        def substitute(root_node, replacement):
            if root_node == self.root:
                self.root = replacement
            elif root_node.parent.left == root_node:
                root_node.parent.left = replacement
            else:
                root_node.parent.right = replacement
            replacement.parent = root_node.parent
            if not root_node.red:
                self._fix_up_tree_after_delete(replacement)

        if node.left == self.nil and node.right == self.nil:
            substitute(node, self.nil)
        elif node.left != self.nil and node.right != self.nil:
            minimal = self.min(subtree=node.right)
            node.value = minimal.value
            self._delete(minimal)
        elif node.left == self.nil:
            substitute(node, node.right)
        elif node.right == self.nil:
            substitute(node, node.left)

    def _fix_up_tree_after_delete(self, node):
        while node != self.root and not node.red:
            if node == node.parent.left:
                tmp = node.parent.right
                if tmp.red:
                    tmp.red = False
                    node.parent.red = True
                    self._left_rotate(node.parent)
                    tmp = node.parent.right
                if not tmp.left.red and not tmp.right.red:
                    tmp.red = True
                    node = node.parent
                else:
                    if not tmp.right.red:
                        tmp.left.red = False
                        tmp.red = True
                        self._right_rotate(tmp)
                        tmp = node.parent.right
                    tmp.red = node.parent.red
                    node.parent.red = False
                    tmp.right.red = False
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                tmp = node.parent.left
                if tmp.red:
                    tmp.red = False
                    node.parent.red = True
                    self._right_rotate(node.parent)
                    tmp = node.parent.left
                if not tmp.right.red and not tmp.left.red:
                    tmp.red = True
                    node = node.parent
                else:
                    if not tmp.left.red:
                        tmp.right.red = False
                        tmp.red = True
                        self._left_rotate(tmp)
                        tmp = node.parent.left
                    tmp.red = node.parent.red
                    node.parent.red = False
                    tmp.left.red = False
                    self._right_rotate(node.parent)
                    node = self.root
        node.red = False
