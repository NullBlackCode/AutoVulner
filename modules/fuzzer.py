# modules/fuzzer.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class Fuzzer:
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
        
        ctk.CTkLabel(setting_frame, text="🎯 Target URL:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = ctk.CTkEntry(setting_frame, placeholder_text="http://example.com/FUZZ", height=30)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew", columnspan=3)
        
        ctk.CTkLabel(setting_frame, text="📁 Wordlist:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.wordlist_entry = ctk.CTkEntry(setting_frame, placeholder_text="Select wordlist...", height=30)
        self.wordlist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=30,
                     command=lambda: self.browse_file(self.wordlist_entry), fg_color="#3498db").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=5, pady=5)
        self.threads_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.threads_entry.insert(0, "100")
        self.threads_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="⏱️ Timeout:", font=ctk.CTkFont(size=12)).grid(row=2, column=2, padx=5, pady=5)
        self.timeout_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.timeout_entry.insert(0, "5")
        self.timeout_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="🔍 Filter:", font=ctk.CTkFont(size=12)).grid(row=3, column=0, padx=5, pady=5)
        self.filter_entry = ctk.CTkEntry(setting_frame, placeholder_text="200,301,302,403,500", height=30)
        self.filter_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=3, column=2, padx=5, pady=5, columnspan=2)
        self.progress_bar.set(0)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start", command=self.start_fuzzing,
                                      fg_color="#2ecc71", hover_color="#27ae60", height=35, width=100,
                                      font=ctk.CTkFont(weight="bold"))
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_fuzzing,
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
        filename = f"fuzz_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_fuzzing(self):
        if "FUZZ" not in self.url_entry.get():
            messagebox.showerror("Error", "URL must contain FUZZ keyword")
            return
        if not self.wordlist_entry.get():
            messagebox.showerror("Error", "Please select wordlist")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget("[*] Starting Fuzzer")
        self.app.set_status("Fuzzing started...")
        
        threading.Thread(target=self._fuzzing_thread, daemon=True).start()
    
    def _fuzzing_thread(self):
        try:
            with open(self.wordlist_entry.get()) as f:
                words = [l.strip() for l in f if l.strip()]
            
            url_template = self.url_entry.get()
            timeout = int(self.timeout_entry.get() or 5)
            thread_count = int(self.threads_entry.get() or 100)
            filter_codes = []
            if self.filter_entry.get():
                filter_codes = [int(x.strip()) for x in self.filter_entry.get().split(",") if x.strip()]
            
            self.log_to_widget(f"[*] Target: {url_template}")
            self.log_to_widget(f"[*] Words: {len(words)}, Threads: {thread_count}")
            self.log_to_widget("-" * 50)
            
            found = 0
            proxies = self.app.get_proxy() if hasattr(self.app, 'get_proxy') else None
            
            def fuzz_word(word):
                if self.stop_flag: return None
                test_url = url_template.replace("FUZZ", word)
                try:
                    r = requests.get(test_url, timeout=timeout, allow_redirects=False, proxies=proxies)
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
                        self.log_to_widget(f"[+] {status} {word} ({size} bytes)")
                        if status in [200, 301, 302]:
                            self.app.vulnerabilities.append({
                                'title': f'Directory: {word}',
                                'description': f'URL: {url_template.replace("FUZZ", word)}\nStatus: {status}',
                                'severity': 'Low',
                                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                    progress = i / len(words)
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
            self.app.set_status("Fuzzing finished")
    
    def stop_fuzzing(self):
        self.stop_flag = True
