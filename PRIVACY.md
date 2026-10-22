# PACE Privacy Notes — Beta 0.2

## Website

The static website has no login system, backend, analytics code, or download tracking. It stores the selected language and theme in the visitor's browser local storage. GitHub Pages or any hosting provider may process ordinary server logs when the page is visited; review the hosting provider's privacy policy.

## Windows app

The application queries selected local status fields from Microsoft Defender, can ask Defender to run a scan, and can open Windows Security. It stores simple local activity timestamps and display settings under `%LOCALAPPDATA%\PACE`. The application source contains no telemetry upload or network scan service.

PACE 0.2 Beta is not a standalone antivirus product and cannot guarantee that a computer is free of malware. Scan and remediation results should be reviewed in Windows Security / Protection history.
