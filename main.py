from sys import path
from domain.Graph import Graph
import matplotlib.pyplot as plt
from utils.read_file import read_file
from construct.construct_solution import Construct_Solution

file = input("Informe o grafo: ")
time = input("Informe o tempo limite (s): ")

f = read_file(file)

graph = Graph(f['nodes'], f['edges'], f['values'], True)

result = Construct_Solution(graph, int(time)).final_result

with open('output.txt', "w") as fd:
    fd.write(f'{result[1]}\n')
    for v in result[0]:
        fd.write(f'{v} ')

print('Um arquivo com o nome output.txt foi escrito na raiz do projeto com a solução encontrada.')
