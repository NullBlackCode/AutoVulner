# modules/rdp_cracker.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import socket
import time
import os

class RDPCracker:
    def __init__(self, tab, app):
        self.app = app
        self.running = False
        self.stop_flag = False
        self.create_widgets(tab)
        
    def create_widgets(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        setting_frame.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(setting_frame, text="📁 IP:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.ip_type = ctk.CTkOptionMenu(setting_frame, values=["Single", "File"], width=80)
        self.ip_type.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.ip_type.set("File")
        self.ip_entry = ctk.CTkEntry(setting_frame, placeholder_text="Enter IP or select file...", height=30)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=30,
                     command=lambda: self.browse_file(self.ip_entry), fg_color="#3498db").grid(row=0, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="👤 User:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.user_type = ctk.CTkOptionMenu(setting_frame, values=["Single", "File"], width=80)
        self.user_type.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.user_type.set("Single")
        self.user_entry = ctk.CTkEntry(setting_frame, placeholder_text="Enter username or select file...", height=30)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=30,
                     command=lambda: self.browse_file(self.user_entry), fg_color="#3498db").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="📁 Password:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=5, pady=5)
        self.pw_type = ctk.CTkOptionMenu(setting_frame, values=["Single", "File"], width=80)
        self.pw_type.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.pw_type.set("File")
        self.pw_entry = ctk.CTkEntry(setting_frame, placeholder_text="Enter password or select file...", height=30)
        self.pw_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=30,
                     command=lambda: self.browse_file(self.pw_entry), fg_color="#3498db").grid(row=2, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=12)).grid(row=3, column=0, padx=5, pady=5)
        self.threads_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.threads_entry.insert(0, "30")
        self.threads_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="⏱️ Timeout:", font=ctk.CTkFont(size=12)).grid(row=3, column=2, padx=5, pady=5)
        self.timeout_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.timeout_entry.insert(0, "15")
        self.timeout_entry.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="🖥️ Port:", font=ctk.CTkFont(size=12)).grid(row=4, column=0, padx=5, pady=5)
        self.port_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.port_entry.insert(0, "3389")
        self.port_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=4, column=2, padx=5, pady=5, columnspan=2)
        self.progress_bar.set(0)
        
        stats_frame = ctk.CTkFrame(setting_frame, fg_color="#0a0a1a", corner_radius=8)
        stats_frame.grid(row=5, column=0, padx=5, pady=5, columnspan=4, sticky="ew")
        stat_row = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stat_row.pack()
        self.success_label = ctk.CTkLabel(stat_row, text="✅ Success: 0", text_color="#2ecc71", font=ctk.CTkFont(size=11))
        self.success_label.pack(side=ctk.LEFT, padx=10)
        self.fail_label = ctk.CTkLabel(stat_row, text="❌ Failed: 0", text_color="#e74c3c", font=ctk.CTkFont(size=11))
        self.fail_label.pack(side=ctk.LEFT, padx=10)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start", command=self.start_attack,
                                      fg_color="#2ecc71", hover_color="#27ae60", height=35, width=100,
                                      font=ctk.CTkFont(weight="bold"))
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_attack,
                                     fg_color="#e74c3c", hover_color="#c0392b", height=35, width=80,
                                     state=ctk.DISABLED)
        self.stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save", command=self.save_log,
                     fg_color="#3498db", hover_color="#2980b9", height=30, width=80).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=self.clear_log,
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=30, width=70).pack(side=ctk.LEFT, padx=5)
    
    def browse_file(self, entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, ctk.END)
            entry.insert(0, path)
    
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
        filename = f"rdp_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_attack(self):
        if not self.ip_entry.get() or not self.pw_entry.get():
            messagebox.showerror("Error", "Please select IP and password sources")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.success_label.configure(text="✅ Success: 0")
        self.fail_label.configure(text="❌ Failed: 0")
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget("[*] Starting RDP Cracking")
        self.app.set_status("RDP Cracking started...")
        
        threading.Thread(target=self._attack_thread, daemon=True).start()
    
    def _attack_thread(self):
        try:
            if self.ip_type.get() == "Single":
                ips = [self.ip_entry.get().strip()]
            else:
                with open(self.ip_entry.get()) as f:
                    ips = [l.strip() for l in f if l.strip()]
            
            if self.user_type.get() == "Single":
                users = [self.user_entry.get().strip() or "Administrator"]
            else:
                with open(self.user_entry.get()) as f:
                    users = [l.strip() for l in f if l.strip()]
            
            if self.pw_type.get() == "Single":
                passwords = [self.pw_entry.get().strip()]
            else:
                with open(self.pw_entry.get()) as f:
                    passwords = [l.strip() for l in f if l.strip()]
            
            timeout = int(self.timeout_entry.get() or 15)
            port = int(self.port_entry.get() or 3389)
            total = len(ips) * len(users) * len(passwords)
            found = 0
            failed = 0
            
            self.log_to_widget(f"[*] Targets: {len(ips)} IPs, {len(users)} users, {len(passwords)} passwords")
            self.log_to_widget(f"[*] Total attempts: {total}")
            self.log_to_widget("-" * 50)
            
            for i, ip in enumerate(ips):
                if self.stop_flag: break
                for user in users:
                    if self.stop_flag: break
                    for j, pwd in enumerate(passwords):
                        if self.stop_flag: break
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(timeout)
                            result = sock.connect_ex((ip, port))
                            sock.close()
                            if result == 0:
                                found += 1
                                self.success_label.configure(text=f"✅ Success: {found}")
                                self.log_to_widget(f"[+] Found: {ip}:{user}:{pwd}")
                                self.app.vulnerabilities.append({
                                    'title': f'RDP Credential: {ip}',
                                    'description': f'Username: {user}\nPassword: {pwd}\nIP: {ip}',
                                    'severity': 'Critical',
                                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                                })
                            else:
                                failed += 1
                                self.fail_label.configure(text=f"❌ Failed: {failed}")
                        except:
                            failed += 1
                            self.fail_label.configure(text=f"❌ Failed: {failed}")
                        
                        progress = (i * len(users) * len(passwords) + users.index(user) * len(passwords) + j) / total
                        self.progress_bar.set(progress)
            
            self.log_to_widget("-" * 50)
            self.log_to_widget(f"[*] Done. Found: {found}, Failed: {failed}")
            
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.progress_bar.set(1.0)
            self.app.set_status("RDP Cracking finished")
    
    def stop_attack(self):
        self.stop_flag = True
