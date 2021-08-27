from hashlib import new
from typing import Any, List, Tuple
import math
import numpy as np
from domain.Graph import Graph
import random
import time


class Construct_Solution:
    list: List[Tuple[float]]
    nodes: int
    start_time: int
    time_to_execute: int
    final_result: Any

    def __init__(self, graph: Graph, time_to_execute: int) -> None:
        self.list = graph.get_list_representation()
        self.nodes = graph.nodes_number
        self.time_to_execute = time_to_execute
        self.start_time = time.time()
        x = self.construct()
        self.sa(x)

    def construct(self):
        current = random.randrange(0, self.nodes)
        solution = self.make_solution(current)
        final = [solution, self.calc(solution)]
        return final

    def make_solution(self, init):
        solution = [init]
        next_nodes = self.list[init]
        while len(solution) != len(self.list):
            min = (None, float('inf'))
            for node in next_nodes:
                minor = min[1] > node[1]
                if minor and node[0] not in solution:
                    min = node
            current = min[0]
            solution.append(min[0])
            next_nodes = self.list[current]
        solution.append(init)
        return solution

    def calc(self, solution):
        u = None
        value = 0
        for v in solution:
            if u == None:
                u = v
                continue
            else:
                for o in self.list[v]:
                    if o[0] == u:
                        value = value + o[1]
                u = v
        return value

    def get_edges_from_solution(self, solution):
        edges = []
        node = None
        for v in solution:
            if node == None:
                node = v
                continue
            else:
                edges.append([node, v])
                node = v
        return edges

    def swap(self, solution, init, last):
        new_solution = [None for _ in solution]
        interval = solution[init:last]
        aux = [x for x in range(init, last)]
        interval = interval[::-1]
        y = 0
        for i, v in enumerate(solution):
            if y < len(aux) and i == aux[y]:
                y = y + 1
                new_solution[i] = interval.pop(0)
                continue
            new_solution[i] = v

        new_solution.append(new_solution[0])
        return new_solution

    def opt3(self, solution, value):
        without_cycle = solution[:len(solution) - 1]
        slicesF = []
        slicesS = []
        slice_f = random.randrange(0, int(len(without_cycle)/5))
        slice_s = random.randrange(slice_f, int(len(without_cycle)/3))
        slice_t = random.randrange(slice_s, len(without_cycle))
        r = [(slice_f, slice_s), (slice_s, slice_t)]
        control = []
        enter = True
        for i, v in enumerate(without_cycle):
            enter = True
            if r[0][0] <= i < r[0][1]:
                enter = False
                slicesF.append(v)
            if r[1][0] <= i < r[1][1]:
                enter = False
                slicesS.append(v)
            if enter:
                control.append(v)
            else:
                control.append(None)
        solutions = self.combine(control, slicesF + slicesS, len(slicesF))
        result = []
        for s in solutions:
            result.append([s, self.calculate_again(solution, s, value)])
        return result

    def calculate_again(self, base, new, value):
        edges_base = self.get_edges_from_solution(base)
        edges_new = self.get_edges_from_solution(new)
        new_value = value
        for i, v in enumerate(edges_base):
            if v[0] != edges_new[i][0] or v[1] != edges_new[i][1]:
                to_remove = self.calc(v)
                new_value = new_value - to_remove
                to_add = self.calc(edges_new[i])
                new_value = new_value + to_add
        return new_value

    def combine(self, control, slice, n):
        inverted = slice[::-1]
        fistInverted = slice[:n][::-1] + slice[n:]
        secondInverted = slice[:n] + slice[n:][::-1]
        bothInverted = slice[:n][::-1] + slice[n:][::-1]
        inverted2 = inverted[:n][::-1] + inverted[n:]
        secondInverted2 = inverted[:n] + inverted[n:][::-1]
        bothInverted2 = inverted[:n][::-1] + inverted[n:][::-1]
        paths = [slice, inverted, fistInverted,
                 secondInverted, bothInverted, inverted2, secondInverted2, bothInverted2]
        solutions = []
        for p in paths:
            f = []
            for c in control:
                if c == None:
                    f.append(p.pop(0))
                else:
                    f.append(c)
            f.append(f[0])
            solutions.append(f)

        return solutions

    def opt2(self, solution, value):
        slice = []
        while len(slice) < 2:
            number = random.randrange(0, len(solution) - 1)
            if number not in slice:
                slice.append(number)

        slice = sorted(slice, key=lambda x: x)
        new_solution = self.swap(
            solution[:len(solution) - 1], slice[0], slice[1])
        return [new_solution, self.calculate_again(solution, new_solution, value)]

    def get_initial_temp(self, neighborhoods):
        dif = 0
        last = None
        for v in neighborhoods:
            if last != None:
                dif = dif + abs(v[1] - last)
            last = v[1]
        CONSTANT = -0.22314355131
        return - (dif / CONSTANT)

    def sa(self, initial_value):
        solution = initial_value[0]
        FO = initial_value[1]
        best = [solution, FO]
        temp = self.get_initial_temp(
            self.opt3(solution, FO) + self.opt3(solution, FO))
        ITER_MAX = 2
        current = best

        while not np.isclose(temp, 0, rtol=1e-20, atol=1e-20, equal_nan=False) and time.time() - self.start_time < self.time_to_execute:
            for _ in range(ITER_MAX):
                new_neighborhood = []

                for _ in range(6):
                    new_neighborhood.append(self.opt2(best[0],
                                                      best[1]))

                for _ in range(1):
                    new_neighborhood.append(self.opt2(current[0],
                                                      current[1]))

                sorter = sorted(
                    new_neighborhood, key=lambda x: x[1])
                best_neighbor = sorter[0]
                delta = best_neighbor[1] - current[1]
                if delta < 0:
                    current = best_neighbor
                    if best[1] > current[1]:
                        best = current
                else:
                    rand = random.random()
                    salt = math.pow(math.e, -(delta / temp))
                    if rand < salt:
                        current = sorter[random.randrange(
                            0, 3)]
            temp = 0.65 * temp
        self.final_result = best
