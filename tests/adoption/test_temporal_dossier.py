"""Consistency checks of the Temporal provider dossier (EXEC-TEMPORAL-PINS-001).

Standard library only. Reads the three dossier files by this file's own path, writes nothing and opens no socket.
"""

import datetime
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "adoption" / "temporal"
HEX64 = re.compile(r"[0-9a-f]{64}")
PLACEHOLDERS = ("<server version>", "<sdk version>", "<pin date>", "UNRESOLVED", "pending:")
ENTRY_KEYS = ("fileName", "version", "sha256", "size", "licence", "uploadTime", "mirrorObject")


def _time(text):
    return datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))


class TemporalDossierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provider = json.loads((DOSSIER / "PROVIDER.json").read_text(encoding="utf-8"))
        cls.sbom = json.loads((DOSSIER / "SBOM.cdx.json").read_text(encoding="utf-8"))
        cls.closure = cls.provider["closure"]

    def test_identity_and_state(self):
        p = self.provider
        self.assertEqual(p["moduleId"], "planeon.orchestrator.temporal")
        self.assertEqual(p["role"], "OPTIONAL")
        self.assertIs(p["selectable"], False)
        self.assertEqual(p["evidenceState"], "PACKET_PUBLISHED")
        self.assertNotIn("READY", json.dumps(p))

    def test_closure_entries(self):
        self.assertTrue(self.closure)
        for e in self.closure:
            for key in ENTRY_KEYS:
                self.assertIn(key, e, e.get("fileName"))
            self.assertRegex(e["sha256"], HEX64)
            self.assertIsInstance(e["size"], int)
            self.assertGreater(e["size"], 0)
            self.assertTrue(e["licence"]["expression"])
            self.assertEqual(e["mirrorObject"], "sha256/" + e["sha256"])
            _time(e["uploadTime"])
        self.assertEqual(len({e["sha256"] for e in self.closure}), len(self.closure))

    def test_no_sdist(self):
        for e in self.closure:
            self.assertIn(e.get("kind"), ("wheel", "release-asset"), e["fileName"])
            if e["kind"] == "wheel":
                self.assertTrue(e["fileName"].endswith(".whl"))

    def test_sbom_matches_record(self):
        self.assertEqual(self.sbom["bomFormat"], "CycloneDX")
        comps = self.sbom["components"]
        self.assertEqual(len(comps), len(self.closure))
        by_hash = {c["hashes"][0]["content"]: c for c in comps}
        for e in self.closure:
            c = by_hash[e["sha256"]]
            self.assertEqual(c["hashes"], [{"alg": "SHA-256", "content": e["sha256"]}])
            self.assertEqual(c["name"], e["fileName"])
            self.assertEqual(c["version"], e["version"])
            self.assertEqual(c["licenses"], [{"expression": e["licence"]["expression"]}])

    def test_quarantine(self):
        q = self.provider["quarantine"]
        self.assertEqual(sorted(q), ["decisionRef", "exemption", "minimumDays", "policyItem", "source"])
        self.assertIn(q["source"], ("OWNER_DECISION", "POLICY_IN_FORCE"))
        self.assertIs(type(q["minimumDays"]), int)
        self.assertGreater(q["minimumDays"], 0)
        self.assertEqual(q["policyItem"], "SUPPLY-QUARANTINE-001")
        self.assertEqual(q["exemption"]["kind"], "SECURITY_UPDATE")
        if q["exemption"]["used"]:
            self.assertTrue(q["exemption"].get("reason"))
            return
        pinned = _time(self.provider["pinnedAt"])
        for e in self.closure:
            self.assertLessEqual(_time(e["uploadTime"]) + datetime.timedelta(days=q["minimumDays"]), pinned,
                                 e["fileName"])

    def test_no_placeholders(self):
        for name in ("PROVIDER.json", "SBOM.cdx.json", "NOTICE.md"):
            text = (DOSSIER / name).read_text(encoding="utf-8")
            for ph in PLACEHOLDERS:
                self.assertNotIn(ph, text, name)


if __name__ == "__main__":
    unittest.main()
