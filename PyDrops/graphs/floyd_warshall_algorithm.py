#-*- coding: utf-8 -*-


def floyd_warshall(graph):
    """Алгоритм Флойда — Уоршелла

       Динамический алгоритм для нахождения кратчайших расстояний между всеми
       вершинами взвешенного ориентированного графа.
       Сложность: Ο(n**3)

       -graph - граф представленный в виде матрицы смежности.

       На выход получаем матрицу кратчайших расстояний между вершинами.
    """
    for table in range(len(graph)):
        for row in range(len(graph)):
            for column in range(len(graph)):
                graph[row][column] = min(graph[row][column], graph[row][table]+graph[table][column])
    return graph


def floyd_warshall_reachability(graph):
    """Алгоритм Флойда — Уоршелла построения матрицы достижимости

       Динамический алгоритм Флойда — Уоршелла для нахождения замыкания отношения E по транзитивности.
       Сложность: Ο(n**3)

       -graph - граф представленный в виде матрицы смежности (0 or 1)

       На выход получаем матрицу достижимости.
    """
    for table in range(len(graph)):
        for row in range(len(graph)):
            for column in range(len(graph)):
                graph[row][column] = graph[row][column] or (graph[row][table] and graph[table][column])
    return graph


if __name__ == "__main__":
    graph_in = [[float("inf"), 2, 5],
                [float("inf"), float("inf"), 1],
                [1, float("inf"), float("inf")]]

    print floyd_warshall(graph_in)
    # >>> [[4, 2, 3], [2, 4, 1], [1, 3, 4]]

    graph_in = [[0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 1],
                [0, 0, 1, 0]]

    print floyd_warshall_reachability(graph_in)
    # >>> [[0, 1, 1, 1], [0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1]]