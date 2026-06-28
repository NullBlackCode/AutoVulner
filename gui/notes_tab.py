# gui/notes_tab.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import time
import os

class NotesTab:
    def __init__(self, tab, app):
        self.app = app
        self.create_widgets(tab)
        self.load_notes()
        
    def create_widgets(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        header_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color="#1a1a2e")
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(header_frame, text="📝 Notes", 
                    font=ctk.CTkFont(size=16, weight="bold"), text_color="#00ff41").pack(side=ctk.LEFT, padx=10)
        
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side=ctk.RIGHT, padx=10)
        
        ctk.CTkButton(btn_frame, text="➕ Add", command=self.add_note,
                     fg_color="#2ecc71", hover_color="#27ae60", height=30, width=80).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="🗑️ Delete", command=self.delete_note,
                     fg_color="#e74c3c", hover_color="#c0392b", height=30, width=80).pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(btn_frame, text="💾 Save", command=self.save_notes,
                     fg_color="#3498db", hover_color="#2980b9", height=30, width=80).pack(side=ctk.LEFT, padx=5)
        
        self.notes_text = ctk.CTkTextbox(tab, wrap="word", state="normal",
                                         font=ctk.CTkFont(size=12), fg_color="#0a0a1a")
        self.notes_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.notes_text.insert("1.0", "# BlackCode Notes\n# Created: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    
    def add_note(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("📝 Add Note")
        dialog.geometry("500x400")
        
        frame = ctk.CTkFrame(dialog, corner_radius=15, fg_color="#1a1a2e")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Title:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        title_entry = ctk.CTkEntry(frame, placeholder_text="Enter note title...", height=35)
        title_entry.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(frame, text="Content:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        content_entry = ctk.CTkTextbox(frame, height=200, fg_color="#0a0a1a")
        content_entry.pack(padx=10, pady=5, fill="both", expand=True)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        def save():
            title = title_entry.get().strip()
            content = content_entry.get("1.0", ctk.END).strip()
            if title and content:
                note = f"\n\n=== {title} ===\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}\n{content}\n"
                self.notes_text.configure(state="normal")
                self.notes_text.insert(ctk.END, note)
                self.notes_text.configure(state="normal")
                self.notes_text.see(ctk.END)
                dialog.destroy()
                messagebox.showinfo("Saved", "Note saved!")
            else:
                messagebox.showerror("Error", "Please enter title and content")
        
        ctk.CTkButton(btn_frame, text="💾 Save", command=save,
                     fg_color="#2ecc71", hover_color="#27ae60", height=35, width=100).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="❌ Cancel", command=dialog.destroy,
                     fg_color="#e74c3c", hover_color="#c0392b", height=35, width=100).pack(side=ctk.LEFT, padx=5)
    
    def delete_note(self):
        if messagebox.askyesno("Delete", "Delete all notes?"):
            self.notes_text.configure(state="normal")
            self.notes_text.delete("1.0", ctk.END)
            self.notes_text.insert("1.0", "# BlackCode Notes\n# Created: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            self.notes_text.configure(state="normal")
    
    def save_notes(self):
        content = self.notes_text.get("1.0", ctk.END)
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Notes saved to {filename}")
    
    def load_notes(self):
        try:
            files = [f for f in os.listdir(".") if f.startswith("notes_")]
            if files:
                latest = sorted(files)[-1]
                with open(latest, "r") as f:
                    content = f.read()
                    self.notes_text.configure(state="normal")
                    self.notes_text.delete("1.0", ctk.END)
                    self.notes_text.insert("1.0", content)
                    self.notes_text.configure(state="normal")
        except:
            pass
