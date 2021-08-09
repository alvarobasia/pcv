from typing import final
from domain.Graph import Graph
from utils.representation_type import Representation


class Graph_Search:
    graph: Graph
    representation: Representation

    def __init__(self, graph: Graph, representation: Representation):
        self.graph = graph
        self.representation = representation

    def search_wide(self, el: int):
        if self.representation == Representation.ADJACENCY_LIST:
            return self.__search_wide_list(el)
        else:
            return self.__search_wide_matrix(el)

    def __search_wide_list(self, el: int):
        graph = self.graph.get_list_representation()
        desc = [0 for i in range(self.graph.nodes_number)]
        Q = [el]
        L = [0 for i in range(self.graph.nodes_number)]
        R = [[el, 0]]
        desc[el] = 1
        while len(Q) != 0:
            u = Q.pop(0)
            for v in graph[u]:
                if desc[v[0]] == 0:
                    Q.append(v[0])
                    level = L[u] + 1
                    L[v[0]] = level
                    R.append([v[0], level])
                    desc[v[0]] = 1
        return R

    def __search_wide_matrix(self, el: int):
        graph = self.graph.get_matrix_representation()
        desc = [0 for i in range(self.graph.nodes_number)]
        Q = [el]
        R = [[el, 0]]
        L = [0 for i in range(self.graph.nodes_number)]
        desc[el] = 1
        while len(Q) != 0:
            u = Q.pop(0)
            for i, v in enumerate(graph[u]):
                if v != 0 and desc[i] == 0:
                    level = L[u] + 1
                    L[i] = level
                    Q.append(i)
                    R.append([i, level])
                    desc[i] = 1
        return R

    def search_deep(self, el: int):
        if self.representation == Representation.ADJACENCY_LIST:
            return self.__search_deep_list(el)
        else:
            return self.__search_deep_matrix(el)

    def __search_deep_list(self, el: int):
        graph = self.graph.get_list_representation()
        desc = [0 for i in range(self.graph.nodes_number)]
        S = [el]
        L = [0 for i in range(self.graph.nodes_number)]
        R = [[el, 0]]
        desc[el] = 1
        while len(S) != 0:
            u = S[-1]
            pop = True
            for v in graph[u]:
                if desc[v[0]] == 0:
                    pop = False
                    S.append(v[0])
                    level = L[u] + 1
                    L[v[0]] = level
                    R.append([v[0], level])
                    desc[v[0]] = 1
                    break
            if pop:
                p = S.pop()

        return R

    def __search_deep_matrix(self, el: int):
        graph = self.graph.get_matrix_representation()
        desc = [0 for i in range(self.graph.nodes_number)]
        S = [el]
        L = [0 for i in range(self.graph.nodes_number)]
        R = [[el, 0]]
        desc[el] = 1
        while len(S) != 0:
            u = S[-1]
            pop = True
            for i, v in enumerate(graph[u]):
                if v != 0 and desc[i] == 0:
                    pop = False
                    S.append(i)
                    level = L[u] + 1
                    L[i] = level
                    R.append([i, level])
                    desc[i] = 1
                    break
            if pop:
                p = S.pop()

        return R
