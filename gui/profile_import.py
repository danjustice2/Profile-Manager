import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List
from gui.widgets import ScrolledFrame
from services import network, filesystem

def open_import_window(parent):
    username = simpledialog.askstring("Brugernavn", "Indtast brugernavnet på den kollega, som har delt proflien:", parent=parent)
    
    if not username:
        return  # User clicked cancel or entered empty string
    
    user_profiles_dir = network.get_user_shared_profiles(username)
    
    if not os.path.exists(user_profiles_dir):
        messagebox.showerror("Fejl", f"Ingen profiler fundet for brugernavn '{username}'.", parent=parent)
        return

    profiles = filesystem.list_xml_files(user_profiles_dir)
    
    if not profiles:
        messagebox.showerror("Fejl", f"Ingen profiler fundet for brugernavn '{username}'.", parent=parent)
        return

    import_window = tk.Toplevel(parent)
    import_window.title(f"Importer profiler fra {username}")
    import_window.geometry("400x500")

    scrolled_frame = ScrolledFrame(import_window)
    scrolled_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    profile_vars = []
    for profile in profiles:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(scrolled_frame.scrollable_frame, text=profile, variable=var)
        chk.pack(anchor='w', pady=2)
        profile_vars.append((profile, var))

    # Action handlers
    def import_selected():
        imported = False
        dest_dir = network.resolve_local_profiles_dir()
        os.makedirs(dest_dir, exist_ok=True)
        for profile_name, var in profile_vars:
            if var.get():
                src = os.path.join(user_profiles_dir, profile_name)
                dst = os.path.join(dest_dir, profile_name)
                filesystem.copy_file(src, dst)
                imported = True
        if imported:
            messagebox.showinfo("Succes", "Valgte profiler er importeret!", parent=import_window)
        else:
            messagebox.showwarning("Ingen profiler valgt", "Venligst vælg mindst én profil til import.", parent=import_window)
        import_window.destroy()

    def select_all():
        for _, var in profile_vars:
            var.set(True)

    def deselect_all():
        for _, var in profile_vars:
            var.set(False)

    # Control buttons
    button_frame = ttk.Frame(import_window)
    button_frame.pack(pady=5)

    ttk.Button(button_frame, text="Vælg alle", command=select_all).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Fravælg alle", command=deselect_all).pack(side=tk.LEFT, padx=5)

    action_frame = ttk.Frame(import_window)
    action_frame.pack(pady=10)

    ttk.Button(action_frame, text="Importer valgte profiler", command=import_selected).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text="Annuller", command=import_window.destroy).pack(side=tk.LEFT, padx=5)

    import_window.bind("<Escape>", lambda e: import_window.destroy())