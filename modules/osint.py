# modules/osint.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import requests
import socket
import time
import re

class OSINT:
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
        
        ctk.CTkLabel(setting_frame, text="🎯 Target:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ctk.CTkEntry(setting_frame, placeholder_text="Email / Username / Domain", height=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="🔍 Type:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.type_menu = ctk.CTkOptionMenu(setting_frame, values=["Email", "Username", "Domain", "Phone"])
        self.type_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.type_menu.set("Email")
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        self.progress_bar.set(0)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Search", command=self.start_search,
                                      fg_color="#2ecc71", hover_color="#27ae60", height=35, width=100,
                                      font=ctk.CTkFont(weight="bold"))
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_search,
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
        filename = f"osint_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_search(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget("[*] Starting OSINT Search")
        self.app.set_status("OSINT search started...")
        
        threading.Thread(target=self._search_thread, daemon=True).start()
    
    def _search_thread(self):
        try:
            target = self.target_entry.get().strip()
            search_type = self.type_menu.get()
            
            self.log_to_widget(f"[*] Target: {target}")
            self.log_to_widget(f"[*] Type: {search_type}")
            self.log_to_widget("-" * 50)
            
            if search_type == "Email":
                self._search_email(target)
            elif search_type == "Username":
                self._search_username(target)
            elif search_type == "Domain":
                self._search_domain(target)
            elif search_type == "Phone":
                self._search_phone(target)
            
            self.log_to_widget("-" * 50)
            self.log_to_widget("[*] Search completed")
            
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.progress_bar.set(1.0)
            self.app.set_status("OSINT search finished")
    
    def _search_email(self, email):
        self.log_to_widget(f"[*] Searching email: {email}")
        
        # بررسی فرمت ایمیل
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.log_to_widget("[!] Invalid email format")
            return
        
        # بررسی دامنه ایمیل
        domain = email.split('@')[1]
        self.log_to_widget(f"[+] Domain: {domain}")
        
        # بررسی MX record
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            for mx in mx_records:
                self.log_to_widget(f"[+] MX Record: {mx.exchange}")
        except:
            pass
        
        # بررسی Have I Been Pwned (نمایشی)
        self.log_to_widget("[*] Checking Have I Been Pwned...")
        try:
            response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", timeout=10)
            if response.status_code == 200:
                breaches = response.json()
                self.log_to_widget(f"[!] Email found in {len(breaches)} breaches!")
                for breach in breaches[:5]:
                    self.log_to_widget(f"    - {breach['Name']} ({breach['BreachDate']})")
            elif response.status_code == 404:
                self.log_to_widget("[+] Email not found in any breaches")
        except:
            self.log_to_widget("[!] Could not check Have I Been Pwned")
        
        self.progress_bar.set(1.0)
    
    def _search_username(self, username):
        self.log_to_widget(f"[*] Searching username: {username}")
        
        sites = {
            "GitHub": f"https://github.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "Tumblr": f"https://{username}.tumblr.com",
            "Medium": f"https://medium.com/@{username}",
            "Dev.to": f"https://dev.to/{username}",
            "GitLab": f"https://gitlab.com/{username}"
        }
        
        found = 0
        for site, url in sites.items():
            if self.stop_flag: break
            try:
                r = requests.get(url, timeout=5, allow_redirects=False)
                if r.status_code == 200:
                    self.log_to_widget(f"[+] {site}: {url}")
                    found += 1
                elif r.status_code == 302:
                    self.log_to_widget(f"[+] {site}: {url} (Redirect)")
                    found += 1
            except:
                pass
            self.progress_bar.set(found / len(sites))
        
        self.log_to_widget(f"[*] Found on {found}/{len(sites)} sites")
    
    def _search_domain(self, domain):
        self.log_to_widget(f"[*] Searching domain: {domain}")
        
        try:
            ip = socket.gethostbyname(domain)
            self.log_to_widget(f"[+] IP Address: {ip}")
        except:
            self.log_to_widget("[!] Could not resolve domain")
        
        try:
            import whois
            w = whois.whois(domain)
            self.log_to_widget(f"[+] Registrar: {w.registrar}")
            self.log_to_widget(f"[+] Creation Date: {w.creation_date}")
            self.log_to_widget(f"[+] Expiration Date: {w.expiration_date}")
            self.log_to_widget(f"[+] Name Servers: {w.name_servers}")
        except:
            self.log_to_widget("[!] Could not get WHOIS info")
        
        try:
            import dns.resolver
            for record_type in ['A', 'MX', 'NS', 'TXT']:
                try:
                    records = dns.resolver.resolve(domain, record_type)
                    for r in records:
                        self.log_to_widget(f"[+] {record_type}: {r}")
                except:
                    pass
        except:
            pass
        
        self.progress_bar.set(1.0)
    
    def _search_phone(self, phone):
        self.log_to_widget(f"[*] Searching phone: {phone}")
        
        # حذف کاراکترهای غیرعددی
        phone_clean = re.sub(r'\D', '', phone)
        self.log_to_widget(f"[+] Clean: {phone_clean}")
        
        # بررسی فرمت شماره
        if len(phone_clean) < 10:
            self.log_to_widget("[!] Phone number too short")
        else:
            self.log_to_widget("[*] Checking phone number...")
            try:
                response = requests.get(f"https://api.veriphone.io/v2/verify?phone={phone_clean}&key=demo", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_to_widget(f"[+] Country: {data.get('country_code')}")
                    self.log_to_widget(f"[+] Carrier: {data.get('carrier')}")
                    self.log_to_widget(f"[+] Valid: {data.get('valid')}")
            except:
                self.log_to_widget("[!] Could not verify phone number")
        
        self.progress_bar.set(1.0)
    
    def stop_search(self):
        self.stop_flag = True
