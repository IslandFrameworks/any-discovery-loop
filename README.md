# ANY discovery loop source and audit example

Companion to *ANY: a relational algebra* by Graham Johns, Island Frameworks.
Research preprint: [ANY: a relational algebra](https://doi.org/10.5281/zenodo.23380347).

This supplement contains the research orchestration source used to propose, develop, audit, implement and integrate ANY research rounds. Round 026 (§500), summarized in paper §11.8, supplies a complete recorded example. The orchestration source is preserved with three configuration changes in `loop/discover.py`: the Vertex project and CLI paths are configurable via the environment, and Vertex authentication requires an explicit project.

## Release status

This is the source snapshot of a solo research workflow. The archived round and
offline checks are the supported starting point. Outside pull requests are
paused. The full research run used paid model calls and cost hundreds of dollars.
The offline replay requires no model calls once dependencies are installed.

## Follow the audit

| Step | File | What to look for |
| --- | --- | --- |
| Proposal | [01_propose.md](loop/rounds/026/01_propose.md) | The question about absolute versus relative cycle orientation |
| Development | [02_develop.md](loop/rounds/026/02_develop.md) | The preliminary matrix representation and trace identity |
| Audit | [03_audit.md](loop/rounds/026/03_audit.md) | The mirror was incorrectly claimed to be diagonal in the cyclic basis. The audit also separated passive relabelling from an active flip with the pairing held fixed. |
| Revision | [04_revise.md](loop/rounds/026/04_revise.md) | The draft separates the cyclic basis from the mirror eigenbasis and states that the relative sign depends on the entered pairing. |
| Verification | [claims.json](loop/rounds/026/claims.json) and [claude_check.md](loop/rounds/026/claude_check.md) | The proposed claims, independently checked identities and limits of the result |
| Research record | [section.md](loop/rounds/026/section.md) | The revised draft at the integration step. Volume VI §500 contains the final research record, including its later referee corrections. |

Gemini 3.8 Flash developed and audited this round when GPT‑6 was unavailable. The independent calculation and recorded referee checks contribute separate evidence. The archived model output is preserved as research provenance. Refer to the final paper and record for the author's conclusions.

## Reproduce the mathematical checks offline

Using Python 3.12 in the extracted directory, create a virtual environment and install the pinned requirements. Once installed, these commands require no model account or network access.

```sh
python -m pip install -r requirements.txt
python -m pytest -q graph/tests
mkdir -p graph/data
python -m graph.derive_relative_orientation_of_coupled_cycles_s500
python loop/rounds/026/claude_spotcheck.py
```

The derivation generates a fresh result file in `graph/data/`. The tests replay the embedded SMT inputs and check the coupled-cycle trace, its joint-mirror invariance, and the scope of the pairing. `fixtures/s500_recorded_results.json` preserves the archived solver output for comparison. The numerical spot-check is a separate implementation.

To exercise the original integration program, work in this extracted copy after running the derivation. The following creates a demonstration volume and appends the archived revised draft and the freshly generated execution record. If a volume already exists, use a fresh extracted copy.

```sh
mkdir -p volumes
printf '# Integration demonstration\n' > volumes/11_Laws_Research_Volume_VI.md
python loop/integrate.py 26
```

The program refuses to append when the results file is missing, an outcome differs from its expectation, the verdict marks the round rejected, or the section already exists.

## Historical live-run context

`loop/discover.py` records the model routing, prompt construction and audit sequence. `loop/implement.py` records how revised claims produce candidate check files. A fresh live round requires a configured model backend, credentials supplied by the operator, and research context such as the operating document, graph progress, open questions and prerequisite check templates. The supplement supports an offline replay of the checks and integration decision. Live provider availability and historical model outputs can vary.

## Working with generated files

A live run may send the selected research context to the configured provider
and write model-generated Python. Use a separate research workspace and your
own provider configuration. Review generated code and the context it receives
before executing or sharing a round. The local spend tracker is an estimate.
Live provider charges are managed through the operator’s account.
