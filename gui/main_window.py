import tkinter as tk
from tkinter import ttk
from gui.profile_import import open_import_window
from gui.profile_export import open_export_window
import services.network as net
from tkinter import messagebox

class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Dynamic Template Profil Manager")
        root.geometry("400x200")

        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Importer profil", command=self.import_profile).pack(pady=10)
        ttk.Button(frame, text="Eksporter profil", command=self.export_profile).pack(pady=10)

    def check_network(self) -> bool:
        if not net.network_drive_available():
            messagebox.showerror("Network Error", "Network drive unavailable.")
            return False
        return True
        
    def import_profile(self):
        if self.check_network():
            open_import_window(self.root)

    def export_profile(self):
        if self.check_network():
            open_export_window(self.root)