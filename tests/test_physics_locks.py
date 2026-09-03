#!/usr/bin/env python3
"""Physics locks for EPSILON v0. Tests, not a formal proof. Not a QUANTUM seal."""

from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import epsilon  # noqa: E402


def _card(**overrides):
    carte = {
        "format": epsilon.FORMAT,
        "epsilon_id": "EP-test",
        "quelle_id": None,
        "temoin_id": None,
        "modele": "none",
        "epsilon": None,
        "hmin": None,
        "simule": True,
        "juridiction": "QC",
        "langue": "fr-CA",
        "pose_at": "2026-09-03T00:00:00Z",
        "note": "v0 test. not a proof.",
    }
    carte.update(overrides)
    return carte


def _refus(fn, *args, **kwargs):
    with unittest.TestCase().assertRaises(SystemExit) as ctx:
        fn(*args, **kwargs)
    return str(ctx.exception)


class EpsilonZeroIsALie(unittest.TestCase):
    def test_epsilon_zero_refuses_on_composable(self):
        msg = _refus(epsilon.ecrire, modele="composable", epsilon=0)
        self.assertIn("refus", msg)
        self.assertIn("0", msg)

    def test_epsilon_zero_float_refuses(self):
        msg = _refus(epsilon.ecrire, modele="asymptotic", epsilon=0.0)
        self.assertIn("refus", msg)

    def test_epsilon_zero_on_card_refuses_juger(self):
        msg = _refus(epsilon.juger, _card(modele="composable", epsilon=0, simule=False))
        self.assertIn("refus", msg)

    def test_epsilon_zero_on_none_is_still_a_lie(self):
        msg = _refus(epsilon.ecrire, modele="none", epsilon=0)
        self.assertIn("refus", msg)

    def test_cli_ecrire_epsilon_zero_refuses(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "epsilon.py"), "ecrire",
             "--modele", "composable", "--epsilon", "0",
             "--vers", _scratch_card()],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("refus", (proc.stderr + proc.stdout).lower())


class NonePlusNullIsHonestAllow(unittest.TestCase):
    def test_default_ecrire_is_none_and_null(self):
        carte = epsilon.ecrire()
        self.assertEqual(carte["modele"], "none")
        self.assertIsNone(carte["epsilon"])
        self.assertEqual(carte["format"], "epsilon.v0")

    def test_none_null_juger_is_allow_not_a_proof(self):
        jugement = epsilon.juger(epsilon.ecrire())
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "none")
        self.assertIsNone(jugement["epsilon"])
        note = jugement["note"].lower()
        self.assertIn("pas de preuve", note)

    def test_example_none_card_allows(self):
        carte = epsilon.lire(str(ROOT / "examples" / "none.epsilon.json"))
        jugement = epsilon.juger(carte)
        self.assertEqual(carte["modele"], "none")
        self.assertIsNone(carte["epsilon"])
        self.assertEqual(jugement["decision"], "allow")

    def test_cli_juger_none_example(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "epsilon.py"), "juger",
             str(ROOT / "examples" / "none.epsilon.json")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "allow")
        self.assertEqual(out["flag"], "none")

    def test_none_with_nonzero_epsilon_refuses(self):
        msg = _refus(epsilon.ecrire, modele="none", epsilon=1e-6)
        self.assertIn("none", msg)
        self.assertIn("null", msg)


class ComposableNeedsEpsilonInOpenUnitInterval(unittest.TestCase):
    def test_composable_without_epsilon_refuses(self):
        msg = _refus(epsilon.ecrire, modele="composable")
        self.assertIn("refus", msg)
        self.assertIn("(0, 1)", msg)
        self.assertNotIn("(0, 1]", msg)

    def test_composable_null_epsilon_refuses(self):
        msg = _refus(epsilon.juger, _card(modele="composable", epsilon=None, simule=False))
        self.assertIn("refus", msg)
        self.assertIn("(0, 1)", msg)
        self.assertNotIn("(0, 1]", msg)

    def test_composable_epsilon_zero_refuses(self):
        msg = _refus(epsilon.ecrire, modele="composable", epsilon=0)
        self.assertIn("refus", msg)

    def test_composable_epsilon_negative_refuses(self):
        msg = _refus(epsilon.ecrire, modele="composable", epsilon=-0.1)
        self.assertIn("refus", msg)

    def test_composable_epsilon_one_refuses(self):
        msg = _refus(epsilon.ecrire, modele="composable", epsilon=1)
        self.assertIn("refus", msg)
        self.assertIn("(0, 1)", msg)
        self.assertNotIn("(0, 1]", msg)

    def test_composable_epsilon_above_one_refuses(self):
        msg = _refus(epsilon.ecrire, modele="composable", epsilon=1.1)
        self.assertIn("refus", msg)
        self.assertIn("(0, 1)", msg)

    def test_composable_with_epsilon_in_interval_allows(self):
        carte = epsilon.ecrire(modele="composable", epsilon=1e-6)
        self.assertEqual(carte["modele"], "composable")
        self.assertEqual(carte["epsilon"], 1e-6)
        jugement = epsilon.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "composable")
        self.assertEqual(jugement["epsilon"], 1e-6)

    def test_iid_with_declared_epsilon_allows_on_this_rail(self):
        """famille juge.v0 calls iid a lie. This rail does not collapse that FLAG."""
        carte = epsilon.ecrire(modele="iid", epsilon=1e-6)
        jugement = epsilon.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "iid")


class LeftoverHashIsRappelNotExtraction(unittest.TestCase):
    def test_leftover_absent_when_no_hmin(self):
        carte = epsilon.ecrire(modele="composable", epsilon=1e-6)
        jugement = epsilon.juger(carte)
        self.assertIsNone(jugement.get("leftover_rappel"))
        self.assertNotIn("extrait", jugement)
        self.assertNotIn("photon", json.dumps(jugement).lower())

    def test_leftover_note_says_v0_does_not_extract(self):
        carte = epsilon.ecrire(modele="composable", epsilon=1e-6, hmin=7.2)
        jugement = epsilon.juger(carte)
        self.assertIn("leftover_rappel", jugement)
        self.assertIsInstance(jugement["leftover_rappel"], float)
        note = jugement["note"]
        self.assertIn("rappel", note.lower())
        self.assertIn("n'extrait pas", note)
        self.assertNotIn("photon", note.lower())
        self.assertNotRegex(note.lower(), r"extrait\s+ℓ")

    def test_positive_leftover_still_rappel_not_a_photon(self):
        # ℓ ≈ 8 - 2 log2(1/0.1) > 0, but plafond must allow ε=0.1
        carte = epsilon.ecrire(modele="composable", epsilon=0.1, hmin=8, plafond=1)
        jugement = epsilon.juger(carte)
        expected = 8 - 2.0 * math.log2(1.0 / 0.1)
        self.assertAlmostEqual(jugement["leftover_rappel"], expected)
        self.assertGreater(jugement["leftover_rappel"], 0)
        self.assertIn("n'extrait pas", jugement["note"])
        self.assertIn("rappel", jugement["note"].lower())

    def test_leftover_helper_is_none_without_epsilon(self):
        self.assertIsNone(epsilon.leftover_rappel(7.2, None))
        self.assertIsNone(epsilon.leftover_rappel(None, 1e-6))
        self.assertIsNone(epsilon.leftover_rappel(7.2, 0))


class MissingTheoryFilesDoNotCrash(unittest.TestCase):
    THEORY_PATHS = (
        ROOT / "theorie" / "epsilon.ec",
        ROOT / "formal-layer" / "leftover.ec",
        ROOT / "easycrypt" / "epsilon.ec",
    )

    def test_theory_style_files_are_absent(self):
        for path in self.THEORY_PATHS:
            self.assertFalse(path.exists(), msg="v0 must not vendor EasyCrypt proofs")

    def test_juger_example_without_theory_files(self):
        carte = epsilon.lire(str(ROOT / "examples" / "juge-sans-theorie.epsilon.json"))
        jugement = epsilon.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "composable")
        self.assertEqual(jugement["epsilon"], 1e-6)
        self.assertIn("n'extrait pas", jugement["note"])

    def test_juger_card_pointing_at_missing_theory(self):
        carte = _card(
            modele="composable",
            epsilon=1e-6,
            hmin=7.2,
            plafond=1e-6,
            termes=[],
            simule=False,
            note="theorie/epsilon.ec absent. formal-layer closed. leftover-hash = rappel.",
        )
        jugement = epsilon.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        dumped = json.dumps(jugement)
        self.assertNotIn("formally verified", dumped.lower())
        self.assertNotIn("quantum seal", dumped.lower())

    def test_cli_juger_missing_theory_example(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "epsilon.py"), "juger",
             str(ROOT / "examples" / "juge-sans-theorie.epsilon.json")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "allow")


def _scratch_card():
    with tempfile.NamedTemporaryFile(suffix=".epsilon.json", delete=False) as tmp:
        return tmp.name


if __name__ == "__main__":
    unittest.main()
