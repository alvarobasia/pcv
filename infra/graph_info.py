from typing import List
from domain.Graph import Graph
from utils.representation_type import Representation


class Graph_info:
    graph: Graph
    representation: Representation

    def __init__(self, graph: Graph, representation: Representation):
        self.graph = graph
        self.representation = representation

    def get_infos(self):
        if self.representation == Representation.ADJACENCY_LIST:
            return self.__get_infos_list()
        else:
            return self.__get_infos_matrix()

    def __get_infos_list(self):
        graph = self.graph.get_list_representation()
        result = [0 for _ in range(self.graph.nodes_number)]
        for v in graph:
            for f in v:
                result[f[0]] = result[f[0]] + 1

        return self.__build_object(result)

    def __get_infos_matrix(self):
        graph = self.graph.get_matrix_representation()
        result = [0 for _ in range(self.graph.nodes_number)]
        for v in graph:
            for f, l in enumerate(v):
                if l != 0:
                    result[f] = result[f] + 1
        return self.__build_object(result)

    def __build_object(self, result: List[int],):
        max_value = max(result)
        min_value = min(result)
        freq_relative = [0 for x in range(max_value + 1)]
        for value in result:
            freq_relative[value] = freq_relative[value] + 1
        freq_relative = [x / sum(freq_relative)
                         for x in freq_relative]
        return {'max_degree': {
            'n': max_value,
            'v': result.index(max_value)
        }, 'min_degree': {
            'n': min_value,
            'v': result.index(min_value)
        },
            'avg': round(sum(result) / len(result), 10),
            'freq': freq_relative
        }
