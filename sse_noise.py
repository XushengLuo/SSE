"""
__author__ = chrislaw
__project__ = SecureStateEstimation
__date__ = 9/26/18
"""
import queue
import datetime
import numpy as np
import pickle
from itertools import product
import scipy.linalg as la
import warnings
import matplotlib.pyplot as plt


class SecureStateEsitmation:
    def __init__(self):
        self.tol = 1e-5
        # performance of tolorance, with larger tol, it is susceptible to errors,
        # treating attacked as attacked-free and attacked-free as attacked.
        with open('sse_test', 'rb') as filehandle:
            self.Y = pickle.load(filehandle)
            self.obsMatrix = pickle.load(filehandle)
            self.p, self.n, self.tau = pickle.load(filehandle)
            self.K = pickle.load(filehandle)
            self.x0 = pickle.load(filehandle)
            self.E = pickle.load(filehandle)
            self.noise_bound = pickle.load(filehandle)
            self.A = pickle.load(filehandle)
            self.C = pickle.load(filehandle)

    def obs(self):
        # whether the system is observable
        import control
        obs = control.obsv(self.A, self.C)
        rank = np.linalg.matrix_rank(obs)
        print("rank", rank, "n", self.n)

    def delta_s(self):
        O_I = self.obsMatrix[[x + y for x, y in product([-1 * i * self.tau for i in self.K], range(self.tau))], :]

    def residual(self, indexOfZero):
        index = [x + y for x, y in product([-1 * i * self.tau for i in indexOfZero], range(self.tau))]
        Y = self.Y[index, :]
        O = self.obsMatrix[index, :]
        x, res, _, _ = la.lstsq(O, Y)
        res = np.linalg.norm(Y - O.dot(x))
        # print(indexOfZero)
        if res <= self.tol + np.linalg.norm(self.noise_bound[np.array(indexOfZero) * -1, :]):
            # if np.shape(res) == (0, ) or res[0] <= self.tol:  # one intersection point
            return True
        else:  # no intersection point
            return False

    def genChild(self, parentnode, childnode, attack, invalidSet):
        """Generating childnote
        """
        childnode.attack = attack
        childnode.level = parentnode.level - 1  # negative, convenient when enqueued
        if childnode in invalidSet:
            childnode.accmuResidual = False
            return
        childnode.parent = parentnode
        childnode.numOfAttacked = parentnode.numOfAttacked + attack
        childnode.indexOfZero = parentnode.indexOfZero + [childnode.level] if not attack else parentnode.indexOfZero
        childnode.accmuResidual = True if attack else self.residual(childnode.indexOfZero)


class Node:
    """Including state, parent, pathcost"""

    def __init__(self, acr=True, noa=0, level=0, attack=1, ioo=list(), par=None):
        self.numOfAttacked = noa
        self.level = level
        self.accmuResidual = acr
        self.attack = attack
        self.indexOfZero = ioo
        self.parent = par

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.attack == other.attack and self.level == other.level  # and self.indexOfZero == other.indexOfZero
            #  should we add the last one. yes, accurate, no, speed
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Node):
            if self.numOfAttacked < other.numOfAttacked or (
                    self.numOfAttacked == other.numOfAttacked and self.level < other.level):
                return True
            else:
                return False

    def __hash__(self):
        return hash((self.attack, self.level))


def main():

    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

    level = []
    # Request the init and goal state
    sse = SecureStateEsitmation()

    # Initializing root node
    root = Node(acr=True, noa=0, level=1, attack=0, ioo=[], par=None)

    # Initializing frontier
    frontier = queue.PriorityQueue()
    discard = queue.PriorityQueue()   # for lazy research when previous search fails
    # a priority queue ordered by PATH-COST, with node as the only element
    frontier.put(root)
    # Initializing explored set
    exploredSet = set()  # set
    # reserve invalid node
    invalidSet = set()

    while True:

        # EMPTY?(frontier) then return failure
        if frontier.empty() and discard.empty():
            break
        if frontier.empty():
            frontier.put(discard.get())    # it's slightly better than  # list(map(frontier.put, discard.queue))
                                                                        #  discard.queue.clear()
            exploredSet.clear()
            continue

        # chooses the lowest-cost node in frontier
        node = frontier.get()

        level.append(node.level * -1 + 1)

        # print("node: ", [i * -1 + 1 for i in node.indexOfZero], node.level * -1 + 1)

        if node.level == -1 * (sse.p - 1):
            # if sse.p - len(node.indexOfZero) > sse.p//2 - 1:
            #     # the right-hand side should be consistent with maximum number of attacked sensors
            #     # frontier.queue.clear()   # it remains to verify whether this is necessary
            #     frontier.put(discard.get())
            #     exploredSet.clear()
            #     continue

            plt.plot(range(1, len(level)+1), level, '-o')
            plt.show()
            print("time: ", (datetime.datetime.now() - start).total_seconds())

            index = [x + y for x, y in product([-1 * i * sse.tau for i in node.indexOfZero], range(sse.tau))]
            Y = sse.Y[index, :]
            O = sse.obsMatrix[index, :]
            x, res, _, _ = la.lstsq(O, Y)

            attackfree = [-1 * i + 1 for i in node.indexOfZero]
            attack = [i for i in range(1, sse.p + 1) if i not in attackfree]

            print("true attack ({0})        : ".format(len(sse.K)), sorted([i + 1 for i in sse.K]))
            print("estimate attack ({0})    : ".format(len(attack)), attack)

            if attack != sorted([i + 1 for i in sse.K]):
                print("true attack ({0})        : ".format(len(sse.K)), sorted([i + 1 for i in sse.K]))
                print("estimate attack ({0})    : ".format(len(attack)), attack)
                return False
            break

        exploredSet.add(node)

        for attack in [0, 1]:

            # child CHILD-NODE(problem,node,action)
            childNode = Node()
            sse.genChild(node, childNode, attack, invalidSet)

            # print("childnode: ", [i * -1 + 1 for i in childNode.indexOfZero], childNode.level * -1 + 1)

            if childNode.accmuResidual:

                # # early stop   # the best position to place this ?????
                if (-1 * childNode.level + 1) - len(childNode.indexOfZero) > sse.p // 2 - 1: # we only discard bad nodes
                    # frontier.queue.clear()
                    #frontier.put(discard.get())
                    #exploredSet.clear()
                    #break
                    print("early stop -------------------------------------------")
                    continue

                if childNode in exploredSet:
                    discard.put(childNode)
                    continue
                # only consider 0 residual

                # option 2
                q = frontier.queue
                if childNode not in q:
                    # print("childnode accepted: ", [i * -1 + 1 for i in childNode.indexOfZero], childNode.level * -1 + 1)
                    frontier.put(childNode)
                else:  # having equal attack indicator and level
                    indices = q.index(childNode)
                    if childNode < q[indices]:
                        discard.put(q[indices])     # we do not discard any node
                        q.remove(q[indices])
                        frontier.put(childNode)
                    else:
                        discard.put(childNode)

    return True


if __name__ == "__main__":
    start = datetime.datetime.now()
    # from generate_test_case import TestCase
    main()
    # trial = 0
    # from generate_test_case import TestCase
    # while True:
    #     trial = trial + 1
    #     testCase = TestCase()
    #     with open('sse_test', 'wb') as filehandle:
    #         pickle.dump(testCase.Y, filehandle)
    #         pickle.dump(testCase.obsMatrix, filehandle)
    #         pickle.dump([testCase.p, testCase.n, testCase.tau], filehandle)
    #         pickle.dump(testCase.K, filehandle)
    #         pickle.dump(testCase.x0, filehandle)
    #         pickle.dump(testCase.E, filehandle)
    #         pickle.dump(testCase.noise_bound, filehandle)
    #         pickle.dump(testCase.A, filehandle)
    #         pickle.dump(testCase.C, filehandle)
    #     start = datetime.datetime.now()
    #     # print(sorted([i + 1 for i in testCase.K]))
    #     if not main():
    #         break
    # print(trial)

# reason for success
# attack power is large enough not to be covered by the noise and tolerance
# set attack power very large and noise, tolerance small