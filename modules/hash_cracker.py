import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import hashlib
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class HashCracker:
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
        
        ctk.CTkLabel(setting_frame, text="🎯 Hash:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.hash_entry = ctk.CTkEntry(setting_frame, placeholder_text="Enter hash to crack...", height=35)
        self.hash_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="📁 Wordlist:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.wordlist_entry = ctk.CTkEntry(setting_frame, placeholder_text="Select wordlist...", height=35)
        self.wordlist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(setting_frame, text="Browse", width=70, height=35,
                     command=self.browse_wordlist, fg_color="#3498db").grid(row=1, column=2, padx=5)
        
        ctk.CTkLabel(setting_frame, text="🔐 Hash Type:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=5, pady=5)
        self.hash_type = ctk.CTkOptionMenu(setting_frame, values=["MD5", "SHA1", "SHA256", "SHA512"])
        self.hash_type.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.hash_type.set("MD5")
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=12)).grid(row=2, column=2, padx=5, pady=5)
        self.threads_entry = ctk.CTkEntry(setting_frame, width=70, height=35)
        self.threads_entry.insert(0, "100")
        self.threads_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=3, column=0, padx=5, pady=5, columnspan=4)
        self.progress_bar.set(0)
        
        self.log = ctk.CTkTextbox(tab, wrap="word", state="disabled", font=ctk.CTkFont(size=11), fg_color="#0a0a1a")
        self.log.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start Cracking", command=self.start_crack,
                                      fg_color="#2ecc71", hover_color="#27ae60", height=35, width=120,
                                      font=ctk.CTkFont(weight="bold"))
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_crack,
                                     fg_color="#e74c3c", hover_color="#c0392b", height=35, width=80,
                                     state=ctk.DISABLED)
        self.stop_btn.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save Log", command=self.save_log,
                     fg_color="#3498db", hover_color="#2980b9", height=30, width=80).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=self.clear_log,
                     fg_color="#95a5a6", hover_color="#7f8c8d", height=30, width=70).pack(side=ctk.LEFT, padx=5)
        
    def browse_wordlist(self):
        path = filedialog.askopenfilename()
        if path:
            self.wordlist_entry.delete(0, ctk.END)
            self.wordlist_entry.insert(0, path)
            
    def log_to_widget(self, msg):
        self.log.configure(state="normal")
        self.log.insert(ctk.END, msg + "\n")
        self.log.see(ctk.END)
        self.log.configure(state="disabled")
        self.app.set_status("Hash Cracking...")
        
    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", ctk.END)
        self.log.configure(state="disabled")
        
    def save_log(self):
        content = self.log.get("1.0", ctk.END)
        filename = f"hash_crack_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
        
    def start_crack(self):
        target_hash = self.hash_entry.get().strip()
        wordlist_path = self.wordlist_entry.get().strip()
        
        if not target_hash or not wordlist_path:
            messagebox.showerror("Error", "Please enter hash and select wordlist")
            return
            
        if not os.path.exists(wordlist_path):
            messagebox.showerror("Error", "Wordlist file not found")
            return
            
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget(f"[*] Starting Hash Cracking")
        self.log_to_widget(f"[*] Hash: {target_hash}")
        self.log_to_widget(f"[*] Type: {self.hash_type.get()}")
        self.log_to_widget("-" * 50)
        
        threading.Thread(target=self._crack_thread, args=(target_hash, wordlist_path), daemon=True).start()
        
    def _crack_thread(self, target_hash, wordlist_path):
        try:
            hash_func = self._get_hash_func()
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [l.strip() for l in f if l.strip()]
                
            total = len(words)
            found = False
            
            with ThreadPoolExecutor(max_workers=int(self.threads_entry.get() or 100)) as executor:
                futures = {executor.submit(self._check_word, word, target_hash, hash_func): word for word in words}
                
                for i, future in enumerate(as_completed(futures)):
                    if self.stop_flag:
                        break
                    result = future.result()
                    if result:
                        found = True
                        self.log_to_widget(f"[+] Found: {result}")
                        self.app.vulnerabilities.append({
                            'title': 'Hash Cracked',
                            'description': f'Hash: {target_hash}\nPassword: {result}\nType: {self.hash_type.get()}',
                            'severity': 'Low',
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        break
                    progress = i / total
                    self.progress_bar.set(progress)
                    
            if not found and not self.stop_flag:
                self.log_to_widget("[*] Password not found in wordlist")
            elif self.stop_flag:
                self.log_to_widget("[!] Stopped by user")
                
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.progress_bar.set(1.0)
            self.app.set_status("Hash Cracking finished")
            
    def _get_hash_func(self):
        hash_type = self.hash_type.get()
        if hash_type == "MD5":
            return hashlib.md5
        elif hash_type == "SHA1":
            return hashlib.sha1
        elif hash_type == "SHA256":
            return hashlib.sha256
        elif hash_type == "SHA512":
            return hashlib.sha512
        return hashlib.md5
        
    def _check_word(self, word, target_hash, hash_func):
        if self.stop_flag:
            return None
        if hash_func(word.encode()).hexdigest() == target_hash:
            return word
        return None
        
    def stop_crack(self):
        self.stop_flag = True
