#-*- coding: utf-8 -*-


def prim(graph, start_vertex=0):
    """Aлгоритм Прима

    Алгоритм построения минимального остовного дерева взвешенного связного
    неориентированного графа.
    Сложность: Ο(V**2)

    -graph - граф представленный в виде матрицы смежности.
    -start_vertex - номер начальной вершины 0..n-1.

    На выход будет возвращены 2 значения [вес графа, путь(последовательный список вершин)].
    """
    weight = 0
    visited = [start_vertex]
    _max = float('inf')
    while len(visited) != len(graph):
        _min = _max
        _min_index = None
        for visited_vertex in visited:
            for index, vertex in enumerate(graph[visited_vertex]):
                if vertex != _max and 0 < vertex < _min and index not in visited:
                    _min = vertex
                    _min_index = index
        if _min_index is None:
            return [None]*2
        weight += _min
        visited.append(_min_index)
    return [weight, visited]


if __name__ == "__main__":
    _ = float('inf')

    graph_in = [[0, 7, _, 5, _, _, _],
                [7, 0, 8, 9, 7, _, _],
                [_, 8, 0, _, 5, _, _],
                [5, 9, _, 0, 15, 6, _],
                [_, 7, 5, 15, 0, 8, 9],
                [_, _, _, 6, 8, 0, 11],
                [_, _, _, _, 9, 11, 0]]

    result = prim(graph_in)
    print 'Вес: ', result[0]
    print 'Путь: ', result[1]
    # >>> Вес: 39
    # >>> Путь: [0, 3, 5, 1, 4, 2, 6]

    print '\n'

    graph_in_two = [[0, 1, _, _],
                    [1, 0, 2, _],
                    [_, 2, 0, _],
                    [_, _, _, 0]]

    result_two = prim(graph_in_two)
    print 'Вес: ', result_two[0]
    print 'Путь: ', result_two[1]
    # >>> Вес: None
    # >>> Путь: None
