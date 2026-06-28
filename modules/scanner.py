# modules/scanner.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class Scanner:
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
        
        ctk.CTkLabel(setting_frame, text="🎯 Target:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ctk.CTkEntry(setting_frame, placeholder_text="IP or Domain", height=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew", columnspan=3)
        
        ctk.CTkLabel(setting_frame, text="📡 Ports:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=5, pady=5)
        self.ports_entry = ctk.CTkEntry(setting_frame, placeholder_text="1-1000 or 21,22,80", height=30)
        self.ports_entry.insert(0, "1-1000")
        self.ports_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(setting_frame, text="🧵 Threads:", font=ctk.CTkFont(size=12)).grid(row=1, column=2, padx=5, pady=5)
        self.threads_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.threads_entry.insert(0, "200")
        self.threads_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="⏱️ Timeout:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=5, pady=5)
        self.timeout_entry = ctk.CTkEntry(setting_frame, width=70, height=30)
        self.timeout_entry.insert(0, "1")
        self.timeout_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(setting_frame, height=18)
        self.progress_bar.grid(row=2, column=2, padx=5, pady=5, columnspan=2)
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
        filename = f"scan_log_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {filename}")
    
    def start_scan(self):
        if not self.target_entry.get():
            messagebox.showerror("Error", "Please enter target")
            return
        
        self.running = True
        self.stop_flag = False
        self.start_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        self.progress_bar.set(0)
        self.clear_log()
        self.log_to_widget("[*] Starting Port Scanner")
        self.app.set_status("Scanning started...")
        
        threading.Thread(target=self._scan_thread, daemon=True).start()
    
    def _scan_thread(self):
        try:
            target = self.target_entry.get()
            ports_str = self.ports_entry.get()
            thread_count = int(self.threads_entry.get() or 200)
            timeout = int(self.timeout_entry.get() or 1)
            
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
            
            self.log_to_widget(f"[*] Target: {target} ({ip})")
            self.log_to_widget(f"[*] Ports: {len(ports)}")
            self.log_to_widget("-" * 50)
            
            open_ports = []
            
            def scan_port(port):
                if self.stop_flag: return None
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
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
                        self.log_to_widget(f"[+] Port {result} OPEN")
                    progress = i / len(ports)
                    self.progress_bar.set(progress)
            
            self.log_to_widget("-" * 50)
            self.log_to_widget(f"[*] Done. Open ports: {len(open_ports)}")
            if open_ports:
                self.log_to_widget(f"[*] List: {sorted(open_ports)}")
                self.app.vulnerabilities.append({
                    'title': f'Open Ports: {target}',
                    'description': f'Open ports: {sorted(open_ports)}\nIP: {ip}',
                    'severity': 'Medium',
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
            
        except Exception as e:
            self.log_to_widget(f"[!] Error: {e}")
        finally:
            self.running = False
            self.start_btn.configure(state=ctk.NORMAL)
            self.stop_btn.configure(state=ctk.DISABLED)
            self.progress_bar.set(1.0)
            self.app.set_status("Scanning finished")
    
    def stop_scan(self):
        self.stop_flag = True
