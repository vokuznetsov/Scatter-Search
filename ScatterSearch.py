import networkx as nx
from random import randint
import Parser
import Diversification
import Improvement
import Combination


# def create_test_graph():
#     letters = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "F"}
#     print letters
#     g = nx.Graph()
#     g.add_edge('1', '2')
#     g.add_edge('1', '4')
#     g.add_edge('1', '5')
#     g.add_edge('2', '1')
#     g.add_edge('2', '3')
#     g.add_edge('3', '2')
#     g.add_edge('4', '1')
#     g.add_edge('4', '5')
#     g.add_edge('4', '6')
#     g.add_edge('5', '1')
#     g.add_edge('5', '4')
#     g.add_edge('5', '6')
#     g.add_edge('6', '4')
#     g.add_edge('6', '5')
#     return g, letters


def scatter_search(file_name):
    P_SIZE = 4
    # graph, letters = create_test_graph()

    dv = Diversification.Diversification()
    graph = Parser.parser(file_name)
    im = Improvement.Improvement(graph)
    cb = Combination.Combination(graph)

    # f_1 = {1: '3', 2: '1', 3: '4', 4: '5', 5: '2', 6: '6'}
    # CW_1 = {'3': 1, '1': 4, '4': 5, '5': 4, '2': 2, '6': 0}
    #
    # f_2 = {1: '3', 2: '2', 3: '1', 4: '4', 5: '5', 6: '6'}
    # CW_2 = {'3': 1, '2': 1, '1': 2, '4': 3, '5': 2, '6': 0}

    f_set = []

    for i in range(0, P_SIZE):
        f, CW, CW_G = dv.diversification(graph)
        f_impr, CW_impr, CW_G_impr = im.improvement(f, CW, CW_G)
        f_set.append(f_impr)

    while len(f_set) != 1:
        one = randint(0, len(f_set) - 1)
        f_1 = f_set.pop(one)
        two = randint(0, len(f_set) - 1)
        f_2 = f_set.pop(two)
        f_com, CW_com, CW_G_com = cb.combination(f_1, f_2)
        f_new, CW_new, CW_G_new = im.improvement(f_com, CW_com, CW_G_com)
        f_set.append(f_new)

    f = f_set.pop()
    CW = im.compute_cutwidth_by_labeling(graph, f)
    CW_G = dv.get_cutwidth_of_graph(CW)


    print 'Labeling: ' + str(f)
    print 'Cutwidth of vertices: ' + str(CW)
    print 'Cutwidth of graph: ' + str(CW_G)
