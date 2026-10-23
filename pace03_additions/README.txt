PACE 0.3 BETA — ADD-ON PACKAGE

This package is intended to be added alongside (not over) the current PACE 0.2 files.
Read SETUP_TR.md before copying files into the GitHub repository.

New files:
  app/pace_app_v03.py
  installer/PACE-Setup-0.3.0-beta.iss
  .github/workflows/build-windows-installer-v03.yml
  PACE-0.3.0-BETA-NOTES.md

This beta uses Microsoft Defender for antivirus scans and adds conservative local file-review heuristics. It is NOT a full antivirus engine. No automatic deletion or quarantine is performed. Do not treat a clean heuristic result as proof that a folder is safe.
