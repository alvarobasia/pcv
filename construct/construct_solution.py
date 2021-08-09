from hashlib import new
from typing import List, Tuple
import math
import numpy as np
from domain.Graph import Graph
import random
import time


class Construct_Solution:
    list: List[Tuple[float]]
    nodes: int
    start_time: int

    def __init__(self, graph: Graph) -> None:
        self.list = graph.get_list_representation()
        self.nodes = graph.nodes_number
        self.start_time = time.time()
        x = self.construct()[0]
        # edges = self.get_edges_from_solution(x)
        # self.sa([[0, 1], [1, 4], [4, 5], [5, 2], [
        #         2, 3], [3, 0]], [0, 1, 4, 5, 2, 3, 0])

        # print(self.opt3([0, 1, 4, 5, 2, 3, 0]))
        self.sa(x)

    def construct(self):
        current = random.randrange(0, self.nodes)
        solution = self.make_solution(current)
        final = [solution, self.calc(solution)]

        # print(sorted(LRC, key=lambda x: x[1])[0])
        return final

    def make_solution(self, init):
        solution = [init]
        next_nodes = self.list[init]
        while len(solution) != len(self.list):
            min = (None, float('inf'))
            for node in next_nodes:
                not_in_solution = all(x != node[0] for x in solution)
                minor = min[1] > node[1]
                if minor and not_in_solution:
                    min = node
            current = min[0]
            solution.append(min[0])
            next_nodes = self.list[current]
        solution.append(init)
        # print(solution)
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

    def opt3(self, solution):
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
        return self.combine(control, slicesF + slicesS, len(slicesF))

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

    def opt2(self, solution):
        slice = []
        while len(slice) < 2:
            number = random.randrange(0, len(solution) - 1)
            if all(x != number for x in slice):
                slice.append(number)

        slice = sorted(slice, key=lambda x: x)
        return self.swap(solution[:len(solution) - 1], slice[0], slice[1])

    def get_initial_temp(self, neighborhoods):
        dif = 0
        last = None
        for v in neighborhoods:
            if last != None:
                dif = dif + abs(v[1] - last)
            last = v[1]
        CONSTANT = -0.22314355131
        return - (dif / CONSTANT)

    def sa(self, solution):
        neighborhoods = []
        for _ in range(100):
            s = self.opt2(solution)
            neighborhoods.append([s, self.calc(s)])
        best = [solution, self.calc(solution)]
        temp = self.get_initial_temp(neighborhoods)
        ITER_MAX = 3
        g = best
        current = best
        while not np.isclose(temp, 0, rtol=1e-20, atol=1e-20, equal_nan=False):
            for _ in range(ITER_MAX):
                new_neighborhood = []
                next = self.opt3(current[0]) + self.opt3(best[0])
                for _ in range(5):
                    next.append(self.opt2(best[0]))
                for _ in range(5):
                    next.append(self.opt2(current[0]))
                for n in next:
                    new_neighborhood.append([n, self.calc(n)])
                best_neighbor = sorted(
                    new_neighborhood, key=lambda x: x[1])[0]
                delta = best_neighbor[1] - current[1]
                if delta < 0:
                    current = best_neighbor
                    if best[1] > current[1]:
                        best = current
                else:
                    rand = random.random()
                    salt = math.pow(math.e, -(delta / temp))
                    if rand < salt:
                        current = sorted(
                            new_neighborhood, key=lambda x: x[1])[:15][random.randrange(0, 15)]
            t = time.time() - self.start_time
            if t > 60:
                print('Tempo acabou!', {t})
                break
            print('---------------------')
            temp = 0.65 * temp
            print(f'atual: {current[1]}')
            print(f'temperatura: {temp}')
            print(F'MELHOR: {best[1]}')
            print('---------------------')
        print(time.time())
        print('b', best[1])
        print('g', g[1])
