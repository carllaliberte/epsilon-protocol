# EPSILON Protocol

**Toute preuve a un ε. Zéro ε est un mensonge.**

Les papiers de QKD et de DI-randomness ne disent pas « sûr ». Ils disent *ε-sûr* : l'avantage pour distinguer le protocole d'une ressource idéale est ≤ ε. C'est Portmann–Renner / la sécurité composable. Ce n'est pas un slogan.

QUELLE dit d'où vient le bit. TÉMOIN dit la force. EPSILON dit *combien on a le droit d'y croire*.

Ce dépôt est la version 0. Téléphone + gratuit. MIT. Voir [INTERDIT.md](INTERDIT.md).

## Primitive

```
carte QUELLE/TÉMOIN  +  modèle  +  ε  +  H_min?  →  fiche .epsilon.json
```

| Modèle | Droit d'écriture |
|---|---|
| `none` | Toujours. Défaut. `epsilon` doit être `null`. |
| `asymptotic` | ε déclaré, régime n → ∞. Pas une preuve finie. |
| `iid` | ε + hypothèse i.i.d. écrite. |
| `composable` | ε ∈ (0, 1). Sinon : refus. |

`epsilon: 0` : refus.
`hmin` : bits d'entropie min **par octet**, 0 à 8, ou `null`.

v0 **écrit** H_min et ε. Il ne prétend pas extraire ℓ (leftover-hash = rappel seulement).

## v0 au cellulaire

```bash
python3 epsilon.py ecrire
python3 epsilon.py ecrire --modele composable --epsilon 1e-6 --hmin 7.2 --quelle-id QL-ex
python3 epsilon.py juger examples/none.epsilon.json
```

Sans labo : `none`. C'est correct.

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

MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe. Les clés restent hors Git.
