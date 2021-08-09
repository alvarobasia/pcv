from interface.output_connect_info import print_connect_info
from infra.connected_component import Connected_Component
from interface.write_search import write_search
from infra.graph_search import Graph_Search
from utils.read_file import read_file
from utils.search_type import Search_type
from utils.representation_type import Representation
from domain.Graph import Graph
from typing import Any
from interface.output_graph_info import print_graph_info
from infra.graph_info import Graph_info
import json


class Input_args:
    data: Any
    representation: Representation
    search_type: Search_type
    initial: int
    infos: str
    connect: str
    file: str
    graph: Graph
    sparse: bool

    def __init__(self, file) -> None:
        self.data = json.load(file)
        self.representation = Representation.ADJACENCY_LIST
        self.search_type = Search_type.WIDE_SEARCH
        self.initial = [-1, '']
        self.infos = ''
        self.connect = ''
        self.graph = None
        self.sparse = True
        if 'file' in self.data:
            self.file = self.data['file']
        else:
            raise Exception(
                'Informe o nome do arquivo contendo o grafo.')
        if 'representation' in self.data and self.data['representation'] == 'matriz':
            self.representation = Representation.ADJACENCY_MATRIX

        if 'sparse' in self.data and self.data['sparse'] == False:
            self.sparse = False

        if 'search_type' in self.data and self.data['search_type'] == 'deep':
            self.search_type = Search_type.DEEP_SEARCH

        if 'search' in self.data:
            if 'init' in self.data['search'] and 'output' in self.data['search']:
                self.initial = [self.data['search']['init'],
                                self.data['search']['output']]

        if 'infos' in self.data:
            if 'output' in self.data['infos']:
                self.infos = self.data['infos']['output']

        if 'connect' in self.data:
            if 'output' in self.data['connect']:
                self.connect = self.data['connect']['output']

        if self.initial[1] == self.infos or self.initial[1] == self.connect or self.infos == self.connect:
            raise Exception(
                'Escolha nomes diferentes para os arquivos de output')

    def exec(self):
        result = read_file(self.file)
        self.graph = Graph(
            result['nodes'], result['edges'], result['values'], self.sparse)
        if self.initial[0] != -1:
            self.__search_in_graph(self.initial[1])
        if self.connect != '':
            self.__connect_components(self.connect)
        if self.infos != '':
            self.__generate_infos(self.infos)

    def __generate_infos(self, file_name):
        info = Graph_info(self.graph, self.representation).get_infos()
        print(
            f"====> SALVANDO NO ARQUIVO {file_name} AS INFORMAÇÕES SOBRE O GRAFO<====")
        print_graph_info(file_name, info)

    def __search_in_graph(self, file_name):
        if self.search_type == Search_type.DEEP_SEARCH:
            s = Graph_Search(self.graph, self.representation).search_deep(
                self.initial[0])
        else:
            s = Graph_Search(self.graph, self.representation).search_wide(
                self.initial[0])
        print(
            f"====> SALVANDO NO ARQUIVO {file_name} O RESULTADO DA BUSCA <====")
        write_search(file_name, s)

    def __connect_components(self, file_name):
        c = Connected_Component(
            self.graph, self.representation, self.search_type).get_info()
        print(
            f"====> SALVANDO NO ARQUIVO {file_name} OS COMPONENTES CONEXOS<====")
        print_connect_info(file_name, c)
