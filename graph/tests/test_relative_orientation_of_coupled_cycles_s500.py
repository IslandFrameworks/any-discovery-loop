"""Independent controls for §500 (two coupled cycles, arrow gauge invariance, PW model)."""
import numpy as np
import sympy as sp
import z3
from graph.derive_relative_orientation_of_coupled_cycles_s500 import (
    z3_certificates,
    symbolic_certificates,
)


def test_smt_queries_replay_from_serialized_assertions():
    for record in z3_certificates():
        solver = z3.Solver()
        solver.set(timeout=15000)
        solver.from_string(record['smt2'])
        assert str(solver.check()) == record['expected']


def test_independent_control_numpy_swap_trace_and_spectrum():
    # Numeric control 1: Recompute swap contraction trace using pure numpy tensor contractions
    Cp = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    Cm = Cp.T
    R = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=float)

    # SWAP trace is sum_{i,j} (Uc)_{i,j} (Us)_{j,i} = Tr(Uc Us^T)
    configs = [(Cp, Cp, 3.0), (Cp, Cm, 0.0), (Cm, Cp, 0.0), (Cm, Cm, 3.0)]
    for Uc, Us, expected in configs:
        trace_val = np.einsum('ij,ji->', Uc, Us.T)
        assert np.isclose(trace_val, expected)
        # Joint mirror invariance
        Uc_m = R @ Uc @ R
        Us_m = R @ Us @ R
        trace_m = np.einsum('ij,ji->', Uc_m, Us_m.T)
        assert np.isclose(trace_m, expected)


def test_independent_control_so2_lie_algebra_exponential():
    # Numeric control 2: Verify J = K/sqrt(3) directly generates planar SO(2) rotation by 2pi/3
    J = np.array([[0.0, 1.0], [-1.0, 0.0]])
    theta = 2.0 * np.pi / 3.0
    # exp(theta * J) via Euler formula cos(theta)*I + sin(theta)*J
    rot_pos = np.cos(theta) * np.eye(2) + np.sin(theta) * J
    rot_neg = np.cos(-theta) * np.eye(2) + np.sin(-theta) * J

    # Eigenvalues of rot_pos must be e^{\pm 2pi i / 3}
    w_pos = np.linalg.eigvals(rot_pos)
    expected_eigs = np.exp([2j * np.pi / 3.0, -2j * np.pi / 3.0])
    assert np.allclose(np.sort_complex(w_pos), np.sort_complex(expected_eigs))

    # Reflection matrix sigma_z anticommutes with J and conjugates rot_pos into rot_neg
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]])
    assert np.allclose(sigma_z @ J @ sigma_z, -J)
    assert np.allclose(sigma_z @ rot_pos @ sigma_z, rot_neg)


def test_independent_control_page_wootters_svd_and_rank():
    # Numeric control 3: Direct SVD rank determination of Page-Wootters constraint matrices
    Cp = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    Cm = Cp.T
    I9 = np.eye(9)

    H_co = I9 - np.kron(Cp, Cp)
    H_counter = I9 - np.kron(Cp, Cm)

    # Rank must be 6, nullity must be 3
    s_co = np.linalg.svd(H_co, compute_uv=False)
    s_counter = np.linalg.svd(H_counter, compute_uv=False)

    rank_co = np.sum(s_co > 1e-10)
    rank_counter = np.sum(s_counter > 1e-10)

    assert rank_co == 6
    assert rank_counter == 6
    assert (9 - rank_co) == 3
    assert (9 - rank_counter) == 3


def test_symbolic_records_match_expected_claims():
    out = symbolic_certificates()
    assert out['500_1_charpoly'] == 'lambda**3 - 1'
    assert out['500_1_traces_1_to_6'] == [0, 0, 3, 0, 0, 3]
    assert out['500_2_swap_traces']['(1,1)'] == 3
    assert out['500_2_swap_traces']['(1,-1)'] == 0
    assert out['500_2_swap_traces']['(-1,1)'] == 0
    assert out['500_2_swap_traces']['(-1,-1)'] == 3
    assert out['500_3_complex_structure_J_v'] == [[0, 1], [-1, 0]]
    assert out['500_4_modular_signs_verified'] is True
    assert out['500_5_PW_kernel_dims'] == {'ker_co': 3, 'ker_counter': 3}
    assert out['500_5_reduced_marginals_identical'] is True
