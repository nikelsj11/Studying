#-*- coding: utf-8 -*-


class EmptyNode(object):
    """Пустой узел"""
    __call__ = lambda self: []
    down_tree = lambda self, value: Node(value)


class Node(object):
    """Класс узла бинарного дерева

    Хранит значение узла дерева и его левого и правого предков.
    """
    left = right = EmptyNode()

    def __init__(self, value):
        self.value = value

    def down_tree(self, value):
        """Конструктор дерева

        Элемент value спускается по правилу, если значение больше значения текущего
        узла идем в правый узел, если меньше идем в левый, если следующего узла нет, создаем новый узел и
        присваиваем это значение ему.

        """
        if self.value > value:
            self.left = self.left.down_tree(value)
        else:
            self.right = self.right.down_tree(value)
        return self

    __call__ = lambda self: self.left() + [self.value] + self.right()


def tree_sort(arr):
    """Сортировка с помощью бинарного дерева

    Алгоритм сортировки, заключающийся в построении двоичного дерева поиска по ключам массива,
    с последующей сборкой результирующего массива путём обхода узлов построенного дерева в необходимом
    порядке следования ключей.
    Средняя сложность: O(n*log(n))

    -array - список который требуется отсортировать.

    На выход отсортированный список.
    """
    tree = Node(arr.pop(0))
    for item in arr:
        tree.down_tree(item)
    return tree()
