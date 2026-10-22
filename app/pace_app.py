from __future__ import annotations

import ctypes
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

APP_NAME = "PACE Anti-Cheat"
APP_VERSION = "0.2 Beta"
IS_WINDOWS = sys.platform == "win32"

TEXT = {
    "en": {
        "dashboard":"Overview", "security":"Security", "activity":"Activity log", "settings":"Settings",
        "beta":"BETA 0.2", "headline":"Your PC security, at a glance.",
        "subhead":"PACE checks Microsoft Defender status and requests scans. It is a companion interface, not a standalone antivirus engine.",
        "defender":"MICROSOFT DEFENDER STATUS", "checking":"Checking…", "refresh":"Refresh status",
        "antivirus":"Antivirus", "realtime":"Real-time protection", "engine":"Defender service", "updated":"Security intelligence updated",
        "yes":"Enabled", "no":"Disabled", "unknown":"Unavailable / unknown", "notchecked":"Not checked yet",
        "scan_title":"Scan this PC", "scan_text":"These buttons request a scan from Microsoft Defender. The actual scan is performed by Windows Security.",
        "quick":"Quick scan", "full":"Full scan", "open_security":"Open Windows Security", "last_action":"LAST ACTION", "no_action":"No scan requested in this session.",
        "notice_title":"Important beta limitation", "notice":"Advanced threat detection is not available. PACE does not have its own malware-detection engine. Use Microsoft Defender or another trusted antivirus for protection.",
        "status_ok":"Status retrieved from Microsoft Defender.", "status_fail":"Could not read Microsoft Defender status. It may be unavailable, disabled, or managed by another security product.",
        "scan_confirm":"Request a {kind} using Microsoft Defender? Windows may ask for administrator approval. PACE will not delete files automatically.",
        "scan_sent":"{kind} request sent to Microsoft Defender at {time}. This confirms only that PACE submitted the request—not that the scan finished.",
        "scan_cancel":"Scan request was not started.", "scan_error":"Could not start the scan. Run PACE on Windows and check that Microsoft Defender is available.",
        "quick_name":"Quick scan", "full_name":"Full scan", "settings_title":"Application settings", "appearance":"Appearance", "dark":"Dark", "light":"Light",
        "language":"Language", "privacy_title":"Privacy by design", "privacy":"PACE does not upload scan data. It reads selected local Defender status fields and stores basic action timestamps locally.",
        "about_title":"About PACE", "about_text":"PACE Anti-Cheat · Windows Security Companion · 0.2 Beta", "about_note":"The product name is retained, but this beta focuses on PC malware checks—not detecting players cheating inside a game.",
        "clear":"Clear log", "log_empty":"No activity yet.", "time":"Time", "event":"Event", "result":"Result", "settings_saved":"Settings saved on this PC.", "requires_windows":"This feature requires Windows and Microsoft Defender PowerShell commands.",
        "working":"Checking local Defender status…", "scan_launching":"Requesting scan…", "ready":"Ready", "status_unknown":"Unknown", "help":"Help & limitations"
    },
    "tr": {
        "dashboard":"Genel Bakış", "security":"Güvenlik", "activity":"Etkinlik kaydı", "settings":"Ayarlar",
        "beta":"BETA 0.2", "headline":"Bilgisayarının güvenliği bir bakışta.",
        "subhead":"PACE, Microsoft Defender durumunu kontrol eder ve tarama isteği gönderir. Tek başına antivirüs motoru değil, yardımcı bir arayüzdür.",
        "defender":"MICROSOFT DEFENDER DURUMU", "checking":"Kontrol ediliyor…", "refresh":"Durumu yenile",
        "antivirus":"Antivirüs", "realtime":"Gerçek zamanlı koruma", "engine":"Defender hizmeti", "updated":"Güvenlik bilgileri güncellemesi",
        "yes":"Etkin", "no":"Devre dışı", "unknown":"Kullanılamıyor / bilinmiyor", "notchecked":"Henüz kontrol edilmedi",
        "scan_title":"Bu bilgisayarı tara", "scan_text":"Bu düğmeler Microsoft Defender üzerinden tarama isteği gönderir. Gerçek taramayı Windows Güvenliği yapar.",
        "quick":"Hızlı tarama", "full":"Tam tarama", "open_security":"Windows Güvenliği'ni aç", "last_action":"SON İŞLEM", "no_action":"Bu oturumda tarama istenmedi.",
        "notice_title":"Önemli beta sınırlaması", "notice":"Gelişmiş tehdit tespiti kullanılamıyor. PACE kendine ait bir zararlı yazılım tespit motoru içermez. Koruma için Microsoft Defender veya başka güvenilir bir antivirüs kullan.",
        "status_ok":"Durum Microsoft Defender'dan alındı.", "status_fail":"Microsoft Defender durumu okunamadı. Kullanılamıyor, devre dışı veya başka bir güvenlik yazılımı tarafından yönetiliyor olabilir.",
        "scan_confirm":"Microsoft Defender ile {kind} başlatma isteği gönderilsin mi? Windows yönetici izni isteyebilir. PACE dosyaları otomatik olarak silmez.",
        "scan_sent":"{time} saatinde Microsoft Defender'a {kind} isteği gönderildi. Bu yalnızca isteğin gönderildiğini doğrular; taramanın bittiğini göstermez.",
        "scan_cancel":"Tarama isteği başlatılmadı.", "scan_error":"Tarama başlatılamadı. PACE'ı Windows'ta çalıştırdığından ve Microsoft Defender'ın kullanılabilir olduğundan emin ol.",
        "quick_name":"Hızlı tarama", "full_name":"Tam tarama", "settings_title":"Uygulama ayarları", "appearance":"Görünüm", "dark":"Koyu", "light":"Açık",
        "language":"Dil", "privacy_title":"Gizlilik tasarımı", "privacy":"PACE tarama verilerini yüklemez. Yerel Defender durumunun belirli alanlarını okur ve temel işlem zamanlarını bu bilgisayarda saklar.",
        "about_title":"PACE hakkında", "about_text":"PACE Anti-Cheat · Windows Güvenlik Yardımcısı · 0.2 Beta", "about_note":"Ürün adı korunmuştur; bu beta oyundaki hilecileri değil, bilgisayara yönelik zararlı yazılım kontrollerini hedefler.",
        "clear":"Kaydı temizle", "log_empty":"Henüz etkinlik yok.", "time":"Zaman", "event":"İşlem", "result":"Sonuç", "settings_saved":"Ayarlar bu bilgisayara kaydedildi.", "requires_windows":"Bu özellik Windows ve Microsoft Defender PowerShell komutları gerektirir.",
        "working":"Yerel Defender durumu kontrol ediliyor…", "scan_launching":"Tarama isteği gönderiliyor…", "ready":"Hazır", "status_unknown":"Bilinmiyor", "help":"Yardım ve sınırlamalar"
    }
}

APP_DIR = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "PACE"
APP_DIR.mkdir(parents=True, exist_ok=True)
PREFS_PATH = APP_DIR / "settings.json"
LOG_PATH = APP_DIR / "activity.json"


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


def defender_status() -> dict:
    """Read selected local Microsoft Defender fields; never treats errors as a clean result."""
    if not IS_WINDOWS:
        raise RuntimeError("Windows only")
    script = (
        "$ErrorActionPreference='Stop'; "
        "$s=Get-MpComputerStatus; "
        "[pscustomobject]@{" 
        "AntivirusEnabled=$s.AntivirusEnabled; "
        "RealTimeProtectionEnabled=$s.RealTimeProtectionEnabled; "
        "AMServiceEnabled=$s.AMServiceEnabled; "
        "AMRunningMode=$s.AMRunningMode; "
        "SignatureUpdated=if($s.AntivirusSignatureLastUpdated){$s.AntivirusSignatureLastUpdated.ToString('yyyy-MM-dd HH:mm')}else{''} "
        "}|ConvertTo-Json -Compress"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True, text=True, timeout=20, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), check=False
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "Defender status unavailable").strip())
    data = json.loads(result.stdout.strip())
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected Defender response")
    return data


def request_defender_scan(scan_type: str) -> None:
    """Request a Defender scan using UAC. The scan is performed by Microsoft Defender."""
    if not IS_WINDOWS:
        raise RuntimeError("Windows only")
    if scan_type not in ("QuickScan", "FullScan"):
        raise ValueError("Unsupported scan type")
    command = f'Start-MpScan -ScanType {scan_type}; Start-Sleep -Seconds 3'
    params = f'-NoProfile -ExecutionPolicy Bypass -Command "{command}"'
    # ShellExecute with the "runas" verb asks Windows to show the standard UAC prompt.
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", params, None, 1)
    if result <= 32:
        raise OSError(f"ShellExecute failed ({result})")


def open_windows_security() -> None:
    if not IS_WINDOWS:
        raise RuntimeError("Windows only")
    subprocess.Popen(["cmd.exe", "/c", "start", "", "windowsdefender:"], creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


class PaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.prefs = read_json(PREFS_PATH, {"theme": "dark", "language": "en"})
        self.logs = read_json(LOG_PATH, [])
        if not isinstance(self.logs, list): self.logs = []
        self.language = self.prefs.get("language", "en")
        if self.language not in TEXT: self.language = "en"
        self.theme = self.prefs.get("theme", "dark")
        if self.theme not in ("dark", "light"): self.theme = "dark"
        self.status_data = None
        self.last_scan_text = None
        self.current_page = "dashboard"
        self.busy = False
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("1120x760")
        self.minsize(900, 650)
        self.configure(bg=self.colors()["bg"])
        self._setup_styles()
        self._build_shell()
        self.render_page("dashboard")
        self.after(450, self.refresh_status)

    def colors(self):
        if self.theme == "light":
            return {"bg":"#F3F6FB","panel":"#FFFFFF","panel2":"#EAF0F8","text":"#18253C","muted":"#62738C","line":"#DCE4EF","blue":"#2563EB","blue_hover":"#1D4ED8","green":"#07865D","green_bg":"#DDF8ED","amber":"#946200","amber_bg":"#FFF2D6","red":"#B42335","sidebar":"#EBF0F7","input":"#F7F9FC"}
        return {"bg":"#080D17","panel":"#101827","panel2":"#142136","text":"#F2F6FC","muted":"#9BAAC0","line":"#263449","blue":"#4E8EFF","blue_hover":"#367AF0","green":"#70F0C1","green_bg":"#123C34","amber":"#F5CB75","amber_bg":"#3A2E19","red":"#FF8491","sidebar":"#0C1422","input":"#111D2E"}

    def t(self, key):
        return TEXT.get(self.language, TEXT["en"]).get(key, TEXT["en"].get(key, key))

    def _setup_styles(self):
        c = self.colors()
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("PACE.TCombobox", fieldbackground=c["input"], background=c["panel2"], foreground=c["text"], arrowcolor=c["muted"], bordercolor=c["line"], padding=7)
        style.map("PACE.TCombobox", fieldbackground=[("readonly", c["input"])], foreground=[("readonly", c["text"])])

    def _build_shell(self):
        c = self.colors()
        outer = tk.Frame(self, bg=c["bg"])
        outer.pack(fill="both", expand=True)
        self.sidebar = tk.Frame(outer, bg=c["sidebar"], width=210, highlightthickness=1, highlightbackground=c["line"])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        brand = tk.Frame(self.sidebar, bg=c["sidebar"])
        brand.pack(fill="x", padx=18, pady=(22, 32))
        self.logo = tk.Canvas(brand, width=40, height=42, bg=c["sidebar"], highlightthickness=0)
        self.logo.pack(side="left")
        self.draw_shield(self.logo, 20, 21, 0.48, c["blue"], c["green"])
        brand_text = tk.Frame(brand, bg=c["sidebar"])
        brand_text.pack(side="left", padx=(9, 0))
        tk.Label(brand_text, text="PACE", bg=c["sidebar"], fg=c["text"], font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(brand_text, text="WINDOWS SECURITY", bg=c["sidebar"], fg=c["muted"], font=("Segoe UI", 7, "bold")).pack(anchor="w")
        self.nav_frame = tk.Frame(self.sidebar, bg=c["sidebar"])
        self.nav_frame.pack(fill="x", padx=12)
        self.nav_buttons = {}
        self._build_nav_buttons()
        foot = tk.Frame(self.sidebar, bg=c["sidebar"])
        foot.pack(side="bottom", fill="x", padx=18, pady=18)
        self.sidebar_status = tk.Label(foot, text="●  " + self.t("ready"), bg=c["sidebar"], fg=c["green"], font=("Segoe UI", 9))
        self.sidebar_status.pack(anchor="w")
        tk.Label(foot, text="PACE · 0.2 BETA", bg=c["sidebar"], fg=c["muted"], font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(7,0))

        self.main = tk.Frame(outer, bg=c["bg"])
        self.main.pack(side="left", fill="both", expand=True)
        self.topbar = tk.Frame(self.main, bg=c["bg"], height=70)
        self.topbar.pack(fill="x", padx=30, pady=(12, 0))
        self.topbar.pack_propagate(False)
        self.top_left = tk.Frame(self.topbar, bg=c["bg"])
        self.top_left.pack(side="left", fill="y")
        self.page_title = tk.Label(self.top_left, text="", bg=c["bg"], fg=c["text"], font=("Segoe UI", 15, "bold"))
        self.page_title.pack(anchor="w", pady=(10, 0))
        self.page_subtitle = tk.Label(self.top_left, text="", bg=c["bg"], fg=c["muted"], font=("Segoe UI", 9))
        self.page_subtitle.pack(anchor="w", pady=(3,0))
        self.settings_button = tk.Button(self.topbar, text="⚙  " + self.t("settings"), command=lambda:self.render_page("settings"), relief="flat", cursor="hand2", padx=12, pady=9, font=("Segoe UI", 9, "bold"), bg=c["panel"], fg=c["text"], activebackground=c["panel2"], activeforeground=c["text"], highlightthickness=1, highlightbackground=c["line"], bd=0)
        self.settings_button.pack(side="right", pady=12)
        self.content = tk.Frame(self.main, bg=c["bg"])
        self.content.pack(fill="both", expand=True, padx=30, pady=(4, 22))

    def draw_shield(self, canvas, x, y, scale, fill, tick):
        pts = [x, y-19*scale, x+15*scale, y-13*scale, x+14*scale, y+2*scale, x+8*scale, y+13*scale, x, y+19*scale, x-8*scale, y+13*scale, x-14*scale, y+2*scale, x-15*scale, y-13*scale]
        canvas.create_polygon(pts, fill=fill, outline=tick, width=1.4)
        canvas.create_line(x-7*scale, y, x-1*scale, y+6*scale, x+8*scale, y-6*scale, fill=tick, width=max(1.3, 3*scale), capstyle="round", joinstyle="round")

    def _build_nav_buttons(self):
        items = [("dashboard", "◈", "dashboard"), ("security", "⌕", "security"), ("activity", "☷", "activity"), ("settings", "⚙", "settings")]
        for key, icon, label in items:
            b = tk.Button(self.nav_frame, text=f" {icon}    {self.t(label)}", anchor="w", command=lambda p=key:self.render_page(p), relief="flat", bd=0, cursor="hand2", padx=13, pady=12, font=("Segoe UI", 10, "bold"))
            b.pack(fill="x", pady=3)
            self.nav_buttons[key] = b
        self._style_nav()

    def _style_nav(self):
        c = self.colors()
        for key, b in self.nav_buttons.items():
            active = key == self.current_page
            b.configure(bg=c["panel2"] if active else c["sidebar"], fg=c["blue"] if active else c["muted"], activebackground=c["panel2"], activeforeground=c["text"], highlightthickness=1 if active else 0, highlightbackground=c["line"])

    def clear_content(self):
        for child in self.content.winfo_children(): child.destroy()

    def card(self, parent, padding=18):
        c = self.colors()
        frame = tk.Frame(parent, bg=c["panel"], highlightbackground=c["line"], highlightthickness=1, bd=0)
        inner = tk.Frame(frame, bg=c["panel"])
        inner.pack(fill="both", expand=True, padx=padding, pady=padding)
        return frame, inner

    def label(self, parent, text, size=10, color=None, bold=False, bg=None, wrap=0, **kwargs):
        c = self.colors()
        return tk.Label(parent, text=text, font=("Segoe UI", size, "bold" if bold else "normal"), bg=bg or c["panel"], fg=color or c["text"], justify="left", anchor="w", wraplength=wrap, **kwargs)

    def button(self, parent, text, command, primary=False, compact=False, state="normal"):
        c = self.colors()
        bg = c["blue"] if primary else c["panel2"]
        fg = "#FFFFFF" if primary else c["text"]
        b = tk.Button(parent, text=text, command=command, state=state, relief="flat", bd=0, cursor="hand2" if state == "normal" else "arrow", padx=15 if not compact else 10, pady=10 if not compact else 7, bg=bg, fg=fg, activebackground=c["blue_hover"] if primary else c["panel"], activeforeground="#FFFFFF" if primary else c["text"], disabledforeground=c["muted"], font=("Segoe UI", 9, "bold"), highlightthickness=1, highlightbackground=c["line"])
        return b

    def render_page(self, page):
        self.current_page = page
        c = self.colors()
        self._style_nav()
        self.settings_button.configure(text="⚙  " + self.t("settings"), bg=c["panel"], fg=c["text"], activebackground=c["panel2"], activeforeground=c["text"], highlightbackground=c["line"])
        self.clear_content()
        titles = {"dashboard": self.t("dashboard"), "security": self.t("security"), "activity": self.t("activity"), "settings": self.t("settings_title")}
        self.page_title.configure(text=titles.get(page, self.t("dashboard")))
        subtitles = {"dashboard": self.t("headline"), "security": self.t("defender"), "activity": self.t("activity"), "settings": self.t("settings_saved")}
        self.page_subtitle.configure(text=subtitles.get(page, ""))
        if page == "dashboard": self.render_dashboard()
        elif page == "security": self.render_security()
        elif page == "activity": self.render_activity()
        else: self.render_settings()

    def render_dashboard(self):
        c = self.colors()
        top = tk.Frame(self.content, bg=c["bg"])
        top.pack(fill="x", pady=(4, 14))
        hero = tk.Frame(top, bg=c["bg"])
        hero.pack(side="left", fill="x", expand=True)
        self.label(hero, self.t("headline"), 21, bold=True, bg=c["bg"]).pack(anchor="w", pady=(0,7))
        self.label(hero, self.t("subhead"), 10, c["muted"], bg=c["bg"], wrap=610).pack(anchor="w")
        beta = tk.Label(top, text="  " + self.t("beta") + "  ", bg=c["amber_bg"], fg=c["amber"], font=("Segoe UI", 8, "bold"), padx=9, pady=6)
        beta.pack(side="right", anchor="n", padx=(10,0), pady=5)

        status_card, status = self.card(self.content, 17)
        status_card.pack(fill="x", pady=(0, 14))
        status_head = tk.Frame(status, bg=c["panel"])
        status_head.pack(fill="x")
        self.label(status_head, self.t("defender"), 9, c["muted"], True).pack(side="left")
        self.button(status_head, "↻  " + self.t("refresh"), self.refresh_status, compact=True).pack(side="right")
        orb_row = tk.Frame(status, bg=c["panel"])
        orb_row.pack(fill="x", pady=(14, 15))
        self.orb = tk.Canvas(orb_row, width=106, height=106, bg=c["panel"], highlightthickness=0, cursor="hand2")
        self.orb.pack(side="left", padx=(0,17))
        self.draw_orb()
        self.orb.bind("<Button-1>", lambda _e:self.refresh_status())
        self.orb.bind("<Enter>", lambda _e:self.orb.configure(cursor="hand2"))
        status_text = tk.Frame(orb_row, bg=c["panel"])
        status_text.pack(side="left", fill="both", expand=True, pady=(9,0))
        self.status_heading = self.label(status_text, self.t("checking"), 16, bold=True)
        self.status_heading.pack(anchor="w")
        self.status_detail = self.label(status_text, self.t("notchecked"), 9, c["muted"], wrap=470)
        self.status_detail.pack(anchor="w", pady=(5,0))
        self.status_bar = tk.Frame(status_text, bg=c["line"], height=4)
        self.status_bar.pack(fill="x", pady=(13,0))
        cards = tk.Frame(status, bg=c["panel"])
        cards.pack(fill="x")
        self.metric_labels = {}
        for idx, (key, label_key) in enumerate([("AntivirusEnabled","antivirus"),("RealTimeProtectionEnabled","realtime"),("AMServiceEnabled","engine"),("SignatureUpdated","updated")]):
            tile = tk.Frame(cards, bg=c["panel2"], highlightthickness=1, highlightbackground=c["line"])
            tile.grid(row=0, column=idx, sticky="nsew", padx=(0 if idx==0 else 5, 0 if idx==3 else 5))
            cards.grid_columnconfigure(idx, weight=1, uniform="metric")
            self.label(tile, self.t(label_key), 8, c["muted"], bg=c["panel2"], wrap=150).pack(anchor="w", padx=10, pady=(11,4))
            value = self.label(tile, self.t("notchecked"), 10, bold=True, bg=c["panel2"], wrap=150)
            value.pack(anchor="w", padx=10, pady=(0,11))
            self.metric_labels[key] = value

        row = tk.Frame(self.content, bg=c["bg"])
        row.pack(fill="both", expand=True)
        scan_card, scan_inner = self.card(row, 17)
        scan_card.pack(side="left", fill="both", expand=True, padx=(0,7))
        self.label(scan_inner, self.t("scan_title"), 13, bold=True).pack(anchor="w")
        self.label(scan_inner, self.t("scan_text"), 9, c["muted"], wrap=480).pack(anchor="w", pady=(5,14))
        scan_buttons = tk.Frame(scan_inner, bg=c["panel"])
        scan_buttons.pack(fill="x")
        self.button(scan_buttons, "⌕  " + self.t("quick"), lambda:self.start_scan("QuickScan"), primary=True).pack(side="left", padx=(0,8))
        self.button(scan_buttons, "▦  " + self.t("full"), lambda:self.start_scan("FullScan")).pack(side="left")
        self.button(scan_inner, "↗  " + self.t("open_security"), self.open_security, compact=True).pack(anchor="w", pady=(11,0))
        action_card, action_inner = self.card(row, 17)
        action_card.configure(width=252)
        action_card.pack(side="left", fill="y", padx=(7,0))
        action_card.pack_propagate(False)
        self.label(action_inner, self.t("last_action"), 8, c["muted"], True).pack(anchor="w")
        self.last_action_label = self.label(action_inner, self.last_scan_text or self.t("no_action"), 10, wrap=210)
        self.last_action_label.pack(anchor="w", pady=(10,0))

        notice = tk.Frame(self.content, bg=c["amber_bg"], highlightthickness=1, highlightbackground=("#785C2D" if self.theme == "dark" else "#E7D19C"))
        notice.pack(fill="x", pady=(14,0))
        self.label(notice, "!  " + self.t("notice_title"), 10, c["amber"], True, bg=c["amber_bg"]).pack(anchor="w", padx=14, pady=(11,3))
        self.label(notice, self.t("notice"), 9, c["muted"], bg=c["amber_bg"], wrap=950).pack(anchor="w", padx=14, pady=(0,11))
        self.apply_status_to_ui()

    def draw_orb(self, pulse=0):
        if not hasattr(self, "orb") or not self.orb.winfo_exists(): return
        c = self.colors()
        self.orb.delete("all")
        self.orb.create_oval(7-pulse, 7-pulse, 99+pulse, 99+pulse, outline=c["line"], width=1)
        self.orb.create_oval(15, 15, 91, 91, fill=c["panel2"], outline=c["blue"], width=2)
        self.orb.create_oval(24, 24, 82, 82, fill=c["panel"], outline=c["line"], width=1)
        self.draw_shield(self.orb, 53, 52, 1.0, c["blue"], c["green"])
        if self.busy:
            self.orb.after(140, lambda:self.draw_orb(0 if pulse else 4))

    def apply_status_to_ui(self):
        if not hasattr(self, "metric_labels"): return
        c = self.colors()
        if not self.status_data:
            for key, label in self.metric_labels.items(): label.configure(text=self.t("notchecked"))
            return
        d = self.status_data
        for key in ("AntivirusEnabled", "RealTimeProtectionEnabled", "AMServiceEnabled"):
            val = d.get(key)
            txt = self.t("yes") if val is True else self.t("no") if val is False else self.t("unknown")
            self.metric_labels[key].configure(text=txt, fg=(c["green"] if val is True else c["red"] if val is False else c["muted"]))
        self.metric_labels["SignatureUpdated"].configure(text=d.get("SignatureUpdated") or self.t("unknown"), fg=c["text"])
        essentials = [d.get("AntivirusEnabled"), d.get("RealTimeProtectionEnabled")]
        if all(x is True for x in essentials):
            self.status_heading.configure(text=self.t("yes"), fg=c["green"])
            self.status_detail.configure(text=self.t("status_ok"))
            self.status_bar.configure(bg=c["green"])
        elif any(x is False for x in essentials):
            self.status_heading.configure(text=self.t("no"), fg=c["red"])
            self.status_detail.configure(text=self.t("status_fail"))
            self.status_bar.configure(bg=c["red"])
        else:
            self.status_heading.configure(text=self.t("status_unknown"), fg=c["amber"])
            self.status_detail.configure(text=self.t("status_fail"))
            self.status_bar.configure(bg=c["amber"])

    def refresh_status(self):
        if self.busy:
            return
        if not IS_WINDOWS:
            messagebox.showinfo(APP_NAME, self.t("requires_windows"))
            return
        self.busy = True
        if hasattr(self, "status_heading"):
            self.status_heading.configure(text=self.t("checking"))
            self.status_detail.configure(text=self.t("working"))
            self.draw_orb(3)
        self.sidebar_status.configure(text="●  " + self.t("checking"))
        threading.Thread(target=self._refresh_worker, daemon=True).start()

    def _refresh_worker(self):
        try:
            data = defender_status()
            self.after(0, lambda d=data:self._refresh_done(d, None))
        except Exception as exc:
            self.after(0, lambda e=str(exc):self._refresh_done(None, e))

    def _refresh_done(self, data, error):
        self.busy = False
        c = self.colors()
        self.sidebar_status.configure(text="●  " + self.t("ready"), fg=c["green"])
        if data:
            self.status_data = data
            self.add_log("Defender status", "Status retrieved")
        else:
            self.status_data = None
            self.add_log("Defender status", "Unavailable")
        if self.current_page == "dashboard":
            self.apply_status_to_ui()
            self.draw_orb(0)
        elif self.current_page == "security":
            self.render_security()
        self.render_activity_if_open()

    def start_scan(self, scan_type):
        if not IS_WINDOWS:
            messagebox.showinfo(APP_NAME, self.t("requires_windows")); return
        key = "quick_name" if scan_type == "QuickScan" else "full_name"
        kind = self.t(key)
        if not messagebox.askyesno(APP_NAME, self.t("scan_confirm").format(kind=kind)):
            self.add_log(kind, self.t("scan_cancel")); return
        try:
            request_defender_scan(scan_type)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_scan_text = self.t("scan_sent").format(kind=kind, time=timestamp)
            self.add_log(kind, "Request submitted at " + timestamp)
            if self.current_page == "dashboard" and hasattr(self, "last_action_label"):
                self.last_action_label.configure(text=self.last_scan_text)
            messagebox.showinfo(APP_NAME, self.last_scan_text)
        except Exception as exc:
            self.add_log(kind, "Could not start: " + str(exc)[:160])
            messagebox.showerror(APP_NAME, self.t("scan_error") + "\n\n" + str(exc)[:280])

    def open_security(self):
        try:
            open_windows_security()
            self.add_log("Open Windows Security", "Opened")
        except Exception as exc:
            messagebox.showerror(APP_NAME, str(exc))

    def add_log(self, event, result):
        self.logs.insert(0, {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": str(event)[:100], "result": str(result)[:260]})
        self.logs = self.logs[:100]
        write_json(LOG_PATH, self.logs)
        self.render_activity_if_open()

    def render_activity_if_open(self):
        if self.current_page == "activity":
            self.render_activity()

    def render_security(self):
        c = self.colors()
        self.label(self.content, self.t("subhead"), 10, c["muted"], bg=c["bg"], wrap=920).pack(anchor="w", pady=(0,18))
        card, inner = self.card(self.content, 19); card.pack(fill="x", pady=(0,14))
        self.label(inner, self.t("defender"), 9, c["muted"], True).pack(anchor="w")
        data = self.status_data or {}
        fields = [("antivirus","AntivirusEnabled"),("realtime","RealTimeProtectionEnabled"),("engine","AMServiceEnabled"),("updated","SignatureUpdated")]
        for i,(label_key,key) in enumerate(fields):
            row = tk.Frame(inner,bg=c["panel"]); row.pack(fill="x", pady=10)
            self.label(row,self.t(label_key),10).pack(side="left")
            val=data.get(key)
            if key=="SignatureUpdated": value=val or self.t("unknown")
            else: value=self.t("yes") if val is True else self.t("no") if val is False else self.t("unknown")
            self.label(row,value,10,c["green"] if val is True else c["red"] if val is False else c["muted"],True).pack(side="right")
            if i < len(fields)-1: tk.Frame(inner,bg=c["line"],height=1).pack(fill="x")
        self.button(self.content,"↻  "+self.t("refresh"),self.refresh_status,primary=True).pack(anchor="w",pady=(0,18))
        notice, ni = self.card(self.content,18); notice.pack(fill="x")
        self.label(ni,self.t("notice_title"),12,c["amber"],True).pack(anchor="w")
        self.label(ni,self.t("notice"),10,c["muted"],wrap=900).pack(anchor="w",pady=(6,0))

    def render_activity(self):
        c=self.colors()
        header=tk.Frame(self.content,bg=c["bg"]); header.pack(fill="x",pady=(0,14))
        self.label(header,self.t("privacy"),9,c["muted"],bg=c["bg"],wrap=720).pack(side="left",anchor="w")
        self.button(header,self.t("clear"),self.clear_log,compact=True).pack(side="right")
        card,inner=self.card(self.content,14); card.pack(fill="both",expand=True)
        heads=tk.Frame(inner,bg=c["panel2"]); heads.pack(fill="x",pady=(0,7))
        for text,width in [(self.t("time"),155),(self.t("event"),180),(self.t("result"),550)]:
            self.label(heads,text,8,c["muted"],True,bg=c["panel2"],width=width).pack(side="left",padx=8,pady=9,anchor="w")
        if not self.logs:
            self.label(inner,self.t("log_empty"),10,c["muted"]).pack(anchor="w",pady=12)
        else:
            canvas=tk.Canvas(inner,bg=c["panel"],highlightthickness=0)
            scroll=ttk.Scrollbar(inner,orient="vertical",command=canvas.yview)
            rows=tk.Frame(canvas,bg=c["panel"])
            rows.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0,0),window=rows,anchor="nw")
            canvas.configure(yscrollcommand=scroll.set)
            canvas.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")
            for item in self.logs:
                line=tk.Frame(rows,bg=c["panel"]);line.pack(fill="x",pady=4)
                self.label(line,item.get("time",""),8,c["muted"],width=155).pack(side="left",padx=8,anchor="n")
                self.label(line,item.get("event",""),9,bold=True,width=180,wrap=170).pack(side="left",padx=8,anchor="n")
                self.label(line,item.get("result",""),8,c["muted"],width=550,wrap=530).pack(side="left",padx=8,anchor="n")
                tk.Frame(rows,bg=c["line"],height=1).pack(fill="x",pady=3)

    def clear_log(self):
        if messagebox.askyesno(APP_NAME, self.t("clear") + "?"):
            self.logs=[]; write_json(LOG_PATH,self.logs); self.render_activity()

    def render_settings(self):
        c=self.colors()
        card,inner=self.card(self.content,22);card.pack(fill="x",pady=(0,14))
        self.label(inner,self.t("settings_title"),15,bold=True).pack(anchor="w",pady=(0,18))
        self.label(inner,self.t("appearance"),10,c["muted"],True).pack(anchor="w")
        self.theme_var=tk.StringVar(value=self.theme)
        theme_row=tk.Frame(inner,bg=c["panel"]);theme_row.pack(fill="x",pady=(7,19))
        for val,key in [("dark","dark"),("light","light")]:
            rb=tk.Radiobutton(theme_row,text=self.t(key),variable=self.theme_var,value=val,command=self.change_theme,indicatoron=False,padx=17,pady=9,bg=c["panel2"],fg=c["text"],selectcolor=c["blue"],activebackground=c["panel2"],activeforeground=c["text"],font=("Segoe UI",9,"bold"),relief="flat",bd=0)
            rb.pack(side="left",padx=(0,8))
        self.label(inner,self.t("language"),10,c["muted"],True).pack(anchor="w")
        self.lang_var=tk.StringVar(value="English" if self.language=="en" else "Türkçe")
        lang=ttk.Combobox(inner,textvariable=self.lang_var,state="readonly",values=["English","Türkçe"],width=18,style="PACE.TCombobox")
        lang.pack(anchor="w",pady=(7,20));lang.bind("<<ComboboxSelected>>",lambda _e:self.change_language())
        self.label(inner,self.t("settings_saved"),9,c["muted"]).pack(anchor="w")
        card2, inner2=self.card(self.content,22);card2.pack(fill="x",pady=(0,14))
        self.label(inner2,self.t("privacy_title"),13,bold=True).pack(anchor="w")
        self.label(inner2,self.t("privacy"),10,c["muted"],wrap=900).pack(anchor="w",pady=(7,0))
        card3, inner3=self.card(self.content,22);card3.pack(fill="x")
        self.label(inner3,self.t("about_title"),13,bold=True).pack(anchor="w")
        self.label(inner3,self.t("about_text"),10,c["muted"]).pack(anchor="w",pady=(7,3))
        self.label(inner3,self.t("about_note"),9,c["muted"],wrap=900).pack(anchor="w")

    def change_theme(self):
        self.theme=self.theme_var.get()
        self.prefs.update({"theme":self.theme,"language":self.language});write_json(PREFS_PATH,self.prefs)
        self.rebuild()

    def change_language(self):
        self.language="tr" if self.lang_var.get()=="Türkçe" else "en"
        self.prefs.update({"theme":self.theme,"language":self.language});write_json(PREFS_PATH,self.prefs)
        self.rebuild()

    def rebuild(self):
        for child in self.winfo_children():child.destroy()
        self.configure(bg=self.colors()["bg"])
        self._setup_styles();self._build_shell();self.render_page(self.current_page)


if __name__ == "__main__":
    try:
        app = PaceApp()
        app.mainloop()
    except Exception as exc:
        try:
            messagebox.showerror(APP_NAME, f"PACE could not start.\n\n{exc}")
        except Exception:
            print(exc, file=sys.stderr)
