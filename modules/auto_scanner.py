# modules/auto_scanner.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import requests
import socket
import ssl
import time
from urllib.parse import urlparse, parse_qs

class AutoScanner:
    def __init__(self, tab, app):
        self.app = app
        self.running = False
        self.stop_flag = False
        self.scan_progress_data = []
        self.start_time = 0
        self.create_widgets(tab)
        
    def create_widgets(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(3, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🎯 Target URL:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com", height=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📁 Wordlist:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.wordlist_entry = ctk.CTkEntry(setting_frame, placeholder_text="Select wordlist...", height=30)
        self.wordlist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=30,
                     command=lambda: self.browse_file(self.wordlist_entry), fg_color="#3498db").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=5, pady=5)
        self.threads_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.threads_entry.insert(0, "50")
        self.threads_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="⏱️ Timeout:", font=ctk.CTkFont(size=12)).grid(row=2, column=2, padx=5, pady=5)
        self.timeout_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.timeout_entry.insert(0, "10")
        self.timeout_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        scan_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        scan_frame.grid(row=3, column=0, padx=5, pady=5, columnspan=4, sticky="ew")
        
        ctk.CTkLabel(scan_frame, text="🔍 Scans:", font=ctk.CTkFont(size=12)).pack(side=ctk.LEFT, padx=5)
        
        self.sqli_check = ctk.CTkCheckBox(scan_frame, text="SQLi")
        self.sqli_check.pack(side=ctk.LEFT, padx=5)
        self.sqli_check.select()
        
        self.xss_check = ctk.CTkCheckBox(scan_frame, text="XSS")
        self.xss_check.pack(side=ctk.LEFT, padx=5)
        self.xss_check.select()
        
        self.port_check = ctk.CTkCheckBox(scan_frame, text="Port")
        self.port_check.pack(side=ctk.LEFT, padx=5)
        self.port_check.select()
        
        self.subdomain_check = ctk.CTkCheckBox(scan_frame, text="Subdomain")
        self.subdomain_check.pack(side=ctk.LEFT, padx=5)
        self.subdomain_check.select()
        
        self.ssl_check = ctk.CTkCheckBox(scan_frame, text="SSL")
        self.ssl_check.pack(side=ctk.LEFT, padx=5)
        self.ssl_check.select()
        
        self.header_check = ctk.CTkCheckBox(scan_frame, text="Headers")
        self.header_check.pack(side=ctk.LEFT, padx=5)
        self.header_check.select()
        
        self.tech_check = ctk.CTkCheckBox(scan_frame, text="Tech")
        self.tech_check.pack(side=ctk.LEFT, padx=5)
        self.tech_check.select()
        
        monitor_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#0a0a1a")
        monitor_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        monitor_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(monitor_frame, text="📊 Scan Monitor", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00ff41").pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(monitor_frame, height=25)
        self.progress_bar.pack(pady=5, padx=10, fill="x")
        self.progress_bar.set(0)
        
        progress_frame = ctk.CTkFrame(monitor_frame, fg_color="transparent")
        progress_frame.pack(fill="x", pady=5, padx=10)
        
        self.status_label = ctk.CTkLabel(progress_frame, text="⏳ Waiting to start...", font=ctk.CTkFont(size=12))
        self.status_label.pack(side=ctk.LEFT, padx=5)
        
        self.percent_label = ctk.CTkLabel(progress_frame, text="0%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00ff41")
        self.percent_label.pack(side=ctk.RIGHT, padx=5)
        
        stats_frame = ctk.CTkFrame(monitor_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=5, padx=10)
        
        self.found_label = ctk.CTkLabel(stats_frame, text="🔍 Found: 0", text_color="#ff6b6b", font=ctk.CTkFont(size=11))
        self.found_label.pack(side=ctk.LEFT, padx=5)
        
        self.scanned_label = ctk.CTkLabel(stats_frame, text="📡 Scanned: 0", text_color="#3498db", font=ctk.CTkFont(size=11))
        self.scanned_label.pack(side=ctk.LEFT, padx=15)
        
        self.elapsed_label = ctk.CTkLabel(stats_frame, text="⏱️ 00:00:00", font=ctk.CTkFont(size=11))
        self.elapsed_label.pack(side=ctk.RIGHT, padx=5)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start", command=self.start_scan,
                                      fg_color="#2ecc71", hover_color="#27ae60", height=40, width=120,
                                      font=ctk.CTkFont(weight="bold"))
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_scan,
                                     fg_color="#e74c3c", hover_color="#c0392b", height=40, width=100,
                                     state=ctk.DISABLED)
        self.stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save", command=self.save_log,
                     fg_color="#3498db", hover_color="#2980b9", height=30, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=self.clear_log,
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=30, width=80).pack(side=ctk.LEFT, padx=5)
    
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
        filename = f"auto_scan_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_scan(self):
        if not self.target_entry.get():
            messagebox.showerror("Error", "Please enter target URL")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.percent_label.configure(text="0%")
        self.found_label.configure(text="🔍 Found: 0")
        self.scanned_label.configure(text="📡 Scanned: 0")
        self.clear_log()
        self.log_to_widget("[*] Starting Auto Scanner")
        self.app.set_status("Auto Scan started...")
        self.start_time = time.time()
        
        threading.Thread(target=self._scan_thread, daemon=True).start()
        threading.Thread(target=self._update_monitor, daemon=True).start()
    
    def _update_monitor(self):
        while self.running:
            try:
                elapsed = time.time() - self.start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                self.elapsed_label.configure(text=f"⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}")
                self.update()
                time.sleep(0.5)
            except:
                break
    
    def _scan_thread(self):
        try:
            target = self.target_entry.get()
            timeout = int(self.timeout_entry.get() or 10)
            proxies = self.app.get_proxy() if hasattr(self.app, 'get_proxy') else None
            
            total_scans = 0
            total_scans += 1 if self.sqli_check.get() else 0
            total_scans += 1 if self.xss_check.get() else 0
            total_scans += 1 if self.port_check.get() else 0
            total_scans += 1 if self.subdomain_check.get() else 0
            total_scans += 1 if self.ssl_check.get() else 0
            total_scans += 1 if self.header_check.get() else 0
            total_scans += 1 if self.tech_check.get() else 0
            
            current_scan = 0
            total_vulns = 0
            scanned_items = 0
            
            self.log_to_widget(f"[*] Target: {target}")
            self.log_to_widget(f"[*] Scans: {total_scans}")
            self.log_to_widget("=" * 50)
            
            if self.sqli_check.get():
                current_scan += 1
                self.status_label.configure(text=f"🔄 SQLi ({current_scan}/{total_scans})...")
                self.progress_bar.set(current_scan/total_scans)
                self.percent_label.configure(text=f"{int((current_scan/total_scans)*100)}%")
                self.log_to_widget(f"\n[>] SQL Injection")
                
                parsed = urlparse(target)
                params = parse_qs(parsed.query)
                payloads = ["' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--"]
                
                for param in params:
                    for payload in payloads:
                        if self.stop_flag: break
                        test_url = f"{target}&{param}={payload}"
                        try:
                            r = requests.get(test_url, timeout=timeout, proxies=proxies)
                            scanned_items += 1
                            if "sql" in r.text.lower() or "mysql" in r.text.lower():
                                total_vulns += 1
                                self.found_label.configure(text=f"🔍 Found: {total_vulns}")
                                self.log_to_widget(f"[!] SQLi on {param}")
                                self.app.vulnerabilities.append({
                                    'title': 'SQL Injection (Auto)',
                                    'description': f'Parameter: {param}\nPayload: {payload}\nURL: {test_url}',
                                    'severity': 'Critical',
                                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                                })
                        except:
                            pass
                        self.scanned_label.configure(text=f"📡 Scanned: {scanned_items}")
            
            if self.xss_check.get():
                current_scan += 1
                self.status_label.configure(text=f"🔄 XSS ({current_scan}/{total_scans})...")
                self.progress_bar.set(current_scan/total_scans)
                self.percent_label.configure(text=f"{int((current_scan/total_scans)*100)}%")
                self.log_to_widget(f"\n[>] XSS")
                
                parsed = urlparse(target)
                params = parse_qs(parsed.query)
                payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
                
                for param in params:
                    for payload in payloads:
                        if self.stop_flag: break
                        test_url = f"{target}&{param}={payload}"
                        try:
                            r = requests.get(test_url, timeout=timeout, proxies=proxies)
                            scanned_items += 1
                            if payload in r.text:
                                total_vulns += 1
                                self.found_label.configure(text=f"🔍 Found: {total_vulns}")
                                self.log_to_widget(f"[!] XSS on {param}")
                                self.app.vulnerabilities.append({
                                    'title': 'XSS (Auto)',
                                    'description': f'Parameter: {param}\nPayload: {payload}\nURL: {test_url}',
                                    'severity': 'High',
                                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                                })
                        except:
                            pass
                        self.scanned_label.configure(text=f"📡 Scanned: {scanned_items}")
            
            if self.port_check.get():
                current_scan += 1
                self.status_label.configure(text=f"🔄 Port ({current_scan}/{total_scans})...")
                self.progress_bar.set(current_scan/total_scans)
                self.percent_label.configure(text=f"{int((current_scan/total_scans)*100)}%")
                self.log_to_widget(f"\n[>] Port Scan")
                
                try:
                    domain = target.replace("http://", "").replace("https://", "").split("/")[0]
                    ip = socket.gethostbyname(domain)
                    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, 8080]
                    open_ports = []
                    for port in common_ports:
                        if self.stop_flag: break
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.5)
                            result = sock.connect_ex((ip, port))
                            sock.close()
                            scanned_items += 1
                            if result == 0:
                                open_ports.append(port)
                                self.log_to_widget(f"[+] Port {port} OPEN")
                        except:
                            pass
                        self.scanned_label.configure(text=f"📡 Scanned: {scanned_items}")
                    
                    if open_ports:
                        total_vulns += 1
                        self.found_label.configure(text=f"🔍 Found: {total_vulns}")
                        self.app.vulnerabilities.append({
                            'title': 'Open Ports (Auto)',
                            'description': f'IP: {ip}\nOpen Ports: {sorted(open_ports)}',
                            'severity': 'Medium',
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                except:
                    pass
            
            if self.subdomain_check.get():
                current_scan += 1
                self.status_label.configure(text=f"🔄 Subdomain ({current_scan}/{total_scans})...")
                self.progress_bar.set(current_scan/total_scans)
                self.percent_label.configure(text=f"{int((current_scan/total_scans)*100)}%")
                self.log_to_widget(f"\n[>] Subdomain")
                
                try:
                    domain = target.replace("http://", "").replace("https://", "").split("/")[0]
                    sub_list = ['www', 'mail', 'ftp', 'admin', 'dev', 'test', 'staging', 'api', 'docs', 'blog']
                    found_subs = []
                    for sub in sub_list:
                        if self.stop_flag: break
                        full = f"{sub}.{domain}"
                        try:
                            socket.gethostbyname(full)
                            found_subs.append(full)
                            self.log_to_widget(f"[+] {full}")
                            scanned_items += 1
                        except:
                            pass
                        self.scanned_label.configure(text=f"📡 Scanned: {scanned_items}")
                    
                    if found_subs:
                        total_vulns += 1
                        self.found_label.configure(text=f"🔍 Found: {total_vulns}")
                        self.app.vulnerabilities.append({
                            'title': 'Subdomains (Auto)',
                            'description': f'Domain: {domain}\nSubdomains: {", ".join(found_subs)}',
                            'severity': 'Low',
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                except:
                    pass
            
            if self.ssl_check.get():
                current_scan += 1
                self.status_label.configure(text=f"🔄 SSL ({current_scan}/{total_scans})...")
                self.progress_bar.set(current_scan/total_scans)
                self.percent_label.configure(text=f"{int((current_scan/total_scans)*100)}%")
                self.log_to_widget(f"\n[>] SSL Check")
                
                try:
                    domain = target.replace("http://", "").replace("https://", "").split("/")[0]
                    context = ssl.create_default_context()
                    with context.wrap_socket(socket.socket(), server_hostname=domain) as s:
                        s.connect((domain, 443))
                        cert = s.getpeercert()
                        scanned_items += 1
                        if cert:
                            self.log_to_widget("[+] SSL Certificate found")
                        else:
                            total_vulns += 1
                            self.found_label.configure(text=f"🔍 Found: {total_vulns}")
                            self.app.vulnerabilities.append({
                                'title': 'Missing SSL (Auto)',
                                'description': f'Domain: {domain}\nNo valid SSL certificate',
                                'severity': 'High',
                                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                except:
                    self.log_to_widget("[!] SSL Check failed")
                    scanned_items += 1
                self.scanned_label.configure(text=f"📡 Scanned: {scanned_items}")
            
            if self.header_check.get():
                current_scan += 1
                self.status_label.configure(text=f"🔄 Headers ({current_scan}/{total_scans})...")
                self.progress_bar.set(current_scan/total_scans)
                self.percent_label.configure(text=f"{int((current_scan/total_scans)*100)}%")
                self.log_to_widget(f"\n[>] Header Analysis")
                
                try:
                    r = requests.get(target, timeout=timeout, proxies=proxies)
                    scanned_items += 1
                    headers = r.headers
                    security_headers = ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options']
                    missing = [h for h in security_headers if h not in headers]
                    if missing:
                        total_vulns += len(missing)
                        self.found_label.configure(text=f"🔍 Found: {total_vulns}")
                        self.log_to_widget(f"[!] Missing: {', '.join(missing)}")
                        self.app.vulnerabilities.append({
                            'title': 'Missing Headers (Auto)',
                            'description': f'Missing: {", ".join(missing)}\nTarget: {target}',
                            'severity': 'Medium',
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                except:
                    pass
                self.scanned_label.configure(text=f"📡 Scanned: {scanned_items}")
            
            if self.tech_check.get():
                current_scan += 1
                self.status_label.configure(text=f"🔄 Tech ({current_scan}/{total_scans})...")
                self.progress_bar.set(current_scan/total_scans)
                self.percent_label.configure(text=f"{int((current_scan/total_scans)*100)}%")
                self.log_to_widget(f"\n[>] Technology Detection")
                
                try:
                    r = requests.get(target, timeout=timeout, proxies=proxies)
                    scanned_items += 1
                    techs = []
                    if 'wp-content' in r.text:
                        techs.append('WordPress')
                    if 'drupal' in r.text.lower():
                        techs.append('Drupal')
                    if 'laravel' in r.text.lower():
                        techs.append('Laravel')
                    if 'django' in r.text.lower():
                        techs.append('Django')
                    if 'react' in r.text.lower():
                        techs.append('React')
                    if 'angular' in r.text.lower():
                        techs.append('Angular')
                    if 'vue' in r.text.lower():
                        techs.append('Vue.js')
                    if 'jquery' in r.text.lower():
                        techs.append('jQuery')
                    if 'bootstrap' in r.text.lower():
                        techs.append('Bootstrap')
                    
                    if techs:
                        self.log_to_widget(f"[+] Technologies: {', '.join(techs)}")
                except:
                    pass
                self.scanned_label.configure(text=f"📡 Scanned: {scanned_items}")
            
            self.status_label.configure(text="✅ Scan Completed!")
            self.progress_bar.set(1.0)
            self.percent_label.configure(text="100%")
            
            self.log_to_widget("\n" + "=" * 50)
            self.log_to_widget(f"[*] Auto Scan completed!")
            self.log_to_widget(f"[*] Vulnerabilities: {total_vulns}")
            self.log_to_widget(f"[*] Scanned: {scanned_items}")
            self.found_label.configure(text=f"🔍 Found: {total_vulns}")
            
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.app.set_status("Auto Scan finished")
    
    def stop_scan(self):
        self.stop_flag = True
        self.status_label.configure(text="⏹ Stopping...")
