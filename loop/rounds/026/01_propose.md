## §500 — The Relative Sign of Two Coupled Cycles, Absolute vs. Gauge Time Orientation, and the Bilinear Coupling of $\mathbb{Z}_2$ Arrows Across Four Operational Determinations (`loop/OPEN.md` Item 5 STILL OPEN)

**Research date:** 14 October 2026 (Toronto; UTC 14 October). **Status:** Proposer draft for Round 026. Following Graham's focus for Round 026 (`loop/OPEN.md` Item 5, after §499.7)—
- **Graham's focus (verbatim):** *"OPEN item 5, the last unknown after §499: Graham's premise (non-stasis + non-self-inversion) forces exactly one 3-state cycle up to direction, $\{C_+, C_-\}$, swapped by the mirror $R$. What, if anything, selects the sign? Graham: keep pressing the chain until something concrete appears. Candidates to make CONCRETE with finite, executable witnesses: (a) the sign as a gauge/naming choice: show precisely which readouts are invariant under $R$ (and so cannot see the sign) and whether ANY's readouts are all of that kind; (b) relative orientation: two coupled cycles (two observers / clock and system, §497 Page-Wootters) where each sign alone is a naming choice but the RELATIVE sign (co-rotating vs counter-rotating) is a physical readout (e.g. beat frequency, Sagnac counter-propagation §478, the null ray pairing $-2c^2$ of §499); is 'which way time runs' really the relative sign between the clock and the rest, so that only the product of signs is physical? (c) composition with the light ray: future vs past null cone as the same $\mathbb{Z}_2$, and whether the causal order (what can influence what, §488 signed increments) fixes the relative sign between the 3-cycle and the cone; (d) the 3-cycle's own phase: $C_+$ has eigenvalues $e^{\pm 2\pi i/3}$; a complex structure (choice of $i$ vs $-i$) is the same $\mathbb{Z}_2$; does any ANY relation require a complex phase (holonomy §498) and thereby fix the sign relative to it? For each give witnesses, near-misses, and say exactly which sign is physical (absolute vs relative). Type every claim; keep item 5 OPEN unless certified. Keep the claims JSON compact."*

---

### Upstream Connections

- **Volume I §§110–111, 119, 136–143 & Volume II §§288–301, 317.1–317.8:** Regime tripartition $\mathcal{T} \neq t \neq \tau$ (§136); nonterminality of zero under Axiom $T_1$ (§§138–139); five non-equivalent meanings of zero (§288); role equality vs. numerical equality vs. physical stasis (§317.1–317.4); and near-miss exclusion (§119, §317.8).
- **Volume IV §§385–386, 393, 398.1:** Relativistic boost tick order producing the signed Wigner rotation (§386); $D = A, T = Y, C = N$; cut conservation and circulation in $\ker B$ on $K_3$ (§398.1).
- **Volume V §§413.2, 416, 424, 453.1–453.2:** Metric lapse $N_{\text{ADM}}$ vs. ANY's contextual role $N$ (§413.2); zero-residual observation fibers ($R_O = 0$ is not stasis, §416); typed operational correspondence $\simeq_O$ (§424); expansion sign erasure in $H^2$ (§453.1).
- **Volume VI §§464.3, 478.2, 488.3, 490.2, 492.6, 494.1–494.4, 497.2–497.5, 498.2–498.6, 499.1–499.5:** Non-commuting transpositions producing $S_3$ cycles ($C_+ = T_2 T_1$, §497.2); Page–Wootters internal clock conditioning and the frozen-mode Near-Miss 3A (§497.4); dihedral commutator anticommutation $R[T_2, T_1]R = -[T_2, T_1]$ (§498.2); Sagnac loop holonomy and the exact join $J_\triangle(H_{\text{mag}}) = J^3\sin\Phi$ (§498.3–498.4); bilinear product coupling of time-odd signs ($\sigma_q \sigma_B$, §494.1); transverse null pairing $\eta(v, n) = -2c^2$ lifting self-orthogonality (§499.3); and the two-tier filter (non-stasis + non-self-inversion) uniquely isolating the cyclic pair $\{C_+, C_-\}$ on three states (§499.2, §499.5).

---

### 500.1 Whole-Graph Context Table & Producer Audit of the Numbers Carrying Weight (§476.7, §480.6)

| Candidate Investigation & Reused Archive Links | Specific Mathematical Readout or Filter $\mathcal{O}$ | Exact Transformation Leaving Readout Invariant or Flipping It | Explicit Finite Witness Proposed for Certification | Surviving Near-Miss / Zero-Fiber Keeping `loop/OPEN.md` Item 5 OPEN (§119, §317.8) | Epistemic Status |
|---|---|---|---|---|---|
| **Determination 1 (Candidate a):** *Single-Cycle Gauge Invariance & $R$-Even Scalar Algebra* (§500.2; reusing §497.2, §498.2, §499.5) | On $\mathcal{A}_{\text{cyc}} = \operatorname{span}\{I_3, S, K\}$, every $R$-invariant linear functional satisfies $\mathcal{O}_{\text{even}}(C_+) = \mathcal{O}_{\text{even}}(C_-) = \frac{1}{2}\mathcal{O}_{\text{even}}(S)$. Any scalar functional distinguishing $C_+$ from $C_-$ is $R$-odd: $\mathcal{O}_{\text{odd}}(R U R) = -\mathcal{O}_{\text{odd}}(U)$. | **Passive reflection / basis swap** $U \mapsto R U R$ ($1 \leftrightarrow 2$, swapping $C_+ \leftrightarrow C_-$ while holding the trace/spectrum fixed). | $\operatorname{Tr}(C_\pm^k) = 0$ ($k=1,2$), $\operatorname{char}(C_\pm) = \lambda^3 - 1$; $\mathcal{O}_{\text{cyc}}(C_\pm) = \pm 1$ is $R$-odd; $S = 3P_{\text{sym}} - I_3$ is $R$-even. | **Near-Miss 1A:** An isolated cycle has no basis-independent scalar distinguishing $C_+$ from $C_-$; the absolute sign is an unobservable gauge convention. | Dihedral algebra: `THEOREM`; Gauge status of absolute sign: `CONDITIONAL` |
| **Determination 2 (Candidate b):** *Two Coupled Cycles & Relative Sign Invariance* (§500.3; reusing §494.1, §497.4, §498.2) | For $U_C = C_+^{\sigma_C}, U_S = C_+^{\sigma_S}$ ($\sigma_C, \sigma_S \in \{+1, -1\}$), the **swap-contraction trace** is $\mathcal{T}_{\text{rel}} := \operatorname{Tr}\big(\operatorname{SWAP}(U_C \otimes U_S^\dagger)\big) = \operatorname{Tr}(U_C U_S^{-1}) = 3\delta_{\sigma_C, \sigma_S}$. | **Joint reflection** $R_{\text{tot}} = R \otimes R$ flips $(\sigma_C, \sigma_S) \mapsto (-\sigma_C, -\sigma_S)$ while holding the product $\sigma_{\text{rel}} = \sigma_C \sigma_S$ and $\mathcal{T}_{\text{rel}}$ strictly invariant! | Co-rotating ($\sigma_{\text{rel}} = +1$): $\operatorname{Tr}(U_C U_S^{-1}) = 3$; Counter-rotating ($\sigma_{\text{rel}} = -1$): $\operatorname{Tr}(U_C U_S^{-1}) = 0$. | **Near-Miss 2A:** Joint mirror $R_{\text{tot}}$ flips both cycles simultaneously without changing $\sigma_{\text{rel}}$; absolute signs remain invisible. | Tensor algebra: `THEOREM`; Bipartite relative observable: `CONDITIONAL` |
| **Determination 3 (Candidate d):** *Planar Complex Structure on $V_0 = \mathbf{1}^\perp$* (§500.4; reusing §498.3–498.4, §499.5) | On the 2D traceless subspace $V_0$, $J := \frac{1}{\sqrt{3}}K = \frac{1}{\sqrt{3}}(C_+ - C_-)$ satisfies $J^2 = -I_{V_0}$. In this plane, $C_\pm = -\frac{1}{2}I_{V_0} \pm \frac{\sqrt{3}}{2}J$. | Conjugating by $R$ yields $R J R = -J$, which is the exact geometric realization of complex conjugation $i \mapsto -i$. | $(J)_{V_0} = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$, $J^2 = -I_2$; eigenvalues $\pm i$; $R$ acts as $\sigma_z$, anticommuting with $J$: $\{R, J\} = 0$. | **Near-Miss 3A:** Choosing $C_+$ over $C_-$ is mathematically identical to choosing $+i$ over $-i$; ANY contains no native preference for $+i$. | Complex structure: `THEOREM`; Identification with time: `SPECULATION` |
| **Determination 4 (Candidate c):** *Coupling with the Causal Cone & Synchronization* (§500.5; reusing §488.3, §490.2, §499.3) | Causal signal propagation $x = \sigma_{\text{cone}} c t$ ($\sigma_{\text{cone}} \in \{+1, -1\}$) couples emission at tick $k_{\text{emit}}$ to reception at $k_{\text{rec}}$: $\Delta k \equiv \sigma_{\text{clock}} \sigma_{\text{cone}} \pmod 3$. | Coordinate time reversal $T: t \mapsto -t$ flips both $\sigma_{\text{cone}} \mapsto -\sigma_{\text{cone}}$ and $\sigma_{\text{clock}} \mapsto -\sigma_{\text{clock}}$, preserving the product $\sigma_{\text{cone}}\sigma_{\text{clock}}$. | Right-propagating causal ray: $v = (c, c)^T$, $\eta(v, n) = -2c^2$; $\sigma_{\text{clock}} \sigma_{\text{cone}} = +1$ for forward causal advance. | **Near-Miss 4A:** $PT$ leaves the null ray invariant as a geometric line and reverses tick order, holding the relative causal synchronization invariant. | Minkowski kinematics: `PHYSICS-IMPORTED` / `ESTABLISHED` |

**Producer audit of the numbers carrying weight in §500 (§476.7, §480.6):**
- **`3` vs. `0` in the swap trace $\operatorname{Tr}(U_C U_S^{-1})$ (§500.3):** When two 3-cycles co-rotate ($\sigma_C = \sigma_S$), $U_C U_S^{-1} = C_+ C_+^{-1} = I_3$, whose trace is the dimension **`3`** of the entered state space. When they counter-rotate ($\sigma_C \neq \sigma_S$), $U_C U_S^{-1} = C_+^2 = C_-$, whose trace is **`0`** because $C_-$ is fixed-point-free. The contrast $3$ vs. $0$ is an invariant integer readout of relative orientation.
- **`-I_2` and `\sqrt{3}` in $J^2 = -I_2$ and $J = K/\sqrt{3}$ (§500.4):** The commutator $K = [T_2, T_1]$ satisfies $K^2 = -3(I_3 - P_{\text{sym}})$. On the 2D subspace orthogonal to $\mathbf{1} = (1,1,1)^T$, $I_3 - P_{\text{sym}} = I_2$, so $K^2 = -3 I_2$. Dividing $K$ by the geometric factor **`\sqrt{3}`** produces a normalized operator $J$ satisfying $J^2 = \mathbf{-I_2}$, which is an exact planar complex structure.
- **`-1/2` and `\sqrt{3}/2` in $C_\pm = -\frac{1}{2}I_2 \pm \frac{\sqrt{3}}{2}J$ (§500.4):** These coefficients are $\cos(2\pi/3) = \mathbf{-1/2}$ and $\sin(2\pi/3) = \mathbf{\sqrt{3}/2}$, reflecting the rotation angle $2\pi/3$ of a 3-cycle in the Euclidean plane.
- **`+1` in $\sigma_{\text{rel}} = \sigma_C \sigma_S$ (§500.3):** The numeral **`+1`** signifies co-rotation (parallel arrows), while **`-1`** signifies counter-rotation (anti-parallel arrows). Both signs are eigenvalues of the $\mathbb{Z}_2$ relative parity operator.

---

### 500.2 Determination 1 — The Absolute Sign as a Gauge/Naming Choice: Invariant Scalar Algebra of a Single Cycle

In Volume VI §499, the two-tier filter (non-stasis $\operatorname{Fix}(U) = \emptyset$ plus non-self-inversion $U \neq U^{-1}$) uniquely isolated the pair of 3-cycles $\{C_+, C_-\}$ on three labelled states $\mathcal{S}_3 = \{0, 1, 2\}$. The conjugating mirror $R = T_1 T_2 T_1 = (1 \leftrightarrow 2)$ swaps them: $R C_+ R = C_-$.

1. **Characterization of $R$-Even vs. $R$-Odd Functionals on the Cycle Algebra (`THEOREM`, proposed in Claim C1):**
   The cycle algebra is $\mathcal{A}_{\text{cyc}} := \operatorname{span}\{I_3, C_+, C_-\} = \operatorname{span}\{I_3, S, K\}$, where $S = C_+ + C_-$ is symmetric and $K = C_+ - C_-$ is antisymmetric (§498.2).
   - Under $R$-conjugation: $R I_3 R = I_3$, $R S R = +S$, and $R K R = -K$.
   - Any linear functional $\mathcal{F}: \mathcal{A}_{\text{cyc}} \to \mathbb{R}$ decomposes uniquely into an $R$-even part and an $R$-odd part:
     \[
     \mathcal{F}(U) = \mathcal{F}_{\text{even}}(U) + \mathcal{F}_{\text{odd}}(U), \qquad \mathcal{F}_{\text{even}}(R U R) = \mathcal{F}_{\text{even}}(U), \quad \mathcal{F}_{\text{odd}}(R U R) = -\mathcal{F}_{\text{odd}}(U).
     \]
   - On the generators $C_\pm = \frac{1}{2}(S \pm K)$:
     \[
     \boxed{\mathcal{F}_{\text{even}}(C_+) = \mathcal{F}_{\text{even}}(C_-) = \frac{1}{2}\mathcal{F}_{\text{even}}(S), \qquad \mathcal{F}_{\text{odd}}(C_+) = -\mathcal{F}_{\text{odd}}(C_-) = \frac{1}{2}\mathcal{F}_{\text{odd}}(K).}
     \]
   - **Consequence for Basis-Independent Observables:**
     Any basis-independent scalar functional $\phi(U)$ that depends only on the similarity class of $U$ (such as trace $\operatorname{Tr}(U^m)$, determinant $\det(U)$, characteristic polynomial $\operatorname{char}(U)$, or von Neumann / linear entropy of an invariant state) satisfies $\phi(R U R) = \phi(U)$ because $R = R^{-1}$. Therefore:
     \[
     \boxed{\phi(C_+) = \phi(C_-) \qquad \text{for every basis-independent scalar functional } \phi.}
     \]
     Specifically, $\operatorname{Tr}(C_+^m) = \operatorname{Tr}(C_-^m)$ for all $m \in \mathbb{N}$, $\det(C_+) = \det(C_-) = 1$, and $\operatorname{char}(C_+) = \operatorname{char}(C_-) = \lambda^3 - 1$.
   - **What Can Distinguish $C_+$ from $C_-$:**
     Only an **$R$-odd functional** $\mathcal{F}_{\text{odd}}$ can distinguish $C_+$ from $C_-$. But an $R$-odd functional requires entering an explicit orientation-odd reference vector (such as $e_1 - e_2$ in the probe $\mathcal{O}_0(U) = (e_1 - e_2)^T U e_0$). If state labels $1$ and $2$ are unobservable internal conventions, the choice between $C_+$ and $C_-$ is an **unobservable gauge degree of freedom** ($\mathbb{Z}_2$ naming choice).

---

### 500.3 Determination 2 — Two Coupled Cycles: The Relative Sign Invariant $\sigma_{\text{rel}} = \sigma_C \sigma_S$

What happens when we consider **two** cycles—such as an internal clock $C$ and an observed system $S$, or two observers?
Let $\mathcal{H}_{\text{tot}} = \mathcal{H}_C \otimes \mathcal{H}_S = \mathbb{C}^3 \otimes \mathbb{C}^3$.
Let $U_C \in \{C_+, C_-\}$ be the clock cycle and $U_S \in \{C_+, C_-\}$ be the system cycle. We write:
\[
U_C = C_+^{\sigma_C}, \qquad U_S = C_+^{\sigma_S}, \qquad \sigma_C, \sigma_S \in \{+1, -1\}.
\]

1. **The Relative Sign $\sigma_{\text{rel}} := \sigma_C \sigma_S$ and Joint Mirror Invariance (`THEOREM`, proposed in Claim C2):**
   Consider the joint reflection mirror $R_{\text{tot}} := R \otimes R$ on $\mathcal{H}_C \otimes \mathcal{H}_S$.
   Under $R_{\text{tot}}$, the two cycles transform as:
   \[
   R_{\text{tot}}\,(U_C \otimes U_S)\,R_{\text{tot}} = (R U_C R) \otimes (R U_S R) = C_-^{\sigma_C} \otimes C_-^{\sigma_S} = C_+^{-\sigma_C} \otimes C_+^{-\sigma_S}.
   \]
   Thus $R_{\text{tot}}$ acts on the individual signs as:
   \[
   (\sigma_C,\, \sigma_S) \;\longmapsto\; (-\sigma_C,\, -\sigma_S).
   \]
   Now evaluate the product $\sigma_{\text{rel}} := \sigma_C \sigma_S$:
   \[
   \boxed{\sigma_{\text{rel}}' = (-\sigma_C)(-\sigma_S) = \sigma_C \sigma_S = \sigma_{\text{rel}}.}
   \]
   **The relative sign $\sigma_{\text{rel}} \in \{+1, -1\}$ is strictly invariant under joint reflection!**

2. **The Swap-Contraction Trace as an Explicit Basis-Independent Observable (`THEOREM`, proposed in Claim C2):**
   Define the bipartite swap operator $\operatorname{SWAP}$ on $\mathcal{H}_C \otimes \mathcal{H}_S$ by $\operatorname{SWAP}|j, k\rangle = |k, j\rangle$.
   For any two operators $A$ on $\mathcal{H}_C$ and $B$ on $\mathcal{H}_S$, the trace contraction with $\operatorname{SWAP}$ satisfies the standard identity:
   \[
   \operatorname{Tr}\big(\operatorname{SWAP}\,(A \otimes B)\big) = \operatorname{Tr}(A B).
   \]
   Now evaluate the relative cycle observable $\mathcal{T}_{\text{rel}}(U_C, U_S) := \operatorname{Tr}\big(\operatorname{SWAP}\,(U_C \otimes U_S^\dagger)\big) = \operatorname{Tr}(U_C U_S^{-1})$:
   - **Case 1: Co-Rotating Cycles ($\sigma_C = \sigma_S \iff \sigma_{\text{rel}} = +1$):**
     If $\sigma_C = \sigma_S = +1$, then $U_C = C_+$ and $U_S = C_+$, so $U_C U_S^{-1} = C_+ C_+^{-1} = I_3$.
     If $\sigma_C = \sigma_S = -1$, then $U_C = C_-$ and $U_S = C_-$, so $U_C U_S^{-1} = C_- C_-^{-1} = I_3$.
     In both cases:
     \[
     \boxed{\mathcal{T}_{\text{rel}} = \operatorname{Tr}(I_3) = 3.}
     \]
   - **Case 2: Counter-Rotating Cycles ($\sigma_C \neq \sigma_S \iff \sigma_{\text{rel}} = -1$):**
     If $\sigma_C = +1, \sigma_S = -1$, then $U_C = C_+$ and $U_S = C_-$, so $U_C U_S^{-1} = C_+ C_-^{-1} = C_+^2 = C_-$.
     If $\sigma_C = -1, \sigma_S = +1$, then $U_C = C_-$ and $U_S = C_+$, so $U_C U_S^{-1} = C_- C_+^{-1} = C_-^2 = C_+$.
     Because both $C_+$ and $C_-$ have zero trace:
     \[
     \boxed{\mathcal{T}_{\text{rel}} = \operatorname{Tr}(C_\pm) = 0.}
     \]
   - **Unified Algebraic Formula:**
     \[
     \boxed{\mathcal{T}_{\text{rel}}(U_C, U_S) = \operatorname{Tr}\big(U_C U_S^{-1}\big) = 3\,\delta_{\sigma_C, \sigma_S} = \frac{3}{2}\big(1 + \sigma_{\text{rel}}\big).}
     \]
     This proves that **relative orientation is an absolute, gauge-invariant physical scalar**! An observer does not need to know whether their clock runs "forward" or "backward" in some cosmic sense; they can unambiguously measure whether a physical system co-rotates with their clock ($\mathcal{T}_{\text{rel}} = 3$) or counter-rotates ($\mathcal{T}_{\text{rel}} = 0$).

---

### 500.4 Determination 3 — The 3-Cycle's Own Phase as a Planar Complex Structure ($J^2 = -I_2$)

Graham asked: *"(d) the 3-cycle's own phase: $C_+$ has eigenvalues $e^{\pm 2\pi i/3}$; a complex structure (choice of $i$ vs $-i$) is the same $\mathbb{Z}_2$; does any ANY relation require a complex phase (holonomy §498) and thereby fix the sign relative to it?"*

1. **Construction of the Complex Structure from the Commutator $K$ (`THEOREM`, proposed in Claim C3):**
   In $\mathbb{R}^3$, the vector $\mathbf{1} = (1, 1, 1)^T$ spans the 1D trivial representation of $S_3$, on which $C_\pm \mathbf{1} = \mathbf{1}$ and $K \mathbf{1} = 0$.
   Let $V_0 := \mathbf{1}^\perp = \{x \in \mathbb{R}^3 : x_0 + x_1 + x_2 = 0\}$ be the 2D orthogonal complement.
   - On $V_0$, the projector is $P_{V_0} = I_3 - \frac{1}{3}\mathbf{1}\mathbf{1}^T = I_3 - P_{\text{sym}}$.
   - In §498.2, we proved $K^2 = -3(I_3 - P_{\text{sym}})$. Therefore, on $V_0$:
     \[
     K|_{V_0}^2 = -3\,I_{V_0}.
     \]
   - Define the normalized operator on $V_0$:
     \[
     \boxed{J := \frac{1}{\sqrt{3}}\,K\Big|_{V_0} \quad \Longrightarrow \quad J^2 = \frac{1}{3}(-3\,I_{V_0}) = -I_{V_0}.}
     \]
   - **$J$ is an exact complex structure on the real 2D plane $V_0$!**
   - In any orthonormal basis of $V_0$ (e.g., $u_1 = \frac{1}{\sqrt{2}}(1, -1, 0)^T$, $u_2 = \frac{1}{\sqrt{6}}(1, 1, -2)^T$), $J$ is represented by the standard symplectic matrix:
     \[
     [J] = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}.
     \]

2. **Action of the Mirror $R$ as Complex Conjugation ($J \mapsto -J$) (`THEOREM`, proposed in Claim C3):**
   Because $R K R = -K$ (§498.2), conjugating $J$ by the mirror $R$ yields:
   \[
   \boxed{R\,J\,R = -J.}
   \]
   In the basis $\{u_1, u_2\}$, $R$ acts as $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} = \sigma_z$, which anticommutes with $[J] = i\sigma_y$: $\{\sigma_z, i\sigma_y\} = 0$.
   Thus the geometric mirror $R$ acts on the complex structure $J$ as:
   \[
   J \;\longmapsto\; -J \quad \Longleftrightarrow \quad i \;\longmapsto\; -i.
   \]
   - **Decomposition of the Cycles in the Complex Structure:**
     Since $S|_{V_0} = -I_{V_0}$ and $K|_{V_0} = \sqrt{3}J$, the restrictions of $C_+$ and $C_-$ to $V_0$ are:
     \[
     \boxed{C_\pm\Big|_{V_0} = \frac{1}{2}\big(S \pm K\big)\Big|_{V_0} = -\frac{1}{2}\,I_{V_0} \pm \frac{\sqrt{3}}{2}\,J = \cos\!\left(\frac{2\pi}{3}\right)I_{V_0} \pm \sin\!\left(\frac{2\pi}{3}\right)J.}
     \]
     This proves that selecting $C_+$ over $C_-$ is **mathematically identical to choosing the orientation of the complex plane ($+i$ over $-i$)**.
   - **Why No Native Relation Selects $+i$ over $-i$:**
     In pure mathematics, complex conjugation is an automorphism of $\mathbb{C}$. The choice of which square root of $-1$ is called "$+i$" is an unobservable convention unless coupled to an orientation-odd external field (such as an external magnetic flux $\Phi$ in §498.3, where $\mathcal{J}_{\text{hol}} = 3\sin\Phi$ couples the loop orientation to $\operatorname{sgn}\Phi$).

---

### 500.5 Determination 4 — Coupling with the Light Ray: Causal Cone Synchronization

Graham asked: *"(c) composition with the light ray: future vs past null cone as the same $\mathbb{Z}_2$, and whether the causal order (what can influence what, §488 signed increments) fixes the relative sign between the 3-cycle and the cone."*

1. **Coupling Clock Ticks to Causal Signals in $(1+1)$ Spacetime (`PHYSICS-IMPORTED` / `CONDITIONAL`):**
   Consider $(1+1)$ Minkowski spacetime with light speed $c > 0$.
   In §499.3, the null cone equation $Q(dt, dx) = -c^2 dt^2 + dx^2 = 0$ carries no intrinsic arrow because $Q(-dt, dx) = Q(dt, dx)$.
   Selecting the **forward causal cone** $V^+ = \{(dt, dx) : c\,dt \ge |dx|, dt > 0\}$ is an entered orientation choice $\sigma_{\text{cone}} = +1$.
   - Suppose an internal 3-cycle clock ticks at events $(t_k, x_k)$ along an emitter's worldline ($x = 0$): $t_k = k\,\Delta \tau$.
   - At tick $k_{\text{emit}} = 0$, the emitter sends a light signal along the forward null ray $x = c(t - t_0)$.
   - A receiver at distance $L = c\,\Delta \tau > 0$ observes the arrival of the signal at coordinate time $t_{\text{rec}} = t_0 + L/c = \Delta \tau$, which corresponds to clock tick $k_{\text{rec}} = 1$.
   - The observed tick increment is:
     \[
     \Delta k := k_{\text{rec}} - k_{\text{emit}} = 1 - 0 = +1 \pmod 3.
     \]
   - If the clock runs under $C_+$, the succession is $0 \to 1 \to 2$, so $\Delta k = +1$.
   - If the clock is relabelled under $C_-$, the succession is $0 \to 2 \to 1$, so the physical forward time step $t_0 \to t_0 + \Delta\tau$ corresponds to tick $k = 2$ ($\Delta k = 2 \equiv -1 \pmod 3$).
   - More generally, the observed tick succession satisfies:
     \[
     \boxed{\operatorname{sgn}(\Delta k) = \sigma_{\text{clock}}\,\sigma_{\text{cone}}.}
     \]
   - Under total spacetime inversion $PT$ (or time reversal $T$ combined with clock reflection $R$):
     \[
     \sigma_{\text{clock}} \;\longmapsto\; -\sigma_{\text{clock}}, \qquad \sigma_{\text{cone}} \;\longmapsto\; -\sigma_{\text{cone}} \quad \Longrightarrow \quad \sigma_{\text{clock}}'\,\sigma_{\text{cone}}' = \sigma_{\text{clock}}\,\sigma_{\text{cone}}.
     \]
     **The causal advance of a clock tick is a relative sign between the clock cycle and the causal cone!**
     Causality does not determine an absolute sign for $\sigma_{\text{clock}}$; it forces the clock to co-synchronize with the light cone ($\sigma_{\text{clock}}\sigma_{\text{cone}} = +1$).

---

### 500.6 ANY Role Packet, Answer to "Mirror or Circle?", and Upstream Impact

**ANY role packet (§500):**
- **A (Identity):** Two 3-cycle operators $U_C = C_+^{\sigma_C}, U_S = C_+^{\sigma_S}$ on $\mathcal{H}_C \otimes \mathcal{H}_S = \mathbb{C}^3 \otimes \mathbb{C}^3$; planar complex structure $J$ on $V_0 = \mathbf{1}^\perp \subset \mathbb{R}^3$; causal light cone $V^\pm$ in $\mathbb{R}^{1,1}$.
- **Y (Influence / Operator):** Joint mirror reflection $R_{\text{tot}} = R \otimes R$; swap-contraction trace $\mathcal{T}_{\text{rel}} = \operatorname{Tr}\big(\operatorname{SWAP}(U_C \otimes U_S^\dagger)\big)$; planar commutator $J = K/\sqrt{3}$; causal light-ray propagation $x = \sigma_{\text{cone}} c t$.
- **N (Realized Relation / Readout):**
  1. The absolute sign $\sigma \in \{+1, -1\}$ of an isolated cycle is an unobservable $\mathbb{Z}_2$ naming convention: all basis-independent scalar functionals satisfy $\phi(C_+) = \phi(C_-)$.
  2. The relative sign $\sigma_{\text{rel}} := \sigma_C \sigma_S$ between two coupled cycles is a gauge-invariant physical observable: $\mathcal{T}_{\text{rel}} = 3\,\delta_{\sigma_C, \sigma_S} = \frac{3}{2}(1 + \sigma_{\text{rel}})$, strictly invariant under $R_{\text{tot}}$.
  3. Selecting $C_+$ over $C_-$ is mathematically isomorphic to choosing the complex structure orientation $+i$ over $-i$ ($J \mapsto -J$ under $R$).
  4. Causal order fixes the relative product $\sigma_{\text{clock}}\sigma_{\text{cone}} = +1$, not the absolute sign.
  5. `loop/OPEN.md` Item 5 remains **STILL OPEN** because ANY's native relations do not select an absolute sign for an isolated cycle without entering an external reference.

**Answer to Graham's "Mirror or Circle?" question (`loop/OPEN.md`):**
- A single isolated circle has **no absolute orientation**: $C_+$ and $C_-$ are mirror reflections of each other ($R C_+ R = C_-$), sharing the identical spectrum and traces.
- When **two circles interact** (clock and system, or emitter and receiver), their **relative orientation** $\sigma_{\text{rel}} = \pm 1$ is an absolute, gauge-invariant physical observable ($\mathcal{T}_{\text{rel}} = 3$ for co-rotating vs. $0$ for counter-rotating).
- "Which way time runs" is not an absolute sign attached to a solitary universe; it is the **mutual alignment** (co-rotation $\sigma_{\text{rel}} = +1$) of all dynamical processes with the chosen clock and the forward causal cone.

---

### Weak points

First, `loop/OPEN.md` Item 5 remains **STILL OPEN**: proving that relative orientation $\sigma_C \sigma_S$ is a gauge-invariant observable does not natively select $\sigma_C = +1$ for an isolated universe. Second, the complex structure $J = K/\sqrt{3}$ is a 2D planar construction; extending it to higher dimensions or physical spacetime requires entering additional metric structure. Third, the causal cone coupling imports Minkowski geometry and the arrow of radiation/causality ($\sigma_{\text{cone}} = +1$), which is not derived natively from $D/T = C$. Fourth, the swap-trace observable $\mathcal{T}_{\text{rel}}$ assumes an exact bipartite tensor product structure $\mathcal{H}_C \otimes \mathcal{H}_S$, which is an entered model assumption.

---

### Proposed Claims for Execution

```json
[
  {
    "id": "C1",
    "statement": "On the 3-state cycle algebra A_cyc = span{I3, S, K}, every R-invariant linear functional satisfies F_even(C+) = F_even(C-) = F_even(S)/2, while every R-odd functional satisfies F_odd(C+) = -F_odd(C-) = F_odd(K)/2; consequently, every basis-independent scalar functional phi depending only on similarity satisfies phi(C+) = phi(C-), including char(C+) = char(C-) = lambda^3 - 1 and Tr(C+^m) = Tr(C-^m) for all m.",
    "premises": {
      "native": ["A ≃ N(Y)", "DTC IS ANY"],
      "conditional": ["S3 transposition representation on R^3", "Cycle algebra A_cyc"],
      "imported": ["Dihedral group D3 algebra"]
    },
    "near_miss": "Claiming that an isolated 3-cycle possesses a basis-independent scalar invariant that distinguishes C+ from C- without an entered R-odd reference vector.",
    "encoding": "SymPy verification of R-even/odd decomposition on A_cyc, charpoly, and traces; Z3 QF_NRA query showing F(C+) - F(C-) = 0 for all R-invariant functionals.",
    "expected": "UNSAT for F(C+) != F(C-) under R-invariance; certified identities in SymPy.",
    "falsifier": "Finding an R-invariant linear functional on A_cyc that yields distinct values on C+ and C-."
  },
  {
    "id": "C2",
    "statement": "For two coupled 3-cycles U_C = C_+^{sigma_C} and U_S = C_+^{sigma_S} (sigma_C, sigma_S in {+1, -1}), the swap-contraction trace T_rel := Tr(SWAP(U_C (x) U_S^dag)) = Tr(U_C U_S^-1) evaluates to 3 if sigma_C = sigma_S (co-rotating) and 0 if sigma_C != sigma_S (counter-rotating), and is strictly invariant under joint mirror reflection R_tot = R (x) R: T_rel(R U_C R, R U_S R) = T_rel(U_C, U_S).",
    "premises": {
      "native": ["A ≃ N(Y)"],
      "conditional": ["Two-cycle tensor product H_C (x) H_S", "SWAP contraction operator"],
      "imported": ["Matrix trace cyclic and tensor properties"]
    },
    "near_miss": "Claiming that joint mirror reflection flips the relative orientation or alters the swap trace T_rel.",
    "encoding": "SymPy verification of Tr(U_C U_S^-1) for all 4 sign configurations; Z3 QF_NRA query confirming T_rel is 3 for co-rotating and 0 for counter-rotating, and invariant under R_tot.",
    "expected": "UNSAT for any deviation from T_rel = 3*delta(sigma_C, sigma_S); certified in SymPy.",
    "falsifier": "Finding a sign configuration where T_rel fails to distinguish co-rotating from counter-rotating, or where R_tot changes T_rel."
  },
  {
    "id": "C3",
    "statement": "On the 2D traceless subspace V_0 = 1^perp subset R^3, the normalized commutator J := K|_{V_0} / sqrt(3) satisfies J^2 = -I_{V_0}, defining an exact planar complex structure; the mirror R satisfies R J R = -J (acting as complex conjugation J |-> -J); and the cycles restrict to C_+|_{V_0} = -1/2 I_{V_0} + sqrt(3)/2 J and C_-|_{V_0} = -1/2 I_{V_0} - sqrt(3)/2 J.",
    "premises": {
      "native": ["DTC IS ANY"],
      "conditional": ["Traceless subspace V_0 = 1^perp", "Commutator K = [T2, T1]"],
      "imported": ["Planar complex structure definition J^2 = -I"]
    },
    "near_miss": "Claiming that the choice between C+ and C- is independent of the choice of planar orientation / complex unit sign.",
    "encoding": "SymPy symbolic matrix calculation projecting K and R onto an orthonormal basis of V_0 and verifying J^2 = -I_2, R J R = -J, and C_pm decomposition; Z3 QF_NRA polynomial check.",
    "expected": "Exact symbolic verification in SymPy and UNSAT for J^2 + I_2 != 0.",
    "falsifier": "Finding that J^2 != -I_2 on V_0 or that R fails to anticommute with J."
  },
  {
    "id": "C4",
    "statement": "In (1+1) Minkowski spacetime, coupling a 3-cycle clock with tick direction sigma_clock in {+1, -1} to a light ray propagating along the causal cone with orientation sigma_cone in {+1, -1} yields a tick arrival increment satisfying sgn(Delta k) = sigma_clock * sigma_cone; the product sigma_clock * sigma_cone is invariant under total spacetime inversion PT.",
    "premises": {
      "native": ["Linear time T", "Potential distance D"],
      "conditional": ["3-cycle clock coupling to null ray"],
      "imported": ["(1+1) Minkowski metric", "Causal cone definition"]
    },
    "near_miss": "Claiming that causal signal propagation fixes the absolute sign of the clock rather than the bilinear product sigma_clock * sigma_cone.",
    "encoding": "SymPy check of event coordinates, null ray arrival time, and modular tick increments under PT; Z3 QF_NRA query.",
    "expected": "UNSAT for PT violation of the relative product sign; exact tick match.",
    "falsifier": "Demonstrating that an emission-absorption signal can determine the absolute clock orientation without entering a causal cone arrow."
  },
  {
    "id": "C5",
    "statement": "In the Page-Wootters bipartite 3-cycle model, the co-rotating constraint (I_9 - C_3 (x) C_3)|Psi> = 0 yields conditional tick succession s_k = k mod 3, while the counter-rotating constraint (I_9 - C_3 (x) C_3^-1)|Psi> = 0 yields s_k = -k mod 3; both branches possess 3D kernels and identical unconditioned marginals rho_S = 1/3 I_3, leaving loop/OPEN.md Item 5 STILL OPEN because native ANY does not select co-rotating over counter-rotating without an entered boundary contract.",
    "premises": {
      "native": ["ANY role packet", "Zero-residual interrogation"],
      "conditional": ["Bipartite 3-cycle Page-Wootters model"],
      "imported": ["Hilbert space tensor product", "Bayes conditioning"]
    },
    "near_miss": "Claiming that the Page-Wootters constraint uniquely selects the co-rotating branch over the counter-rotating branch.",
    "encoding": "SymPy verification of kernels of I_9 - C_3 (x) C_3 and I_9 - C_3 (x) C_3^-1, their conditional probabilities, and reduced density matrices; Z3 QF_NRA check.",
    "expected": "Both kernels have dimension 3; unconditioned density matrices are identical (1/3 I_3); conditional progressions are exact opposites.",
    "falsifier": "Finding that one of the constraints has a trivial kernel or that native ANY derives a preference for co-rotation."
  }
]
```