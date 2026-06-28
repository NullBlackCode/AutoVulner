#BlackCode
# core/app.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import json
from datetime import datetime

from .theme import setup_theme, get_style
from .utils import get_proxy, save_log, load_config, save_config, get_public_ip

from modules.ssh_cracker import SSHCracker
from modules.rdp_cracker import RDPCracker
from modules.fuzzer import Fuzzer
from modules.scanner import Scanner
from modules.web_login import WebLogin
from modules.subdomain import Subdomain
from modules.sqli import SQLi
from modules.xss import XSS
from modules.network_tools import NetworkTools
from modules.auto_scanner import AutoScanner
from modules.pentest_tools import PentestTools
from modules.hash_cracker import HashCracker
from modules.dir_brute import DirBrute
from modules.osint import OSINT

from gui.request_controller import RequestController
from gui.reports_tab import ReportsTab
from gui.notes_tab import NotesTab

class BlackCodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        setup_theme()
        
        self.title("🛡️ BlackCode v2.1.0 | Pentesting GUI")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.92)
        window_height = int(screen_height * 0.88)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(int(window_width * 0.7), int(window_height * 0.7))
        
        self.config = load_config()
        self.proxy_config = self.config.get('proxy', {})
        self.output_dir = "logs"
        self.report_dir = "reports"
        self.vulnerabilities = []
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#0a0a1a")
        main_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkFrame(main_frame, fg_color="transparent", height=60)
        header.grid(row=0, column=0, padx=10, pady=(10, 15), sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header, text="🛡️ BlackCode Ultimate v8.0", 
                    font=ctk.CTkFont(size=26, weight="bold"), text_color="#00ff41").grid(row=0, column=0, padx=10)
        
        ctk.CTkButton(header, text="🌙", width=40, command=self.toggle_theme,
                     fg_color="#2c3e50", hover_color="#34495e").grid(row=0, column=2, padx=10)
        
        ctk.CTkButton(header, text="🌐 Request Controller", command=self.open_request_controller,
                     fg_color="#9b59b6", hover_color="#8e44ad", height=35, width=180).grid(row=0, column=3, padx=10)
        
        self.tab_view = ctk.CTkTabview(main_frame, corner_radius=10)
        self.tab_view.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        tabs = [
            "🔑 SSH", "🖥️ RDP", "🎯 Fuzzer", "🔍 Scanner", "🌐 Web Login",
            "🌍 Subdomain", "💉 SQLi", "🕸️ XSS", "📡 Network", "🤖 Auto Scanner",
            "🔧 Pentest", "🔐 Hash", "🔍 Dir Brute", "🕵️ OSINT", "📊 Reports", "📝 Notes"
        ]
        
        for tab_name in tabs:
            self.tab_view.add(tab_name)
        
        self.modules = {}
        
        ssh_tab = self.tab_view.tab("🔑 SSH")
        self.modules['ssh'] = SSHCracker(ssh_tab, self)
        
        rdp_tab = self.tab_view.tab("🖥️ RDP")
        self.modules['rdp'] = RDPCracker(rdp_tab, self)
        
        fuzz_tab = self.tab_view.tab("🎯 Fuzzer")
        self.modules['fuzzer'] = Fuzzer(fuzz_tab, self)
        
        scan_tab = self.tab_view.tab("🔍 Scanner")
        self.modules['scanner'] = Scanner(scan_tab, self)
        
        web_tab = self.tab_view.tab("🌐 Web Login")
        self.modules['web_login'] = WebLogin(web_tab, self)
        
        sub_tab = self.tab_view.tab("🌍 Subdomain")
        self.modules['subdomain'] = Subdomain(sub_tab, self)
        
        sqli_tab = self.tab_view.tab("💉 SQLi")
        self.modules['sqli'] = SQLi(sqli_tab, self)
        
        xss_tab = self.tab_view.tab("🕸️ XSS")
        self.modules['xss'] = XSS(xss_tab, self)
        
        net_tab = self.tab_view.tab("📡 Network")
        self.modules['network'] = NetworkTools(net_tab, self)
        
        auto_tab = self.tab_view.tab("🤖 Auto Scanner")
        self.modules['auto_scanner'] = AutoScanner(auto_tab, self)
        
        pentest_tab = self.tab_view.tab("🔧 Pentest")
        self.modules['pentest'] = PentestTools(pentest_tab, self)
        
        hash_tab = self.tab_view.tab("🔐 Hash")
        self.modules['hash'] = HashCracker(hash_tab, self)
        
        dir_tab = self.tab_view.tab("🔍 Dir Brute")
        self.modules['dir_brute'] = DirBrute(dir_tab, self)
        
        osint_tab = self.tab_view.tab("🕵️ OSINT")
        self.modules['osint'] = OSINT(osint_tab, self)
        
        reports_tab = self.tab_view.tab("📊 Reports")
        self.modules['reports'] = ReportsTab(reports_tab, self)
        
        notes_tab = self.tab_view.tab("📝 Notes")
        self.modules['notes'] = NotesTab(notes_tab, self)
        
        status_frame = ctk.CTkFrame(main_frame, corner_radius=10, height=30, fg_color="#1a1a2e")
        status_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(status_frame, text="✅ System Ready | BlackCode v8.0", anchor="w", font=ctk.CTkFont(size=11))
        self.status_label.grid(row=0, column=0, padx=10, sticky="w")
        
        self.network_label = ctk.CTkLabel(status_frame, text="🌐 Loading...", font=ctk.CTkFont(size=11), text_color="#00ccff")
        self.network_label.grid(row=0, column=1, padx=10, sticky="e")
        
        self.update_network_display()
        
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")
        
    def open_request_controller(self):
        RequestController(self)
        
    def update_network_display(self):
        ip = get_public_ip()
        proxy_status = "🔓" if not self.proxy_config.get('enabled') else "🔒"
        self.network_label.configure(text=f"🌐 {ip} | {proxy_status} Proxy")
        
    def set_status(self, msg):
        self.status_label.configure(text=f"✅ {msg}")
        
    def get_proxy(self):
        if self.proxy_config.get('enabled', False):
            proxy = self.proxy_config.get('proxy', '')
            username = self.proxy_config.get('username', '')
            password = self.proxy_config.get('password', '')
            if username and password:
                proxy = proxy.replace('://', f'://{username}:{password}@')
            return {'http': proxy, 'https': proxy}
        return None
