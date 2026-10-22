# PACE Anti-Cheat — Windows Security Companion (0.2 Beta)

PACE is a Windows desktop companion for viewing selected Microsoft Defender status values and requesting Defender scans. It is **not** a standalone antivirus product and is not intended to detect players cheating inside games.

## Website

The public static website is in the repository root and is published with GitHub Pages. It starts in English and supports Turkish, German, Spanish, and French, with dark/light/system appearance choices. The download button checks the official GitHub Release and remains disabled until the expected installer asset is publicly published.

Expected URL: https://pacefulguy1-hash.github.io/pace-anti-cheat/

## Windows application

- Source: `app/pace_app.py`
- Setup definition: `installer/PACE-Setup.iss`
- Local build helper: `build_windows.bat`
- CI build: **Actions → Build PACE Windows Installer → Run workflow**

The GitHub Actions workflow builds the EXE and installer on a Windows runner, uploads a 30-day test artifact, computes SHA-256, and creates/updates a **draft** beta release. Test the artifact on Windows before publishing the draft release.

## Security limitations

- PACE does not contain its own malware-detection engine or real-time protection.
- Scan requests are sent to Microsoft Defender; a request being sent is not proof that a scan completed.
- This beta is not digitally signed. SmartScreen warnings may occur.
- Keep Microsoft Defender or another trusted antivirus enabled.

See `START_HERE_TR.md` for setup instructions in Turkish and `RELEASE_NOTES.md` for the beta limitations.
