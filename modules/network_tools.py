# modules/network_tools.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import socket
import requests
import dns.resolver
import whois
import ssl
import time

class NetworkTools:
    def __init__(self, tab, app):
        self.app = app
        self.create_widgets(tab)
        
    def create_widgets(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🎯 Target:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ctk.CTkEntry(setting_frame, placeholder_text="IP or Domain", height=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tool_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        tool_frame.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        
        tools = [
            ("📡 Ping", self.ping_sweep, "#2ecc71"),
            ("🔍 DNS", self.dns_lookup, "#3498db"),
            ("📋 Whois", self.whois_lookup, "#9b59b6"),
            ("🔄 Traceroute", self.traceroute, "#f39c12"),
            ("🔐 SSL", self.ssl_check, "#1abc9c"),
            ("🕸️ IP Info", self.ip_info, "#00ff41")
        ]
        
        for i, (name, func, color) in enumerate(tools):
            btn = ctk.CTkButton(tool_frame, text=name, command=func,
                               fg_color=color, hover_color="#2c3e50",
                               height=30, width=100, font=ctk.CTkFont(size=11))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="💾 Save", command=self.save_log,
                     fg_color="#3498db", hover_color="#2980b9", height=30, width=80).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=self.clear_log,
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=30, width=70).pack(side=ctk.LEFT, padx=5)
    
    def log_to_widget(self, msg):
        self.log.configure(state="normal")
        self.log.insert(ctk.END, msg + "\n")
        self.log.see(ctk.END)
        self.log.configure(state="disabled")
    
    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", ctk.END)
        self.log.configure(state="disabled")
    
    def save_log(self):
        content = self.log.get("1.0", ctk.END)
        filename = f"network_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def ping_sweep(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        self.clear_log()
        self.log_to_widget(f"[*] Ping Sweep: {target}")
        try:
            response = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True)
            self.log_to_widget(response.stdout)
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
    
    def dns_lookup(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        self.clear_log()
        self.log_to_widget(f"[*] DNS Lookup: {target}")
        try:
            ip = socket.gethostbyname(target)
            self.log_to_widget(f"[+] IP: {ip}")
            try:
                for r in dns.resolver.resolve(target, 'A'):
                    self.log_to_widget(f"[+] A: {r}")
                for r in dns.resolver.resolve(target, 'MX'):
                    self.log_to_widget(f"[+] MX: {r}")
                for r in dns.resolver.resolve(target, 'NS'):
                    self.log_to_widget(f"[+] NS: {r}")
            except:
                pass
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
    
    def whois_lookup(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        self.clear_log()
        self.log_to_widget(f"[*] Whois: {target}")
        try:
            result = whois.whois(target)
            self.log_to_widget(str(result))
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
    
    def traceroute(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        self.clear_log()
        self.log_to_widget(f"[*] Traceroute: {target}")
        try:
            response = subprocess.run(["traceroute", target], capture_output=True, text=True)
            self.log_to_widget(response.stdout)
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
    
    def ssl_check(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        self.clear_log()
        self.log_to_widget(f"[*] SSL/TLS: {target}")
        try:
            cert = ssl.get_server_certificate((target, 443))
            self.log_to_widget(cert[:500] + "...")
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
    
    def ip_info(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        self.clear_log()
        self.log_to_widget(f"[*] IP Info: {target}")
        try:
            response = requests.get(f"http://ip-api.com/json/{target}")
            data = response.json()
            for key, value in data.items():
                self.log_to_widget(f"{key}: {value}")
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
