from typing import Any, List
from domain.Graph import Graph
from utils.representation_type import Representation
from utils.search_type import Search_type


class Connected_Component:
    result: List[int]
    graph: Graph
    tag: int
    representation: Representation
    search: Search_type

    def __init__(self, graph: Graph, representation: Representation, search: Search_type):
        self.tag = 0
        self.graph = graph
        self.result = [0 for _ in range(graph.nodes_number)]
        self.representation = representation
        self.search = search

    def get_info(self):
        graph: Any
        if self.representation == Representation.ADJACENCY_LIST:
            graph = self.graph.get_list_representation()
        else:
            graph = self.graph.get_matrix_representation()

        for u in range(len(graph)):
            if self.result[u] == 0:
                self.tag = self.tag + 1
                self.__get_correct_search_method()(u, graph)
        return self.result

    def __get_correct_search_method(self):
        if self.representation == Representation.ADJACENCY_LIST:
            if self.search == Search_type.WIDE_SEARCH:
                return self.__wide_search_list_connect
            else:
                return self.__deep_search_list_connect
        else:
            if self.search == Search_type.WIDE_SEARCH:
                return self.__wide_search_matrix_connect
            else:
                return self.__deep_search_matrix_connect

    def __deep_search_list_connect_rec(self, el, graph):
        self.result[el] = self.tag
        for v in graph[el]:
            if self.result[v[0]] == 0:
                self.__deep_search_list_connect_rec(v[0], graph)

    def __deep_search_matrix_connect_rec(self, el, graph):
        self.result[el] = self.tag
        for i, v in enumerate(graph[el]):
            if v != 0 and self.result[i] == 0:
                self.__deep_search_matrix_connect_rec(i, graph)

    def __wide_search_list_connect(self, el, graph):
        self.result[el] = self.tag
        Q = [el]
        while len(Q) != 0:
            u = Q.pop(0)
            for v in graph[u]:
                if self.result[v[0]] == 0:
                    Q.append(v[0])
                    self.result[v[0]] = self.tag

    def __wide_search_matrix_connect(self, el, graph):
        self.result[el] = self.tag
        Q = [el]
        while len(Q) != 0:
            u = Q.pop(0)
            for i, v in enumerate(graph[u]):
                if v != 0 and self.result[i] == 0:
                    Q.append(i)
                    self.result[i] = self.tag

    def __deep_search_list_connect(self, el, graph):
        self.result[el] = self.tag
        Q = [el]
        while len(Q) != 0:
            u = Q[-1]
            pop = True
            for v in graph[u]:
                if self.result[v[0]] == 0:
                    pop = False
                    Q.append(v[0])
                    self.result[v[0]] = self.tag
                    break
            if pop:
                Q.pop()

    def __deep_search_matrix_connect(self, el, graph):
        self.result[el] = self.tag
        Q = [el]
        while len(Q) != 0:
            u = Q[-1]
            pop = True
            for i, v in enumerate(graph[u]):
                if v != 0 and self.result[i] == 0:
                    pop = False
                    Q.append(i)
                    self.result[i] = self.tag
                    break
            if pop:
                Q.pop()
