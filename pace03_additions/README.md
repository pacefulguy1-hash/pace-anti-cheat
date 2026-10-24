# Paceful Shield — Windows Security Companion (0.4 Beta)

**Paceful Shield** is a Windows desktop companion that works alongside Microsoft Defender. Its desktop shortcut is named **Pace**. It combines selected Defender status information, monitored-folder review, local exclusions, notifications, activity history, and user-approved Recycle Bin removal.

## Download

The 0.4 installer is published as a beta release after it has been built and tested:

- GitHub release: https://github.com/pacefulguy1-hash/pace-shield/releases/tag/v0.4.0-beta
- Windows x64 installer filename: `Paceful-Shield-Setup-0.4.0-beta.exe`

## Build from source on Windows

Requirements: Python 3.11 and Inno Setup 6.

```powershell
py -3.11 -m pip install --upgrade pip pyinstaller customtkinter darkdetect watchdog pystray pillow winotify Send2Trash psutil
python -m unittest discover -s tests -v
pyinstaller --noconfirm --clean --onefile --windowed --name PacefulShield04 --icon app/assets/paceful-shield.ico --add-data "app/assets/paceful-shield.png;assets" --collect-all customtkinter --collect-all darkdetect --collect-all watchdog --collect-all pystray --collect-all winotify --collect-all psutil --hidden-import pystray._win32 app/pace_app_v04.py
```

Compile `installer/Paceful-Shield-Setup-0.4.0-beta.iss` with Inno Setup 6. The GitHub Actions workflow can build the installer and create a draft beta release.

## Important security limitations

- This is an experimental companion, not a full antivirus product. Keep Microsoft Defender enabled.
- Heuristic findings can be false positives or miss malware. A finding is not proof of infection.
- The app watches selected folders and runs limited periodic scans; this is not antivirus-grade, kernel-level real-time protection.
- It can show threat history returned by Defender but cannot inject its own findings into Windows Security as Defender-confirmed detections.
- Individual file execution blocking at the operating-system level is not implemented in 0.4 Beta.
- The app can hide in the system tray and optionally start at user sign-in. It cannot guarantee survival against termination or disabling by an administrator or privileged attacker.
- Removal requires explicit user confirmation and uses the Recycle Bin where supported. There is no automatic deletion or quarantine.
- Paceful Shield exclusions only affect Paceful Shield's own review; they do not change Microsoft Defender exclusions.
- Files, hashes, and local scan results are not automatically uploaded. Microsoft Defender may handle detections according to Windows security/cloud-protection settings.
- The installer is unsigned unless a valid code-signing certificate is configured in GitHub Actions secrets. SmartScreen warnings may appear.
- Test the executable and installer on Windows before treating this beta as ready for public use.
