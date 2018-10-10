"""
__author__ = chrislaw
__project__ = SecureStateEstimation
__date__ = 10/5/18
"""

import matplotlib.pyplot as plt
import numpy as np

# smt = np.array([0.154398249700000,	0.155091903300000,	0.0978938188000000,	0.190196719900000,	0.261311356100000,	0.5363312293000005])
# search = np.array([0.009015, 0.013133, 0.032277, 0.041411, 0.171899, 0.361232])
# n = np.array([10, 25, 50, 75, 100, 150])
#
# smt_error = np.array([3.38569233839563e-16,	1.95818672448298e-15,	3.89344813365748e-14,	4.09295088643850e-12,	3.05051986671621e-09,
#                       0.000481281063203100])
# search_error = np.array([1.2730451658146966e-15, 3.0229509803775837e-15, 7.660902400161737e-14, 3.885420093390361e-12,
#                          3.450610400660245e-09, 4.5971654934011094e-05])
#
#
# fig, ax = plt.subplots(2, 1)
# plt.rc('text', usetex=True)
# plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
# l1 = ax[0].plot(n, search, 'b--d')
# l2 = ax[0].plot(n, smt, 'r--o')
# ax[0].legend([r'Alg.1', r'IMHOTEP-SMT'])
# ax[0].set_xlabel(r'Number of states $n$', usetex=True)
# ax[0].set_ylabel(r'Execution time (sec)', usetex=True)
# # ax[0].set_ylim(-0.02, 0.8)
# # ax[0].set_yticks([0,  0.2, 0.4, 0.6,  0.8])
#
# ax[1].semilogy(n, search_error, 'b--d')
# ax[1].semilogy(n, smt_error, 'r--o')
# # plt.legend([r'Alg.1', r'IMHOTEP-SMT'])
# ax[1].set_xlabel(r'Number of states $n$', usetex=True)
# ax[1].set_ylabel(r'$\|x^* - x\|_2 / \|x^*\|_2$', usetex=True)
# # ax[1].set_ylim(1e-16, 10)  # outliers only
# # ax[1].set_yticks([1e-16,  1e-12, 1e-8, 1e-4,  1])
#
# # fig.legend((l1, l2), ('Alg.1', 'IMHOTEP-SMT'), 'lower center')
# fig.tight_layout()
#
# plt.savefig('/Users/chrislaw/Box Sync/SSE/figure/vs_n.pdf', bbox_inches='tight', dpi=600)
#
# plt.show()
# -------------------------------------------------
smt = np.array([0.00517343650000000,	0.0900785035000000,	0.292310873900000,	0.587996512200000,	1.08013216610000,	2.04450678640000])
search = np.array([0.001249, 0.017305, 0.059303, 0.09473, 0.155242, 0.271379])
p = np.array([3, 30, 60, 90, 120, 150])

smt_error = np.array([3.94300156107503e-13,	9.43331534203525e-16,	8.25980683692100e-16,	6.21825516131406e-16,	7.54161309646470e-16,
	8.14853383136167e-16])
search_error = np.array([1.9985174439237436e-13, 3.714474161369242e-15, 1.6162963019025597e-15,
                          3.654963358195414e-15, 2.494607697774148e-15, 3.151280538128965e-15])

fig, ax = plt.subplots(2, 1)
plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
l1 = ax[0].plot(p, search, 'b--d')
l2 = ax[0].plot(p, smt, 'r--o')
ax[0].legend([r'Alg.1', r'IMHOTEP-SMT'])
ax[0].set_xlabel(r'Number of sensors $p$', usetex=True)
ax[0].set_ylabel(r'Execution time (sec)', usetex=True)
# ax[0].set_ylim(-0.02, 0.8)
# ax[0].set_yticks([0,  0.2, 0.4, 0.6,  0.8])

ax[1].semilogy(p, search_error, 'b--d')
ax[1].semilogy(p, smt_error, 'r--o')
# plt.legend([r'Alg.1', r'IMHOTEP-SMT'])
ax[1].set_xlabel(r'Number of sensors $p$', usetex=True)
ax[1].set_ylabel(r'$\|x^* - x\|_2 / \|x^*\|_2$', usetex=True)
# ax[1].set_ylim(1e-16, 10)  # outliers only
# ax[1].set_yticks([1e-16,  1e-12, 1e-8, 1e-4,  1])

# fig.legend((l1, l2), ('Alg.1', 'IMHOTEP-SMT'), 'lower center')
fig.tight_layout()

plt.savefig('/Users/chrislaw/Box Sync/SSE/figure/vs_p.pdf', bbox_inches='tight', dpi=600)
plt.show()
