# Paceful Shield 0.4 Beta — Windows

Paceful Shield is a Windows security companion designed to work alongside Microsoft Defender. The desktop shortcut is named **Pace**; the product is **Paceful Shield**.

## What's new in 0.4 Beta

- Updated Paceful Shield brand and shield artwork.
- Automatic monitoring of user-selected folders, with Downloads, Desktop, and Documents suggested by default when available.
- Limited automatic scans of watched locations on startup and on a six-hour schedule.
- Windows toast notifications for newly observed heuristic findings and newly observed Defender threat-history entries, when Windows notifications are available.
- Microsoft Defender status overview, Quick Scan and Full Scan request buttons, targeted custom-scan requests for a flagged file, and a view of threat records reported by Defender.
- A local Paceful Shield exclusions list for files and folders. These exclusions do **not** change Microsoft Defender's settings.
- Read-only CPU, memory, disk, top-memory process, common startup-location, and active network-connection views for diagnostics. They are inventories, not malware verdicts.
- User-approved file removal through the Windows Recycle Bin; files are never automatically deleted or quarantined.
- System-tray behavior: closing the window hides the app when the tray dependency is available. An optional per-user Windows startup entry is available in Settings.
- Local activity and finding history stored under `%LOCALAPPDATA%\PacefulShield` in separate 0.4 files.

## Important limitations

- This is an experimental security companion, not a full antivirus engine. Heuristic findings can be false positives and can miss malware. Microsoft Defender or another trusted antivirus must remain enabled.
- Automatic file monitoring and the local heuristic review are not equivalent to kernel-level or antivirus-grade real-time protection. The process and network panels are read-only inventories; they do not prove whether a process or connection is malicious.
- Defender scan requests are requests; Paceful Shield cannot always confirm that a scan completed.
- The app can display threat history returned by Microsoft Defender, but cannot inject its own heuristic findings into Windows Security as if Defender had confirmed them.
- Per-file operating-system execution blocking is **not implemented** in this beta. Applying arbitrary AppLocker or Software Restriction Policy rules without robust validation could disrupt legitimate Windows applications. Use Windows Security and Windows' own application controls for actual blocking.
- Closing the window hides it in the system tray when available, and optional startup can relaunch it at sign-in. A regular user or administrator can still terminate or disable a user-mode app; this release does not claim tamper-proof protection or anti-termination guarantees.
- File removal requires explicit user confirmation and uses the Recycle Bin when supported. It is not quarantine and may not work for every location or locked file.
- Toast notifications depend on Windows notification settings and the notification library working correctly. If unavailable, events are recorded in the local activity history.
- The installer is unsigned unless code-signing secrets are configured in the repository's Actions settings. SmartScreen warnings may appear.
- This package was source-checked in a non-Windows environment. The Windows installer and user-interface behavior must be built and tested on Windows before publishing it as a stable release.

## Privacy

The local file review does not upload files, file contents, hashes, or scan results to a remote service. Defender may handle detections according to the user's Windows security and cloud-protection settings. The app stores settings, activity, and findings locally.
