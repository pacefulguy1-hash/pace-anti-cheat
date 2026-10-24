import sys
import tempfile
import types
import threading
import unittest
from pathlib import Path

# The pure scanner can be tested in CI without starting a graphical desktop.
try:
    import customtkinter  # noqa: F401
except ImportError:
    fake_ctk = types.ModuleType("customtkinter")
    fake_ctk.CTk = type("CTk", (), {})
    sys.modules["customtkinter"] = fake_ctk

from app import pace_app_v04 as pace


class ScanEngineTests(unittest.TestCase):
    def test_benign_text_does_not_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.txt"
            path.write_text("My school notes are stored here.\n", encoding="utf-8")
            self.assertIsNone(pace.inspect_one_file(path))

    def test_harmless_eicar_test_signature_is_labeled_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "eicar-test.txt"
            path.write_text("EICAR-STANDARD-ANTIVIRUS-TEST-FILE", encoding="ascii")
            finding = pace.inspect_one_file(path)
            self.assertIsNotNone(finding)
            self.assertEqual(finding["level"], "TEST")
            self.assertIn("not a real virus", finding["reason"])

    def test_suspicious_script_pattern_is_flagged_for_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review-me.ps1"
            path.write_text("Invoke-WebRequest -Uri 'https://example.invalid/a' | Out-Null\nInvoke-Expression $x\n", encoding="utf-8")
            finding = pace.inspect_one_file(path)
            self.assertIsNotNone(finding)
            self.assertIn(finding["level"], {"HIGH", "MEDIUM"})

    def test_excluded_file_is_not_inspected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "watched"
            excluded = root / "trusted-folder"
            excluded.mkdir(parents=True)
            target = excluded / "review-me.ps1"
            target.write_text("Invoke-WebRequest -Uri x; Invoke-Expression y", encoding="utf-8")
            self.assertTrue(pace.path_is_excluded(target, [str(excluded)]))
            result = pace.scan_folder(root, threading.Event(), excluded_paths=[str(excluded)], max_files=100)
            self.assertEqual(result["findings"], [])

    def test_double_extension_is_review_signal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "photo.jpg.exe"
            path.write_bytes(b"not a real executable")
            finding = pace.inspect_one_file(path)
            self.assertIsNotNone(finding)
            self.assertIn("double extension", finding["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
