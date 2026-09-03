# EPSILON Protocol

**Toute preuve a un ε. Zéro ε est un mensonge.**
**Every proof has an ε. `epsilon: 0` is a lie.**

QKD and DI-randomness papers do not say “safe”. They say *ε-secure*: the advantage for distinguishing the protocol from an ideal resource is ≤ ε. That is Portmann–Renner / composable security. It is not a slogan.

QUELLE names where the bit came from. TÉMOIN names the strength. EPSILON names *how much you may believe it*.

This repository is version 0. Phone + free. MIT. See [INTERDIT.md](INTERDIT.md).

## Models

```
QUELLE/TÉMOIN card  +  model  +  ε  +  H_min?  →  .epsilon.json card
```

| Model | Right to write |
|---|---|
| `none` | Always. Honest default. `epsilon` must be `null`. **Allow, not a proof.** |
| `asymptotic` | Declared ε, regime n → ∞. Not a finite-n proof. |
| `iid` | ε + a written i.i.d. hypothesis. |
| `composable` | ε ∈ (0, 1). Otherwise: refuse. |

`epsilon: 0`: refuse. A finite sample has no zero advantage.
`hmin`: min-entropy bits **per byte**, 0 to 8, or `null`.

v0 **writes** H_min and ε. It does not extract ℓ. leftover-hash is a *rappel* only — not a photon.

## Physics locks (this rail)

- Every proof has an ε. `epsilon: 0` is a lie. Refused.
- Honest default: `modele: none` and `epsilon: null`. That is allow, not a proof.
- **Missing ε is not zero ε.** Named below as a FLAG on other consumers — not a theorem of this rail.
- leftover-hash is a rappel. v0 does not extract ℓ.
- QUANTUM signs later. Keys stay off Git. This repo is not a QUANTUM seal.
- No IBM Job. No BB84-as-composable-proof. No token, L1, or marketplace of ε.
- `os` is phone entropy = classique. This rail does not mint `quantique`.

### Missing ≠ zero (FLAG, not this theorem)

Absence of ε is not `epsilon: 0`. This rail does not treat “field missing” as “advantage zero”.

This rail does not unwind famille `d55799e` (sdk missing → `classique`).
This rail does not collapse the three-consumer FLAG into one rule:

| Consumer (closed — not this repo) | When ε is missing |
|---|---|
| acorn-juge Worker | `400 EPSILON_MISSING` |
| famille sdk (`d55799e`) | `classique` |
| GARDE | fail-closed |

Imagine those closed. Judgment here is Carl: `python3 epsilon.py juger`.

## How to run

```bash
python3 epsilon.py ecrire
python3 epsilon.py ecrire --modele composable --epsilon 1e-6 --hmin 7.2 --quelle-id QL-ex
python3 epsilon.py lire examples/none.epsilon.json
python3 epsilon.py juger examples/none.epsilon.json
python3 epsilon.py juger examples/juge-sans-theorie.epsilon.json
```

No lab: `none`. That is correct. That is not a proof.

Physics locks (stdlib, no extra packages):

```bash
python3 -m unittest discover -s tests -v
```

## Verified vs assumed

This rail is **not formally verified**. Tests lock the rows below. Nothing in this repository is a QUANTUM seal.

| Claim | Status |
|---|---|
| `epsilon: 0` is refused | **verified** by tests on this rail |
| `none` + `epsilon: null` is allow, not a proof | **verified** |
| `composable` without ε in (0, 1) is refused | **verified** |
| leftover-hash is not claimed as extraction | **verified** |
| missing theory-style files do not crash `juger` | **verified** |
| Portmann–Renner meaning of ε | **assumed** (paper, not proven here) |
| leftover-hash lemma as a formula | **assumed**, written as rappel |
| QUANTUM signature | **later** — keys off Git, not in this repo |
| EasyCrypt / formal-layer | **not here** |
| `os` → `quantique` | **refused** — phone entropy stays classique |

## What v0 is not

See [INTERDIT.md](INTERDIT.md). In short:

1. Do not write `epsilon: 0`.
2. Do not write `modele: composable` without ε in (0, 1).
3. Do not say “unconditional security” without ε.
4. Do not paste an IBM Job / software BB84 as a composable proof.
5. Do not write `hmin` outside `[0, 8]` bits per byte.
6. No token, L1, marketplace of ε.
7. Do not pass leftover-hash off as a photon.

The honest default is `modele: none`, `epsilon: null`.
A QKD paper writes ε. A pitch does not.

## Physique (borne, pas décor)

- CHSH ∈ (2, 2√2] → TÉMOIN `di`
- Trous de détection / localité / liberté → BRUIT (zip tant que repo fermé)
- Un run 2026 ≠ un run 2031 → ANCRAGE (zip)
- ε-sécurité composable + H_min → **EPSILON**
- Harvest-now-decrypt-later → HORIZON (`UFHY1` = Ed25519 + ML-DSA-65)

Pas de Host Alice. Pas de Job IBM.

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |
| [EPSILON](https://github.com/carllaliberte/epsilon-protocol) | avec quel ε |

MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe **plus tard**. Les clés restent hors Git. Ce dépôt n'est pas un sceau QUANTUM.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`PHYSIQUE.md`](PHYSIQUE.md) — supervision (borne, pas décor)
- [`JUGE.md`](JUGE.md) — pointe le juge universel (autre rail ; `iid` y est un mensonge, pas ici)
- [`schema/epsilon.v0.json`](schema/epsilon.v0.json)
- [`epsilon.py`](epsilon.py) — `ecrire` / `lire` / `juger`
- [`examples/none.epsilon.json`](examples/none.epsilon.json) — défaut honnête
- [`examples/juge-sans-theorie.epsilon.json`](examples/juge-sans-theorie.epsilon.json) — ε déclaré, fichiers de théorie absents
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
