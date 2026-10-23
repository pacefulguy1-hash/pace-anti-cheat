from __future__ import annotations

import ctypes
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import customtkinter as ctk

APP_NAME = "PACE"
APP_VERSION = "0.3 Beta"
IS_WINDOWS = sys.platform == "win32"

# Separate settings/log files preserve all existing PACE 0.2 user data.
APP_DIR = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "PACE"
APP_DIR.mkdir(parents=True, exist_ok=True)
PREFS_PATH = APP_DIR / "settings-v03.json"
LOG_PATH = APP_DIR / "activity-v03.json"
MAX_FILES = 12000
MAX_HASH_BYTES = 200 * 1024 * 1024
MAX_TOTAL_HASH_BYTES = 1024 * 1024 * 1024
MAX_SCRIPT_BYTES = 1024 * 1024

COLORS = {
    "bg": "#0B1020", "sidebar": "#0E1526", "panel": "#131D31", "panel2": "#192740",
    "line": "#293852", "text": "#F4F7FC", "muted": "#9BAAC2", "accent": "#65D6B0",
    "accent_hover": "#45BD98", "blue": "#77A7FF", "warning": "#F5C977", "danger": "#FF8794",
    "white": "#FFFFFF", "input": "#101A2D"
}
LIGHT = {
    "bg": "#F3F6FC", "sidebar": "#E9EEF7", "panel": "#FFFFFF", "panel2": "#EDF2FA",
    "line": "#D7E0EF", "text": "#152238", "muted": "#63748D", "accent": "#087B5C",
    "accent_hover": "#06664C", "blue": "#245BD5", "warning": "#8A5A00", "danger": "#B42335",
    "white": "#FFFFFF", "input": "#F7F9FD"
}

I18N = {
    "en": {
        "overview":"Overview", "scan":"Local scan", "activity":"Activity", "settings":"Settings",
        "beta":"BETA 0.3", "welcome":"Your PC. More visible. More understandable.",
        "subtitle":"A Windows security companion with Microsoft Defender status and an early local file-review engine.",
        "defender":"MICROSOFT DEFENDER", "refresh":"Refresh status", "enabled":"Enabled", "disabled":"Disabled",
        "unknown":"Unknown / unavailable", "antivirus":"Antivirus", "realtime":"Real-time protection",
        "service":"Defender service", "updated":"Signatures updated", "quick":"Quick scan", "full":"Full scan",
        "open_security":"Open Windows Security", "scan_title":"Check a folder yourself", "scan_text":"PACE checks selected files for a small set of known test strings and suspicious patterns. Findings are clues—not proof of malware.",
        "choose_folder":"Choose folder to review", "scanning":"Reviewing files…", "last_scan":"LATEST RESULT", "no_scan":"No local review has run yet.",
        "disclaimer_title":"Important: early detection engine", "disclaimer":"This basic engine is experimental and can miss malware or flag harmless files. It does not replace Microsoft Defender and never deletes or quarantines files.",
        "scan_intro":"Choose a folder you want PACE to review. Avoid scanning the whole Windows drive in this early beta.",
        "results":"Review results", "files_checked":"Files checked", "flagged":"Needs review", "clean":"No rule matched", "scan_stopped":"Stopped by user",
        "rule":"Reason", "file":"File", "risk":"Review level", "high":"High review priority", "medium":"Review", "info":"Information",
        "no_findings":"No rules matched in this folder. This does not prove the folder is malware-free.", "activity_empty":"No activity yet.",
        "clear_log":"Clear activity", "language":"Language", "appearance":"Appearance", "dark":"Dark", "light":"Light",
        "about":"About PACE", "about_text":"PACE 0.3 Beta · Windows Security + basic local heuristic review",
        "no_upload":"Local folder analysis stays on this PC. PACE does not upload files or scan results.", "cancel_scan":"Stop review", "run_defender":"Run Microsoft Defender", "scan_started":"Microsoft Defender scan was requested. Windows performs the actual scan; this does not confirm completion.",
        "pick_first":"Choose a folder first.", "working":"Working", "ready":"Ready", "error":"Could not complete the operation.", "note":"A suspicious result is not the same as a confirmed virus.",
        "task_manager":"PACE remains a normal user-controlled app. You can close it from Windows at any time.",
        "scan_done":"Local review finished.", "checking":"Checking…", "privacy":"Privacy", "path":"Folder", "stopped":"Stop requested; finishing the current file…"
    },
    "tr": {
        "overview":"Genel Bakış", "scan":"Yerel Tarama", "activity":"Etkinlik", "settings":"Ayarlar",
        "beta":"BETA 0.3", "welcome":"Bilgisayarın. Daha görünür. Daha anlaşılır.",
        "subtitle":"Microsoft Defender durumunu ve temel yerel dosya inceleme motorunu bir araya getiren Windows güvenlik yardımcısı.",
        "defender":"MICROSOFT DEFENDER", "refresh":"Durumu yenile", "enabled":"Etkin", "disabled":"Devre dışı",
        "unknown":"Bilinmiyor / kullanılamıyor", "antivirus":"Antivirüs", "realtime":"Gerçek zamanlı koruma",
        "service":"Defender hizmeti", "updated":"İmza güncellemesi", "quick":"Hızlı tarama", "full":"Tam tarama",
        "open_security":"Windows Güvenliği'ni aç", "scan_title":"Klasörü kendin incele", "scan_text":"PACE seçili dosyalarda bazı bilinen test metinlerini ve şüpheli örüntüleri arar. Bulgular ipucudur; zararlı yazılım kanıtı değildir.",
        "choose_folder":"İncelenecek klasörü seç", "scanning":"Dosyalar inceleniyor…", "last_scan":"SONUÇ", "no_scan":"Henüz yerel inceleme yapılmadı.",
        "disclaimer_title":"Önemli: erken aşama tespit motoru", "disclaimer":"Bu temel motor deneyseldir; zararlıları kaçırabilir veya zararsız dosyaları işaretleyebilir. Microsoft Defender'ın yerine geçmez; dosyaları asla otomatik silmez veya karantinaya almaz.",
        "scan_intro":"PACE'nin incelemesini istediğin klasörü seç. Bu erken beta sürümünde tüm Windows diskini taramaktan kaçın.",
        "results":"İnceleme sonuçları", "files_checked":"Kontrol edilen dosya", "flagged":"İncelenmeli", "clean":"Kural eşleşmedi", "scan_stopped":"Kullanıcı durdurdu",
        "rule":"Neden", "file":"Dosya", "risk":"İnceleme düzeyi", "high":"Öncelikli inceleme", "medium":"İncele", "info":"Bilgi",
        "no_findings":"Bu klasörde kurallarla eşleşen bulgu yok. Bu, klasörün kesinlikle temiz olduğunu kanıtlamaz.", "activity_empty":"Henüz etkinlik yok.",
        "clear_log":"Etkinliği temizle", "language":"Dil", "appearance":"Görünüm", "dark":"Koyu", "light":"Açık",
        "about":"PACE hakkında", "about_text":"PACE 0.3 Beta · Windows Güvenliği + temel yerel örüntü incelemesi",
        "no_upload":"Yerel klasör incelemesi bu bilgisayarda kalır. PACE dosyaları veya tarama sonuçlarını internete yüklemez.", "cancel_scan":"İncelemeyi durdur", "run_defender":"Microsoft Defender'ı çalıştır", "scan_started":"Microsoft Defender taraması istendi. Gerçek taramayı Windows yapar; bu mesaj taramanın bittiğini doğrulamaz.",
        "pick_first":"Önce bir klasör seç.", "working":"Çalışıyor", "ready":"Hazır", "error":"İşlem tamamlanamadı.", "note":"Şüpheli bulgu, doğrulanmış virüs demek değildir.",
        "task_manager":"PACE kullanıcı kontrolünde kalan normal bir uygulamadır. İstediğinde Windows'tan kapatabilirsin.",
        "scan_done":"Yerel inceleme tamamlandı.", "checking":"Kontrol ediliyor…", "privacy":"Gizlilik", "path":"Klasör", "stopped":"Durdurma istendi; geçerli dosya tamamlanıyor…"
    }
}

# These patterns are deliberately conservative. A hit asks for human/Defender review; it never means "infected".
EXECUTABLE_EXTS = {".exe", ".dll", ".scr", ".com", ".msi", ".sys"}
SCRIPT_EXTS = {".ps1", ".bat", ".cmd", ".vbs", ".vbe", ".js", ".jse", ".hta", ".wsf", ".reg"}
DOUBLE_EXT_RE = re.compile(r"\.(pdf|docx?|xlsx?|pptx?|jpe?g|png|gif|txt|rtf)\.(exe|scr|com|bat|cmd|js|vbs|hta)$", re.I)
RULES = [
    ("HIGH", "Encoded PowerShell + download/execute pattern", re.compile(r"(?is)(-encodedcommand|-enc\s+[A-Za-z0-9+/=]{20,}).{0,120}(downloadstring|invoke-expression|\biex\b)|(?:downloadstring|invoke-expression|\biex\b).{0,120}(-encodedcommand|-enc\s+)") ),
    ("HIGH", "Script combines remote download and execution pattern", re.compile(r"(?is)(downloadstring|invoke-webrequest|start-bitstransfer).{0,300}(invoke-expression|\biex\b|start-process)|(invoke-expression|\biex\b).{0,300}(downloadstring|invoke-webrequest|start-bitstransfer)")),
    ("MEDIUM", "Script contains Base64 decoding and execution keywords", re.compile(r"(?is)(frombase64string|certutil\s+-decode).{0,250}(invoke-expression|\biex\b|start-process|wscript\.shell)")),
]


def read_json(path: Path, default):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data
    except (OSError, ValueError):
        return default


def write_json(path: Path, data) -> None:
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def powershell_json(script: str, timeout: int = 25) -> dict:
    if not IS_WINDOWS:
        raise RuntimeError("Windows only")
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "RemoteSigned", "-Command", script],
        capture_output=True, text=True, timeout=timeout,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), check=False
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "PowerShell request failed").strip())
    data = json.loads(result.stdout.strip())
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected response from Windows security query")
    return data


def defender_status() -> dict:
    return powershell_json(
        "$ErrorActionPreference='Stop'; $s=Get-MpComputerStatus; "
        "[pscustomobject]@{AntivirusEnabled=$s.AntivirusEnabled; "
        "RealTimeProtectionEnabled=$s.RealTimeProtectionEnabled; AMServiceEnabled=$s.AMServiceEnabled; "
        "AMRunningMode=$s.AMRunningMode; SignatureUpdated=if($s.AntivirusSignatureLastUpdated){$s.AntivirusSignatureLastUpdated.ToString('yyyy-MM-dd HH:mm')}else{''}} | ConvertTo-Json -Compress"
    )


def request_defender_scan(scan_type: str) -> None:
    if not IS_WINDOWS or scan_type not in {"QuickScan", "FullScan"}:
        raise RuntimeError("This scan requires Windows and Microsoft Defender.")
    params = f'-NoProfile -ExecutionPolicy RemoteSigned -Command "Start-MpScan -ScanType {scan_type}"'
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", params, None, 1)
    if result <= 32:
        raise OSError(f"Windows could not start the Defender scan (code {result}).")


def open_windows_security() -> None:
    if not IS_WINDOWS:
        raise RuntimeError("Windows only")
    os.startfile("windowsdefender:")  # noqa: S606 - opens the Windows Security URI, no user-supplied command.


def inspect_one_file(path: Path, calculate_hash: bool = True) -> dict | None:
    findings: list[tuple[str, str]] = []
    suffix = path.suffix.lower()
    name_lower = path.name.lower()
    try:
        stat = path.stat()
        if not path.is_file():
            return None
        # Deceptive double extensions are not proof of malware, but merit a look.
        if DOUBLE_EXT_RE.search(name_lower):
            findings.append(("MEDIUM", "Document/image-like double extension ending in executable or script"))
        # Unexpected executables inside temporary folders are only a review signal.
        lowered = str(path).lower().replace("/", "\\")
        temp_root = os.environ.get("TEMP", "").lower().replace("/", "\\")
        local_temp = os.path.join(os.environ.get("LOCALAPPDATA", ""), "temp").lower().replace("/", "\\")
        if suffix in EXECUTABLE_EXTS and ((temp_root and lowered.startswith(temp_root + "\\")) or (local_temp and lowered.startswith(local_temp + "\\"))):
            findings.append(("MEDIUM", "Executable file stored in a temporary folder"))

        if stat.st_size <= MAX_SCRIPT_BYTES:
            try:
                raw_content = path.read_bytes()
            except OSError:
                raw_content = b""
            if b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" in raw_content:
                findings.append(("HIGH", "EICAR harmless antivirus test signature (not a real virus)"))
            if suffix in SCRIPT_EXTS:
                content = raw_content.decode("utf-8", errors="ignore")
                for level, reason, pattern in RULES:
                    if pattern.search(content):
                        findings.append((level, reason))

        digest = "not calculated (size or scan-budget limit)"
        # Hash only flagged items, not every file. This keeps ordinary directory
        # reviews much faster and avoids claiming the hash itself proves malware.
        if findings and calculate_hash and stat.st_size <= MAX_HASH_BYTES:
            h = hashlib.sha256()
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            digest = h.hexdigest()
        if findings:
            # preserve unique reason strings and highest severity
            unique = list(dict.fromkeys(findings))
            rank = {"HIGH": 0, "MEDIUM": 1, "INFO": 2}
            unique.sort(key=lambda item: rank.get(item[0], 9))
            return {"path": str(path), "name": path.name, "level": unique[0][0], "reason": "; ".join(reason for _, reason in unique), "sha256": digest, "size": stat.st_size}
    except (OSError, PermissionError):
        return None
    return None


def scan_folder(root: Path, cancel: threading.Event, progress_callback) -> dict:
    findings = []
    checked = 0
    errors = 0
    bytes_hashed = 0
    stopped = False
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d.lower() not in {".git", "node_modules", "__pycache__", ".venv", "venv"}]
        if cancel.is_set():
            stopped = True
            break
        for filename in files:
            if cancel.is_set():
                stopped = True
                break
            path = Path(current) / filename
            try:
                checked += 1
                size = path.stat().st_size
                hash_budget_available = size <= MAX_HASH_BYTES and (bytes_hashed + size) <= MAX_TOTAL_HASH_BYTES
                found = inspect_one_file(path, calculate_hash=hash_budget_available)
                if found:
                    findings.append(found)
                    if hash_budget_available:
                        bytes_hashed += size
            except Exception:
                errors += 1
            if checked % 25 == 0:
                progress_callback(checked, len(findings), str(path))
            if checked >= MAX_FILES:
                stopped = True
                break
        if stopped:
            break
    return {"root": str(root), "checked": checked, "findings": findings, "errors": errors, "stopped": stopped, "limit": MAX_FILES}


class PaceApp(ctk.CTk):
    def __init__(self):
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.prefs = read_json(PREFS_PATH, {"theme": "dark", "language": "en"})
        if not isinstance(self.prefs, dict): self.prefs = {"theme": "dark", "language": "en"}
        self.language = self.prefs.get("language", "en") if self.prefs.get("language") in I18N else "en"
        self.theme = self.prefs.get("theme", "dark") if self.prefs.get("theme") in {"dark", "light"} else "dark"
        self.logs = read_json(LOG_PATH, [])
        if not isinstance(self.logs, list): self.logs = []
        self.status_data = None
        self.current_page = "overview"
        self.scan_thread = None
        self.cancel_event = threading.Event()
        self.last_result = None
        self.active_folder = ""
        self.colors = LIGHT if self.theme == "light" else COLORS
        ctk.set_appearance_mode(self.theme)
        self.title("PACE · Windows Security")
        self.geometry("1210x820")
        self.minsize(980, 680)
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
        self.content.grid(row=1, column=0, sticky="nsew", padx=28, pady=(6, 26))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        self._render_page("overview")
        self.after(500, self.refresh_status)

    def t(self, key: str) -> str:
        return I18N[self.language].get(key, I18N["en"].get(key, key))

    def _build_sidebar(self):
        c = self.colors
        self.sidebar = ctk.CTkFrame(self, width=228, corner_radius=0, fg_color=c["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=22, pady=(25, 34))
        ctk.CTkLabel(brand, text="◈", text_color=c["accent"], font=ctk.CTkFont(family="Segoe UI Variable", size=34, weight="bold")).pack(side="left", padx=(0, 10))
        namebox = ctk.CTkFrame(brand, fg_color="transparent")
        namebox.pack(side="left", anchor="center")
        ctk.CTkLabel(namebox, text="PACE", text_color=c["text"], font=ctk.CTkFont(family="Segoe UI Variable", size=25, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(namebox, text="PC SECURITY", text_color=c["muted"], font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w")
        self.nav = {}
        for key in ("overview", "scan", "activity", "settings"):
            b = ctk.CTkButton(self.sidebar, text=self.t(key), anchor="w", height=44, corner_radius=10,
                fg_color="transparent", hover_color=c["panel2"], text_color=c["text"],
                font=ctk.CTkFont(size=13, weight="bold"), command=lambda page=key:self._render_page(page))
            b.pack(fill="x", padx=13, pady=4)
            self.nav[key] = b
        foot = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        foot.pack(side="bottom", fill="x", padx=20, pady=21)
        self.side_status = ctk.CTkLabel(foot, text="●  " + self.t("ready"), text_color=c["accent"], anchor="w", font=ctk.CTkFont(size=11, weight="bold"))
        self.side_status.pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(foot, text="PACE 0.3 BETA", text_color=c["muted"], anchor="w", font=ctk.CTkFont(size=10)).pack(anchor="w")

    def _build_header(self):
        c = self.colors
        self.header = ctk.CTkFrame(self.main, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=30, pady=(24, 8))
        self.header.grid_columnconfigure(0, weight=1)
        self.header_title = ctk.CTkLabel(self.header, text="", font=ctk.CTkFont(family="Segoe UI Variable", size=26, weight="bold"), text_color=c["text"])
        self.header_title.grid(row=0, column=0, sticky="w")
        self.header_sub = ctk.CTkLabel(self.header, text="", font=ctk.CTkFont(size=12), text_color=c["muted"])
        self.header_sub.grid(row=1, column=0, sticky="w", pady=(3, 0))
        ctk.CTkLabel(self.header, text=self.t("beta"), width=96, height=32, fg_color=c["panel2"], corner_radius=8,
                     text_color=c["accent"], font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=1, rowspan=2, sticky="e", padx=(12, 0))

    def _card(self, parent, **kwargs):
        return ctk.CTkFrame(parent, fg_color=self.colors["panel"], corner_radius=16, border_width=1,
                            border_color=self.colors["line"], **kwargs)

    def _label(self, parent, text, size=12, color=None, bold=False, **kwargs):
        return ctk.CTkLabel(parent, text=text, text_color=color or self.colors["text"],
                            font=ctk.CTkFont(family="Segoe UI Variable", size=size, weight="bold" if bold else "normal"),
                            justify="left", anchor="w", **kwargs)

    def _button(self, parent, text, command, primary=False, **kwargs):
        c = self.colors
        return ctk.CTkButton(parent, text=text, command=command, height=40, corner_radius=10,
            fg_color=c["accent"] if primary else c["panel2"],
            hover_color=c["accent_hover"] if primary else c["line"],
            text_color="#061811" if primary else c["text"], font=ctk.CTkFont(size=12, weight="bold"), **kwargs)

    def _render_page(self, page: str):
        self.current_page = page
        for key, button in self.nav.items():
            button.configure(fg_color=self.colors["panel2"] if key == page else "transparent")
        for child in self.content.winfo_children(): child.destroy()
        titles = {"overview": self.t("overview"), "scan": self.t("scan"), "activity": self.t("activity"), "settings": self.t("settings")}
        subtitles = {"overview": self.t("welcome"), "scan": self.t("scan_intro"), "activity": self.t("no_upload"), "settings": self.t("task_manager")}
        self.header_title.configure(text=titles[page]); self.header_sub.configure(text=subtitles[page])
        if page == "overview": self._page_overview()
        elif page == "scan": self._page_scan()
        elif page == "activity": self._page_activity()
        else: self._page_settings()

    def _page_overview(self):
        c = self.colors
        self._label(self.content, self.t("subtitle"), 13, c["muted"], wraplength=880).grid(row=0, column=0, sticky="w", pady=(0, 18))
        card = self._card(self.content); card.grid(row=1, column=0, sticky="ew", pady=(0, 14)); card.grid_columnconfigure(0, weight=1)
        top = ctk.CTkFrame(card, fg_color="transparent"); top.pack(fill="x", padx=20, pady=(18, 8))
        self._label(top, self.t("defender"), 11, c["muted"], True).pack(side="left")
        self._button(top, "↻  " + self.t("refresh"), self.refresh_status).pack(side="right")
        self.defender_title = self._label(card, self.t("checking"), 22, c["text"], True)
        self.defender_title.pack(anchor="w", padx=20, pady=(2, 4))
        self.defender_description = self._label(card, self.t("unknown"), 12, c["muted"])
        self.defender_description.pack(anchor="w", padx=20, pady=(0, 16))
        grid = ctk.CTkFrame(card, fg_color="transparent"); grid.pack(fill="x", padx=15, pady=(0, 18))
        keys = [("AntivirusEnabled", "antivirus"), ("RealTimeProtectionEnabled", "realtime"), ("AMServiceEnabled", "service"), ("SignatureUpdated", "updated")]
        self.status_tiles = {}
        for i, (field, label) in enumerate(keys):
            tile = ctk.CTkFrame(grid, fg_color=c["panel2"], corner_radius=11)
            tile.grid(row=0, column=i, padx=5, sticky="nsew")
            grid.grid_columnconfigure(i, weight=1, uniform="status")
            self._label(tile, self.t(label), 10, c["muted"], wraplength=140).pack(anchor="w", padx=12, pady=(12, 4))
            value = self._label(tile, self.t("unknown"), 12, c["text"], True, wraplength=150)
            value.pack(anchor="w", padx=12, pady=(0, 12)); self.status_tiles[field] = value
        actions = ctk.CTkFrame(self.content, fg_color="transparent"); actions.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        actions.grid_columnconfigure((0, 1), weight=1, uniform="action")
        left = self._card(actions); left.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        self._label(left, self.t("scan_title"), 16, c["text"], True).pack(anchor="w", padx=18, pady=(16, 7))
        self._label(left, self.t("scan_text"), 11, c["muted"], wraplength=450).pack(anchor="w", padx=18, pady=(0, 12))
        row = ctk.CTkFrame(left, fg_color="transparent"); row.pack(anchor="w", padx=18, pady=(0, 16))
        self._button(row, self.t("choose_folder"), lambda:self._render_page("scan"), primary=True).pack(side="left", padx=(0, 8))
        self._button(row, self.t("open_security"), self._open_security).pack(side="left")
        right = self._card(actions); right.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        self._label(right, self.t("run_defender"), 16, c["text"], True).pack(anchor="w", padx=18, pady=(16, 7))
        self._label(right, self.t("scan_started"), 11, c["muted"], wraplength=430).pack(anchor="w", padx=18, pady=(0, 12))
        row2 = ctk.CTkFrame(right, fg_color="transparent"); row2.pack(anchor="w", padx=18, pady=(0, 16))
        self._button(row2, self.t("quick"), lambda:self._request_scan("QuickScan"), primary=True).pack(side="left", padx=(0, 8))
        self._button(row2, self.t("full"), lambda:self._request_scan("FullScan")).pack(side="left")
        notice = ctk.CTkFrame(self.content, fg_color=c["panel2"], corner_radius=12)
        notice.grid(row=3, column=0, sticky="ew")
        self._label(notice, "ⓘ  " + self.t("disclaimer_title"), 12, c["warning"], True).pack(anchor="w", padx=16, pady=(12, 4))
        self._label(notice, self.t("disclaimer"), 11, c["muted"], wraplength=950).pack(anchor="w", padx=16, pady=(0, 12))
        self._apply_status()

    def _apply_status(self):
        if not hasattr(self, "status_tiles"): return
        c = self.colors
        data = self.status_data or {}
        core = [data.get("AntivirusEnabled"), data.get("RealTimeProtectionEnabled")]
        if all(v is True for v in core):
            self.defender_title.configure(text=self.t("enabled"), text_color=c["accent"])
            self.defender_description.configure(text="Microsoft Defender reports that antivirus and real-time protection are enabled.")
        elif any(v is False for v in core):
            self.defender_title.configure(text=self.t("disabled"), text_color=c["danger"])
            self.defender_description.configure(text="Microsoft Defender reports that a protection setting is disabled. Review Windows Security.")
        else:
            self.defender_title.configure(text=self.t("unknown"), text_color=c["warning"])
            self.defender_description.configure(text="PACE could not confirm the protection state. Check Windows Security directly.")
        for key in ("AntivirusEnabled", "RealTimeProtectionEnabled", "AMServiceEnabled"):
            value = data.get(key)
            text = self.t("enabled") if value is True else self.t("disabled") if value is False else self.t("unknown")
            color = c["accent"] if value is True else c["danger"] if value is False else c["muted"]
            self.status_tiles[key].configure(text=text, text_color=color)
        self.status_tiles["SignatureUpdated"].configure(text=data.get("SignatureUpdated") or self.t("unknown"), text_color=c["text"])

    def refresh_status(self):
        if not IS_WINDOWS:
            messagebox.showinfo(APP_NAME, "This status check requires Windows."); return
        self.side_status.configure(text="●  " + self.t("checking"))
        threading.Thread(target=self._status_worker, daemon=True).start()

    def _status_worker(self):
        try: data = defender_status(); error = None
        except Exception as exc: data, error = None, str(exc)
        self.after(0, lambda:self._status_done(data, error))

    def _status_done(self, data, error):
        self.status_data = data
        self.side_status.configure(text="●  " + self.t("ready"))
        if data:
            self._add_log("Defender status", "Read selected local status fields")
        else:
            self._add_log("Defender status", "Unavailable: " + (error or "unknown error")[:160])
        if self.current_page == "overview": self._apply_status()

    def _request_scan(self, kind):
        if not IS_WINDOWS:
            messagebox.showinfo(APP_NAME, "This feature requires Windows and Microsoft Defender."); return
        friendly = self.t("quick") if kind == "QuickScan" else self.t("full")
        if not messagebox.askyesno(APP_NAME, f"{friendly}\n\nWindows may request administrator permission. PACE will not delete files."):
            return
        try:
            request_defender_scan(kind)
            self._add_log(friendly, "Request sent to Microsoft Defender; completion not verified")
            messagebox.showinfo(APP_NAME, self.t("scan_started"))
        except Exception as exc:
            messagebox.showerror(APP_NAME, f"{self.t('error')}\n\n{exc}")

    def _open_security(self):
        try:
            open_windows_security()
            self._add_log("Open Windows Security", "Opened the Windows Security URI")
        except Exception as exc:
            messagebox.showerror(APP_NAME, str(exc))

    def _page_scan(self):
        c = self.colors
        card = self._card(self.content); card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self._label(card, self.t("scan_title"), 18, c["text"], True).pack(anchor="w", padx=20, pady=(18, 6))
        self._label(card, self.t("scan_intro"), 12, c["muted"], wraplength=900).pack(anchor="w", padx=20, pady=(0, 16))
        row = ctk.CTkFrame(card, fg_color="transparent"); row.pack(fill="x", padx=20, pady=(0, 10))
        self.folder_label = self._label(row, self.active_folder or "No folder selected", 11, c["muted"], wraplength=650)
        self.folder_label.pack(side="left", fill="x", expand=True)
        self._button(row, self.t("choose_folder"), self._choose_folder, primary=True).pack(side="right", padx=(10, 0))
        self.progress = ctk.CTkProgressBar(card, height=7, corner_radius=5, progress_color=c["accent"], fg_color=c["panel2"])
        self.progress.pack(fill="x", padx=20, pady=(6, 10)); self.progress.set(0)
        buttons = ctk.CTkFrame(card, fg_color="transparent"); buttons.pack(anchor="w", padx=20, pady=(0, 18))
        self.run_local_btn = self._button(buttons, "▶  " + self.t("choose_folder"), self._choose_and_scan, primary=True)
        self.run_local_btn.pack(side="left", padx=(0, 8))
        self.cancel_btn = self._button(buttons, self.t("cancel_scan"), self._cancel_scan, state="disabled")
        self.cancel_btn.pack(side="left")
        self.scan_status = self._label(card, self.t("no_scan"), 11, c["muted"], wraplength=900)
        self.scan_status.pack(anchor="w", padx=20, pady=(0, 17))
        results = self._card(self.content); results.grid(row=1, column=0, sticky="nsew")
        self._label(results, self.t("results"), 15, c["text"], True).pack(anchor="w", padx=18, pady=(16, 4))
        self.results_summary = self._label(results, self.t("no_findings"), 11, c["muted"], wraplength=900)
        self.results_summary.pack(anchor="w", padx=18, pady=(0, 10))
        self.results_list = ctk.CTkScrollableFrame(results, fg_color="transparent", height=240)
        self.results_list.pack(fill="both", expand=True, padx=10, pady=(0, 12))
        self._populate_results(self.last_result)

    def _choose_folder(self):
        folder = filedialog.askdirectory(title="Choose a folder to review")
        if folder:
            self.active_folder = folder
            if hasattr(self, "folder_label"): self.folder_label.configure(text=folder)

    def _choose_and_scan(self):
        if not self.active_folder: self._choose_folder()
        if not self.active_folder:
            messagebox.showinfo(APP_NAME, self.t("pick_first")); return
        if self.scan_thread and self.scan_thread.is_alive(): return
        root = Path(self.active_folder)
        if not root.is_dir():
            messagebox.showerror(APP_NAME, "The selected folder is unavailable."); return
        self.cancel_event.clear()
        self.progress.set(0)
        self.scan_status.configure(text=self.t("scanning"))
        self.run_local_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.scan_thread = threading.Thread(target=self._local_scan_worker, args=(root,), daemon=True)
        self.scan_thread.start()

    def _local_scan_worker(self, root: Path):
        try:
            result = scan_folder(root, self.cancel_event, lambda checked, flagged, path:self.after(0, lambda:self._progress_update(checked, flagged, path)))
            self.after(0, lambda:self._local_scan_done(result, None))
        except Exception as exc:
            self.after(0, lambda e=str(exc):self._local_scan_done(None, e))

    def _progress_update(self, checked: int, flagged: int, path: str):
        if not hasattr(self, "scan_status"): return
        self.scan_status.configure(text=f"{self.t('scanning')}  ·  {checked:,}  ·  {self.t('flagged')}: {flagged}\n{path}")
        self.progress.set(min(checked / MAX_FILES, 0.98))

    def _local_scan_done(self, result, error):
        # The user may navigate away while the worker thread is scanning. Do not
        # touch widgets that belonged to the old page after they were destroyed.
        if self.current_page != "scan":
            if result:
                self.last_result = result
                self._add_log("Local folder review", f"Checked {result['checked']} files; {len(result['findings'])} item(s) need review; root={result['root']}")
            elif error:
                self._add_log("Local folder review", "Failed: " + error[:200])
            return
        self.run_local_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        if error or not result:
            self.scan_status.configure(text=f"{self.t('error')} {error or ''}")
            return
        self.last_result = result
        self.progress.set(1 if not result["stopped"] else 0.99)
        summary = f"{self.t('files_checked')}: {result['checked']:,}  ·  {self.t('flagged')}: {len(result['findings'])}  ·  {self.t('path')}: {result['root']}"
        if result["stopped"]: summary += f"\n{self.t('scan_stopped')} (maximum {MAX_FILES:,} files or user stop)."
        self.scan_status.configure(text=self.t("scan_done") + "\n" + summary)
        self.results_summary.configure(text=summary if result["findings"] else self.t("no_findings"))
        self._populate_results(result)
        self._add_log("Local folder review", f"Checked {result['checked']} files; {len(result['findings'])} item(s) need review; root={result['root']}")

    def _cancel_scan(self):
        self.cancel_event.set()
        self.scan_status.configure(text=self.t("stopped"))
        self.cancel_btn.configure(state="disabled")

    def _populate_results(self, result):
        if not hasattr(self, "results_list"): return
        for child in self.results_list.winfo_children(): child.destroy()
        if not result or not result.get("findings"):
            self._label(self.results_list, self.t("no_findings"), 11, self.colors["muted"], wraplength=820).pack(anchor="w", padx=8, pady=8)
            return
        for item in result["findings"]:
            card = ctk.CTkFrame(self.results_list, fg_color=self.colors["panel2"], corner_radius=10)
            card.pack(fill="x", padx=4, pady=5)
            color = self.colors["danger"] if item["level"] == "HIGH" else self.colors["warning"]
            head = ctk.CTkFrame(card, fg_color="transparent"); head.pack(fill="x", padx=12, pady=(10, 2))
            self._label(head, item["name"], 12, self.colors["text"], True, wraplength=530).pack(side="left", fill="x", expand=True)
            self._label(head, item["level"], 10, color, True).pack(side="right", padx=(8, 0))
            self._label(card, item["reason"], 10, self.colors["muted"], wraplength=820).pack(anchor="w", padx=12, pady=(0, 5))
            self._label(card, f"SHA-256: {item['sha256']}  ·  {item['path']}", 9, self.colors["muted"], wraplength=820).pack(anchor="w", padx=12, pady=(0, 10))

    def _page_activity(self):
        c = self.colors
        card = self._card(self.content); card.grid(row=0, column=0, sticky="nsew")
        top = ctk.CTkFrame(card, fg_color="transparent"); top.pack(fill="x", padx=18, pady=(16, 10))
        self._label(top, self.t("no_upload"), 11, c["muted"], wraplength=650).pack(side="left", fill="x", expand=True)
        self._button(top, self.t("clear_log"), self._clear_log).pack(side="right", padx=(10, 0))
        listing = ctk.CTkScrollableFrame(card, fg_color="transparent")
        listing.pack(fill="both", expand=True, padx=10, pady=(0, 14))
        if not self.logs:
            self._label(listing, self.t("activity_empty"), 12, c["muted"]).pack(anchor="w", padx=10, pady=14)
        for item in self.logs[:100]:
            row = ctk.CTkFrame(listing, fg_color=c["panel2"], corner_radius=9); row.pack(fill="x", padx=4, pady=4)
            self._label(row, item.get("time", ""), 10, c["muted"]).pack(anchor="w", padx=12, pady=(9, 2))
            self._label(row, item.get("event", ""), 12, c["text"], True).pack(anchor="w", padx=12)
            self._label(row, item.get("result", ""), 10, c["muted"], wraplength=850).pack(anchor="w", padx=12, pady=(2, 9))

    def _page_settings(self):
        c = self.colors
        card = self._card(self.content); card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self._label(card, self.t("settings"), 18, c["text"], True).pack(anchor="w", padx=20, pady=(18, 16))
        self._label(card, self.t("appearance"), 12, c["muted"], True).pack(anchor="w", padx=20)
        row = ctk.CTkFrame(card, fg_color="transparent"); row.pack(anchor="w", padx=20, pady=(8, 18))
        self._button(row, "☾  " + self.t("dark"), lambda:self._change_theme("dark"), primary=self.theme == "dark").pack(side="left", padx=(0, 8))
        self._button(row, "☼  " + self.t("light"), lambda:self._change_theme("light"), primary=self.theme == "light").pack(side="left")
        self._label(card, self.t("language"), 12, c["muted"], True).pack(anchor="w", padx=20)
        row2 = ctk.CTkFrame(card, fg_color="transparent"); row2.pack(anchor="w", padx=20, pady=(8, 20))
        self._button(row2, "English", lambda:self._change_language("en"), primary=self.language == "en").pack(side="left", padx=(0, 8))
        self._button(row2, "Türkçe", lambda:self._change_language("tr"), primary=self.language == "tr").pack(side="left")
        card2 = self._card(self.content); card2.grid(row=1, column=0, sticky="ew")
        self._label(card2, self.t("about"), 15, c["text"], True).pack(anchor="w", padx=20, pady=(16, 6))
        self._label(card2, self.t("about_text"), 11, c["muted"]).pack(anchor="w", padx=20, pady=(0, 7))
        self._label(card2, self.t("disclaimer"), 11, c["muted"], wraplength=900).pack(anchor="w", padx=20, pady=(0, 16))

    def _change_theme(self, theme):
        self.theme = theme
        self.prefs.update({"theme": self.theme, "language": self.language})
        write_json(PREFS_PATH, self.prefs)
        self.colors = LIGHT if theme == "light" else COLORS
        ctk.set_appearance_mode(theme)
        # Rebuild the entire view using the selected palette.
        for child in self.winfo_children(): child.destroy()
        self.configure(fg_color=self.colors["bg"])
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self.main = ctk.CTkFrame(self, fg_color=self.colors["bg"], corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew"); self.main.grid_columnconfigure(0, weight=1); self.main.grid_rowconfigure(1, weight=1)
        self._build_header()
        self.content = ctk.CTkFrame(self.main, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=28, pady=(6, 26)); self.content.grid_columnconfigure(0, weight=1)
        self._render_page(self.current_page)

    def _change_language(self, lang):
        self.language = lang
        self.prefs.update({"theme": self.theme, "language": self.language})
        write_json(PREFS_PATH, self.prefs)
        self._change_theme(self.theme)

    def _add_log(self, event: str, result: str):
        self.logs.insert(0, {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": event[:100], "result": result[:600]})
        self.logs = self.logs[:100]
        write_json(LOG_PATH, self.logs)
        if self.current_page == "activity": self._render_page("activity")

    def _clear_log(self):
        if messagebox.askyesno(APP_NAME, self.t("clear_log") + "?"):
            self.logs = []; write_json(LOG_PATH, self.logs); self._render_page("activity")


if __name__ == "__main__":
    try:
        app = PaceApp()
        app.mainloop()
    except Exception as exc:
        try: messagebox.showerror("PACE", f"PACE could not start.\n\n{exc}")
        except Exception: print(exc, file=sys.stderr)
