# Paceful Shield 0.4 Beta — Windows

Paceful Shield is a Windows desktop companion for Microsoft Defender, watched-folder review, notifications, and local security history. It is **not** a standalone antivirus and does not guarantee that malware will be detected.

## Build on Windows

Use Python 3.11 and install these dependencies:

```powershell
py -3.11 -m pip install --upgrade pip customtkinter darkdetect watchdog pystray pillow winotify Send2Trash pyinstaller
```

From the repository root, build the Windows executable:

```powershell
py -3.11 -m PyInstaller --noconfirm --clean --onefile --windowed --name PacefulShield04 --icon app/assets/paceful-shield.ico --add-data "app/assets/paceful-shield.png;assets" --collect-all customtkinter --collect-all darkdetect --collect-all watchdog --collect-all pystray --collect-all winotify --hidden-import pystray._win32 app/pace_app_v04.py
```

Then compile `installer/Paceful-Shield-Setup-0.4.0-beta.iss` with Inno Setup 6.

## Features in this beta

- Reads selected Microsoft Defender status fields.
- Requests Defender Quick Scan or Full Scan and displays available threat-history records.
- Watches configured folders and runs limited automatic scans on a six-hour schedule.
- Shows Windows toast notifications for new local heuristic findings or new Defender threat-history entries where notifications are available.
- Lets the user add file/folder exclusions that apply only to Paceful Shield's own scanner.
- Lets the user explicitly move a finding to the Windows Recycle Bin after confirmation.
- Closes to the system tray when available and can start at the current user's Windows sign-in.

## Do not overstate the protection

- Heuristic matches are warnings, not proof of infection.
- The app does not include a kernel driver or antivirus-grade real-time engine.
- Per-file OS-level execution blocking is not implemented in this beta.
- A user-mode application cannot guarantee it will survive termination by an administrator or a privileged attacker.
- Keep Microsoft Defender enabled. Test the executable and installer on Windows before publishing a public release.
