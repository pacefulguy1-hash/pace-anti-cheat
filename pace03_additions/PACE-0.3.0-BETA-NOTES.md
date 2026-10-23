# PACE 0.3 Beta — Windows

## What's new
- Modern CustomTkinter-based dark/light interface designed for modern Windows desktops.
- Microsoft Defender status overview and Quick/Full scan request buttons.
- Early local file-review engine: computes SHA-256 for flagged accessible files up to 200 MB, within a 1 GB total hash budget, and flags a small set of conservative heuristic patterns for review.
- Local analysis results and activity are stored locally under `%LOCALAPPDATA%\PACE` in separate v0.3 files.
- No files are automatically deleted or quarantined.

## Important limitations
- The local heuristic review is an experimental foundation, not a full antivirus engine. It can miss malware and produce false positives. A flagged file is not confirmed malware; a folder with no matches is not guaranteed clean.
- Microsoft Defender remains the real antivirus scanner. PACE asks Defender to run scans but cannot confirm that the scans have completed.
- PACE deliberately remains a normal user-controlled desktop app and does not block Task Manager or prevent users from closing it.
- The installer is unsigned unless a trusted code-signing certificate is configured in GitHub Actions secrets.
