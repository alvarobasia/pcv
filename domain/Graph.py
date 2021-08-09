from typing import List, Tuple
import numpy as np
from scipy.sparse import *
from scipy import *


class Graph:
    nodes_number: int
    edges_number: int
    values: List[List[int]]
    sparse: bool

    def __init__(self, nodes_number: int, edges_number: int, values: List[List[int]], sparse: bool) -> None:
        self.edges_number = edges_number
        self.nodes_number = nodes_number
        self.values = values
        self.sparse = sparse

    def get_matrix_representation(self) -> List[List[int]]:
        if self.sparse:
            matrix = self.__sparse_matrix()
        else:
            matrix = self.__native()

        for v in self.values:
            matrix[v[0]][v[1]] = v[2]
            matrix[v[1]][v[0]] = v[2]
        return matrix

    def get_list_representation(self) -> List[Tuple[int]]:
        list = [[] for x in range(self.nodes_number)]
        for v in self.values:
            list[v[0]].append((v[1], v[2]))
            list[v[1]].append((v[0], v[2]))
        return list

    def __sparse_matrix(self):
        matriz = csc_matrix(
            (self.nodes_number, self.nodes_number), dtype=np.float64).toarray()
        return matriz

    def __native(self):
        matriz = [[]for x in range(self.nodes_number + 1)]
        for v in range(len(matriz)):
            matriz[v] = [0 for x in range(self.nodes_number + 1)]
        return matriz
