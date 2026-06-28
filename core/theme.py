import customtkinter as ctk

def setup_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

def get_style():
    return """
        QMainWindow { background-color: #0a0a1a; }
        QWidget { background-color: transparent; color: #c0c0c0; font-family: 'Segoe UI'; }
        QPushButton { background-color: #1a1a2e; color: #00ff41; border: 2px solid #00ff41; border-radius: 8px; padding: 8px; }
        QPushButton:hover { background-color: #00ff41; color: #0a0a1a; }
        QLineEdit, QTextEdit { background-color: #0f1a2b; color: #00ff41; border: 1px solid #00ff41; border-radius: 5px; padding: 5px; }
        QTabWidget::pane { border: 1px solid #00ff41; background-color: #0a0a1a; }
        QTabBar::tab { background-color: #1a1a2e; color: #8899aa; padding: 10px 20px; border: 1px solid #00ff41; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; }
        QTabBar::tab:selected { background-color: #00ff41; color: #0a0a1a; }
        QProgressBar { border: 1px solid #00ff41; border-radius: 5px; text-align: center; color: #ffffff; background-color: #0a0a1a; }
        QProgressBar::chunk { background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff41, stop:0.5 #00ccff, stop:1 #0066ff); border-radius: 5px; }
        QMenuBar { background-color: #0f1a2b; color: #00ff41; border-bottom: 2px solid #00ff41; }
        QMenuBar::item:selected { background-color: #00ff41; color: #0a0a1a; }
        QMenu { background-color: #0f1a2b; color: #00ff41; border: 1px solid #00ff41; }
        QMenu::item:selected { background-color: #00ff41; color: #0a0a1a; }
        QStatusBar { background-color: #0f1a2b; color: #00ff41; border-top: 1px solid #00ff41; }
    """
