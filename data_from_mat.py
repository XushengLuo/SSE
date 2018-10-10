"""
__author__ = chrislaw
__project__ = SecureStateEstimation
__date__ = 10/5/18
"""

import scipy.io as sio

from scipy.sparse import random
import numpy as np
from control.matlab import *
import pickle


class TestCase(object):

    def __init__(self):
        data = sio.loadmat('/Users/chrislaw/Box Sync/SSE/Imhotep-smt-master/ImhotepSMT/Examples/'
                           'Random examples/Test1_states/test_n100_p150.mat')

        self.p = data['p'][0][0]
        self.n = data['n'][0][0]
        self.tau = self.n
        # Generate a system with a random A matrix
        self.A = data['A']
        # The 'C' matrix of the system
        self.C = data['C']

        self.x0 = data['x0']

        self.attackpower = data['attackpower'][0][0] # Magnitude of the attacks (i.e., norm of the attack vector)
        # self.max_s = int(np.floor(self.p // 3) - 1)
        self.s = data['s'][0] # np.random.randint(0, self.max_s, 1)[0]

        # self.per = sorted(range(0, self.p), reverse=True)
        self.K = data['K'][0]

        # Choose an initial condition
        Y = np.array([]).reshape(self.p, 0)
        E = np.array([]).reshape(self.p, 0)
        # noise power
        self.noise_bound = np.array([0]*self.p).reshape(self.p, 1)  # 20

        # for i in range(0, self.tau):
        #     # Generate a random attack vector supported on K
        #     a = np.zeros((self.p, 1))
        #     a[self.K] = self.attackpower * np.random.randn(len(self.K), 1)
        #     E = np.concatenate((E, a), axis=1)
        #
        #     # The measurement is y=C*x+a
        #     y = self.C.dot(x) + a + noise_power * np.random.randn(self.p, 1)  # np.random.uniform(-1, 1, (self.p, 1))
        #     # Update the arrays X,Y,E
        #     Y = np.concatenate((Y, y), axis=1)
        #
        #     x = self.A.dot(x) + process_noise_power * np.random.randn(self.n, 1) # np.random.uniform(-1, 1, (self.n, 1))

        self.Y = np.transpose(data['Y']).reshape(np.size(data['Y']), 1, order='F')
        self.E = 0
        # Y = [ Y_1^t
        #       Y_2^t           Y_i^t = []_(t, 1)
        #        ...
        #       Y_p^t ]

        self.obsMatrix = np.array([]).reshape(0, self.n)

        for k in range(self.p):
            obs = self.C[k, :].reshape(1, self.n)
            oi = np.array([]).reshape(0, self.n)
            for i in range(0, self.tau):
                obs = obs.dot(self.A) if i else obs
                oi = np.concatenate((oi, obs), axis=0)

            self.obsMatrix = np.concatenate((self.obsMatrix, oi), axis=0)
            # O = [ O_1
            #       O_2        O_i = []_(self.tau, self.n)
            #       ...
            #       O_p ]


testCase = TestCase()
with open('sse_test_from_mat', 'wb') as filehandle:
            pickle.dump(testCase.Y, filehandle)
            pickle.dump(testCase.obsMatrix, filehandle)
            pickle.dump([testCase.p, testCase.n, testCase.tau], filehandle)
            pickle.dump(testCase.K, filehandle)
            pickle.dump(testCase.x0, filehandle)
            pickle.dump(testCase.E, filehandle)
            pickle.dump(testCase.noise_bound, filehandle)
            pickle.dump(testCase.A, filehandle)
            pickle.dump(testCase.C, filehandle)