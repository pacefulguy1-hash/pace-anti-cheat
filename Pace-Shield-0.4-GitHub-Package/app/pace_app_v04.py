from __future__ import annotations

import base64
import ctypes
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

import customtkinter as ctk

try:
    from send2trash import send2trash
except Exception:
    send2trash = None

try:
    from winotify import Notification
except Exception:
    Notification = None

try:
    import watchdog.events
    from watchdog.observers import Observer
except Exception:
    watchdog = None
    Observer = None

try:
    import pystray
    from PIL import Image, ImageDraw
except Exception:
    pystray = None
    Image = None
    ImageDraw = None

try:
    import psutil
except Exception:
    psutil = None

APP_NAME = "Pace"
PRODUCT_NAME = "Paceful Shield"
APP_VERSION = "0.4 Beta"
IS_WINDOWS = sys.platform == "win32"
MAX_FILES = 12000
MAX_AUTO_FILES = 4500
MAX_SCRIPT_BYTES = 1024 * 1024
MAX_HASH_BYTES = 200 * 1024 * 1024
AUTO_SCAN_INTERVAL_MS = 6 * 60 * 60 * 1000

APP_DIR = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "PacefulShield"
APP_DIR.mkdir(parents=True, exist_ok=True)
PREFS_PATH = APP_DIR / "settings-v04.json"
LOG_PATH = APP_DIR / "activity-v04.json"
FINDINGS_PATH = APP_DIR / "findings-v04.json"

COLORS = {
    "bg": "#080D17", "sidebar": "#0D1525", "panel": "#111C2E", "panel2": "#17263B",
    "line": "#2A3A53", "text": "#F4F7FC", "muted": "#A0AEC2", "accent": "#52D6C0",
    "accent_hover": "#35B9A6", "blue": "#53A5FF", "warning": "#F6C766", "danger": "#FF7E8A",
    "white": "#FFFFFF", "input": "#101A2D"
}
LIGHT = {
    "bg": "#F3F6FC", "sidebar": "#E9EEF7", "panel": "#FFFFFF", "panel2": "#EDF2FA",
    "line": "#D7E0EF", "text": "#152238", "muted": "#63748D", "accent": "#087B79",
    "accent_hover": "#066A66", "blue": "#245BD5", "warning": "#8A5A00", "danger": "#B42335",
    "white": "#FFFFFF", "input": "#F7F9FD"
}

TEXT = {
    "tr": {
        "overview": "Genel Bakış", "scan": "Tarama Merkezi", "system": "Sistem / Performans", "network": "Ağ Bağlantıları", "activity": "Etkinlik", "settings": "Ayarlar",
        "system_desc": "İşlemci, bellek, disk kullanımı ve başlangıç uygulamalarını incele.", "network_desc": "Aktif ağ bağlantılarının yerel görünümü. Bilgiler internete gönderilmez.",
        "cpu": "İşlemci kullanımı", "ram": "Bellek kullanımı", "disk": "Disk kullanımı", "top_processes": "Belleği en çok kullanan işlemler", "process": "İşlem", "pid": "PID", "memory": "Bellek",
        "startup_apps": "Başlangıç uygulamaları", "startup_settings": "Windows başlangıç ayarlarını aç", "startup_note": "Bu liste yaygın başlangıç konumlarını gösterir; tüm otomatik başlatma yöntemlerini kapsamaz.",
        "network_connections": "Bağlantılar", "local_address": "Yerel adres", "remote_address": "Uzak adres", "state": "Durum", "owner_process": "İşlem", "network_permission": "Bazı bağlantılar yönetici izni olmadan görünmeyebilir.", "no_data": "Bilgi alınamadı.", "refresh_system": "Yenile", "system_readonly": "Salt okunur işlem görünümü. İşlem adı ve kaynak kullanımı zararlı faaliyet kanıtı değildir.", "connections_returned": "{count} bağlantı listelendi. Bu yerel görünüm bir zararlı yazılım kararı değildir.",
        "welcome": "Bilgisayarın. Daha görünür. Daha anlaşılır.",
        "subtitle": "Otomatik dosya izlemesi, Microsoft Defender bilgileri ve güvenlik bildirimleri.",
        "defender": "MICROSOFT DEFENDER", "refresh": "Durumu yenile", "enabled": "Etkin", "disabled": "Devre dışı",
        "unknown": "Bilinmiyor / kullanılamıyor", "antivirus": "Antivirüs", "realtime": "Gerçek zamanlı koruma",
        "service": "Defender hizmeti", "updated": "İmza güncellemesi", "quick": "Hızlı tarama", "full": "Tam tarama",
        "open_security": "Windows Güvenliği'ni aç", "scan_title": "Dosya ve klasör inceleme", "choose_folder": "Klasör seç",
        "scan_selected": "Seçili klasörü tara", "scan_watched": "İzlenen konumları tara", "scan_intro": "İstersen tek bir klasörü incele veya Paceful Shield'ın izlediği konumları birlikte tara.",
        "last_scan": "SONUÇ", "no_scan": "Henüz tarama yapılmadı.", "results": "İnceleme sonuçları", "files_checked": "Kontrol edilen dosya",
        "flagged": "İncelenmeli", "clean": "Kural eşleşmedi", "rule": "Neden", "file": "Dosya", "risk": "İnceleme düzeyi",
        "high": "Yüksek öncelik", "medium": "İncele", "test": "Test imzası", "no_findings": "Kural eşleşmesi yok. Bu sonuç, dosyaların kesinlikle temiz olduğunu kanıtlamaz.",
        "activity_empty": "Henüz etkinlik yok.", "clear_log": "Etkinliği temizle", "language": "Dil", "appearance": "Görünüm",
        "dark": "Koyu", "light": "Açık", "about": "Paceful Shield hakkında", "monitoring": "Otomatik izleme",
        "monitoring_desc": "İzlenen klasörlerde yeni veya değiştirilen dosyaları incele ve belirli aralıklarla tarama yap.",
        "watch_paths": "İzlenen konumlar", "add_folder": "Klasör ekle", "remove": "Kaldır", "exclusions": "Paceful Shield istisnaları",
        "exclusions_desc": "İstisnalar yalnızca Paceful Shield'ın kendi incelemesini atlar; Microsoft Defender ayarlarını değiştirmez.",
        "add_file": "Dosya ekle", "add_exclusion_folder": "Klasör istisnası ekle", "autostart": "Windows açıldığında başlat",
        "autostart_desc": "Kullanıcı hesabının başlangıç kayıtlarına eklenir; yönetici izni gerekmez.", "tray_note": "Pencereyi kapatmak uygulamayı sistem tepsisine küçültür. Görev Yöneticisi veya yönetici yetkili bir saldırgana karşı kapatılamazlık garanti edilemez.",
        "recycle": "Geri Dönüşüm Kutusu'na taşı", "exclude_this": "Bu dosyayı istisnaya ekle", "open_security_scan": "Defender ile tara",
        "scan_started": "Microsoft Defender tarama isteği gönderildi. Bu, taramanın tamamlandığını doğrulamaz.", "no_upload": "Dosyalar ve yerel inceleme sonuçları bu bilgisayarda tutulur. Dosyalar kendiliğinden internete yüklenmez.",
        "done": "İşlem tamamlandı.", "checking": "Kontrol ediliyor…", "ready": "Hazır", "error": "İşlem tamamlanamadı.",
        "not_proof": "Şüpheli bir bulgu, doğrulanmış kötü amaçlı yazılım demek değildir.", "test_notice": "Bu geliştirme sürümündeki inceleme kuralları deneysel olabilir; Microsoft Defender'ı kapatmayın.",
        "monitor_on": "Otomatik izleme açık", "monitor_off": "Otomatik izleme kapalı", "cancel": "Durdur", "stop_requested": "Durdurma istendi…",
        "auto_scan": "Otomatik tarama", "defender_findings": "Defender'ın bildirdiği tehditler", "no_defender_findings": "Defender'ın kayıtlı tehdit sonucu alınamadı veya kayıt bulunamadı.",
        "send_trash_confirm": "Bu dosyayı Geri Dönüşüm Kutusu'na taşımak istiyor musun? Bu uygulamanın bulgusu tek başına dosyanın zararlı olduğunu kanıtlamaz.",
        "trash_done": "Dosya Geri Dönüşüm Kutusu'na taşındı.", "trash_failed": "Dosya Geri Dönüşüm Kutusu'na taşınamadı.",
        "rule_block_unavailable": "Paceful Shield 0.4, tek tek dosyaların işletim sistemi düzeyinde çalıştırılmasını güvenilir biçimde engellemiyor. Yanlış bir kural Windows uygulamalarını bozabileceği için bu özellik doğrulanmış sürüme bırakıldı. Dosyayı Microsoft Defender ile kontrol edebilir veya Windows Güvenliği'ni açabilirsin.",
        "monitor_unavailable": "Otomatik dosya izleme bağımlılığı yüklenmemiş. El ile tarama yine kullanılabilir.",
        "watch_add_prompt": "İzlenecek klasörü seç", "exclusion_add_prompt": "İstisna yapılacak klasörü seç", "select_file": "İstisna yapılacak dosyayı seç",
        "status_ok": "Koruma açık görünüyor", "status_warning": "Koruma durumunu kontrol et", "manual_scan_done": "İnceleme tamamlandı.",
    },
    "en": {
        "overview": "Overview", "scan": "Scan Center", "system": "System / Performance", "network": "Network Connections", "activity": "Activity", "settings": "Settings",
        "system_desc": "Review CPU, memory, disk usage, and startup applications.", "network_desc": "A local view of active network connections. This information is not uploaded.",
        "cpu": "CPU usage", "ram": "Memory usage", "disk": "Disk usage", "top_processes": "Processes using the most memory", "process": "Process", "pid": "PID", "memory": "Memory",
        "startup_apps": "Startup applications", "startup_settings": "Open Windows startup settings", "startup_note": "This list covers common startup locations, not every possible auto-start technique.",
        "network_connections": "Connections", "local_address": "Local address", "remote_address": "Remote address", "state": "State", "owner_process": "Process", "network_permission": "Some connections may not be visible without administrator permission.", "no_data": "Information is unavailable.", "refresh_system": "Refresh", "system_readonly": "Read-only process view. Names and resource usage are not proof of malicious activity.", "connections_returned": "{count} connection(s) returned. This is a local inventory, not a malware verdict.",
        "welcome": "Your PC. More visible. More understandable.",
        "subtitle": "Automatic file monitoring, Microsoft Defender status, and security notifications.",
        "defender": "MICROSOFT DEFENDER", "refresh": "Refresh status", "enabled": "Enabled", "disabled": "Disabled",
        "unknown": "Unknown / unavailable", "antivirus": "Antivirus", "realtime": "Real-time protection", "service": "Defender service",
        "updated": "Signatures updated", "quick": "Quick scan", "full": "Full scan", "open_security": "Open Windows Security",
        "scan_title": "File and folder review", "choose_folder": "Choose folder", "scan_selected": "Scan selected folder",
        "scan_watched": "Scan watched locations", "scan_intro": "Review a folder or scan the locations Paceful Shield watches.",
        "last_scan": "LATEST RESULT", "no_scan": "No scan has run yet.", "results": "Review results", "files_checked": "Files checked",
        "flagged": "Needs review", "clean": "No rule matched", "rule": "Reason", "file": "File", "risk": "Review level",
        "high": "High priority", "medium": "Review", "test": "Test signature", "no_findings": "No rule matched. This does not prove files are clean.",
        "activity_empty": "No activity yet.", "clear_log": "Clear activity", "language": "Language", "appearance": "Appearance", "dark": "Dark", "light": "Light",
        "about": "About Paceful Shield", "monitoring": "Automatic monitoring", "monitoring_desc": "Review new or changed files in watched folders and run periodic scans.",
        "watch_paths": "Watched locations", "add_folder": "Add folder", "remove": "Remove", "exclusions": "Paceful Shield exclusions",
        "exclusions_desc": "These exclusions only skip Paceful Shield's own review; they do not change Microsoft Defender settings.",
        "add_file": "Add file", "add_exclusion_folder": "Exclude folder", "autostart": "Start when Windows starts",
        "autostart_desc": "Uses this Windows account's startup registry; no administrator permission is required.",
        "tray_note": "Closing the window hides the app in the system tray. It cannot be guaranteed to survive Task Manager termination or a privileged attacker.",
        "recycle": "Move to Recycle Bin", "exclude_this": "Exclude this file", "open_security_scan": "Scan with Defender",
        "scan_started": "A Microsoft Defender scan was requested. This does not confirm completion.", "no_upload": "Files and local review results stay on this PC. Files are not uploaded automatically.",
        "done": "Operation complete.", "checking": "Checking…", "ready": "Ready", "error": "The operation could not be completed.",
        "not_proof": "A suspicious finding is not confirmed malware.", "test_notice": "Heuristic rules in this beta are experimental; do not disable Microsoft Defender.",
        "monitor_on": "Automatic monitoring enabled", "monitor_off": "Automatic monitoring disabled", "cancel": "Stop", "stop_requested": "Stop requested…",
        "auto_scan": "Automatic scan", "defender_findings": "Threats reported by Defender", "no_defender_findings": "No recorded Defender threat result was available or returned.",
        "send_trash_confirm": "Move this file to the Recycle Bin? This app's finding alone does not prove that the file is malicious.",
        "trash_done": "File moved to the Recycle Bin.", "trash_failed": "Could not move the file to the Recycle Bin.",
        "rule_block_unavailable": "Paceful Shield 0.4 does not reliably block individual files at the operating-system level. An incorrect rule could disrupt Windows apps, so this is deferred until it can be validated. You can check the file with Microsoft Defender or open Windows Security.",
        "monitor_unavailable": "The automatic file-monitoring dependency is unavailable. Manual scans remain available.",
        "watch_add_prompt": "Choose a folder to monitor", "exclusion_add_prompt": "Choose a folder to exclude", "select_file": "Choose a file to exclude",
        "status_ok": "Protection appears enabled", "status_warning": "Check protection status", "manual_scan_done": "Review complete.",
    }
}

EXECUTABLE_EXTS = {".exe", ".dll", ".scr", ".com", ".msi", ".sys"}
SCRIPT_EXTS = {".ps1", ".bat", ".cmd", ".vbs", ".vbe", ".js", ".jse", ".hta", ".wsf", ".reg"}
DOUBLE_EXT_RE = re.compile(r"\.(pdf|docx?|xlsx?|pptx?|jpe?g|png|gif|txt|rtf)\.(exe|scr|com|bat|cmd|js|vbs|hta)$", re.I)
RULES = [
    ("HIGH", "Encoded PowerShell plus download/execute pattern", re.compile(r"(?is)(-encodedcommand|-enc\s+[A-Za-z0-9+/=]{20,}).{0,120}(downloadstring|invoke-expression|\biex\b)|(?:downloadstring|invoke-expression|\biex\b).{0,120}(-encodedcommand|-enc\s+)")),
    ("HIGH", "Script combines remote download and execution patterns", re.compile(r"(?is)(downloadstring|invoke-webrequest|start-bitstransfer).{0,300}(invoke-expression|\biex\b|start-process)|(invoke-expression|\biex\b).{0,300}(downloadstring|invoke-webrequest|start-bitstransfer)")),
    ("MEDIUM", "Script contains Base64 decoding and execution keywords", re.compile(r"(?is)(frombase64string|certutil\s+-decode).{0,250}(invoke-expression|\biex\b|start-process|wscript\.shell)")),
]


def resource_path(name: str) -> Path:
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    candidates = [root / "assets" / name, Path(__file__).resolve().parent / "assets" / name]
    for item in candidates:
        if item.exists():
            return item
    return candidates[0]


def default_watch_paths() -> list[str]:
    home = Path.home()
    options = [home / "Downloads", home / "Desktop", home / "Documents"]
    return [str(path) for path in options if path.exists()]


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path: Path, data) -> None:
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def normalized_path(path: str | Path) -> str:
    try:
        return os.path.normcase(os.path.abspath(os.path.expandvars(os.path.expanduser(str(path)))))
    except Exception:
        return os.path.normcase(str(path))


def path_is_excluded(path: str | Path, exclusions: list[str]) -> bool:
    target = normalized_path(path)
    for entry in exclusions:
        excluded = normalized_path(entry)
        if target == excluded or target.startswith(excluded.rstrip("\\/") + os.sep):
            return True
    return False


def powershell_json(script: str, timeout: int = 25):
    if not IS_WINDOWS:
        raise RuntimeError("This feature requires Windows PowerShell.")
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True, text=True, timeout=timeout,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "PowerShell request failed").strip())
    raw = result.stdout.strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Windows returned an unreadable security result.") from exc


def defender_status() -> dict:
    return powershell_json(
        "$ErrorActionPreference='Stop'; $s=Get-MpComputerStatus; "
        "[pscustomobject]@{AntivirusEnabled=$s.AntivirusEnabled; "
        "RealTimeProtectionEnabled=$s.RealTimeProtectionEnabled; AMServiceEnabled=$s.AMServiceEnabled; "
        "AMRunningMode=$s.AMRunningMode; SignatureUpdated=if($s.AntivirusSignatureLastUpdated){$s.AntivirusSignatureLastUpdated.ToString('yyyy-MM-dd HH:mm')}else{''}} | ConvertTo-Json -Compress"
    )


def defender_detections() -> list[dict]:
    result = powershell_json(
        "$ErrorActionPreference='Stop'; $items=@(Get-MpThreatDetection -ErrorAction SilentlyContinue | "
        "Select-Object -First 30 InitialDetectionTime,ThreatName,Resources,ActionSuccess,ThreatID,ProcessName); "
        "$items | ConvertTo-Json -Depth 5 -Compress", timeout=35
    )
    if isinstance(result, dict):
        return [result]
    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]
    return []


def request_defender_scan(scan_type: str) -> None:
    if not IS_WINDOWS or scan_type not in {"QuickScan", "FullScan"}:
        raise RuntimeError("This scan requires Windows and Microsoft Defender.")
    params = f'-NoProfile -ExecutionPolicy Bypass -Command "Start-MpScan -ScanType {scan_type}"'
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", params, None, 1)
    if result <= 32:
        raise OSError(f"Windows could not start the Defender scan (code {result}).")


def request_defender_path_scan(path: str) -> None:
    if not IS_WINDOWS or not Path(path).exists():
        raise RuntimeError("The file is unavailable or this feature requires Windows.")
    # PowerShell's -EncodedCommand uses UTF-16LE and avoids unsafe string interpolation.
    escaped_path = str(Path(path).resolve()).replace("'", "''")
    script = f"$ErrorActionPreference='Stop'; Start-MpScan -ScanType CustomScan -ScanPath '{escaped_path}'"
    encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
    params = f"-NoProfile -NonInteractive -ExecutionPolicy Bypass -EncodedCommand {encoded}"
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", params, None, 1)
    if result <= 32:
        raise OSError(f"Windows could not start the targeted Defender scan (code {result}).")


def open_windows_security() -> None:
    if not IS_WINDOWS:
        raise RuntimeError("Windows only")
    os.startfile("windowsdefender:")


def inspect_one_file(path: Path, calculate_hash: bool = True, exclusions: list[str] | None = None) -> dict | None:
    if exclusions and path_is_excluded(path, exclusions):
        return None
    findings: list[tuple[str, str]] = []
    try:
        stat = path.stat()
        if not path.is_file():
            return None
        suffix = path.suffix.lower()
        lowered = normalized_path(path).replace("/", "\\")
        name_lower = path.name.lower()
        if DOUBLE_EXT_RE.search(name_lower):
            findings.append(("MEDIUM", "Document/image-like double extension ending in executable or script"))
        temp_roots = [os.environ.get("TEMP", ""), os.path.join(os.environ.get("LOCALAPPDATA", ""), "temp")]
        if suffix in EXECUTABLE_EXTS and any(root and lowered.startswith(normalized_path(root).replace("/", "\\").rstrip("\\") + "\\") for root in temp_roots):
            findings.append(("MEDIUM", "Executable file stored in a temporary folder"))
        if stat.st_size <= MAX_SCRIPT_BYTES:
            try:
                raw = path.read_bytes()
            except OSError:
                raw = b""
            if b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" in raw:
                findings.append(("TEST", "EICAR harmless antivirus test signature (not a real virus)"))
            if suffix in SCRIPT_EXTS:
                content = raw.decode("utf-8", errors="ignore")
                for level, reason, pattern in RULES:
                    if pattern.search(content):
                        findings.append((level, reason))
        if not findings:
            return None
        digest = "not calculated (size limit)"
        if calculate_hash and stat.st_size <= MAX_HASH_BYTES:
            h = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(chunk)
            digest = h.hexdigest()
        unique = list(dict.fromkeys(findings))
        rank = {"HIGH": 0, "MEDIUM": 1, "TEST": 2, "INFO": 3}
        unique.sort(key=lambda item: rank.get(item[0], 9))
        return {
            "path": str(path), "name": path.name, "level": unique[0][0],
            "reason": "; ".join(reason for _, reason in unique), "sha256": digest,
            "size": stat.st_size, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except (OSError, PermissionError):
        return None


def scan_folder(root: Path, cancel: threading.Event, progress_callback=None,
                excluded_paths: list[str] | None = None, max_files: int = MAX_FILES) -> dict:
    findings: list[dict] = []
    checked = 0
    errors = 0
    stopped = False
    excluded_paths = excluded_paths or []
    root = Path(root)
    if not root.is_dir() or path_is_excluded(root, excluded_paths):
        return {"root": str(root), "checked": 0, "findings": [], "errors": 0, "stopped": False, "limit": max_files}
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d.lower() not in {".git", "node_modules", "__pycache__", ".venv", "venv"}
                   and not path_is_excluded(Path(current) / d, excluded_paths)]
        if cancel.is_set():
            stopped = True
            break
        for filename in files:
            if cancel.is_set():
                stopped = True
                break
            path = Path(current) / filename
            if path_is_excluded(path, excluded_paths):
                continue
            try:
                checked += 1
                found = inspect_one_file(path, exclusions=excluded_paths)
                if found:
                    findings.append(found)
            except Exception:
                errors += 1
            if progress_callback and checked % 40 == 0:
                try:
                    progress_callback(checked, len(findings), str(path))
                except Exception:
                    pass
            if checked >= max_files:
                stopped = True
                break
        if stopped:
            break
    return {"root": str(root), "checked": checked, "findings": findings, "errors": errors, "stopped": stopped, "limit": max_files}


class PaceApp(ctk.CTk):
    def __init__(self):
        ctk.set_default_color_theme("blue")
        super().__init__()
        prefs = read_json(PREFS_PATH, {})
        if not isinstance(prefs, dict):
            prefs = {}
        prefs.setdefault("theme", "dark")
        prefs.setdefault("language", "tr")
        prefs.setdefault("monitoring_enabled", True)
        prefs.setdefault("watch_paths", default_watch_paths())
        prefs.setdefault("exclusions", [])
        prefs.setdefault("autostart", False)
        prefs.setdefault("seen_defender_keys", [])
        if not isinstance(prefs.get("watch_paths"), list): prefs["watch_paths"] = default_watch_paths()
        if not isinstance(prefs.get("exclusions"), list): prefs["exclusions"] = []
        if not isinstance(prefs.get("seen_defender_keys"), list): prefs["seen_defender_keys"] = []
        self.prefs = prefs
        self.language = self.prefs.get("language", "tr") if self.prefs.get("language") in TEXT else "tr"
        self.theme = self.prefs.get("theme", "dark") if self.prefs.get("theme") in {"dark", "light"} else "dark"
        self.logs = read_json(LOG_PATH, [])
        self.findings = read_json(FINDINGS_PATH, [])
        if not isinstance(self.logs, list): self.logs = []
        else: self.logs = [item for item in self.logs if isinstance(item, dict)]
        if not isinstance(self.findings, list): self.findings = []
        else: self.findings = [item for item in self.findings if isinstance(item, dict)]
        self.status_data = None
        self.defender_detections = []
        self.current_page = "overview"
        self.system_refresh_inflight = False
        self.network_refresh_inflight = False
        self.active_folder = ""
        self.last_result = None
        self.scan_thread = None
        self.scan_busy = False
        self.cancel_event = threading.Event()
        self.auto_scan_after_id = None
        self.colors = LIGHT if self.theme == "light" else COLORS
        self.observer = None
        self.tray_icon = None
        self.recent_event_timers: dict[str, threading.Timer] = {}
        self.alerted_keys: set[str] = set()
        self.known_defender_keys = set(self.prefs.get("seen_defender_keys", []))
        self.defender_baseline_loaded = bool(self.prefs.get("defender_baseline_loaded", False))
        ctk.set_appearance_mode(self.theme)
        self.title(f"{PRODUCT_NAME} · {APP_VERSION}")
        self.geometry("1230x860")
        self.minsize(1000, 700)
        self.configure(fg_color=self.colors["bg"])
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self.main = ctk.CTkFrame(self, fg_color=self.colors["bg"], corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self._build_header()
        self.content = ctk.CTkFrame(self.main, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=26, pady=(6, 22))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self._render_page("overview")
        self.protocol("WM_DELETE_WINDOW", self._hide_to_tray)
        self._setup_tray()
        self.after(600, self.refresh_status)
        self.after(1700, self.refresh_defender_detections)
        if self.prefs.get("monitoring_enabled", True):
            self.after(3500, self._start_monitoring)
            self._schedule_auto_scan(9000)
        self.after(300000, self._defender_poll_loop)
        self._save_prefs()

    def t(self, key: str) -> str:
        return TEXT[self.language].get(key, TEXT["en"].get(key, key))

    def _save_prefs(self):
        self.prefs["theme"] = self.theme
        self.prefs["language"] = self.language
        write_json(PREFS_PATH, self.prefs)

    def _label(self, parent, text, size=12, color=None, bold=False, wraplength=None):
        return ctk.CTkLabel(parent, text=text, text_color=color or self.colors["text"],
                            font=ctk.CTkFont(family="Segoe UI", size=size, weight="bold" if bold else "normal"),
                            wraplength=wraplength, justify="left")

    def _card(self, parent):
        return ctk.CTkFrame(parent, fg_color=self.colors["panel"], corner_radius=14,
                            border_width=1, border_color=self.colors["line"])

    def _button(self, parent, text, command, primary=False, state="normal", width=None):
        return ctk.CTkButton(parent, text=text, command=command, state=state, width=width,
            height=36, corner_radius=9, fg_color=self.colors["accent"] if primary else self.colors["panel2"],
            hover_color=self.colors["accent_hover"] if primary else self.colors["line"],
            text_color="#06151A" if primary else self.colors["text"], font=ctk.CTkFont(size=12, weight="bold"))

    def _build_sidebar(self):
        c = self.colors
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color=c["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=18, pady=(22, 26))
        try:
            logo = Image.open(resource_path("paceful-shield.png")).convert("RGBA") if Image else None
            if logo:
                logo.thumbnail((48, 48))
                self.logo_image = ctk.CTkImage(light_image=logo, dark_image=logo, size=(44, 44))
                ctk.CTkLabel(brand, text="", image=self.logo_image).pack(side="left", padx=(0, 10))
        except Exception:
            ctk.CTkLabel(brand, text="◈", text_color=c["accent"], font=ctk.CTkFont(size=34, weight="bold")).pack(side="left", padx=(0, 10))
        namebox = ctk.CTkFrame(brand, fg_color="transparent")
        namebox.pack(side="left", anchor="center")
        ctk.CTkLabel(namebox, text="Paceful", text_color=c["text"], font=ctk.CTkFont(size=23, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(namebox, text="SHIELD  ·  BETA 0.4", text_color=c["muted"], font=ctk.CTkFont(size=9, weight="bold")).pack(anchor="w")
        self.nav = {}
        for key in ("overview", "scan", "system", "network", "activity", "settings"):
            b = ctk.CTkButton(self.sidebar, text=self.t(key), anchor="w", height=44, corner_radius=10,
                fg_color="transparent", hover_color=c["panel2"], text_color=c["text"],
                font=ctk.CTkFont(size=13, weight="bold"), command=lambda page=key: self._render_page(page))
            b.pack(fill="x", padx=12, pady=4)
            self.nav[key] = b
        foot = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        foot.pack(side="bottom", fill="x", padx=18, pady=18)
        self.side_status = ctk.CTkLabel(foot, text="●  " + self.t("ready"), text_color=c["accent"], anchor="w", font=ctk.CTkFont(size=11, weight="bold"))
        self.side_status.pack(anchor="w", pady=(0, 6))
        self.monitor_status = ctk.CTkLabel(foot, text=self.t("monitor_on") if self.prefs.get("monitoring_enabled", True) else self.t("monitor_off"), text_color=c["muted"], anchor="w", wraplength=185, font=ctk.CTkFont(size=10))
        self.monitor_status.pack(anchor="w")

    def _build_header(self):
        c = self.colors
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=26, pady=(20, 8))
        header.grid_columnconfigure(0, weight=1)
        self.header_title = ctk.CTkLabel(header, text="", text_color=c["text"], font=ctk.CTkFont(size=25, weight="bold"))
        self.header_title.grid(row=0, column=0, sticky="w")
        self.header_sub = ctk.CTkLabel(header, text="", text_color=c["muted"], font=ctk.CTkFont(size=12), wraplength=820, justify="left")
        self.header_sub.grid(row=1, column=0, sticky="w", pady=(4, 0))
        self._button(header, self.t("open_security"), self._open_security).grid(row=0, column=1, rowspan=2, sticky="e", padx=(14, 0))

    def _render_page(self, page: str):
        self.current_page = page
        for key, button in self.nav.items():
            button.configure(fg_color=self.colors["panel2"] if key == page else "transparent")
        for child in self.content.winfo_children():
            child.destroy()
        titles = {k: self.t(k) for k in ("overview", "scan", "system", "network", "activity", "settings")}
        subtitles = {"overview": self.t("welcome"), "scan": self.t("scan_intro"), "system": self.t("system_desc"), "network": self.t("network_desc"), "activity": self.t("no_upload"), "settings": self.t("tray_note")}
        self.header_title.configure(text=titles[page])
        self.header_sub.configure(text=subtitles[page])
        if page == "overview": self._page_overview()
        elif page == "scan": self._page_scan()
        elif page == "system": self._page_system()
        elif page == "network": self._page_network()
        elif page == "activity": self._page_activity()
        else: self._page_settings()

    def _page_overview(self):
        c = self.colors
        self.content.grid_rowconfigure(0, weight=0)
        self.content.grid_rowconfigure(1, weight=1)
        self._label(self.content, self.t("subtitle"), 13, c["muted"], wraplength=900).grid(row=0, column=0, sticky="w", pady=(0, 12))
        container = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_columnconfigure((0, 1), weight=1)
        status_card = self._card(container); status_card.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12)); status_card.grid_columnconfigure(0, weight=1)
        head = ctk.CTkFrame(status_card, fg_color="transparent"); head.pack(fill="x", padx=18, pady=(15, 8))
        self._label(head, self.t("defender"), 11, c["muted"], True).pack(side="left")
        self._button(head, "↻  " + self.t("refresh"), self.refresh_status).pack(side="right")
        self.defender_summary = self._label(status_card, self.t("unknown"), 19, c["warning"], True)
        self.defender_summary.pack(anchor="w", padx=18, pady=(0, 4))
        self.defender_details = self._label(status_card, self.t("unknown"), 11, c["muted"], wraplength=900)
        self.defender_details.pack(anchor="w", padx=18, pady=(0, 12))
        tiles = ctk.CTkFrame(status_card, fg_color="transparent"); tiles.pack(fill="x", padx=14, pady=(0, 14))
        for col, (title, key) in enumerate(((self.t("antivirus"), "AntivirusEnabled"), (self.t("realtime"), "RealTimeProtectionEnabled"), (self.t("service"), "AMServiceEnabled"), (self.t("updated"), "SignatureUpdated"))):
            tile = ctk.CTkFrame(tiles, fg_color=c["panel2"], corner_radius=10); tile.grid(row=0, column=col, sticky="ew", padx=4); tiles.grid_columnconfigure(col, weight=1)
            self._label(tile, title, 10, c["muted"], True, wraplength=150).pack(anchor="w", padx=10, pady=(10, 3))
            value = self.status_data.get(key) if isinstance(self.status_data, dict) else None
            display = self._status_value(value)
            color = c["accent"] if value is True or (key == "SignatureUpdated" and value) else c["danger"] if value is False else c["muted"]
            lab = self._label(tile, display, 11, color, True, wraplength=160); lab.pack(anchor="w", padx=10, pady=(0, 10))
            if key == "AntivirusEnabled": self.tile_av = lab
            elif key == "RealTimeProtectionEnabled": self.tile_rt = lab
            elif key == "AMServiceEnabled": self.tile_service = lab
            else: self.tile_signatures = lab
        action1 = self._card(container); action1.grid(row=1, column=0, sticky="nsew", padx=(0, 6), pady=(0, 12))
        self._label(action1, "◉  " + self.t("scan_watched"), 15, c["text"], True).pack(anchor="w", padx=16, pady=(16, 6))
        self._label(action1, "Downloads, Desktop and Documents (plus any folders you add).", 11, c["muted"], wraplength=450).pack(anchor="w", padx=16, pady=(0, 12))
        self._button(action1, self.t("scan_watched"), self._scan_watched_roots, primary=True).pack(anchor="w", padx=16, pady=(0, 16))
        action2 = self._card(container); action2.grid(row=1, column=1, sticky="nsew", padx=(6, 0), pady=(0, 12))
        self._label(action2, "◈  " + self.t("run_defender") if hasattr(self, "run_defender") else "◈  Microsoft Defender", 15, c["text"], True).pack(anchor="w", padx=16, pady=(16, 6))
        self._label(action2, self.t("scan_started"), 11, c["muted"], wraplength=450).pack(anchor="w", padx=16, pady=(0, 12))
        row = ctk.CTkFrame(action2, fg_color="transparent"); row.pack(anchor="w", padx=16, pady=(0, 16))
        self._button(row, self.t("quick"), lambda: self._request_scan("QuickScan"), primary=True).pack(side="left", padx=(0, 8))
        self._button(row, self.t("full"), lambda: self._request_scan("FullScan")).pack(side="left")
        detections = self._card(container); detections.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        dhead = ctk.CTkFrame(detections, fg_color="transparent"); dhead.pack(fill="x", padx=16, pady=(13, 7))
        self._label(dhead, self.t("defender_findings"), 14, c["text"], True).pack(side="left")
        self._button(dhead, self.t("refresh"), self.refresh_defender_detections).pack(side="right")
        self.defender_threat_list = ctk.CTkFrame(detections, fg_color="transparent"); self.defender_threat_list.pack(fill="x", padx=12, pady=(0, 12))
        self._populate_defender_threats()
        notice = ctk.CTkFrame(container, fg_color=c["panel2"], corner_radius=12); notice.grid(row=3, column=0, columnspan=2, sticky="ew")
        self._label(notice, "ⓘ  " + self.t("test_notice"), 11, c["warning"], True, wraplength=900).pack(anchor="w", padx=15, pady=12)
        self._apply_status()

    def _status_value(self, value):
        if value is True: return self.t("enabled")
        if value is False: return self.t("disabled")
        if value is None or value == "": return self.t("unknown")
        return str(value)

    def _apply_status(self):
        if not hasattr(self, "defender_summary"):
            return
        c = self.colors
        data = self.status_data or {}
        core = [data.get("AntivirusEnabled"), data.get("RealTimeProtectionEnabled")]
        if all(x is True for x in core):
            self.defender_summary.configure(text=self.t("status_ok"), text_color=c["accent"])
            self.defender_details.configure(text="Microsoft Defender reports that antivirus and real-time protection are enabled.")
        elif any(x is False for x in core):
            self.defender_summary.configure(text=self.t("status_warning"), text_color=c["danger"])
            self.defender_details.configure(text="Microsoft Defender reports a disabled protection setting. Review Windows Security.")
        else:
            self.defender_summary.configure(text=self.t("unknown"), text_color=c["warning"])
            self.defender_details.configure(text="Paceful Shield could not confirm the protection state. Check Windows Security directly.")
        for attr, key in (("tile_av", "AntivirusEnabled"), ("tile_rt", "RealTimeProtectionEnabled"), ("tile_service", "AMServiceEnabled"), ("tile_signatures", "SignatureUpdated")):
            label = getattr(self, attr, None)
            if label:
                val = data.get(key)
                color = c["accent"] if val is True or (key == "SignatureUpdated" and val) else c["danger"] if val is False else c["muted"]
                label.configure(text=self._status_value(val), text_color=color)

    def refresh_status(self):
        if not IS_WINDOWS:
            self._set_status_text("Windows only")
            return
        self._set_status_text(self.t("checking"))
        threading.Thread(target=self._status_worker, daemon=True).start()

    def _status_worker(self):
        try: data = defender_status(); error = None
        except Exception as exc: data, error = None, str(exc)
        try: self.after(0, lambda: self._status_done(data, error))
        except Exception: pass

    def _status_done(self, data, error):
        self.status_data = data
        self._set_status_text(self.t("ready"))
        if data:
            self._add_log("Defender status", "Read selected local Microsoft Defender status fields")
        else:
            self._add_log("Defender status", "Unavailable: " + (error or "unknown error")[:180])
        self._apply_status()

    def _set_status_text(self, value):
        try: self.side_status.configure(text="●  " + value)
        except Exception: pass

    def _page_scan(self):
        c = self.colors
        self.content.grid_rowconfigure(0, weight=0); self.content.grid_rowconfigure(1, weight=1)
        card = self._card(self.content); card.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self._label(card, self.t("scan_title"), 18, c["text"], True).pack(anchor="w", padx=18, pady=(16, 5))
        self._label(card, self.t("scan_intro"), 11, c["muted"], wraplength=900).pack(anchor="w", padx=18, pady=(0, 12))
        row = ctk.CTkFrame(card, fg_color="transparent"); row.pack(fill="x", padx=18, pady=(0, 10))
        self.folder_label = self._label(row, self.active_folder or "(no folder selected)", 11, c["muted"], wraplength=650)
        self.folder_label.pack(side="left", fill="x", expand=True)
        self._button(row, self.t("choose_folder"), self._choose_folder).pack(side="right", padx=(10, 0))
        self.progress = ctk.CTkProgressBar(card, height=7, corner_radius=5, progress_color=c["accent"], fg_color=c["panel2"])
        self.progress.pack(fill="x", padx=18, pady=(4, 10)); self.progress.set(0)
        buttons = ctk.CTkFrame(card, fg_color="transparent"); buttons.pack(anchor="w", padx=18, pady=(0, 15))
        self.run_local_btn = self._button(buttons, self.t("scan_selected"), self._scan_selected_folder, primary=True)
        self.run_local_btn.pack(side="left", padx=(0, 8))
        self._button(buttons, self.t("scan_watched"), self._scan_watched_roots).pack(side="left", padx=(0, 8))
        self.cancel_btn = self._button(buttons, self.t("cancel"), self._cancel_scan, state="disabled")
        self.cancel_btn.pack(side="left")
        self.scan_status = self._label(card, self.t("no_scan"), 11, c["muted"], wraplength=900)
        self.scan_status.pack(anchor="w", padx=18, pady=(0, 15))
        results = self._card(self.content); results.grid(row=1, column=0, sticky="nsew")
        self._label(results, self.t("results"), 15, c["text"], True).pack(anchor="w", padx=15, pady=(13, 3))
        self.results_summary = self._label(results, self.t("no_findings"), 10, c["muted"], wraplength=900)
        self.results_summary.pack(anchor="w", padx=15, pady=(0, 6))
        self.results_list = ctk.CTkScrollableFrame(results, fg_color="transparent")
        self.results_list.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        if self.last_result:
            self._populate_findings(self.last_result.get("findings", []))
            self.results_summary.configure(text=f"{self.t('files_checked')}: {self.last_result.get('checked', 0):,}  ·  {self.t('flagged')}: {len(self.last_result.get('findings', []))}")
        else:
            self._populate_findings(self.findings[:30])

    def _choose_folder(self):
        folder = filedialog.askdirectory(title=self.t("choose_folder"))
        if folder:
            self.active_folder = folder
            if hasattr(self, "folder_label"):
                self.folder_label.configure(text=folder)

    def _scan_selected_folder(self):
        if not self.active_folder:
            self._choose_folder()
        if not self.active_folder:
            return
        self._start_scan([self.active_folder], manual=True)

    def _scan_watched_roots(self):
        roots = [p for p in self.prefs.get("watch_paths", []) if Path(p).is_dir() and not path_is_excluded(p, self.prefs.get("exclusions", []))]
        if not roots:
            messagebox.showinfo(PRODUCT_NAME, "No available watched folders. Add a folder in Settings.")
            return
        self._start_scan(roots, manual=True, max_total=MAX_FILES)

    def _start_scan(self, roots: list[str], manual: bool, max_total: int | None = None):
        if self.scan_busy:
            messagebox.showinfo(PRODUCT_NAME, "A scan is already running.")
            return
        self.scan_busy = True
        self.cancel_event = threading.Event()
        if hasattr(self, "progress"):
            self.progress.set(0)
        if hasattr(self, "scan_status"):
            self.scan_status.configure(text=self.t("checking"))
        if hasattr(self, "run_local_btn"):
            self.run_local_btn.configure(state="disabled")
        if hasattr(self, "cancel_btn"):
            self.cancel_btn.configure(state="normal")
        limit = max_total or MAX_FILES
        self.scan_thread = threading.Thread(target=self._scan_worker, args=(roots, manual, limit, self.cancel_event), daemon=True)
        self.scan_thread.start()

    def _scan_worker(self, roots: list[str], manual: bool, max_total: int, cancel: threading.Event):
        checked = 0; errors = 0; findings = []; stopped = False
        exclusions = list(self.prefs.get("exclusions", []))
        valid_roots = [str(Path(p)) for p in roots if Path(p).is_dir()]
        if not valid_roots:
            valid_roots = roots[:1]
        for root in valid_roots:
            if cancel.is_set() or checked >= max_total:
                stopped = True; break
            remaining = max_total - checked
            result = scan_folder(Path(root), cancel,
                progress_callback=lambda n, f, p: self._queue_progress(checked + n, f, p),
                excluded_paths=exclusions, max_files=max(1, remaining))
            checked += result["checked"]; errors += result["errors"]; findings.extend(result["findings"])
            stopped = stopped or result["stopped"]
        payload = {"root": "; ".join(valid_roots), "checked": checked, "findings": findings, "errors": errors, "stopped": stopped, "manual": manual}
        try: self.after(0, lambda: self._scan_finished(payload))
        except Exception: pass

    def _queue_progress(self, checked, found, path):
        try: self.after(0, lambda: self._update_progress(checked, found, path))
        except Exception: pass

    def _update_progress(self, checked, found, path):
        if hasattr(self, "scan_status"):
            self.scan_status.configure(text=f"{self.t('checking')}  ·  {checked:,} files  ·  {self.t('flagged')}: {found}\n{path}")
            self.progress.set(min(checked / MAX_FILES, 0.98))

    def _scan_finished(self, result):
        self.scan_busy = False
        if hasattr(self, "run_local_btn"): self.run_local_btn.configure(state="normal")
        if hasattr(self, "cancel_btn"): self.cancel_btn.configure(state="disabled")
        self.last_result = result
        existing_finding_keys = {x.get("sha256", "") + "|" + x.get("path", "") for x in self.findings}
        new_automatic_findings = [x for x in result["findings"] if (x.get("sha256", "") + "|" + x.get("path", "")) not in existing_finding_keys]
        if hasattr(self, "progress"): self.progress.set(0.99 if result.get("stopped") else 1)
        summary = f"{self.t('files_checked')}: {result['checked']:,}  ·  {self.t('flagged')}: {len(result['findings'])}  ·  {result['root']}"
        if result.get("stopped"): summary += "  ·  Stopped/limit reached"
        if hasattr(self, "scan_status"): self.scan_status.configure(text=self.t("manual_scan_done") + "\n" + summary)
        if hasattr(self, "results_summary"): self.results_summary.configure(text=summary if result["findings"] else self.t("no_findings"))
        for item in result["findings"]:
            self._record_finding(item, notify=False)
        self._add_log("Automatic review" if not result.get("manual") else "Local folder review", f"Checked {result['checked']} files; {len(result['findings'])} item(s) need review; roots={result['root']}")
        if self.current_page == "scan":
            self._populate_findings(result["findings"])
        if new_automatic_findings and not result.get("manual"):
            for item in new_automatic_findings[:3]:
                self._notify_finding(item)
            if len(new_automatic_findings) > 3:
                self._notify(f"{len(new_automatic_findings) - 3} additional item(s) need review", "Open Paceful Shield to review the scan results.")

    def _cancel_scan(self):
        if self.scan_busy:
            self.cancel_event.set()
            if hasattr(self, "scan_status"): self.scan_status.configure(text=self.t("stop_requested"))

    def _populate_findings(self, findings):
        if not hasattr(self, "results_list"):
            return
        for child in self.results_list.winfo_children(): child.destroy()
        if not findings:
            self._label(self.results_list, self.t("no_findings"), 11, self.colors["muted"], wraplength=850).pack(anchor="w", padx=8, pady=8)
            return
        for item in findings[:100]:
            card = ctk.CTkFrame(self.results_list, fg_color=self.colors["panel2"], corner_radius=10)
            card.pack(fill="x", padx=4, pady=4)
            head = ctk.CTkFrame(card, fg_color="transparent"); head.pack(fill="x", padx=11, pady=(9, 2))
            color = self.colors["danger"] if item.get("level") == "HIGH" else self.colors["warning"] if item.get("level") == "MEDIUM" else self.colors["blue"]
            self._label(head, item.get("name", "Unknown file"), 11, self.colors["text"], True, wraplength=500).pack(side="left", fill="x", expand=True)
            level_text = self.t("test") if item.get("level") == "TEST" else item.get("level", "INFO")
            self._label(head, level_text, 10, color, True).pack(side="right", padx=(8, 0))
            self._label(card, item.get("reason", ""), 10, self.colors["muted"], wraplength=850).pack(anchor="w", padx=11, pady=(0, 3))
            self._label(card, f"SHA-256: {item.get('sha256', 'not calculated')}\n{item.get('path', '')}", 9, self.colors["muted"], wraplength=850).pack(anchor="w", padx=11, pady=(0, 7))
            row = ctk.CTkFrame(card, fg_color="transparent"); row.pack(anchor="w", padx=11, pady=(0, 9))
            self._button(row, self.t("recycle"), lambda found=item: self._move_to_recycle_bin(found)).pack(side="left", padx=(0, 7))
            self._button(row, self.t("exclude_this"), lambda found=item: self._add_exclusion_path(found.get("path", ""), rerender=True)).pack(side="left", padx=(0, 7))
            self._button(row, self.t("open_security_scan"), lambda found=item: self._scan_with_defender(found)).pack(side="left")

    def _record_finding(self, item: dict, notify: bool):
        key = item.get("sha256", "") + "|" + item.get("path", "")
        if not key.strip("|"):
            return
        existed = any((entry.get("sha256", "") + "|" + entry.get("path", "")) == key for entry in self.findings)
        if not existed:
            self.findings.insert(0, item)
            self.findings = self.findings[:200]
            write_json(FINDINGS_PATH, self.findings)
            self._add_log("File requires review", f"{item.get('level')}: {item.get('reason')} · {item.get('path')}")
            if notify:
                self._notify_finding(item)
            if self.current_page == "scan":
                self._populate_findings(self.findings[:60])

    def _move_to_recycle_bin(self, finding: dict):
        path = finding.get("path", "")
        if not path or not Path(path).exists():
            messagebox.showwarning(PRODUCT_NAME, "The file no longer exists or is not accessible.")
            return
        if not messagebox.askyesno(PRODUCT_NAME, self.t("send_trash_confirm") + f"\n\n{path}"):
            return
        if send2trash is None:
            messagebox.showerror(PRODUCT_NAME, "Recycle Bin support is unavailable in this build.")
            return
        try:
            send2trash(path)
            self._add_log("User-approved file removal", path)
            messagebox.showinfo(PRODUCT_NAME, self.t("trash_done"))
            self.findings = [x for x in self.findings if x.get("path") != path]
            write_json(FINDINGS_PATH, self.findings)
            if self.current_page == "scan": self._populate_findings(self.last_result.get("findings", []) if self.last_result else self.findings)
        except Exception as exc:
            messagebox.showerror(PRODUCT_NAME, f"{self.t('trash_failed')}\n\n{exc}")

    def _scan_with_defender(self, finding: dict):
        path = finding.get("path", "")
        if not path or not Path(path).exists():
            messagebox.showwarning(PRODUCT_NAME, "The file no longer exists or is not accessible.")
            return
        prompt = ("Ask Microsoft Defender to scan this specific file? Windows may ask for administrator permission. "
                  "Paceful Shield will only send the request; it cannot confirm when the scan finishes.\n\n" + path)
        if not messagebox.askyesno(PRODUCT_NAME, prompt):
            return
        try:
            request_defender_path_scan(path)
            self._add_log("Targeted Defender scan requested", path)
            messagebox.showinfo(PRODUCT_NAME, self.t("scan_started"))
        except Exception as exc:
            messagebox.showerror(PRODUCT_NAME, f"{self.t('error')}\n\n{exc}")

    def _page_system(self):
        c = self.colors
        self.content.grid_rowconfigure(0, weight=1)
        wrapper = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.grid_columnconfigure(0, weight=1)
        metrics = self._card(wrapper); metrics.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        head = ctk.CTkFrame(metrics, fg_color="transparent"); head.pack(fill="x", padx=16, pady=(13, 9))
        self._label(head, self.t("system_desc"), 13, c["text"], True).pack(side="left")
        self._button(head, self.t("refresh_system"), self._refresh_system_metrics).pack(side="right")
        grid = ctk.CTkFrame(metrics, fg_color="transparent"); grid.pack(fill="x", padx=12, pady=(0, 14))
        self.metric_labels = {}
        for col, key in enumerate(("cpu", "ram", "disk")):
            tile = ctk.CTkFrame(grid, fg_color=c["panel2"], corner_radius=10); tile.grid(row=0, column=col, sticky="ew", padx=4)
            grid.grid_columnconfigure(col, weight=1)
            self._label(tile, self.t(key), 10, c["muted"], True).pack(anchor="w", padx=11, pady=(10, 4))
            label = self._label(tile, self.t("checking"), 17, c["accent"], True); label.pack(anchor="w", padx=11, pady=(0, 10))
            self.metric_labels[key] = label

        processes = self._card(wrapper); processes.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self._label(processes, self.t("top_processes"), 14, c["text"], True).pack(anchor="w", padx=15, pady=(12, 5))
        self._label(processes, self.t("system_readonly"), 10, c["muted"], wraplength=900).pack(anchor="w", padx=15, pady=(0, 6))
        self.system_process_list = ctk.CTkFrame(processes, fg_color="transparent"); self.system_process_list.pack(fill="x", padx=9, pady=(0, 11))
        self._populate_processes([])

        startup = self._card(wrapper); startup.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        self._label(startup, self.t("startup_apps"), 14, c["text"], True).pack(anchor="w", padx=15, pady=(12, 4))
        self._label(startup, self.t("startup_note"), 10, c["muted"], wraplength=900).pack(anchor="w", padx=15, pady=(0, 6))
        self.startup_list = ctk.CTkFrame(startup, fg_color="transparent"); self.startup_list.pack(fill="x", padx=9, pady=(0, 7))
        self._populate_startup_items([])
        self._button(startup, self.t("startup_settings"), self._open_startup_settings).pack(anchor="w", padx=15, pady=(0, 12))
        self.after(150, self._refresh_system_metrics)

    def _refresh_system_metrics(self):
        if self.current_page != "system" or self.system_refresh_inflight:
            return
        if psutil is None:
            for label in getattr(self, "metric_labels", {}).values(): label.configure(text=self.t("no_data"))
            self._populate_processes([])
            self._populate_startup_items([])
            return
        self.system_refresh_inflight = True
        threading.Thread(target=self._system_metrics_worker, daemon=True).start()

    def _system_metrics_worker(self):
        try:
            cpu = psutil.cpu_percent(interval=0.15)
            memory = psutil.virtual_memory()
            drive = Path.home().anchor or "C:\\"
            disk = psutil.disk_usage(drive)
            processes = []
            for proc in psutil.process_iter(["pid", "name", "memory_info"]):
                try:
                    info = proc.info
                    mem_info = info.get("memory_info")
                    processes.append({"pid": info.get("pid", 0), "name": info.get("name") or "Unknown", "memory": int(getattr(mem_info, "rss", 0) or 0)})
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            processes.sort(key=lambda x: x["memory"], reverse=True)
            data = {"cpu": cpu, "ram_percent": memory.percent, "ram_used": memory.used, "ram_total": memory.total,
                    "disk_percent": disk.percent, "disk_used": disk.used, "disk_total": disk.total,
                    "processes": processes[:10], "startup": self._get_startup_items(), "error": None}
        except Exception as exc:
            data = {"error": str(exc), "processes": [], "startup": []}
        try: self.after(0, lambda: self._apply_system_metrics(data))
        except Exception: pass

    def _apply_system_metrics(self, data):
        self.system_refresh_inflight = False
        if self.current_page != "system":
            return
        labels = getattr(self, "metric_labels", {})
        if data.get("error"):
            for label in labels.values(): label.configure(text=self.t("no_data"))
        else:
            labels.get("cpu") and labels["cpu"].configure(text=f"{data['cpu']:.0f}%")
            labels.get("ram") and labels["ram"].configure(text=f"{data['ram_percent']:.0f}%  ·  {data['ram_used'] / (1024**3):.1f}/{data['ram_total'] / (1024**3):.1f} GB")
            labels.get("disk") and labels["disk"].configure(text=f"{data['disk_percent']:.0f}%  ·  {data['disk_used'] / (1024**3):.0f}/{data['disk_total'] / (1024**3):.0f} GB")
        self._populate_processes(data.get("processes", []))
        self._populate_startup_items(data.get("startup", []))
        self.after(5000, self._refresh_system_metrics)

    def _populate_processes(self, processes):
        if not hasattr(self, "system_process_list"):
            return
        for child in self.system_process_list.winfo_children(): child.destroy()
        if not processes:
            self._label(self.system_process_list, self.t("no_data"), 10, self.colors["muted"]).pack(anchor="w", padx=6, pady=5)
            return
        for proc in processes:
            row = ctk.CTkFrame(self.system_process_list, fg_color=self.colors["panel2"], corner_radius=7); row.pack(fill="x", padx=3, pady=2)
            self._label(row, str(proc.get("name", "Unknown"))[:90], 10, self.colors["text"], True, wraplength=560).pack(side="left", padx=9, pady=6, fill="x", expand=True)
            self._label(row, f"PID {proc.get('pid', '?')}", 9, self.colors["muted"]).pack(side="left", padx=6)
            self._label(row, f"{proc.get('memory', 0) / (1024**2):.0f} MB", 9, self.colors["accent"], True).pack(side="right", padx=9)

    def _get_startup_items(self):
        items = []
        if not IS_WINDOWS:
            return items
        try:
            import winreg
            keys = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "Current user"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "Local machine"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run", "Local machine 32-bit"),
            ]
            for hive, subkey, scope in keys:
                try:
                    with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as key:
                        index = 0
                        while True:
                            try:
                                name, command, _kind = winreg.EnumValue(key, index); index += 1
                                items.append({"name": f"{name} ({scope})", "command": str(command)})
                            except OSError:
                                break
                except OSError:
                    continue
        except Exception:
            pass
        startup_dirs = [
            Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs/Startup",
            Path(os.environ.get("PROGRAMDATA", "")) / "Microsoft/Windows/Start Menu/Programs/Startup",
        ]
        for folder in startup_dirs:
            try:
                if folder.is_dir():
                    for item in folder.iterdir():
                        items.append({"name": f"{item.name} (Startup folder)", "command": str(item)})
            except OSError:
                continue
        return items[:80]

    def _populate_startup_items(self, items):
        if not hasattr(self, "startup_list"):
            return
        for child in self.startup_list.winfo_children(): child.destroy()
        if not items:
            self._label(self.startup_list, self.t("no_data"), 10, self.colors["muted"]).pack(anchor="w", padx=6, pady=5)
            return
        for entry in items:
            row = ctk.CTkFrame(self.startup_list, fg_color=self.colors["panel2"], corner_radius=7); row.pack(fill="x", padx=3, pady=2)
            self._label(row, entry.get("name", "Startup item"), 10, self.colors["text"], True, wraplength=800).pack(anchor="w", padx=9, pady=(6, 1))
            self._label(row, entry.get("command", ""), 9, self.colors["muted"], wraplength=900).pack(anchor="w", padx=9, pady=(0, 6))

    def _open_startup_settings(self):
        try:
            if IS_WINDOWS: os.startfile("ms-settings:startupapps")
            else: messagebox.showinfo(PRODUCT_NAME, "Windows only")
        except Exception as exc:
            messagebox.showerror(PRODUCT_NAME, str(exc))

    def _page_network(self):
        c = self.colors
        self.content.grid_rowconfigure(0, weight=1)
        card = self._card(self.content); card.grid(row=0, column=0, sticky="nsew")
        head = ctk.CTkFrame(card, fg_color="transparent"); head.pack(fill="x", padx=16, pady=(13, 6))
        self._label(head, self.t("network_connections"), 15, c["text"], True).pack(side="left")
        self._button(head, self.t("refresh_system"), self._refresh_network_connections).pack(side="right")
        self._label(card, self.t("network_desc") + "  " + self.t("network_permission"), 10, c["muted"], wraplength=900).pack(anchor="w", padx=16, pady=(0, 9))
        self.network_status = self._label(card, self.t("checking"), 10, c["muted"], wraplength=900)
        self.network_status.pack(anchor="w", padx=16, pady=(0, 6))
        self.network_list = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.network_list.pack(fill="both", expand=True, padx=8, pady=(0, 10))
        self.after(150, self._refresh_network_connections)

    def _refresh_network_connections(self):
        if self.current_page != "network" or self.network_refresh_inflight:
            return
        if psutil is None:
            if hasattr(self, "network_status"): self.network_status.configure(text=self.t("no_data"))
            return
        self.network_refresh_inflight = True
        threading.Thread(target=self._network_worker, daemon=True).start()

    def _network_worker(self):
        rows = []; error = None
        try:
            for conn in psutil.net_connections(kind="inet")[:80]:
                pid = conn.pid
                process = "Unknown"
                if pid:
                    try: process = psutil.Process(pid).name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): process = "Not available"
                def fmt(addr):
                    if not addr: return "—"
                    try: return f"{addr.ip}:{addr.port}"
                    except AttributeError:
                        try: return f"{addr[0]}:{addr[1]}"
                        except Exception: return str(addr)
                rows.append({"pid": pid, "process": process, "local": fmt(conn.laddr), "remote": fmt(conn.raddr), "status": conn.status or "—"})
            rows.sort(key=lambda x: (x["process"].lower(), x["remote"]))
        except Exception as exc:
            error = str(exc)
        try: self.after(0, lambda: self._apply_network_connections(rows, error))
        except Exception: pass

    def _apply_network_connections(self, rows, error):
        self.network_refresh_inflight = False
        if self.current_page != "network":
            return
        for child in self.network_list.winfo_children(): child.destroy()
        if error:
            self.network_status.configure(text=self.t("no_data") + " " + error[:180])
            return
        self.network_status.configure(text=self.t("connections_returned").format(count=len(rows)))
        if not rows:
            self._label(self.network_list, self.t("no_data"), 10, self.colors["muted"]).pack(anchor="w", padx=5, pady=6)
            return
        for item in rows[:80]:
            row = ctk.CTkFrame(self.network_list, fg_color=self.colors["panel2"], corner_radius=8); row.pack(fill="x", padx=3, pady=3)
            self._label(row, f"{item['process']}  ·  PID {item['pid'] or '?'}", 10, self.colors["text"], True, wraplength=850).pack(anchor="w", padx=9, pady=(7, 2))
            self._label(row, f"{self.t('local_address')}: {item['local']}\n{self.t('remote_address')}: {item['remote']}  ·  {self.t('state')}: {item['status']}", 9, self.colors["muted"], wraplength=900).pack(anchor="w", padx=9, pady=(0, 7))

    def _page_activity(self):
        self.content.grid_rowconfigure(0, weight=1)
        card = self._card(self.content); card.grid(row=0, column=0, sticky="nsew")
        top = ctk.CTkFrame(card, fg_color="transparent"); top.pack(fill="x", padx=16, pady=(14, 8))
        self._label(top, self.t("no_upload"), 10, self.colors["muted"], wraplength=650).pack(side="left", fill="x", expand=True)
        self._button(top, self.t("clear_log"), self._clear_log).pack(side="right", padx=(10, 0))
        listing = ctk.CTkScrollableFrame(card, fg_color="transparent")
        listing.pack(fill="both", expand=True, padx=8, pady=(0, 10))
        if not self.logs:
            self._label(listing, self.t("activity_empty"), 12, self.colors["muted"]).pack(anchor="w", padx=10, pady=14)
        for item in self.logs[:150]:
            row = ctk.CTkFrame(listing, fg_color=self.colors["panel2"], corner_radius=9); row.pack(fill="x", padx=4, pady=4)
            self._label(row, item.get("time", ""), 9, self.colors["muted"]).pack(anchor="w", padx=11, pady=(8, 2))
            self._label(row, item.get("event", ""), 11, self.colors["text"], True).pack(anchor="w", padx=11)
            self._label(row, item.get("result", ""), 10, self.colors["muted"], wraplength=900).pack(anchor="w", padx=11, pady=(2, 8))

    def _page_settings(self):
        c = self.colors
        self.content.grid_rowconfigure(0, weight=1)
        wrapper = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.grid_columnconfigure(0, weight=1)
        appearance = self._card(wrapper); appearance.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self._label(appearance, self.t("appearance"), 16, c["text"], True).pack(anchor="w", padx=16, pady=(13, 8))
        row = ctk.CTkFrame(appearance, fg_color="transparent"); row.pack(anchor="w", padx=16, pady=(0, 12))
        self._button(row, "☾  " + self.t("dark"), lambda: self._change_theme("dark"), primary=self.theme == "dark").pack(side="left", padx=(0, 7))
        self._button(row, "☼  " + self.t("light"), lambda: self._change_theme("light"), primary=self.theme == "light").pack(side="left")
        self._label(appearance, self.t("language"), 11, c["muted"], True).pack(anchor="w", padx=16)
        row2 = ctk.CTkFrame(appearance, fg_color="transparent"); row2.pack(anchor="w", padx=16, pady=(6, 14))
        self._button(row2, "Türkçe", lambda: self._change_language("tr"), primary=self.language == "tr").pack(side="left", padx=(0, 7))
        self._button(row2, "English", lambda: self._change_language("en"), primary=self.language == "en").pack(side="left")

        monitor = self._card(wrapper); monitor.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self._label(monitor, self.t("monitoring"), 16, c["text"], True).pack(anchor="w", padx=16, pady=(13, 4))
        self._label(monitor, self.t("monitoring_desc"), 10, c["muted"], wraplength=900).pack(anchor="w", padx=16, pady=(0, 8))
        self.monitor_var = ctk.BooleanVar(value=bool(self.prefs.get("monitoring_enabled", True)))
        ctk.CTkCheckBox(monitor, text=self.t("monitoring"), variable=self.monitor_var, command=self._toggle_monitoring,
                        text_color=c["text"], fg_color=c["accent"], hover_color=c["accent_hover"]).pack(anchor="w", padx=16, pady=(0, 10))
        self._label(monitor, self.t("watch_paths"), 11, c["muted"], True).pack(anchor="w", padx=16, pady=(0, 5))
        self.watch_list = ctk.CTkFrame(monitor, fg_color="transparent"); self.watch_list.pack(fill="x", padx=10, pady=(0, 5))
        self._populate_path_list(self.watch_list, self.prefs.get("watch_paths", []), self._remove_watch_path)
        self._button(monitor, self.t("add_folder"), self._add_watch_folder).pack(anchor="w", padx=16, pady=(3, 13))

        auto = self._card(wrapper); auto.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        self._label(auto, self.t("autostart"), 15, c["text"], True).pack(anchor="w", padx=16, pady=(13, 4))
        self._label(auto, self.t("autostart_desc"), 10, c["muted"], wraplength=900).pack(anchor="w", padx=16, pady=(0, 8))
        self.autostart_var = ctk.BooleanVar(value=bool(self.prefs.get("autostart", False)))
        ctk.CTkCheckBox(auto, text=self.t("autostart"), variable=self.autostart_var, command=self._toggle_autostart,
                        text_color=c["text"], fg_color=c["accent"], hover_color=c["accent_hover"]).pack(anchor="w", padx=16, pady=(0, 13))

        exclusions = self._card(wrapper); exclusions.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        self._label(exclusions, self.t("exclusions"), 16, c["text"], True).pack(anchor="w", padx=16, pady=(13, 4))
        self._label(exclusions, self.t("exclusions_desc"), 10, c["muted"], wraplength=900).pack(anchor="w", padx=16, pady=(0, 8))
        self.exclusion_list = ctk.CTkFrame(exclusions, fg_color="transparent"); self.exclusion_list.pack(fill="x", padx=10, pady=(0, 5))
        self._populate_path_list(self.exclusion_list, self.prefs.get("exclusions", []), self._remove_exclusion)
        buttons = ctk.CTkFrame(exclusions, fg_color="transparent"); buttons.pack(anchor="w", padx=16, pady=(3, 13))
        self._button(buttons, self.t("add_file"), self._add_exclusion_file).pack(side="left", padx=(0, 7))
        self._button(buttons, self.t("add_exclusion_folder"), self._add_exclusion_folder).pack(side="left")

        about = self._card(wrapper); about.grid(row=4, column=0, sticky="ew", pady=(0, 12))
        self._label(about, self.t("about"), 14, c["text"], True).pack(anchor="w", padx=16, pady=(12, 4))
        self._label(about, f"{PRODUCT_NAME} · {APP_VERSION} · Windows", 10, c["muted"]).pack(anchor="w", padx=16, pady=(0, 6))
        self._label(about, self.t("tray_note"), 10, c["warning"], wraplength=900).pack(anchor="w", padx=16, pady=(0, 7))
        self._label(about, self.t("rule_block_unavailable"), 10, c["muted"], wraplength=900).pack(anchor="w", padx=16, pady=(0, 12))

    def _populate_path_list(self, container, paths: list[str], remove_callback):
        for child in container.winfo_children(): child.destroy()
        if not paths:
            self._label(container, "(none)", 10, self.colors["muted"]).pack(anchor="w", padx=7, pady=5)
        for path in paths:
            row = ctk.CTkFrame(container, fg_color=self.colors["panel2"], corner_radius=8); row.pack(fill="x", padx=4, pady=3)
            self._label(row, path, 10, self.colors["text"], wraplength=740).pack(side="left", fill="x", expand=True, padx=9, pady=7)
            self._button(row, self.t("remove"), lambda value=path: remove_callback(value), width=75).pack(side="right", padx=6, pady=4)

    def _add_watch_folder(self):
        folder = filedialog.askdirectory(title=self.t("watch_add_prompt"))
        if not folder: return
        paths = self.prefs.setdefault("watch_paths", [])
        if normalized_path(folder) in [normalized_path(p) for p in paths]: return
        paths.append(folder); self._save_prefs(); self._restart_monitoring(); self._render_page("settings")

    def _remove_watch_path(self, path):
        self.prefs["watch_paths"] = [p for p in self.prefs.get("watch_paths", []) if normalized_path(p) != normalized_path(path)]
        self._save_prefs(); self._restart_monitoring(); self._render_page("settings")

    def _add_exclusion_file(self):
        path = filedialog.askopenfilename(title=self.t("select_file"))
        if path: self._add_exclusion_path(path, rerender=True)

    def _add_exclusion_folder(self):
        path = filedialog.askdirectory(title=self.t("exclusion_add_prompt"))
        if path: self._add_exclusion_path(path, rerender=True)

    def _add_exclusion_path(self, path: str, rerender: bool = False):
        if not path: return
        paths = self.prefs.setdefault("exclusions", [])
        if normalized_path(path) not in [normalized_path(p) for p in paths]:
            paths.append(path); self._save_prefs(); self._add_log("Paceful Shield exclusion added", path)
        if rerender and self.current_page == "settings": self._render_page("settings")
        elif self.current_page == "scan" and hasattr(self, "results_list"): self._render_page("scan")
        self._restart_monitoring()

    def _remove_exclusion(self, path):
        self.prefs["exclusions"] = [p for p in self.prefs.get("exclusions", []) if normalized_path(p) != normalized_path(path)]
        self._save_prefs(); self._add_log("Paceful Shield exclusion removed", path); self._restart_monitoring(); self._render_page("settings")

    def _toggle_monitoring(self):
        enabled = bool(self.monitor_var.get())
        self.prefs["monitoring_enabled"] = enabled; self._save_prefs()
        if enabled:
            self._start_monitoring()
            self._schedule_auto_scan(1000)
        else: self._stop_monitoring()
        try: self.monitor_status.configure(text=self.t("monitor_on") if enabled else self.t("monitor_off"))
        except Exception: pass
        self._add_log("Automatic monitoring", "Enabled" if enabled else "Disabled")

    def _toggle_autostart(self):
        enabled = bool(self.autostart_var.get())
        if not IS_WINDOWS:
            messagebox.showwarning(PRODUCT_NAME, "Windows startup integration is only available on Windows.")
            self.autostart_var.set(False); return
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                if enabled:
                    if getattr(sys, "frozen", False):
                        command = f'"{sys.executable}" --background'
                    else:
                        command = f'"{sys.executable}" "{Path(__file__).resolve()}" --background'
                    winreg.SetValueEx(key, "PacefulShield", 0, winreg.REG_SZ, command)
                else:
                    try: winreg.DeleteValue(key, "PacefulShield")
                    except FileNotFoundError: pass
            self.prefs["autostart"] = enabled; self._save_prefs()
            self._add_log("Windows startup setting", "Enabled" if enabled else "Disabled")
        except Exception as exc:
            self.autostart_var.set(not enabled)
            messagebox.showerror(PRODUCT_NAME, f"{self.t('error')}\n\n{exc}")

    def _change_theme(self, theme):
        self.theme = theme; self._save_prefs(); ctk.set_appearance_mode(theme)
        self.colors = LIGHT if theme == "light" else COLORS
        # Rebuild the UI without resetting observers or background state.
        for child in self.winfo_children(): child.destroy()
        self.configure(fg_color=self.colors["bg"])
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self.main = ctk.CTkFrame(self, fg_color=self.colors["bg"], corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew"); self.main.grid_columnconfigure(0, weight=1); self.main.grid_rowconfigure(1, weight=1)
        self._build_header()
        self.content = ctk.CTkFrame(self.main, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=26, pady=(6, 22)); self.content.grid_columnconfigure(0, weight=1); self.content.grid_rowconfigure(0, weight=1)
        self._render_page(self.current_page)
        self.protocol("WM_DELETE_WINDOW", self._hide_to_tray)

    def _change_language(self, lang):
        self.language = lang; self._save_prefs(); self._change_theme(self.theme)

    def _add_log(self, event: str, result: str):
        self.logs.insert(0, {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": event[:120], "result": result[:800]})
        self.logs = self.logs[:200]
        write_json(LOG_PATH, self.logs)
        if self.current_page == "activity":
            try: self._render_page("activity")
            except Exception: pass

    def _clear_log(self):
        if messagebox.askyesno(PRODUCT_NAME, self.t("clear_log") + "?"):
            self.logs = []; write_json(LOG_PATH, self.logs); self._render_page("activity")

    def _request_scan(self, kind):
        if not IS_WINDOWS:
            messagebox.showinfo(PRODUCT_NAME, "This feature requires Windows and Microsoft Defender."); return
        friendly = self.t("quick") if kind == "QuickScan" else self.t("full")
        if not messagebox.askyesno(PRODUCT_NAME, f"{friendly}\n\nWindows may request administrator permission. Paceful Shield does not delete files automatically."):
            return
        try:
            request_defender_scan(kind)
            self._add_log(friendly, "Request sent to Microsoft Defender; completion not verified")
            messagebox.showinfo(PRODUCT_NAME, self.t("scan_started"))
        except Exception as exc:
            messagebox.showerror(PRODUCT_NAME, f"{self.t('error')}\n\n{exc}")

    def _open_security(self):
        try:
            open_windows_security()
            self._add_log("Open Windows Security", "Opened Windows Security URI")
        except Exception as exc:
            messagebox.showerror(PRODUCT_NAME, str(exc))

    def refresh_defender_detections(self):
        if not IS_WINDOWS:
            return
        threading.Thread(target=self._defender_detections_worker, daemon=True).start()

    def _defender_detections_worker(self):
        try: results = defender_detections(); error = None
        except Exception as exc: results, error = [], str(exc)
        try: self.after(0, lambda: self._apply_defender_detections(results, error))
        except Exception: pass

    def _detection_key(self, item):
        resources = item.get("Resources", "")
        return str(item.get("ThreatID", "")) + "|" + str(item.get("InitialDetectionTime", "")) + "|" + str(resources)

    def _apply_defender_detections(self, results, error):
        if error:
            self._add_log("Defender threat history", "Unavailable: " + error[:200])
            return
        self.defender_detections = results
        keys_now = {self._detection_key(x) for x in results}
        new_keys = keys_now - self.known_defender_keys
        # First successful poll establishes a baseline and does not notify for historical detections.
        if self.defender_baseline_loaded and new_keys:
            for item in results:
                if self._detection_key(item) in new_keys:
                    name = str(item.get("ThreatName") or "Threat reported by Defender")
                    self._notify("Microsoft Defender reported a threat", name[:200])
                    self._add_log("Defender threat reported", name + " · " + str(item.get("Resources", ""))[:300])
        self.known_defender_keys |= keys_now
        self.known_defender_keys = set(list(self.known_defender_keys)[-500:])
        self.prefs["seen_defender_keys"] = list(self.known_defender_keys)
        self.prefs["defender_baseline_loaded"] = True
        self.defender_baseline_loaded = True
        self._save_prefs()
        self._populate_defender_threats()

    def _populate_defender_threats(self):
        if not hasattr(self, "defender_threat_list"):
            return
        for child in self.defender_threat_list.winfo_children(): child.destroy()
        if not self.defender_detections:
            self._label(self.defender_threat_list, self.t("no_defender_findings"), 10, self.colors["muted"], wraplength=850).pack(anchor="w", padx=4, pady=5)
            return
        for item in self.defender_detections[:10]:
            name = str(item.get("ThreatName") or "Threat reported by Defender")
            when = str(item.get("InitialDetectionTime") or "")
            resources = item.get("Resources", "")
            if isinstance(resources, list): resources = "; ".join(map(str, resources[:3]))
            line = ctk.CTkFrame(self.defender_threat_list, fg_color=self.colors["panel2"], corner_radius=8); line.pack(fill="x", padx=3, pady=3)
            self._label(line, name, 11, self.colors["text"], True, wraplength=800).pack(anchor="w", padx=9, pady=(7, 2))
            self._label(line, f"{when} · {str(resources)[:450]}", 9, self.colors["muted"], wraplength=850).pack(anchor="w", padx=9, pady=(0, 7))

    def _defender_poll_loop(self):
        self.refresh_defender_detections()
        self.after(300000, self._defender_poll_loop)

    def _start_monitoring(self):
        if not self.prefs.get("monitoring_enabled", True):
            return
        if Observer is None or watchdog is None:
            try: self.monitor_status.configure(text=self.t("monitor_unavailable"))
            except Exception: pass
            return
        self._stop_monitoring()
        class Handler(watchdog.events.FileSystemEventHandler):
            def __init__(self, app): self.app = app
            def on_created(self, event):
                if not event.is_directory: self.app._queue_file_check(event.src_path)
            def on_modified(self, event):
                if not event.is_directory: self.app._queue_file_check(event.src_path)
            def on_moved(self, event):
                if not event.is_directory: self.app._queue_file_check(event.dest_path)
        observer = Observer()
        handler = Handler(self)
        scheduled = 0
        for path in self.prefs.get("watch_paths", []):
            try:
                folder = Path(path)
                if folder.is_dir() and not path_is_excluded(folder, self.prefs.get("exclusions", [])):
                    observer.schedule(handler, str(folder), recursive=True); scheduled += 1
            except Exception as exc:
                self._add_log("Watch setup", f"Could not watch {path}: {exc}")
        if scheduled:
            observer.daemon = True
            observer.start()
            self.observer = observer
            try: self.monitor_status.configure(text=self.t("monitor_on"))
            except Exception: pass
            self._add_log("Automatic file monitoring", f"Monitoring {scheduled} folder(s)")
        else:
            try: self.monitor_status.configure(text="No watched folder available")
            except Exception: pass

    def _stop_monitoring(self):
        if self.observer is not None:
            try:
                self.observer.stop(); self.observer.join(timeout=2)
            except Exception: pass
            self.observer = None

    def _restart_monitoring(self):
        if self.prefs.get("monitoring_enabled", True):
            self._start_monitoring()

    def _queue_file_check(self, path: str):
        if path_is_excluded(path, self.prefs.get("exclusions", [])):
            return
        try:
            p = Path(path)
            if p.suffix.lower() not in EXECUTABLE_EXTS | SCRIPT_EXTS and not DOUBLE_EXT_RE.search(p.name.lower()):
                # EICAR string may exist in an arbitrary test file, so check small files too.
                if p.exists() and p.stat().st_size > MAX_SCRIPT_BYTES:
                    return
        except OSError:
            return
        key = normalized_path(path)
        prior = self.recent_event_timers.pop(key, None)
        if prior: prior.cancel()
        timer = threading.Timer(1.5, self._check_changed_file, args=(path,))
        timer.daemon = True
        self.recent_event_timers[key] = timer
        timer.start()

    def _check_changed_file(self, path: str):
        key = normalized_path(path)
        self.recent_event_timers.pop(key, None)
        if path_is_excluded(path, self.prefs.get("exclusions", [])):
            return
        try:
            p = Path(path)
            if not p.is_file(): return
            size1 = p.stat().st_size
            time.sleep(0.35)
            if not p.is_file() or p.stat().st_size != size1:
                return
            found = inspect_one_file(p, exclusions=self.prefs.get("exclusions", []))
            if found:
                try: self.after(0, lambda item=found: self._record_finding(item, notify=True))
                except Exception: pass
        except (OSError, PermissionError):
            return

    def _schedule_auto_scan(self, delay_ms: int):
        if self.auto_scan_after_id is not None:
            try: self.after_cancel(self.auto_scan_after_id)
            except Exception: pass
        self.auto_scan_after_id = self.after(delay_ms, self._automatic_scan)

    def _automatic_scan(self):
        self.auto_scan_after_id = None
        if self.prefs.get("monitoring_enabled", True):
            roots = [p for p in self.prefs.get("watch_paths", []) if Path(p).is_dir() and not path_is_excluded(p, self.prefs.get("exclusions", []))]
            if roots and not self.scan_busy:
                self._start_scan(roots, manual=False, max_total=MAX_AUTO_FILES)
        self._schedule_auto_scan(AUTO_SCAN_INTERVAL_MS)

    def _notify_finding(self, item):
        level = item.get("level", "INFO")
        self._notify("Paceful Shield: file needs review", f"{item.get('name', 'File')} · {level}: {item.get('reason', '')[:180]}")

    def _notify(self, title: str, message: str):
        message = message[:240]
        if Notification is not None and IS_WINDOWS:
            try:
                Notification(app_id=PRODUCT_NAME, title=title[:100], msg=message, duration="long").show()
                return
            except Exception as exc:
                self._add_log("Desktop notification", f"Could not show toast: {exc}")
        # If toast notifications are unavailable, record the event. Avoid modal prompts from background threads.
        self._add_log("Notification unavailable", title + " — " + message)

    def _setup_tray(self):
        if pystray is None or Image is None:
            self.tray_icon = None
            self._add_log("System tray", "Tray dependency unavailable; window close will minimize to taskbar")
            return
        try:
            img_path = resource_path("paceful-shield.png")
            icon_image = Image.open(img_path).convert("RGBA") if img_path.exists() else Image.new("RGBA", (64, 64), (8, 13, 23, 255))
            icon_image.thumbnail((64, 64))
            menu = pystray.Menu(
                pystray.MenuItem("Open Paceful Shield", self._tray_show, default=True),
                pystray.MenuItem("Exit", self._tray_exit),
            )
            self.tray_icon = pystray.Icon("PacefulShield", icon_image, PRODUCT_NAME, menu)
            self.tray_icon.run_detached()
        except Exception as exc:
            self.tray_icon = None
            self._add_log("System tray", f"Could not initialize tray icon: {exc}")

    def _tray_show(self, icon=None, item=None):
        try: self.after(0, self._restore_window)
        except Exception: pass

    def _restore_window(self):
        self.deiconify(); self.state("normal"); self.lift()
        try: self.focus_force()
        except Exception: pass

    def _hide_to_tray(self):
        if self.tray_icon is not None:
            self.withdraw()
            self._notify("Paceful Shield is still running", "The app is hidden in the system tray. Use the tray icon to reopen or exit.")
        else:
            self.iconify()

    def _tray_exit(self, icon=None, item=None):
        try: self.after(0, self._quit_app)
        except Exception: pass

    def _quit_app(self):
        self._stop_monitoring()
        for timer in list(self.recent_event_timers.values()):
            try: timer.cancel()
            except Exception: pass
        if self.tray_icon is not None:
            try: self.tray_icon.stop()
            except Exception: pass
        self.destroy()


if __name__ == "__main__":
    try:
        app = PaceApp()
        if "--background" in sys.argv:
            app.withdraw()
        app.mainloop()
    except Exception as exc:
        try: messagebox.showerror("Paceful Shield", f"Paceful Shield could not start.\n\n{exc}")
        except Exception: print(exc, file=sys.stderr)
