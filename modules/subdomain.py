# modules/subdomain.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class Subdomain:
    def __init__(self, tab, app):
        self.app = app
        self.running = False
        self.stop_flag = False
        self.create_widgets(tab)
        
    def create_widgets(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        setting_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        setting_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setting_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(setting_frame, text="🌐 Domain:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.domain_entry = ctk.CTkEntry(setting_frame, placeholder_text="example.com", height=30)
        self.domain_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📁 Wordlist:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.wordlist_entry = ctk.CTkEntry(setting_frame, placeholder_text="Select subdomain wordlist...", height=30)
        self.wordlist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=30,
                     command=lambda: self.browse_file(self.wordlist_entry), fg_color="#3498db").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=5, pady=5)
        self.threads_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.threads_entry.insert(0, "100")
        self.threads_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=2, column=2, padx=5, pady=5)
        self.progress_bar.set(0)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start", command=self.start_finding,
                                      fg_color="#2ecc71", hover_color="#27ae60", height=35, width=100,
                                      font=ctk.CTkFont(weight="bold"))
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_finding,
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
        filename = f"subdomain_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_finding(self):
        if not self.domain_entry.get() or not self.wordlist_entry.get():
            messagebox.showerror("Error", "Please enter domain and select wordlist")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget("[*] Starting Subdomain Finder")
        self.app.set_status("Subdomain finding started...")
        
        threading.Thread(target=self._finding_thread, daemon=True).start()
    
    def _finding_thread(self):
        try:
            with open(self.wordlist_entry.get()) as f:
                subs = [l.strip() for l in f if l.strip()]
            
            domain = self.domain_entry.get()
            thread_count = int(self.threads_entry.get() or 100)
            
            self.log_to_widget(f"[*] Domain: {domain}")
            self.log_to_widget(f"[*] Subdomains: {len(subs)}")
            self.log_to_widget("-" * 50)
            
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
                        self.log_to_widget(f"[+] {result}")
                        self.app.vulnerabilities.append({
                            'title': f'Subdomain: {result}',
                            'description': f'Domain: {domain}\nSubdomain: {result}',
                            'severity': 'Low',
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                    progress = i / len(subs)
                    self.progress_bar.set(progress)
            
            self.log_to_widget("-" * 50)
            self.log_to_widget(f"[*] Done. Found: {len(found)}")
            
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.progress_bar.set(1.0)
            self.app.set_status("Subdomain finding finished")
    
    def stop_finding(self):
        self.stop_flag = True
