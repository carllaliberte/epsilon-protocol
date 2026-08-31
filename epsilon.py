#!/usr/bin/env python3
"""EPSILON v0 — écrire / lire / juger un ε. Zéro ε est un mensonge."""

from __future__ import annotations

import argparse
import json
import math
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

FORMAT = "epsilon.v0"
MODELES = ("none", "asymptotic", "iid", "composable")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _garde(carte: dict) -> None:
    modele = carte.get("modele")
    if modele not in MODELES:
        raise SystemExit("modele : none | asymptotic | iid | composable")
    eps = carte.get("epsilon")
    hmin = carte.get("hmin")
    if modele == "none":
        if eps is not None:
            raise SystemExit("refus : modele none exige epsilon null")
    else:
        if not isinstance(eps, (int, float)) or isinstance(eps, bool):
            raise SystemExit("refus : " + modele + " exige epsilon dans (0, 1]")
        if eps <= 0:
            raise SystemExit("refus : epsilon 0. un échantillon fini n'a pas d'avantage nul")
        if eps > 1:
            raise SystemExit("refus : epsilon > 1")
    if hmin is not None:
        if not isinstance(hmin, (int, float)) or isinstance(hmin, bool):
            raise SystemExit("hmin : nombre ou null")
        if hmin < 0 or hmin > 8:
            raise SystemExit("refus : hmin hors [0, 8] bits/octet")
    note = (carte.get("note") or "").lower()
    if "inconditionnel" in note or "unconditional" in note:
        raise SystemExit("refus : inconditionnel sans droit. écris epsilon")


def leftover_rappel(hmin: float | None, eps: float | None) -> float | None:
    if hmin is None or eps is None or eps <= 0:
        return None
    return hmin - 2.0 * math.log2(1.0 / float(eps))


def ecrire(
    modele: str = "none",
    epsilon: float | None = None,
    hmin: float | None = None,
    quelle_id: str | None = None,
    temoin_id: str | None = None,
    simule: bool | None = None,
    juridiction: str = "QC",
    langue: str = "fr-CA",
) -> dict:
    modele = (modele or "none").strip().lower()
    if simule is None:
        simule = modele != "composable"
    carte = {
        "format": FORMAT,
        "epsilon_id": "EP-" + uuid.uuid4().hex[:12],
        "quelle_id": quelle_id or None,
        "temoin_id": temoin_id or None,
        "modele": modele,
        "epsilon": epsilon,
        "hmin": hmin,
        "simule": bool(simule),
        "juridiction": juridiction,
        "langue": langue,
        "pose_at": _now(),
        "note": "v0 non signée. QUANTUM signe plus tard. ε=0 interdit.",
    }
    _garde(carte)
    return carte


def lire(chemin: str) -> dict:
    p = Path(chemin).expanduser()
    carte = json.loads(p.read_text(encoding="utf-8"))
    if carte.get("format") != FORMAT:
        raise SystemExit("pas une fiche epsilon.v0")
    _garde(carte)
    return carte


def juger(carte: dict) -> dict:
    _garde(carte)
    modele = carte["modele"]
    eps = carte.get("epsilon")
    hmin = carte.get("hmin")
    rappel = leftover_rappel(hmin, eps)
    if modele == "none":
        return {
            "decision": "allow",
            "flag": "none",
            "epsilon": None,
            "note": "pas de preuve. l'acte est vrai. la borne est nulle.",
        }
    note = "ε déclaré sous modèle " + modele + "."
    if rappel is not None:
        note += " leftover-hash rappel ℓ≈%.3f bit/octet. v0 n'extrait pas." % rappel
        if rappel < 0:
            note += " H_min insuffisant pour cet ε."
    return {
        "decision": "allow",
        "flag": modele,
        "epsilon": eps,
        "hmin": hmin,
        "leftover_rappel": rappel,
        "simule": carte.get("simule"),
        "note": note,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="epsilon")
    sub = p.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("ecrire")
    pe.add_argument("--modele", default="none")
    pe.add_argument("--epsilon", type=float, default=None)
    pe.add_argument("--hmin", type=float, default=None)
    pe.add_argument("--quelle-id", default=None)
    pe.add_argument("--temoin-id", default=None)
    pe.add_argument("--simule", action="store_true", default=False)
    pe.add_argument("--pas-simule", action="store_true", default=False)
    pe.add_argument("--juridiction", default="QC")
    pe.add_argument("--langue", default="fr-CA")
    pe.add_argument("--vers", default="carte.epsilon.json")
    pl = sub.add_parser("lire")
    pl.add_argument("fichier")
    pj = sub.add_parser("juger")
    pj.add_argument("fichier")
    args = p.parse_args(argv)
    if args.cmd == "ecrire":
        simule = False if args.pas_simule else (True if args.simule else None)
        carte = ecrire(
            modele=args.modele,
            epsilon=args.epsilon,
            hmin=args.hmin,
            quelle_id=args.quelle_id,
            temoin_id=args.temoin_id,
            simule=simule,
            juridiction=args.juridiction,
            langue=args.langue,
        )
        Path(args.vers).write_text(
            json.dumps(carte, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        out = dict(carte)
        out["fichier"] = args.vers
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.cmd == "lire":
        print(json.dumps(lire(args.fichier), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(juger(lire(args.fichier)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
