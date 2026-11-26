import numpy as np, itertools
P = lambda p: np.eye(3)[:, list(p)]          # column i -> e_{p[i]}
Cp = P((1, 2, 0)); Cm = Cp.T; R = P((0, 2, 1)); I3 = np.eye(3)
assert np.allclose(R @ Cp @ R, Cm)
SWAP = np.zeros((9, 9))
for i, j in itertools.product(range(3), range(3)): SWAP[j*3+i, i*3+j] = 1
for sc, ss in itertools.product((1, -1), repeat=2):
    UC = Cp if sc == 1 else Cm; US = Cp if ss == 1 else Cm
    t = np.trace(SWAP @ np.kron(UC, US.conj().T)).real
    tR = np.trace(SWAP @ np.kron(R@UC@R, (R@US@R).conj().T)).real
    print(f'sigma_C={sc:+d} sigma_S={ss:+d}  T_rel={t:.0f}  under R(x)R {tR:.0f}  (3/2)(1+s_rel)={1.5*(1+sc*ss):.0f}')
# single-cycle conjugation invariants agree
print('traces C+^k vs C-^k', [round(np.trace(np.linalg.matrix_power(Cp,k)).real,9)==round(np.trace(np.linalg.matrix_power(Cm,k)).real,9) for k in range(1,4)])
# complex structure on 1-perp: J = (C+ - C-)/sqrt3
J = (Cp - Cm) / np.sqrt(3); B = np.linalg.qr(np.array([[1,-1,0],[1,1,-2]]).T.astype(float))[0]  # basis of 1-perp
Jb = B.T @ J @ B; print('J^2 on 1-perp', np.round(Jb @ Jb, 9).tolist(), ' R J R = -J:', np.allclose(R@J@R, -J))
# Page-Wootters kernel of I - C3 (x) C3, and the joint mirror
K = np.eye(9) - np.kron(Cp, Cp); w, v = np.linalg.eig(K); ker = v[:, abs(w) < 1e-9]; print('ker dim', ker.shape[1])
RR = np.kron(R, R); proj = ker @ np.linalg.pinv(ker)
print('kernel invariant under R(x)R:', np.allclose(RR @ proj @ RR, proj))
