# modules/web_login.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import requests
import time

class WebLogin:
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
        
        ctk.CTkLabel(setting_frame, text="🌐 Login URL:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com/login", height=30)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="👤 Username Field:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.user_field_entry = ctk.CTkEntry(setting_frame, placeholder_text="username", height=30)
        self.user_field_entry.insert(0, "username")
        self.user_field_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="🔑 Password Field:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=5, pady=5)
        self.pass_field_entry = ctk.CTkEntry(setting_frame, placeholder_text="password", height=30)
        self.pass_field_entry.insert(0, "password")
        self.pass_field_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="👤 Username:", font=ctk.CTkFont(size=12)).grid(row=3, column=0, padx=5, pady=5)
        self.user_entry = ctk.CTkEntry(setting_frame, placeholder_text="admin", height=30)
        self.user_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📁 Password List:", font=ctk.CTkFont(size=12)).grid(row=4, column=0, padx=5, pady=5)
        self.wordlist_entry = ctk.CTkEntry(setting_frame, placeholder_text="Select password list...", height=30)
        self.wordlist_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=30,
                     command=lambda: self.browse_file(self.wordlist_entry), fg_color="#3498db").grid(row=4, column=2, padx=5)
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=5, column=0, padx=5, pady=5, columnspan=3)
        self.progress_bar.set(0)
        
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
        filename = f"web_login_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_attack(self):
        if not self.url_entry.get() or not self.wordlist_entry.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget("[*] Starting Web Login Attack")
        self.app.set_status("Web Login attack started...")
        
        threading.Thread(target=self._attack_thread, daemon=True).start()
    
    def _attack_thread(self):
        try:
            with open(self.wordlist_entry.get()) as f:
                passwords = [l.strip() for l in f if l.strip()]
            
            url = self.url_entry.get()
            username = self.user_entry.get()
            user_field = self.user_field_entry.get()
            pass_field = self.pass_field_entry.get()
            proxies = self.app.get_proxy() if hasattr(self.app, 'get_proxy') else None
            found = 0
            
            self.log_to_widget(f"[*] Target: {url}")
            self.log_to_widget(f"[*] Username: {username}")
            self.log_to_widget(f"[*] Passwords: {len(passwords)}")
            self.log_to_widget("-" * 50)
            
            for i, pwd in enumerate(passwords):
                if self.stop_flag: break
                try:
                    data = {user_field: username, pass_field: pwd}
                    r = requests.post(url, data=data, timeout=5, proxies=proxies, allow_redirects=True)
                    if "login" not in r.url.lower() and "error" not in r.text.lower() and len(r.text) > 100:
                        found += 1
                        self.log_to_widget(f"[+] Found: {username}:{pwd}")
                        self.app.vulnerabilities.append({
                            'title': f'Web Login: {url}',
                            'description': f'Username: {username}\nPassword: {pwd}\nURL: {url}',
                            'severity': 'High',
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                except:
                    pass
                progress = i / len(passwords)
                self.progress_bar.set(progress)
            
            self.log_to_widget("-" * 50)
            self.log_to_widget(f"[*] Done. Found: {found}")
            
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.progress_bar.set(1.0)
            self.app.set_status("Web Login finished")
    
    def stop_attack(self):
        self.stop_flag = True
