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

def distance(f_set, f_new):
    DTHRESH = 80

    if len(f_set) == 0:
        return True
    else:
        for cw, f in f_set.items():
            count = 0
            for i in range(1, len(f) + 1):
                if f[i] == f_new[i]:
                    count += 1
            if 100 * (count / len(f_new)) > DTHRESH:
                return False
        return True

def is_best(best_f, best_CW, best_CW_G, f_impr, CW_impr, CW_G_impr):
    if CW_G_impr < best_CW_G:
        print 'Update CW_G: ' + str(CW_G_impr)
        return f_impr, CW_impr, CW_G_impr, True
    else:
        return best_f, best_CW, best_CW_G, False


def scatter_search(file_name):
    P_SIZE = 100
    FAILED_ATTEMPT = 0
    LIMIT_FAILED_ATTEMPT = 10
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

    f_set = {}
    f, CW, CW_G = dv.diversification(graph)
    best_f, best_CW, best_CW_G = im.improvement(f, CW, CW_G)
    f_set[best_CW_G] = best_f
    print 'First best CW_G: ' + str(best_CW_G)

    for i in range(1, P_SIZE):
        f, CW, CW_G = dv.diversification(graph)
        f_impr, CW_impr, CW_G_impr = im.improvement(f, CW, CW_G)
        best_f, best_CW, best_CW_G, is_upd = is_best(best_f, best_CW, best_CW_G, f_impr, CW_impr, CW_G_impr)

        if is_upd:
            f_set[CW_G_impr] = f_impr
        elif distance(f_set, f_impr):
            FAILED_ATTEMPT = 0
            f_set[CW_G_impr] = f_impr
        else:
            FAILED_ATTEMPT += 1

        if FAILED_ATTEMPT > LIMIT_FAILED_ATTEMPT:
            print 'FAILED ATTEMPTS EXCEEDED LIMIT'
            break

    print 'Lenght of f_set: ' + str(len(f_set))
    print 'Combination start!'

    while len(f_set) > 1:
        f_set_sorted = sorted(f_set.items(), key=lambda x: x[1], reverse=True)
        f_1 = f_set.pop(f_set_sorted[0][0])
        f_2 = f_set.pop(f_set_sorted[1][0])
        f_com, CW_com, CW_G_com = cb.combination_2(f_1, f_2)
        f_new, CW_new, CW_G_new = im.improvement(f_com, CW_com, CW_G_com)
        best_f, best_CW, best_CW_G, is_upd = is_best(best_f, best_CW, best_CW_G, f_new, CW_new, CW_G_new)
        f_set[CW_G_new] = f_new

    print 'Best labeling: ' + str(best_f)
    print 'Best Cutwidth of vertices: ' + str(best_CW)
    print 'Best Cutwidth of graph: ' + str(best_CW_G)
