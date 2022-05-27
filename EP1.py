"""
    Implementado por Bruno Leite de Andrade
    Nº USP: 11369642
    All comments in english to make depuration easier
"""
import re
import sys


def dfs(graph, vertex, visited, scc):
    visited[vertex] = True
    scc.append(vertex)
    for v in graph[vertex]:
        if not visited[v]:
            dfs(graph, v, visited, scc)


def fill_order(graph, v, visited, stack):
    visited[v] = True
    for vertex in graph[v]:
        if not visited[vertex]:
            fill_order(graph, vertex, visited, stack)
    stack = stack.append(v)


def get_scc(graph):
    stack = []
    visited = {v: False for v in graph}

    for v in graph:
        if not visited[v]:
            fill_order(graph, v, visited, stack)

    transposed = transpose_graph(graph)

    visited = {v: False for v in graph}
    scc_list = []
    while stack:
        i = stack.pop()
        if not visited[i]:
            scc = []
            dfs(transposed, i, visited, scc)
            scc_list.append(scc)
    return scc_list


def transpose_graph(graph: dict):
    transposed = {vertex: [] for vertex in graph}
    for vertex, adjacent_list in graph.items():
        for adjacent in adjacent_list:
            transposed[adjacent].append(vertex)
    return transposed


if __name__ == "__main__":
    graph = {}

    for _ in range(int(sys.stdin.readline())):
        line = re.split('[;:]', sys.stdin.readline())
        graph[line[0]] = []

        for destination in line[1:-1]:
            graph[line[0]].append(destination.strip())

    output_mode = sys.stdin.readline()
    scc_list = get_scc(graph)
    print("Sim") if len(scc_list) == 1 else print("Não")
    print(len(scc_list))

    scc_graph = {tuple(scc): set() for scc in scc_list}
    for scc in scc_list:
        for component in scc:
            for adjacent_to_component in graph[component]:
                if adjacent_to_component not in scc:
                    for scc2 in scc_list:
                        if adjacent_to_component in scc2:
                            scc_graph[tuple(scc)].add(tuple(scc2))

    if output_mode == '1':
        for scc in scc_list:
            print(' '.join(scc) + ': ', end='')
            print('; '.join([' '.join(scc2) for scc2 in scc_graph[tuple(scc)]]))

    elif output_mode == '2':
        print(' | '.join([' '.join(scc) for scc in scc_list]))
        print('\t' + ' | '.join([' '.join(scc) for scc in scc_list]), end='')
        print(' |')
        for scc in scc_list:
            print(' '.join(scc), end=' ' * (8 - len(' '.join(scc))))
            print('|', end='')
            for scc2 in scc_list:
                if tuple(scc) in scc_graph[tuple(scc2)]:
                    print("  1  |", end='')
                else:
                    print('  0  |', end='')
            print()
    else:
        print(f'Representação de grafo não especificada para {output_mode}')
