#!/usr/bin/python

# Copyright 2018, Gurobi Optimization, LLC
"""
Use Gurobi to solve the MIQCP
"""
from gurobipy import *
import pickle
import numpy as np
import scipy.linalg as la
from itertools import product
import datetime


class SecureStateEsitmation:
    def __init__(self):
        self.tol = 1e-5
        # performance of tolorance, with larger tol, it is susceptible to errors,
        # treating attacked as attacked-free and attacked-free as attacked.
        with open('sse_test_from_mat', 'rb') as filehandle:
            self.Y = pickle.load(filehandle)
            self.obsMatrix = pickle.load(filehandle)
            self.p, self.n, self.tau = pickle.load(filehandle)
            self.K = pickle.load(filehandle)
            self.x0 = pickle.load(filehandle)
            self.E = pickle.load(filehandle)
            self.noise_bound = pickle.load(filehandle)
            self.A = pickle.load(filehandle)
            self.C = pickle.load(filehandle)


T = []
for it in range(1):

    sse = SecureStateEsitmation()
    # Create a new model
    m = Model("qp")

    M = 1e8

    # Create variables
    b = [m.addVar(vtype=GRB.BINARY, name='b{0}'.format(i + 1)) for i in range(sse.p)]
    b = np.array(b)
    x = [m.addVar(name='x{0}'.format(i + 1)) for i in range(sse.n)]
    x = np.array(x)
    # set object
    obj = LinExpr()
    for i in range(sse.p):
        obj = obj + b[i]
    m.setObjective(obj, GRB.MINIMIZE)
    m.update()
    # constraints
    for i in range(sse.p):
        index = [i * sse.tau + j for j in range(sse.tau)]
        Y = sse.Y[index, :]
        O = sse.obsMatrix[index, :]

        m.addQConstr(
            (-2 * np.transpose(Y).dot(O).dot(x) - M * b[i] + np.transpose(x).dot(np.transpose(O).dot(O).dot(x)))[0] <=
            -1 * np.transpose(Y).dot(Y)[0][0] + 1e-5 + 2.25,  name='c{0}'.format(i))

    m.setParam('OutputFlag', False)
    # m.Params.Aggregate = 0
    # m.Params.numericFocus = 3
    # m.Params.presolve = 0
    start = datetime.datetime.now()
    m.optimize()
    T.append((datetime.datetime.now() - start).total_seconds())
    estimate = []
    indexOfZero = []
    indexOfOne = []
    id = 0
    for v in m.getVars():
        if 'b' in v.varName and v.x == 0:
            indexOfZero.append(id)
        if v.x == 1:
            indexOfOne.append(id)
        if 'x' in v.varName:
            estimate.append(v.x)
        id = id + 1

    print(indexOfOne)
    print(sorted(sse.K))

    index = [x + y for x, y in product([1 * i * sse.tau for i in indexOfZero], range(sse.tau))]
    Y = sse.Y[index, :]
    O = sse.obsMatrix[index, :]
    x, res, _, _ = la.lstsq(O, Y)
print(np.mean(T))
print(np.linalg.norm(x- sse.x0) / np.linalg.norm(sse.x0))


# An useful example of the use of Gorobi can be found at
# https://github.com/kehlert/multistage_portfolio/blob/d5c9c040e095330fd68efda050803572a41093ae/code/markowitz.py
