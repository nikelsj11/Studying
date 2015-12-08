#-*- coding: utf-8 -*-
from operator import itemgetter
from data_structure.union_find import UnionFind


def kruskal(edges):
    """Алгоритм Крускала

    Эффективный алгоритм построения минимального остовного дерева взвешенного связного
    неориентированного графа.
    Сложность: Ο(E*logV)

    -edges - граф представленный в виде списка ребер [("FROM", "TO", weight), ...].

    На выход будет возвращены 2 значения [вес графа, последовательный список ребер вошедших в остовное дерево].
    """
    union_find = UnionFind()
    res_edges, res_weight = [], 0

    for edge in sorted(edges, key=itemgetter(2)):
        start, stop, weight = edge

        if not union_find[start] == union_find[stop]:
            res_edges.append(edge)
            res_weight += weight
            union_find.union(start, stop)

    return [res_weight, res_edges]


if __name__ == "__main__":
    in_edges = [("A", "B", 7),
                ("A", "D", 5),
                ("B", "C", 8),
                ("B", "D", 9),
                ("B", "E", 7),
                ("C", "E", 5),
                ("D", "E", 15),
                ("D", "F", 6),
                ("E", "F", 8),
                ("E", "G", 9),
                ("F", "G", 11)]

    result = kruskal(in_edges)
    print 'Вес: ', result[0]
    # >>> 39
    print 'Ребра: ', result[1]
    # >>> [('A', 'D', 5), ('C', 'E', 5), ('D', 'F', 6), ('A', 'B', 7), ('B', 'E', 7), ('E', 'G', 9)]