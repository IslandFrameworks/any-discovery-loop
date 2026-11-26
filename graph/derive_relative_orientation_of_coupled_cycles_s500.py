"""ANY §500: relative sign of two coupled cycles, absolute vs gauge time orientation, and bilinear arrow coupling.

Claims C1-C5 were drafted by the discovery loop (loop/rounds/026, Round 026) answering Graham's question
on loop/OPEN.md Item 5 after §499.7, and are executed here by Claude.
Z3 results quantify the ENCODED finite families only.
"""
from __future__ import annotations
import json
from pathlib import Path
import platform
import sympy as sp
from sympy.physics.quantum import TensorProduct
import z3

ROOT = Path(__file__).resolve().parent.parent


def solver_record(name, constraints, expected, witness_vars=()):
    solver = z3.Solver()
    solver.set(timeout=15000)
    solver.add(*constraints)
    answer = solver.check()
    result = {'name': name, 'expected': expected, 'result': str(answer), 'smt2': solver.to_smt2()}
    if answer == z3.sat:
        model = solver.model()
        result['witness'] = {str(v): str(model.eval(v, model_completion=True)) for v in witness_vars}
    if answer == z3.unknown:
        result['reason_unknown'] = solver.reason_unknown()
    if str(answer) != expected:
        raise AssertionError(result)
    return result


def z3_certificates():
    r = []
    # C1: Every R-invariant functional on A_cyc gives identical values on C+ and C-
    m = [[z3.Real(f'm_{i}_{j}') for j in range(3)] for i in range(3)]
    r_inv = [
        m[0][1] == m[0][2],
        m[1][0] == m[2][0],
        m[1][1] == m[2][2],
        m[1][2] == m[2][1],
    ]
    tr_C_plus = m[0][1] + m[1][2] + m[2][0]
    tr_C_minus = m[0][2] + m[1][0] + m[2][1]
    r.append(solver_record(
        '500_1_R_invariant_functional_cannot_distinguish_cycles',
        r_inv + [tr_C_plus != tr_C_minus],
        'unsat',
    ))

    # C2: Swap trace T_rel is 3 for co-rotating, 0 for counter-rotating; invariant under R_tot
    sC, sS = z3.Ints('sigma_C sigma_S')
    valid_signs = [z3.Or(sC == 1, sC == -1), z3.Or(sS == 1, sS == -1)]
    s_rel = sC * sS
    t_rel = z3.If(s_rel == 1, 3, 0)
    formula_match = [2 * t_rel != 3 * (1 + s_rel)]
    r.append(solver_record(
        '500_2_swap_trace_discrete_product',
        valid_signs + formula_match,
        'unsat',
    ))
    r_tot_flip = [(-sC) * (-sS) != s_rel]
    r.append(solver_record(
        '500_2_joint_reflection_invariance',
        valid_signs + r_tot_flip,
        'unsat',
    ))

    # C3: Commutator squared relation K^2 + 3(I_3 - P_sym) = 0 in QF_LRA
    # K = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    # K^2 = [[-2, 1, 1], [1, -2, 1], [1, 1, -2]]
    # 3*(I_3 - P_sym) = [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]
    k2 = [[-2, 1, 1], [1, -2, 1], [1, 1, -2]]
    proj_diff = [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]
    rel_violation = [z3.Or(*[k2[i][j] + proj_diff[i][j] != 0 for i in range(3) for j in range(3)])]
    r.append(solver_record(
        '500_3_planar_commutator_squared_relation',
        rel_violation,
        'unsat',
    ))

    # C4: Causal tick increment product invariant under PT
    s_clk, s_cn = z3.Ints('sigma_clock sigma_cone')
    valid_c4 = [z3.Or(s_clk == 1, s_clk == -1), z3.Or(s_cn == 1, s_cn == -1)]
    pt_violation = [(-s_clk) * (-s_cn) != s_clk * s_cn]
    r.append(solver_record(
        '500_4_causal_tick_advance_PT_invariant',
        valid_c4 + pt_violation,
        'unsat',
    ))

    # C5: Page-Wootters co-rotating vs counter-rotating branch distinctness
    k = z3.Int('k')
    valid_k = [z3.Or(k == 1, k == 2)]
    s_co = k
    s_counter = 3 - k
    r.append(solver_record(
        '500_5_PW_corotating_counterrotating_branches_distinct',
        valid_k + [s_co == s_counter],
        'unsat',
    ))

    return r


def symbolic_certificates():
    out = {}

    # Define fundamental 3-cycle matrices
    Cp = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    Cm = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    R = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    I3 = sp.eye(3)
    S = Cp + Cm
    K = Cp - Cm
    P_sym = sp.Rational(1, 3) * sp.ones(3, 3)

    # Claim C1: Single-cycle algebra, conjugation and traces
    assert R * Cp * R == Cm
    assert R * Cm * R == Cp
    assert R * S * R == S
    assert R * K * R == -K
    lam = sp.symbols('lambda')
    cp_char = Cp.charpoly(lam).as_expr()
    cm_char = Cm.charpoly(lam).as_expr()
    assert cp_char == lam**3 - 1
    assert cm_char == lam**3 - 1
    out['500_1_charpoly'] = str(cp_char)
    traces_match = [int(sp.trace(Cp**m)) == int(sp.trace(Cm**m)) for m in range(1, 7)]
    assert all(traces_match)
    out['500_1_traces_1_to_6'] = [int(sp.trace(Cp**m)) for m in range(1, 7)]

    # Claim C2: Coupled cycles and swap trace
    # SWAP matrix on C^3 (x) C^3
    SWAP = sp.zeros(9, 9)
    for i in range(3):
        for j in range(3):
            SWAP[j * 3 + i, i * 3 + j] = 1

    R_tot = TensorProduct(R, R)
    configs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    swap_traces = {}
    for sc, ss in configs:
        Uc = Cp if sc == 1 else Cm
        Us = Cp if ss == 1 else Cm
        t_swap = int(sp.trace(SWAP * TensorProduct(Uc, Us.H)))
        t_direct = int(sp.trace(Uc * Us.inv()))
        assert t_swap == t_direct
        expected_t = 3 if sc == ss else 0
        assert t_swap == expected_t
        # Joint mirror invariance check
        Uc_mirr = R * Uc * R
        Us_mirr = R * Us * R
        t_mirr = int(sp.trace(SWAP * TensorProduct(Uc_mirr, Us_mirr.H)))
        assert t_mirr == t_swap
        swap_traces[f'({sc},{ss})'] = t_swap

    out['500_2_swap_traces'] = swap_traces

    # Claim C3: Planar complex structure on V_0 = 1^perp
    assert K**2 + 3 * (I3 - P_sym) == sp.zeros(3, 3)

    # R-eigenbasis
    v_plus = sp.Matrix([-2, 1, 1]) / sp.sqrt(6)
    v_minus = sp.Matrix([0, 1, -1]) / sp.sqrt(2)
    assert sp.simplify(v_plus.dot(v_minus)) == 0
    assert sp.simplify(v_plus.dot(v_plus)) == 1
    assert sp.simplify(v_minus.dot(v_minus)) == 1
    assert R * v_plus == v_plus
    assert R * v_minus == -v_minus

    R_v = sp.Matrix([
        [v_plus.dot(R * v_plus), v_plus.dot(R * v_minus)],
        [v_minus.dot(R * v_plus), v_minus.dot(R * v_minus)],
    ])
    K_v = sp.Matrix([
        [v_plus.dot(K * v_plus), v_plus.dot(K * v_minus)],
        [v_minus.dot(K * v_plus), v_minus.dot(K * v_minus)],
    ])
    assert R_v == sp.Matrix([[1, 0], [0, -1]])  # sigma_z
    J_v = sp.simplify(K_v / sp.sqrt(3))
    assert J_v == sp.Matrix([[0, 1], [-1, 0]])
    assert J_v**2 == -sp.eye(2)
    assert R_v * J_v * R_v == -J_v
    assert R_v * J_v + J_v * R_v == sp.zeros(2, 2)

    Cp_v = sp.Matrix([
        [v_plus.dot(Cp * v_plus), v_plus.dot(Cp * v_minus)],
        [v_minus.dot(Cp * v_plus), v_minus.dot(Cp * v_minus)],
    ])
    Cm_v = sp.Matrix([
        [v_plus.dot(Cm * v_plus), v_plus.dot(Cm * v_minus)],
        [v_minus.dot(Cm * v_plus), v_minus.dot(Cm * v_minus)],
    ])
    expected_Cp_v = -sp.Rational(1, 2) * sp.eye(2) + (sp.sqrt(3) / 2) * J_v
    expected_Cm_v = -sp.Rational(1, 2) * sp.eye(2) - (sp.sqrt(3) / 2) * J_v
    assert sp.simplify(Cp_v - expected_Cp_v) == sp.zeros(2, 2)
    assert sp.simplify(Cm_v - expected_Cm_v) == sp.zeros(2, 2)
    out['500_3_complex_structure_J_v'] = [[int(x) for x in row] for row in J_v.tolist()]

    # Cyclic basis u_1, u_2
    u1 = sp.Matrix([1, -1, 0]) / sp.sqrt(2)
    u2 = sp.Matrix([1, 1, -2]) / sp.sqrt(6)
    K_u = sp.Matrix([
        [u1.dot(K * u1), u1.dot(K * u2)],
        [u2.dot(K * u1), u2.dot(K * u2)],
    ])
    J_u = sp.simplify(K_u / sp.sqrt(3))
    assert J_u == sp.Matrix([[0, -1], [1, 0]])
    assert J_u**2 == -sp.eye(2)

    # Claim C4: Light ray duration and centered modular sign
    L, c = sp.symbols('L c', positive=True)
    t_rec_pos = 0 + 1 * (L / c)
    t_rec_neg = 0 + (-1) * (L / c)
    assert t_rec_pos - 0 == L / c
    assert t_rec_neg - 0 == -L / c

    def sgn3(dk):
        return 1 if (dk % 3) == 1 else (-1 if (dk % 3) == 2 else 0)

    for s_clock in (1, -1):
        for s_cone in (1, -1):
            dk = (s_clock * s_cone) % 3
            assert sgn3(dk) == s_clock * s_cone
            # Invariance under PT
            assert (-s_clock) * (-s_cone) == s_clock * s_cone
    out['500_4_modular_signs_verified'] = True

    # Claim C5: Page-Wootters bipartite 3-cycle model
    H_co = sp.eye(9) - TensorProduct(Cp, Cp)
    H_counter = sp.eye(9) - TensorProduct(Cp, Cm)
    ker_co = H_co.nullspace()
    ker_counter = H_counter.nullspace()
    assert len(ker_co) == 3
    assert len(ker_counter) == 3
    out['500_5_PW_kernel_dims'] = {'ker_co': len(ker_co), 'ker_counter': len(ker_counter)}

    e = [sp.Matrix([1 if i == k else 0 for i in range(3)]) for k in range(3)]
    psi_clock = sp.Rational(1, 1) / sp.sqrt(3) * sum((TensorProduct(e[k], e[k]) for k in range(3)), sp.zeros(9, 1))
    assert sp.simplify(H_co * psi_clock) == sp.zeros(9, 1)
    assert sp.simplify(R_tot * psi_clock) == psi_clock

    psi_counter = sp.Rational(1, 1) / sp.sqrt(3) * sum((TensorProduct(e[k], e[(-k) % 3]) for k in range(3)), sp.zeros(9, 1))
    assert sp.simplify(H_counter * psi_counter) == sp.zeros(9, 1)

    # Reduced density matrices for both branches are 1/3 * I_3
    # Tr_C(|psi><psi|)
    def partial_trace_C(psi):
        rho = psi * psi.H
        rho_S = sp.zeros(3, 3)
        for k in range(3):
            proj_k = TensorProduct(e[k].T, sp.eye(3))
            rho_S += proj_k * rho * proj_k.T
        return sp.simplify(rho_S)

    rho_S_co = partial_trace_C(psi_clock)
    rho_S_counter = partial_trace_C(psi_counter)
    assert rho_S_co == sp.Rational(1, 3) * sp.eye(3)
    assert rho_S_counter == sp.Rational(1, 3) * sp.eye(3)
    out['500_5_reduced_marginals_identical'] = True

    return out


def main():
    payload = {
        'section': 500,
        'source': 'loop/rounds/026 (two coupled cycles, absolute vs gauge arrow, OPEN item 5); executed by Claude',
        'z3': z3_certificates(),
        'sympy': symbolic_certificates(),
        'versions': {
            'python': platform.python_version(),
            'sympy': sp.__version__,
            'z3': z3.get_version_string(),
        },
    }
    path = ROOT / 'graph' / 'data' / 's500_relative_orientation_of_coupled_cycles.json'
    path.write_text(json.dumps(payload, indent=2, default=str) + '\n')
    print(f"{len(payload['z3'])} Z3 certificates and symbolic checks passed; wrote {path}")


if __name__ == '__main__':
    main()
