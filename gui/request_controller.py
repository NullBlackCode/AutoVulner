# gui/request_controller.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import requests
import json
import time

class RequestController(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🌐 Request Controller - Burp Style")
        self.geometry("1000x800")
        self.resizable(True, True)
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header, text="🌐 Request Controller", 
                    font=ctk.CTkFont(size=22, weight="bold"), text_color="#00ff41").pack(side=ctk.LEFT)
        
        method_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        method_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(method_frame, text="Method:", font=ctk.CTkFont(size=13)).pack(side=ctk.LEFT, padx=5)
        self.method_combo = ctk.CTkOptionMenu(method_frame, values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        self.method_combo.pack(side=ctk.LEFT, padx=5)
        self.method_combo.set("GET")
        
        ctk.CTkLabel(method_frame, text="URL:", font=ctk.CTkFont(size=13)).pack(side=ctk.LEFT, padx=5)
        self.url_entry = ctk.CTkEntry(method_frame, placeholder_text="http://example.com/api", width=500, height=35)
        self.url_entry.pack(side=ctk.LEFT, padx=5, fill="x", expand=True)
        
        self.tab_view = ctk.CTkTabview(main_frame, corner_radius=10)
        self.tab_view.pack(fill="both", expand=True, pady=10)
        
        self.tab_view.add("📋 Headers")
        self.tab_view.add("📦 Body")
        self.tab_view.add("📊 Response")
        
        headers_tab = self.tab_view.tab("📋 Headers")
        self.headers_text = ctk.CTkTextbox(headers_tab, font=ctk.CTkFont(size=12), fg_color="#0a0a1a")
        self.headers_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.headers_text.insert("1.0", "Content-Type: application/json\nUser-Agent: BlackCode/8.0")
        
        body_tab = self.tab_view.tab("📦 Body")
        self.body_text = ctk.CTkTextbox(body_tab, font=ctk.CTkFont(size=12), fg_color="#0a0a1a")
        self.body_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.body_text.insert("1.0", '{"key": "value"}')
        
        response_tab = self.tab_view.tab("📊 Response")
        self.response_text = ctk.CTkTextbox(response_tab, font=ctk.CTkFont(size=12), fg_color="#0a0a1a", state="disabled")
        self.response_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_frame, text="🚀 Send", command=self.send_request,
                     fg_color="#2ecc71", hover_color="#27ae60", height=35, width=100,
                     font=ctk.CTkFont(weight="bold")).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="🗑️ Clear", command=self.clear_response,
                     fg_color="#e74c3c", hover_color="#c0392b", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="📋 Copy", command=self.copy_response,
                     fg_color="#3498db", hover_color="#2980b9", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save", command=self.save_request,
                     fg_color="#f39c12", hover_color="#e67e22", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="📂 Load", command=self.load_request,
                     fg_color="#9b59b6", hover_color="#8e44ad", height=35, width=100).pack(side=ctk.LEFT, padx=5)
    
    def send_request(self):
        try:
            method = self.method_combo.get()
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter URL")
                return
            
            headers_text = self.headers_text.get("1.0", ctk.END).strip()
            headers = {}
            for line in headers_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
            
            body = self.body_text.get("1.0", ctk.END).strip()
            
            self.response_text.configure(state="normal")
            self.response_text.delete("1.0", ctk.END)
            self.response_text.insert("1.0", f"⏳ Sending {method} request...\n\n")
            self.response_text.configure(state="disabled")
            self.update()
            
            start_time = time.time()
            
            if method == "GET":
                r = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                r = requests.post(url, headers=headers, data=body, timeout=30)
            elif method == "PUT":
                r = requests.put(url, headers=headers, data=body, timeout=30)
            elif method == "DELETE":
                r = requests.delete(url, headers=headers, timeout=30)
            else:
                r = requests.request(method, url, headers=headers, data=body, timeout=30)
            
            elapsed = time.time() - start_time
            
            self.response_text.configure(state="normal")
            self.response_text.delete("1.0", ctk.END)
            
            response_output = f"""
╔══════════════════════════════════════╗
║              RESPONSE                ║
╠══════════════════════════════════════╣
║ Status: {r.status_code} {r.reason}
║ Time: {elapsed:.3f}s
║ Size: {len(r.content)} bytes
╠══════════════════════════════════════╣
║ HEADERS
╠══════════════════════════════════════╣
"""
            for key, value in r.headers.items():
                response_output += f"  {key}: {value}\n"
            
            response_output += f"""
╠══════════════════════════════════════╣
║ BODY
╠══════════════════════════════════════╣
"""
            try:
                if 'application/json' in r.headers.get('Content-Type', ''):
                    response_output += json.dumps(r.json(), indent=2)[:3000]
                else:
                    response_output += r.text[:3000]
            except:
                response_output += r.text[:3000]
            
            if len(r.content) > 3000:
                response_output += "\n\n... (truncated)"
            
            self.response_text.insert("1.0", response_output)
            self.response_text.configure(state="disabled")
            
        except Exception as e:
            self.response_text.configure(state="normal")
            self.response_text.delete("1.0", ctk.END)
            self.response_text.insert("1.0", f"❌ Error: {str(e)}")
            self.response_text.configure(state="disabled")
    
    def clear_response(self):
        self.response_text.configure(state="normal")
        self.response_text.delete("1.0", ctk.END)
        self.response_text.configure(state="disabled")
    
    def copy_response(self):
        content = self.response_text.get("1.0", ctk.END)
        self.clipboard_clear()
        self.clipboard_append(content)
        messagebox.showinfo("Copied", "Response copied!")
    
    def save_request(self):
        data = {
            'method': self.method_combo.get(),
            'url': self.url_entry.get(),
            'headers': self.headers_text.get("1.0", ctk.END),
            'body': self.body_text.get("1.0", ctk.END)
        }
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", "Request saved!")
    
    def load_request(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r") as f:
                data = json.load(f)
            self.method_combo.set(data.get('method', 'GET'))
            self.url_entry.delete(0, ctk.END)
            self.url_entry.insert(0, data.get('url', ''))
            self.headers_text.delete("1.0", ctk.END)
            self.headers_text.insert("1.0", data.get('headers', ''))
            self.body_text.delete("1.0", ctk.END)
            self.body_text.insert("1.0", data.get('body', ''))
            messagebox.showinfo("Loaded", "Request loaded!")
