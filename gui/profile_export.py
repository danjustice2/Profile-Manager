import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from gui.widgets import ScrolledFrame
from services import network, filesystem

def open_export_window(parent):
    username = os.getenv('USERNAME')
    export_dir = network.get_user_shared_profiles(username)
    os.makedirs(export_dir, exist_ok=True)

    local_profiles_dir = network.resolve_local_profiles_dir()
    if not os.path.exists(local_profiles_dir):
        messagebox.showerror("Fejl", "Ingen lokale profiler fundet til eksport.", parent=parent)
        return

    profiles = filesystem.list_xml_files(local_profiles_dir)
    if not profiles:
        messagebox.showerror("Fejl", "Ingen lokale profiler fundet til eksport.", parent=parent)
        return

    export_window = tk.Toplevel(parent)
    export_window.title("Eksporter dine profiler")
    export_window.geometry("400x500")

    scrolled_frame = ScrolledFrame(export_window)
    scrolled_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    profile_vars = []
    for profile in profiles:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(scrolled_frame.scrollable_frame, text=profile, variable=var)
        chk.pack(anchor='w', pady=2)
        profile_vars.append((profile, var))

    # Action handlers
    def export_selected():
        exported = False
        for profile_name, var in profile_vars:
            if var.get():
                src = os.path.join(local_profiles_dir, profile_name)
                dst = os.path.join(export_dir, profile_name)
                filesystem.copy_file(src, dst)
                exported = True
        if exported:
            messagebox.showinfo("Succes", f"Valgte profiler er eksporteret til {export_dir}!", parent=export_window)
        else:
            messagebox.showwarning(
                "Ingen profiler valgt", 
                "Venligst vælg mindst én profil til eksport.",
                parent=export_window
            )
        export_window.destroy()

    def select_all():
        for _, var in profile_vars:
            var.set(True)

    def deselect_all():
        for _, var in profile_vars:
            var.set(False)

    # Control buttons
    button_frame = ttk.Frame(export_window)
    button_frame.pack(pady=5)

    ttk.Button(button_frame, text="Vælg alle", command=select_all).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Fravælg alle", command=deselect_all).pack(side=tk.LEFT, padx=5)

    action_frame = ttk.Frame(export_window)
    action_frame.pack(pady=10)

    ttk.Button(action_frame, text="Eksporter valgte profiler", command=export_selected).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text="Annuller", command=export_window.destroy).pack(side=tk.LEFT, padx=5)

    export_window.bind("<Escape>", lambda e: export_window.destroy())