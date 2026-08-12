import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gps_score import assess_project, scan_compliance


class GPSTests(unittest.TestCase):
    def test_insufficient_evidence_cannot_be_called_gold(self):
        report = assess_project({"name": "智净巡检", "track": "高教主赛道", "group": "创意组",
                                 "claims": ["多模态 AI 可降低误报率"], "evidence": [],
                                 "team": {"members": 4, "leader_status": "在校生"}})
        self.assertIn(report["level"], {"不可判定", "市级/省级基础"})
        self.assertLess(report["confidence"], 0.5)
        self.assertTrue(report["blocking_gaps"])

    def test_verified_chain_reaches_national_band(self):
        evidence = [{"type": t, "status": "verified", "source": f"test/{t}.pdf"}
                    for t in ("experiment", "ip", "customer", "financial", "team_contribution", "survey")]
        report = assess_project({"name": "样机项目", "track": "高教主赛道", "group": "创业组",
                                 "claims": ["在线监测降低误报率"], "evidence": evidence,
                                 "team": {"members": 6, "leader_status": "在校生", "leader_equity": .15, "team_equity": .4}})
        self.assertIn(report["level"], {"国银潜力", "国金潜力"})
        self.assertGreaterEqual(report["score"], 60)
        self.assertGreaterEqual(report["evidence_coverage"], .6)

    def test_compliance_scanner_flags_unverified_numbers_and_outsourcing(self):
        findings = scan_compliance({"claims": ["市场规模 100 亿元", "误报率降低 60%"],
                                    "evidence": [{"type": "draft", "status": "unverified", "source": "draft.pptx"}],
                                    "workflow": {"external_vendor_writing": True}})
        codes = {item["code"] for item in findings}
        self.assertIn("UNVERIFIED_CLAIM", codes)
        self.assertIn("OUTSOURCED_CORE_MATERIAL", codes)

    def test_demo_is_json_serializable(self):
        data = json.loads((ROOT / "examples" / "demo-project.json").read_text(encoding="utf-8"))
        json.dumps(assess_project(data), ensure_ascii=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
