from sys import path
from domain.Graph import Graph
from utils.read_file import read_file
from construct.construct_solution import Construct_Solution
f = read_file('./graph/ali535.txt')
graph = Graph(f['nodes'], f['edges'], f['values'], True)
Construct_Solution(graph)
