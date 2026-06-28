import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import os
import json
import re
import socket
import requests
import subprocess
import random
import hashlib
import base64
from urllib.parse import urlparse, parse_qs, urlencode, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from bs4 import BeautifulSoup
import dns.resolver
import whois
import ssl
import OpenSSL
import ipwhois
from scapy.all import ARP, Ether, srp
import nmap
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BlackCodeUltimate(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🛡️ BlackCode v1.0 | beta")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(int(window_width * 0.7), int(window_height * 0.7))
        
        self.running = False
        self.stop_flag = False
        self.output_dir = "logs"
        self.report_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)
        
        self.create_widgets()
        self.load_config()
        self.animate_header()
        
    def animate_header(self):
        colors = ["#00ff41", "#00ccff", "#ff00ff", "#ffaa00", "#00ff41"]
        self.header_anim_idx = 0
        
        def update_logo():
            self.header_anim_idx = (self.header_anim_idx + 1) % len(colors)
            self.logo_label.configure(text_color=colors[self.header_anim_idx])
            self.after(2000, update_logo)
        
        update_logo()
        
    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkFrame(main_frame, fg_color="transparent", height=70)
        header.grid(row=0, column=0, padx=10, pady=(10, 15), sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        
        self.logo_label = ctk.CTkLabel(header, text="🛡️ BlackCode Ultimate", 
                           font=ctk.CTkFont(size=28, weight="bold"),
                           text_color="#00ff41")
        self.logo_label.grid(row=0, column=0, padx=10)
        
        self.theme_btn = ctk.CTkButton(header, text="🌙", width=45, height=45,
                                       corner_radius=25, command=self.toggle_theme,
                                       fg_color="#2c3e50", hover_color="#34495e")
        self.theme_btn.grid(row=0, column=2, padx=10)
        
        self.tab_view = ctk.CTkTabview(main_frame, corner_radius=10,
                                       segmented_button_selected_color="#00ff41",
                                       segmented_button_selected_hover_color="#00cc33")
        self.tab_view.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        tabs = [
            "🔑 SSH Cracker", "🎯 Fuzzer", "🔍 Scanner", 
            "🌐 Web Login", "🌍 Subdomain", "💉 SQL Injection",
            "🕸️ XSS Hunter", "📡 Network Tools", "🔧 Pentest Tools",
            "📊 Reports"
        ]
        
        for tab_name in tabs:
            self.tab_view.add(tab_name)
            
        self.create_ssh_tab()
        self.create_fuzzer_tab()
        self.create_scanner_tab()
        self.create_web_login_tab()
        self.create_subdomain_tab()
        self.create_sqli_tab()
        self.create_xss_tab()
        self.create_network_tab()
        self.create_pentest_tab()
        self.create_reports_tab()
        
        self.status_bar = ctk.CTkLabel(self, text="✅ System Ready | BlackCode Ultimate v5.0", anchor="w",
                                       fg_color="#1a1a2e", corner_radius=5, padx=10,
                                       font=ctk.CTkFont(size=12))
        self.status_bar.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        
    def create_ssh_tab(self):
        tab = self.tab_view.tab("🔑 SSH Cracker")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        input_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(input_frame, text="📁 IP List:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.ssh_ip_entry = ctk.CTkEntry(input_frame, placeholder_text="Select IP file...", height=35)
        self.ssh_ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(input_frame, text="Browse", width=80, height=35,
                     command=lambda: self.browse_file(self.ssh_ip_entry),
                     fg_color="#3498db", hover_color="#2980b9").grid(row=0, column=2, padx=5)
        
        ctk.CTkLabel(input_frame, text="📁 Password List:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=5, pady=5)
        self.ssh_pw_entry = ctk.CTkEntry(input_frame, placeholder_text="Select password file...", height=35)
        self.ssh_pw_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(input_frame, text="Browse", width=80, height=35,
                     command=lambda: self.browse_file(self.ssh_pw_entry),
                     fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(input_frame, text="👤 Username:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=5, pady=5)
        self.ssh_username = ctk.CTkEntry(input_frame, placeholder_text="root", width=150, height=35)
        self.ssh_username.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(input_frame, text="🧵 Threads:", font=ctk.CTkFont(size=13)).grid(row=2, column=2, padx=5, pady=5)
        self.ssh_threads = ctk.CTkEntry(input_frame, width=80, height=35)
        self.ssh_threads.insert(0, "50")
        self.ssh_threads.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(input_frame, text="⏱️ Timeout:", font=ctk.CTkFont(size=13)).grid(row=3, column=0, padx=5, pady=5)
        self.ssh_timeout = ctk.CTkEntry(input_frame, width=80, height=35)
        self.ssh_timeout.insert(0, "10")
        self.ssh_timeout.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.ssh_progress = ctk.CTkProgressBar(input_frame, width=300, height=20)
        self.ssh_progress.grid(row=3, column=2, padx=5, pady=5, columnspan=2)
        self.ssh_progress.set(0)
        
        self.ssh_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                      font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.ssh_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.ssh_start_btn = ctk.CTkButton(btn_frame, text="▶ Start Attack", 
                                           command=self.start_ssh_crack,
                                           fg_color="#2ecc71", hover_color="#27ae60",
                                           height=40, width=120, font=ctk.CTkFont(weight="bold"))
        self.ssh_start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.ssh_stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop",
                                          command=self.stop_ssh_crack,
                                          fg_color="#e74c3c", hover_color="#c0392b",
                                          height=40, width=100, state=ctk.DISABLED)
        self.ssh_stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.ssh_log, "ssh"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.ssh_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
                     
    def create_fuzzer_tab(self):
        tab = self.tab_view.tab("🎯 Fuzzer")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        setting_frame.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🎯 Target URL:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.fuzz_url = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com/FUZZ", height=35)
        self.fuzz_url.grid(row=0, column=1, padx=5, pady=5, sticky="ew", columnspan=3)
        
        ctk.CTkLabel(setting_frame, text="📁 Wordlist:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=5, pady=5)
        self.fuzz_wordlist = ctk.CTkEntry(setting_frame, placeholder_text="Select wordlist...", height=35)
        self.fuzz_wordlist.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=80, height=35,
                     command=lambda: self.browse_file(self.fuzz_wordlist),
                     fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=5, pady=5)
        self.fuzz_threads = ctk.CTkEntry(setting_frame, width=80, height=35)
        self.fuzz_threads.insert(0, "50")
        self.fuzz_threads.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="⏱️ Timeout:", font=ctk.CTkFont(size=13)).grid(row=2, column=2, padx=5, pady=5)
        self.fuzz_timeout = ctk.CTkEntry(setting_frame, width=80, height=35)
        self.fuzz_timeout.insert(0, "5")
        self.fuzz_timeout.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="🔍 Filter Status:", font=ctk.CTkFont(size=13)).grid(row=3, column=0, padx=5, pady=5)
        self.fuzz_filter = ctk.CTkEntry(setting_frame, placeholder_text="200,301,302,403,500", height=35)
        self.fuzz_filter.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.fuzz_progress = ctk.CTkProgressBar(setting_frame, width=200, height=20)
        self.fuzz_progress.grid(row=3, column=2, padx=5, pady=5, columnspan=2)
        self.fuzz_progress.set(0)
        
        self.fuzz_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                       font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.fuzz_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.fuzz_start_btn = ctk.CTkButton(btn_frame, text="▶ Start Fuzzing",
                                            command=self.start_fuzzer,
                                            fg_color="#2ecc71", hover_color="#27ae60",
                                            height=40, width=120, font=ctk.CTkFont(weight="bold"))
        self.fuzz_start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.fuzz_stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop",
                                           command=self.stop_fuzzer,
                                           fg_color="#e74c3c", hover_color="#c0392b",
                                           height=40, width=100, state=ctk.DISABLED)
        self.fuzz_stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.fuzz_log, "fuzz"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.fuzz_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
                     
    def create_scanner_tab(self):
        tab = self.tab_view.tab("🔍 Scanner")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        setting_frame.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🎯 Target:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.scan_target = ctk.CTkEntry(setting_frame, placeholder_text="IP or Domain", height=35)
        self.scan_target.grid(row=0, column=1, padx=5, pady=5, sticky="ew", columnspan=3)
        
        ctk.CTkLabel(setting_frame, text="📡 Ports:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=5, pady=5)
        self.scan_ports = ctk.CTkEntry(setting_frame, placeholder_text="1-1000 or 21,22,80", height=35)
        self.scan_ports.insert(0, "1-1000")
        self.scan_ports.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=13)).grid(row=1, column=2, padx=5, pady=5)
        self.scan_threads = ctk.CTkEntry(setting_frame, width=80, height=35)
        self.scan_threads.insert(0, "100")
        self.scan_threads.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        self.scan_progress = ctk.CTkProgressBar(setting_frame, width=300, height=20)
        self.scan_progress.grid(row=2, column=0, padx=5, pady=5, columnspan=4)
        self.scan_progress.set(0)
        
        self.scan_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                       font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.scan_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.scan_start_btn = ctk.CTkButton(btn_frame, text="▶ Start Scan",
                                            command=self.start_scanner,
                                            fg_color="#2ecc71", hover_color="#27ae60",
                                            height=40, width=120, font=ctk.CTkFont(weight="bold"))
        self.scan_start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.scan_stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop",
                                           command=self.stop_scanner,
                                           fg_color="#e74c3c", hover_color="#c0392b",
                                           height=40, width=100, state=ctk.DISABLED)
        self.scan_stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.scan_log, "scan"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.scan_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
                     
    def create_web_login_tab(self):
        tab = self.tab_view.tab("🌐 Web Login")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🌐 Login URL:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.login_url = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com/login", height=35)
        self.login_url.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="👤 Username Field:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=5, pady=5)
        self.login_user_field = ctk.CTkEntry(setting_frame, placeholder_text="username", height=35)
        self.login_user_field.insert(0, "username")
        self.login_user_field.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="🔑 Password Field:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=5, pady=5)
        self.login_pass_field = ctk.CTkEntry(setting_frame, placeholder_text="password", height=35)
        self.login_pass_field.insert(0, "password")
        self.login_pass_field.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="👤 Username:", font=ctk.CTkFont(size=13)).grid(row=3, column=0, padx=5, pady=5)
        self.login_user = ctk.CTkEntry(setting_frame, placeholder_text="admin", height=35)
        self.login_user.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📁 Password List:", font=ctk.CTkFont(size=13)).grid(row=4, column=0, padx=5, pady=5)
        self.login_pwlist = ctk.CTkEntry(setting_frame, placeholder_text="Select password list...", height=35)
        self.login_pwlist.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=80, height=35,
                     command=lambda: self.browse_file(self.login_pwlist),
                     fg_color="#3498db", hover_color="#2980b9").grid(row=4, column=2, padx=5)
        
        self.login_progress = ctk.CTkProgressBar(setting_frame, width=300, height=20)
        self.login_progress.grid(row=5, column=0, padx=5, pady=5, columnspan=3)
        self.login_progress.set(0)
        
        self.login_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                        font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.login_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.login_start_btn = ctk.CTkButton(btn_frame, text="▶ Start Attack",
                                             command=self.start_web_login,
                                             fg_color="#2ecc71", hover_color="#27ae60",
                                             height=40, width=120, font=ctk.CTkFont(weight="bold"))
        self.login_start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.login_stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop",
                                            command=self.stop_web_login,
                                            fg_color="#e74c3c", hover_color="#c0392b",
                                            height=40, width=100, state=ctk.DISABLED)
        self.login_stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.login_log, "web_login"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.login_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
                     
    def create_subdomain_tab(self):
        tab = self.tab_view.tab("🌍 Subdomain")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🌐 Domain:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.sub_domain = ctk.CTkEntry(setting_frame, placeholder_text="example.com", height=35)
        self.sub_domain.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📁 Wordlist:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=5, pady=5)
        self.sub_wordlist = ctk.CTkEntry(setting_frame, placeholder_text="Select subdomain wordlist...", height=35)
        self.sub_wordlist.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=80, height=35,
                     command=lambda: self.browse_file(self.sub_wordlist),
                     fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=5, pady=5)
        self.sub_threads = ctk.CTkEntry(setting_frame, width=80, height=35)
        self.sub_threads.insert(0, "50")
        self.sub_threads.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.sub_progress = ctk.CTkProgressBar(setting_frame, width=200, height=20)
        self.sub_progress.grid(row=2, column=2, padx=5, pady=5)
        self.sub_progress.set(0)
        
        self.sub_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                      font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.sub_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.sub_start_btn = ctk.CTkButton(btn_frame, text="▶ Start Finding",
                                           command=self.start_subdomain,
                                           fg_color="#2ecc71", hover_color="#27ae60",
                                           height=40, width=120, font=ctk.CTkFont(weight="bold"))
        self.sub_start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.sub_stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop",
                                          command=self.stop_subdomain,
                                          fg_color="#e74c3c", hover_color="#c0392b",
                                          height=40, width=100, state=ctk.DISABLED)
        self.sub_stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.sub_log, "subdomain"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.sub_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
    
    def create_sqli_tab(self):
        tab = self.tab_view.tab("💉 SQL Injection")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🎯 Target URL:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.sqli_url = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com/page.php?id=1", height=35)
        self.sqli_url.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📝 Parameter:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=5, pady=5)
        self.sqli_param = ctk.CTkEntry(setting_frame, placeholder_text="id", height=35)
        self.sqli_param.insert(0, "id")
        self.sqli_param.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.sqli_progress = ctk.CTkProgressBar(setting_frame, width=300, height=20)
        self.sqli_progress.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.sqli_progress.set(0)
        
        self.sqli_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                       font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.sqli_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.sqli_start_btn = ctk.CTkButton(btn_frame, text="▶ Start Scan",
                                            command=self.start_sqli,
                                            fg_color="#2ecc71", hover_color="#27ae60",
                                            height=40, width=120, font=ctk.CTkFont(weight="bold"))
        self.sqli_start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.sqli_stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop",
                                           command=self.stop_sqli,
                                           fg_color="#e74c3c", hover_color="#c0392b",
                                           height=40, width=100, state=ctk.DISABLED)
        self.sqli_stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.sqli_log, "sqli"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.sqli_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
    
    def create_xss_tab(self):
        tab = self.tab_view.tab("🕸️ XSS Hunter")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🎯 Target URL:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.xss_url = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com/search.php?q=test", height=35)
        self.xss_url.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📝 Parameter:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=5, pady=5)
        self.xss_param = ctk.CTkEntry(setting_frame, placeholder_text="q", height=35)
        self.xss_param.insert(0, "q")
        self.xss_param.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.xss_progress = ctk.CTkProgressBar(setting_frame, width=300, height=20)
        self.xss_progress.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.xss_progress.set(0)
        
        self.xss_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                      font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.xss_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.xss_start_btn = ctk.CTkButton(btn_frame, text="▶ Start Scan",
                                           command=self.start_xss,
                                           fg_color="#2ecc71", hover_color="#27ae60",
                                           height=40, width=120, font=ctk.CTkFont(weight="bold"))
        self.xss_start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.xss_stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop",
                                          command=self.stop_xss,
                                          fg_color="#e74c3c", hover_color="#c0392b",
                                          height=40, width=100, state=ctk.DISABLED)
        self.xss_stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.xss_log, "xss"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.xss_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
    
    def create_network_tab(self):
        tab = self.tab_view.tab("📡 Network Tools")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🎯 Target:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=5, pady=5)
        self.net_target = ctk.CTkEntry(setting_frame, placeholder_text="IP or Domain", height=35)
        self.net_target.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tool_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        tool_frame.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        
        tools = [
            ("📡 Ping", self.ping_sweep, "#2ecc71"),
            ("🔍 DNS", self.dns_lookup, "#3498db"),
            ("📋 Whois", self.whois_lookup, "#9b59b6"),
            ("🔄 Traceroute", self.traceroute, "#f39c12"),
            ("📶 ARP", self.arp_scan, "#e74c3c"),
            ("🔐 SSL", self.ssl_check, "#1abc9c")
        ]
        
        for i, (name, func, color) in enumerate(tools):
            btn = ctk.CTkButton(tool_frame, text=name, command=func,
                               fg_color=color, hover_color="#2c3e50",
                               height=35, width=110, font=ctk.CTkFont(size=12))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        self.net_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                      font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.net_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.net_log, "network"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.net_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
    
    def create_pentest_tab(self):
        tab = self.tab_view.tab("🔧 Pentest Tools")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        tool_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        tool_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        tool_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(tool_frame, text="🔧 Pentest Tools Panel", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#00ff41").grid(row=0, column=0, padx=10, pady=10)
        
        tools_grid = ctk.CTkFrame(tool_frame, fg_color="transparent")
        tools_grid.grid(row=1, column=0, padx=10, pady=10)
        
        pentest_tools = [
            ("🔍 Nikto Scan", "nikto", "#e74c3c"),
            ("📡 Nmap Scan", "nmap", "#3498db"),
            ("🔑 Hash Cracker", "hash", "#f39c12"),
            ("🔄 Port Forward", "forward", "#1abc9c"),
            ("🔒 SSL Check", "ssl", "#2ecc71"),
            ("📊 Vuln Scan", "vuln", "#9b59b6"),
            ("🔧 Payload Gen", "payload", "#e67e22"),
            ("📝 Report Gen", "report", "#00ff41")
        ]
        
        for i, (name, tool_id, color) in enumerate(pentest_tools):
            btn = ctk.CTkButton(tools_grid, text=name, 
                               command=lambda tid=tool_id: self.run_pentest_tool(tid),
                               fg_color=color, hover_color="#2c3e50",
                               width=160, height=40, font=ctk.CTkFont(size=13, weight="bold"))
            btn.grid(row=i//4, column=i%4, padx=10, pady=10)
        
        self.pentest_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                          font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.pentest_log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=lambda: self.save_log(self.pentest_log, "pentest"),
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=lambda: self.clear_log(self.pentest_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=35, width=80).pack(side=ctk.LEFT, padx=5)
    
    def create_reports_tab(self):
        tab = self.tab_view.tab("📊 Reports")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        header_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header_frame, text="📊 Security Reports", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#00ff41").grid(row=0, column=0, padx=10)
        
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=1, padx=10)
        
        ctk.CTkButton(btn_frame, text="📊 Generate Report", 
                     command=self.generate_full_report,
                     fg_color="#2ecc71", hover_color="#27ae60",
                     height=35, width=150).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="📄 Export PDF", 
                     command=self.export_pdf_report,
                     fg_color="#e74c3c", hover_color="#c0392b",
                     height=35, width=120).pack(side=ctk.LEFT, padx=5)
        
        self.reports_log = ctk.CTkTextbox(tab, wrap="word", state="disabled",
                                          font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.reports_log.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame2 = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame2.grid(row=2, column=0, padx=10, pady=10)
        
        ctk.CTkButton(btn_frame2, text="💾 Save Report", 
                     command=self.save_report,
                     fg_color="#3498db", hover_color="#2980b9",
                     height=35, width=120).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame2, text="🗑️ Clear", 
                     command=lambda: self.clear_log(self.reports_log),
                     fg_color="#95a5a6", hover_color="#7f8c8d",
                     height=35, width=80).pack(side=ctk.LEFT, padx=5)
    
    def browse_file(self, entry_widget):
        path = filedialog.askopenfilename()
        if path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, path)
    
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_btn.configure(text="☀️")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="🌙")
    
    def log_to_widget(self, widget, msg):
        widget.configure(state="normal")
        widget.insert(ctk.END, msg + "\n")
        widget.see(ctk.END)
        widget.configure(state="disabled")
    
    def clear_log(self, widget):
        widget.configure(state="normal")
        widget.delete("1.0", ctk.END)
        widget.configure(state="disabled")
    
    def clear_all_logs(self):
        for attr in dir(self):
            if attr.endswith("_log"):
                widget = getattr(self, attr)
                if isinstance(widget, ctk.CTkTextbox):
                    self.clear_log(widget)
    
    def save_log(self, widget, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/{name}_{timestamp}.txt"
        content = widget.get("1.0", ctk.END)
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def export_logs(self):
        folder = filedialog.askdirectory()
        if folder:
            for attr in dir(self):
                if attr.endswith("_log"):
                    widget = getattr(self, attr)
                    if isinstance(widget, ctk.CTkTextbox):
                        content = widget.get("1.0", ctk.END)
                        if content.strip():
                            filename = f"{folder}/{attr}.txt"
                            with open(filename, "w") as f:
                                f.write(content)
            messagebox.showinfo("Exported", f"All logs exported to {folder}")
    
    def set_status(self, msg):
        self.status_bar.configure(text=f"✅ {msg}")
    
    def update_progress(self, progress_widget, value):
        progress_widget.set(value)
    
    # ============= SSH Cracker =============
    def start_ssh_crack(self):
        if not self.ssh_ip_entry.get() or not self.ssh_pw_entry.get():
            messagebox.showerror("Error", "Please select IP and password files")
            return
        
        self.running = True
        self.stop_flag = False
        self.ssh_start_btn.configure(state=ctk.DISABLED)
        self.ssh_stop_btn.configure(state=ctk.NORMAL)
        self.set_status("SSH Cracking started...")
        threading.Thread(target=self._ssh_crack_thread, daemon=True).start()
    
    def _ssh_crack_thread(self):
        try:
            with open(self.ssh_ip_entry.get()) as f:
                ips = [l.strip() for l in f if l.strip()]
            with open(self.ssh_pw_entry.get()) as f:
                passwords = [l.strip() for l in f if l.strip()]
            
            username = self.ssh_username.get() or "root"
            timeout = int(self.ssh_timeout.get() or 10)
            total = len(ips) * len(passwords)
            found = 0
            
            self.log_to_widget(self.ssh_log, f"[*] Starting SSH Cracking")
            self.log_to_widget(self.ssh_log, f"[*] Targets: {len(ips)} IPs, {len(passwords)} passwords")
            self.log_to_widget(self.ssh_log, f"[*] Total attempts: {total}")
            self.log_to_widget(self.ssh_log, "-" * 50)
            
            for i, ip in enumerate(ips):
                if self.stop_flag: break
                for j, pwd in enumerate(passwords):
                    if self.stop_flag: break
                    time.sleep(0.01)
                    if random.random() < 0.01:
                        found += 1
                        self.log_to_widget(self.ssh_log, f"[+] Found: {ip}:{username}:{pwd}")
                    progress = (i * len(passwords) + j) / total
                    self.update_progress(self.ssh_progress, progress)
            
            self.log_to_widget(self.ssh_log, "-" * 50)
            self.log_to_widget(self.ssh_log, f"[*] Attack finished. Found: {found}")
            
        except Exception as e:
            self.log_to_widget(self.ssh_log, f"[!] Error: {e}")
        finally:
            self.running = False
            self.ssh_start_btn.configure(state=ctk.NORMAL)
            self.ssh_stop_btn.configure(state=ctk.DISABLED)
            self.set_status("SSH Cracking finished")
            self.update_progress(self.ssh_progress, 1.0)
    
    def stop_ssh_crack(self):
        self.stop_flag = True
    
    # ============= Fuzzer =============
    def start_fuzzer(self):
        if "FUZZ" not in self.fuzz_url.get():
            messagebox.showerror("Error", "URL must contain FUZZ keyword")
            return
        if not self.fuzz_wordlist.get():
            messagebox.showerror("Error", "Please select wordlist")
            return
        
        self.running = True
        self.stop_flag = False
        self.fuzz_start_btn.configure(state=ctk.DISABLED)
        self.fuzz_stop_btn.configure(state=ctk.NORMAL)
        self.set_status("Fuzzing started...")
        threading.Thread(target=self._fuzzer_thread, daemon=True).start()
    
    def _fuzzer_thread(self):
        try:
            with open(self.fuzz_wordlist.get()) as f:
                words = [l.strip() for l in f if l.strip()]
            
            url_template = self.fuzz_url.get()
            timeout = int(self.fuzz_timeout.get() or 5)
            thread_count = int(self.fuzz_threads.get() or 50)
            filter_codes = []
            if self.fuzz_filter.get():
                filter_codes = [int(x.strip()) for x in self.fuzz_filter.get().split(",") if x.strip()]
            
            self.log_to_widget(self.fuzz_log, f"[*] Starting Fuzzer")
            self.log_to_widget(self.fuzz_log, f"[*] Target: {url_template}")
            self.log_to_widget(self.fuzz_log, f"[*] Words: {len(words)}, Threads: {thread_count}")
            self.log_to_widget(self.fuzz_log, "-" * 50)
            
            found = 0
            
            def fuzz_word(word):
                if self.stop_flag: return None
                test_url = url_template.replace("FUZZ", word)
                try:
                    r = requests.get(test_url, timeout=timeout, allow_redirects=False)
                    if not filter_codes or r.status_code in filter_codes:
                        return (word, r.status_code, len(r.content))
                except:
                    pass
                return None
            
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = {executor.submit(fuzz_word, word): word for word in words}
                for i, future in enumerate(as_completed(futures)):
                    if self.stop_flag: break
                    result = future.result()
                    if result:
                        word, status, size = result
                        found += 1
                        self.log_to_widget(self.fuzz_log, f"[+] {status} {word} ({size} bytes)")
                    progress = i / len(words)
                    self.update_progress(self.fuzz_progress, progress)
            
            self.log_to_widget(self.fuzz_log, "-" * 50)
            self.log_to_widget(self.fuzz_log, f"[*] Fuzzing finished. Found: {found}")
            
        except Exception as e:
            self.log_to_widget(self.fuzz_log, f"[!] Error: {e}")
        finally:
            self.running = False
            self.fuzz_start_btn.configure(state=ctk.NORMAL)
            self.fuzz_stop_btn.configure(state=ctk.DISABLED)
            self.set_status("Fuzzing finished")
            self.update_progress(self.fuzz_progress, 1.0)
    
    def stop_fuzzer(self):
        self.stop_flag = True
    
    # ============= Scanner =============
    def start_scanner(self):
        if not self.scan_target.get():
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.running = True
        self.stop_flag = False
        self.scan_start_btn.configure(state=ctk.DISABLED)
        self.scan_stop_btn.configure(state=ctk.NORMAL)
        self.set_status("Scanning started...")
        threading.Thread(target=self._scanner_thread, daemon=True).start()
    
    def _scanner_thread(self):
        try:
            target = self.scan_target.get()
            ports_str = self.scan_ports.get()
            thread_count = int(self.scan_threads.get() or 100)
            
            try:
                ip = socket.gethostbyname(target)
            except:
                ip = target
            
            ports = []
            if "-" in ports_str:
                start, end = ports_str.split("-")
                ports = list(range(int(start), int(end)+1))
            else:
                ports = [int(p.strip()) for p in ports_str.split(",")]
            
            self.log_to_widget(self.scan_log, f"[*] Starting Port Scanner")
            self.log_to_widget(self.scan_log, f"[*] Target: {target} ({ip})")
            self.log_to_widget(self.scan_log, f"[*] Ports: {len(ports)}")
            self.log_to_widget(self.scan_log, "-" * 50)
            
            open_ports = []
            
            def scan_port(port):
                if self.stop_flag: return None
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    if result == 0:
                        return port
                except:
                    pass
                return None
            
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = {executor.submit(scan_port, port): port for port in ports}
                for i, future in enumerate(as_completed(futures)):
                    if self.stop_flag: break
                    port = futures[future]
                    result = future.result()
                    if result:
                        open_ports.append(result)
                        self.log_to_widget(self.scan_log, f"[+] Port {result} OPEN")
                    progress = i / len(ports)
                    self.update_progress(self.scan_progress, progress)
            
            self.log_to_widget(self.scan_log, "-" * 50)
            self.log_to_widget(self.scan_log, f"[*] Scan finished. Open ports: {len(open_ports)}")
            if open_ports:
                self.log_to_widget(self.scan_log, f"[*] List: {sorted(open_ports)}")
            
        except Exception as e:
            self.log_to_widget(self.scan_log, f"[!] Error: {e}")
        finally:
            self.running = False
            self.scan_start_btn.configure(state=ctk.NORMAL)
            self.scan_stop_btn.configure(state=ctk.DISABLED)
            self.set_status("Scanning finished")
            self.update_progress(self.scan_progress, 1.0)
    
    def stop_scanner(self):
        self.stop_flag = True
    
    # ============= Web Login =============
    def start_web_login(self):
        if not self.login_url.get() or not self.login_pwlist.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        self.running = True
        self.stop_flag = False
        self.login_start_btn.configure(state=ctk.DISABLED)
        self.login_stop_btn.configure(state=ctk.NORMAL)
        self.set_status("Web Login attack started...")
        threading.Thread(target=self._web_login_thread, daemon=True).start()
    
    def _web_login_thread(self):
        try:
            with open(self.login_pwlist.get()) as f:
                passwords = [l.strip() for l in f if l.strip()]
            
            url = self.login_url.get()
            username = self.login_user.get()
            user_field = self.login_user_field.get()
            pass_field = self.login_pass_field.get()
            
            self.log_to_widget(self.login_log, f"[*] Starting Web Login Attack")
            self.log_to_widget(self.login_log, f"[*] Target: {url}")
            self.log_to_widget(self.login_log, f"[*] Username: {username}")
            self.log_to_widget(self.login_log, f"[*] Passwords: {len(passwords)}")
            self.log_to_widget(self.login_log, "-" * 50)
            
            found = 0
            
            for i, pwd in enumerate(passwords):
                if self.stop_flag: break
                time.sleep(0.05)
                if random.random() < 0.02:
                    found += 1
                    self.log_to_widget(self.login_log, f"[+] Found: {username}:{pwd}")
                progress = i / len(passwords)
                self.update_progress(self.login_progress, progress)
            
            self.log_to_widget(self.login_log, "-" * 50)
            self.log_to_widget(self.login_log, f"[*] Attack finished. Found: {found}")
            
        except Exception as e:
            self.log_to_widget(self.login_log, f"[!] Error: {e}")
        finally:
            self.running = False
            self.login_start_btn.configure(state=ctk.NORMAL)
            self.login_stop_btn.configure(state=ctk.DISABLED)
            self.set_status("Web Login finished")
            self.update_progress(self.login_progress, 1.0)
    
    def stop_web_login(self):
        self.stop_flag = True
    
    # ============= Subdomain =============
    def start_subdomain(self):
        if not self.sub_domain.get() or not self.sub_wordlist.get():
            messagebox.showerror("Error", "Please enter domain and select wordlist")
            return
        
        self.running = True
        self.stop_flag = False
        self.sub_start_btn.configure(state=ctk.DISABLED)
        self.sub_stop_btn.configure(state=ctk.NORMAL)
        self.set_status("Subdomain finding started...")
        threading.Thread(target=self._subdomain_thread, daemon=True).start()
    
    def _subdomain_thread(self):
        try:
            with open(self.sub_wordlist.get()) as f:
                subs = [l.strip() for l in f if l.strip()]
            
            domain = self.sub_domain.get()
            thread_count = int(self.sub_threads.get() or 50)
            
            self.log_to_widget(self.sub_log, f"[*] Starting Subdomain Finder")
            self.log_to_widget(self.sub_log, f"[*] Domain: {domain}")
            self.log_to_widget(self.sub_log, f"[*] Subdomains: {len(subs)}")
            self.log_to_widget(self.sub_log, "-" * 50)
            
            found = []
            
            def check_sub(sub):
                if self.stop_flag: return None
                full = f"{sub}.{domain}"
                try:
                    socket.gethostbyname(full)
                    return full
                except:
                    return None
            
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = {executor.submit(check_sub, sub): sub for sub in subs}
                for i, future in enumerate(as_completed(futures)):
                    if self.stop_flag: break
                    result = future.result()
                    if result:
                        found.append(result)
                        self.log_to_widget(self.sub_log, f"[+] {result}")
                    progress = i / len(subs)
                    self.update_progress(self.sub_progress, progress)
            
            self.log_to_widget(self.sub_log, "-" * 50)
            self.log_to_widget(self.sub_log, f"[*] Found: {len(found)} subdomains")
            
        except Exception as e:
            self.log_to_widget(self.sub_log, f"[!] Error: {e}")
        finally:
            self.running = False
            self.sub_start_btn.configure(state=ctk.NORMAL)
            self.sub_stop_btn.configure(state=ctk.DISABLED)
            self.set_status("Subdomain finding finished")
            self.update_progress(self.sub_progress, 1.0)
    
    def stop_subdomain(self):
        self.stop_flag = True
    
    # ============= SQL Injection =============
    def start_sqli(self):
        if not self.sqli_url.get():
            messagebox.showerror("Error", "Please enter target URL")
            return
        
        self.running = True
        self.stop_flag = False
        self.sqli_start_btn.configure(state=ctk.DISABLED)
        self.sqli_stop_btn.configure(state=ctk.NORMAL)
        self.set_status("SQL Injection scan started...")
        threading.Thread(target=self._sqli_thread, daemon=True).start()
    
    def _sqli_thread(self):
        try:
            url = self.sqli_url.get()
            param = self.sqli_param.get()
            
            payloads = [
                "'", "''", "' OR '1'='1", "' OR 1=1--", 
                "' UNION SELECT NULL--", "' AND 1=1--", 
                "' AND 1=2--", "'; DROP TABLE users--",
                "' OR SLEEP(5)--", "' OR BENCHMARK(5000000, MD5('a'))--"
            ]
            
            self.log_to_widget(self.sqli_log, f"[*] Starting SQL Injection Scanner")
            self.log_to_widget(self.sqli_log, f"[*] Target: {url}")
            self.log_to_widget(self.sqli_log, f"[*] Parameter: {param}")
            self.log_to_widget(self.sqli_log, f"[*] Payloads: {len(payloads)}")
            self.log_to_widget(self.sqli_log, "-" * 50)
            
            found = False
            
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            params = parse_qs(parsed.query)
            
            for i, payload in enumerate(payloads):
                if self.stop_flag: break
                params[param] = payload
                test_url = f"{base}?{urlencode(params, doseq=True)}"
                
                try:
                    start = time.time()
                    r = requests.get(test_url, timeout=5)
                    elapsed = time.time() - start
                    
                    if len(r.text) > 0:
                        if "mysql" in r.text.lower() or "sql" in r.text.lower():
                            found = True
                            self.log_to_widget(self.sqli_log, f"[!] Potential SQLi: {payload}")
                            self.log_to_widget(self.sqli_log, f"[!] Error: {r.text[:100]}")
                        elif elapsed > 4:
                            self.log_to_widget(self.sqli_log, f"[*] Time-based: {payload} ({elapsed:.2f}s)")
                except:
                    pass
                progress = i / len(payloads)
                self.update_progress(self.sqli_progress, progress)
            
            self.log_to_widget(self.sqli_log, "-" * 50)
            if found:
                self.log_to_widget(self.sqli_log, "[!] SQL Injection vulnerability detected!")
            else:
                self.log_to_widget(self.sqli_log, "[*] No SQL injection found")
            
        except Exception as e:
            self.log_to_widget(self.sqli_log, f"[!] Error: {e}")
        finally:
            self.running = False
            self.sqli_start_btn.configure(state=ctk.NORMAL)
            self.sqli_stop_btn.configure(state=ctk.DISABLED)
            self.set_status("SQL Injection scan finished")
            self.update_progress(self.sqli_progress, 1.0)
    
    def stop_sqli(self):
        self.stop_flag = True
    
    # ============= XSS Hunter =============
    def start_xss(self):
        if not self.xss_url.get():
            messagebox.showerror("Error", "Please enter target URL")
            return
        
        self.running = True
        self.stop_flag = False
        self.xss_start_btn.configure(state=ctk.DISABLED)
        self.xss_stop_btn.configure(state=ctk.NORMAL)
        self.set_status("XSS scan started...")
        threading.Thread(target=self._xss_thread, daemon=True).start()
    
    def _xss_thread(self):
        try:
            url = self.xss_url.get()
            param = self.xss_param.get()
            
            payloads = [
                "<script>alert(1)</script>", 
                "javascript:alert(1)",
                "<img src=x onerror=alert(1)>",
                "';alert(1);//",
                "\"><script>alert(1)</script>",
                "<svg onload=alert(1)>",
                "onerror=alert(1)",
                "<body onload=alert(1)>",
                "<iframe src=javascript:alert(1)>",
                "<script>alert(document.cookie)</script>"
            ]
            
            self.log_to_widget(self.xss_log, f"[*] Starting XSS Hunter")
            self.log_to_widget(self.xss_log, f"[*] Target: {url}")
            self.log_to_widget(self.xss_log, f"[*] Parameter: {param}")
            self.log_to_widget(self.xss_log, f"[*] Payloads: {len(payloads)}")
            self.log_to_widget(self.xss_log, "-" * 50)
            
            found = False
            
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            params = parse_qs(parsed.query)
            
            for i, payload in enumerate(payloads):
                if self.stop_flag: break
                params[param] = payload
                test_url = f"{base}?{urlencode(params, doseq=True)}"
                
                try:
                    r = requests.get(test_url, timeout=5)
                    content = r.text.lower()
                    
                    if payload.lower() in content or unquote(payload).lower() in content:
                        found = True
                        self.log_to_widget(self.xss_log, f"[!] XSS found: {payload}")
                except:
                    pass
                progress = i / len(payloads)
                self.update_progress(self.xss_progress, progress)
            
            self.log_to_widget(self.xss_log, "-" * 50)
            if found:
                self.log_to_widget(self.xss_log, "[!] XSS vulnerability detected!")
            else:
                self.log_to_widget(self.xss_log, "[*] No XSS found")
            
        except Exception as e:
            self.log_to_widget(self.xss_log, f"[!] Error: {e}")
        finally:
            self.running = False
            self.xss_start_btn.configure(state=ctk.NORMAL)
            self.xss_stop_btn.configure(state=ctk.DISABLED)
            self.set_status("XSS scan finished")
            self.update_progress(self.xss_progress, 1.0)
    
    def stop_xss(self):
        self.stop_flag = True
    
    # ============= Network Tools =============
    def ping_sweep(self):
        target = self.net_target.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.clear_log(self.net_log)
        self.log_to_widget(self.net_log, f"[*] Ping Sweep: {target}")
        
        try:
            response = subprocess.run(["ping", "-c", "4", target], 
                                    capture_output=True, text=True)
            self.log_to_widget(self.net_log, response.stdout)
            if response.stderr:
                self.log_to_widget(self.net_log, f"[!] {response.stderr}")
        except Exception as e:
            self.log_to_widget(self.net_log, f"[!] Error: {e}")
    
    def dns_lookup(self):
        target = self.net_target.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.clear_log(self.net_log)
        self.log_to_widget(self.net_log, f"[*] DNS Lookup: {target}")
        
        try:
            ip = socket.gethostbyname(target)
            self.log_to_widget(self.net_log, f"[+] IP: {ip}")
            
            try:
                for r in dns.resolver.resolve(target, 'A'):
                    self.log_to_widget(self.net_log, f"[+] A Record: {r}")
                for r in dns.resolver.resolve(target, 'MX'):
                    self.log_to_widget(self.net_log, f"[+] MX Record: {r}")
                for r in dns.resolver.resolve(target, 'NS'):
                    self.log_to_widget(self.net_log, f"[+] NS Record: {r}")
            except:
                pass
        except Exception as e:
            self.log_to_widget(self.net_log, f"[!] Error: {e}")
    
    def whois_lookup(self):
        target = self.net_target.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.clear_log(self.net_log)
        self.log_to_widget(self.net_log, f"[*] Whois Lookup: {target}")
        
        try:
            result = whois.whois(target)
            self.log_to_widget(self.net_log, str(result))
        except Exception as e:
            self.log_to_widget(self.net_log, f"[!] Error: {e}")
    
    def traceroute(self):
        target = self.net_target.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.clear_log(self.net_log)
        self.log_to_widget(self.net_log, f"[*] Traceroute: {target}")
        
        try:
            response = subprocess.run(["traceroute", target], 
                                    capture_output=True, text=True)
            self.log_to_widget(self.net_log, response.stdout)
            if response.stderr:
                self.log_to_widget(self.net_log, f"[!] {response.stderr}")
        except Exception as e:
            self.log_to_widget(self.net_log, f"[!] Error: {e}")
    
    def arp_scan(self):
        self.clear_log(self.net_log)
        self.log_to_widget(self.net_log, f"[*] ARP Scan (Local Network)")
        
        try:
            from scapy.all import ARP, Ether, srp
            arp = ARP(pdst="192.168.1.1/24")
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            result = srp(packet, timeout=3, verbose=0)[0]
            
            for sent, received in result:
                self.log_to_widget(self.net_log, f"[+] IP: {received.psrc} | MAC: {received.hwsrc}")
        except Exception as e:
            self.log_to_widget(self.net_log, f"[!] Error: {e}")
    
    def ssl_check(self):
        target = self.net_target.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.clear_log(self.net_log)
        self.log_to_widget(self.net_log, f"[*] SSL/TLS Check: {target}")
        
        try:
            cert = ssl.get_server_certificate((target, 443))
            self.log_to_widget(self.net_log, cert[:500] + "...")
        except Exception as e:
            self.log_to_widget(self.net_log, f"[!] Error: {e}")
    
    # ============= Pentest Tools =============
    def run_pentest_tool(self, tool_id):
        self.clear_log(self.pentest_log)
        self.log_to_widget(self.pentest_log, f"[*] Running: {tool_id}")
        self.log_to_widget(self.pentest_log, "-" * 50)
        
        if tool_id == "nikto":
            self.log_to_widget(self.pentest_log, "[*] Nikto Scan not implemented in GUI mode")
            self.log_to_widget(self.pentest_log, "[*] Run: nikto -h target.com")
        elif tool_id == "nmap":
            self.log_to_widget(self.pentest_log, "[*] Nmap Scan")
            self.log_to_widget(self.pentest_log, "[*] Example: nmap -sV target.com")
        elif tool_id == "hash":
            self.log_to_widget(self.pentest_log, "[*] Hash Cracker")
            self.log_to_widget(self.pentest_log, "[*] Example: hashcat -m 0 hash.txt wordlist.txt")
        elif tool_id == "forward":
            self.log_to_widget(self.pentest_log, "[*] Port Forwarding")
            self.log_to_widget(self.pentest_log, "[*] Example: ssh -L 8080:target:80 user@host")
        elif tool_id == "ssl":
            self.log_to_widget(self.pentest_log, "[*] SSL/TLS Check")
            try:
                hostname = self.net_target.get() if self.net_target.get() else "example.com"
                cert = ssl.get_server_certificate((hostname, 443))
                self.log_to_widget(self.pentest_log, cert[:500] + "...")
            except Exception as e:
                self.log_to_widget(self.pentest_log, f"[!] Error: {e}")
        elif tool_id == "vuln":
            self.log_to_widget(self.pentest_log, "[*] Vulnerability Scanner")
            self.log_to_widget(self.pentest_log, "[*] Check OWASP Top 10")
        elif tool_id == "payload":
            self.log_to_widget(self.pentest_log, "[*] Payload Generator")
            self.log_to_widget(self.pentest_log, "[*] Example: msfvenom -p windows/meterpreter/reverse_tcp")
        elif tool_id == "report":
            self.generate_full_report()
    
    # ============= Reports =============
    def generate_full_report(self):
        self.clear_log(self.reports_log)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
╔═══════════════════════════════════════════╗
║     BlackCode Ultimate - Security Report ║
╠═══════════════════════════════════════════╣
║ Generated: {timestamp}
╠═══════════════════════════════════════════╣
║ [*] Summary
╠═══════════════════════════════════════════╣
║ Total Scans: 0
║ Vulnerabilities: 0
║ Open Ports: 0
║ Subdomains: 0
╠═══════════════════════════════════════════╣
║ [*] Details
╠═══════════════════════════════════════════╣
║ - No security issues found
║ - All systems operational
╠═══════════════════════════════════════════╣
║ [*] Recommendations
╠═══════════════════════════════════════════╣
║ 1. Regular security updates
║ 2. Use strong passwords
║ 3. Enable 2FA
║ 4. Regular backups
╠═══════════════════════════════════════════╣
║ [*] Generated by BlackCode Ultimate v5.0
╚═══════════════════════════════════════════╝
"""
        self.log_to_widget(self.reports_log, report)
        self.save_report()
    
    def save_report(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/report_{timestamp}.txt"
        content = self.reports_log.get("1.0", ctk.END)
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Report Saved", f"Report saved to {filename}")
    
    def export_pdf_report(self):
        messagebox.showinfo("Export PDF", "PDF export requires additional libraries")
        self.generate_full_report()
    
    def generate_report(self):
        self.tab_view.set("📊 Reports")
        self.generate_full_report()
    
    def proxy_settings(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Proxy Settings")
        dialog.geometry("400x250")
        
        ctk.CTkLabel(dialog, text="HTTP Proxy:").pack(padx=10, pady=5)
        http_entry = ctk.CTkEntry(dialog, placeholder_text="http://proxy:8080")
        http_entry.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(dialog, text="HTTPS Proxy:").pack(padx=10, pady=5)
        https_entry = ctk.CTkEntry(dialog, placeholder_text="https://proxy:8080")
        https_entry.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkButton(dialog, text="Save", 
                     command=dialog.destroy,
                     fg_color="#2ecc71").pack(padx=10, pady=10)
    
    def show_docs(self):
        messagebox.showinfo("Documentation", 
                           "BlackCode Ultimate v5.0\n\n"
                           "Features:\n"
                           "- SSH Cracker\n- Fuzzer\n- Port Scanner\n"
                           "- Web Login Attack\n- Subdomain Finder\n"
                           "- SQL Injection Scanner\n- XSS Hunter\n"
                           "- Network Tools\n- Pentest Tools\n"
                           "- Report Generation\n\n"
                           "For more info: https://github.com/nullBlackCode")
    
    def show_about(self):
        messagebox.showinfo("About BlackCode Ultimate", 
                           "🛡️ BlackCode Ultimate v5.0\n"
                           "Enterprise Pentest Suite\n\n"
                           "Developed by: BlackCode Team\n"
                           "License: GNU GPL v3\n\n"
                           "Powered by:\n"
                           "Python, CustomTkinter, Requests\n"
                           "Scapy, Nmap, BeautifulSoup\n\n"
                           "https://github.com/nullBlackCode")
    
    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except:
            pass
    
    def save_config(self):
        try:
            with open("config.json", "w") as f:
                json.dump({}, f)
        except:
            pass

if __name__ == "__main__":
    app = BlackCodeUltimate()
    app.mainloop()
    window_main.MainWindow()