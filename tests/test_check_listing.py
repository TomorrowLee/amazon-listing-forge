import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_listing import inspect


class ListingChecks(unittest.TestCase):
    def test_boundary_includes_spaces(self):
        self.assertTrue(inspect({"title": "A" * 74 + " "})["structural_pass"])
        self.assertFalse(inspect({"title": "A" * 74 + " B"})["structural_pass"])

    def test_highlights_boundary(self):
        self.assertTrue(inspect({"title": "A", "item_highlights": "B" * 125})["structural_pass"])
        self.assertFalse(inspect({"title": "A", "item_highlights": "B" * 126})["structural_pass"])

    def test_bytes_are_not_characters(self):
        result = inspect({"title": "A", "search_terms": "浴刷"}, search_terms_max_bytes=5)
        self.assertEqual(result["metrics"]["search_terms"], {"characters": 2, "utf8_bytes": 6})
        self.assertFalse(result["structural_pass"])

    def test_no_implicit_backend_limit(self):
        self.assertTrue(inspect({"title": "A", "search_terms": "刷" * 200})["structural_pass"])

    def test_risk_term_is_not_hard_failure(self):
        result = inspect({"title": "Bath Brush", "bullets": ["Clean with a dry cloth."]})
        self.assertTrue(result["structural_pass"])
        self.assertEqual(result["issues"][0]["level"], "review")

    def test_invalid_schema_does_not_crash(self):
        for data in ([], {"title": 3}, {"title": "Bath Brush", "bullets": [None]}):
            self.assertFalse(inspect(data)["structural_pass"])

    def test_custom_limits(self):
        self.assertTrue(inspect({"title": "A" * 80}, title_limit=100)["structural_pass"])


if __name__ == "__main__":
    unittest.main()
