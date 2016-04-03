#-*- coding: utf-8 -*-


def dfs(graph, vertex=0):
    """Поиск в глубину (Depth-first search, DFS)

    Один из методов обхода графа. Нерекурсивный вариант.
    Сложность: O(|E|+|V|)

    -graph - граф представленный в виде матрицы смежности.
    -vertex - начальная вершина. По умолчанию 0.

    ~На выход будет возвращен список посещенных ребер.
    """
    visited = [vertex]
    vertexes = [vertex]
    graph_passed = False
    while not graph_passed:
        graph_passed = True
        for item in range(len(graph)):
            for vertex in vertexes:
                if graph[vertex][item] and not item in visited:
                    visited.append(item)
                    vertexes.append(item)
                    graph_passed = False
    return visited
