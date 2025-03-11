import os
import hashlib
from tkinter import filedialog, messagebox, simpledialog, ttk
import win32com.client as win32
import tkinter as tk
import shutil
import json

class ScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.bind("<Enter>", self._bind_to_mousewheel)
        self.bind("<Leave>", self._unbind_from_mousewheel)

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_network_drive():
    if not os.path.exists('Q:\\'):
        messagebox.showerror("Netværksfejl", "Forbind til Tønder Kommunes netværk for at fortsætte.")
        return False
    return True

def profiles():
    if not check_network_drive():
        return
    
    profiles_dir = os.path.join(os.getenv('APPDATA'), 'dynamictemplate', 'Profiler')
    shared_profiles = os.path.join('Q:\\DynamicTemplate\\Delte Profiler')
    
    for file_name in os.listdir(profiles_dir):
        local_file_path = os.path.join(profiles_dir, file_name)
        remote_file_path = os.path.join(shared_profiles, file_name)
        
        if os.path.exists(remote_file_path):
            local_checksum = calculate_checksum(local_file_path)
            remote_checksum = calculate_checksum(remote_file_path)
            
            if local_checksum != remote_checksum:
                local_mtime = os.path.getmtime(local_file_path)
                remote_mtime = os.path.getmtime(remote_file_path)
                
                if local_mtime > remote_mtime:
                    shutil.copy(local_file_path, remote_file_path)
                else:
                    shutil.copy(remote_file_path, local_file_path)

def send_email():
    if not check_network_drive():
        return
    
    profiles_dir = os.path.join(os.getenv('APPDATA'), 'dynamictemplate', 'Profiler')
    file_path = filedialog.askopenfilename(initialdir=profiles_dir, title="Vælg profil til at sende", filetypes=[("XML filer", "*.xml")])
    if file_path:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Attachments.Add(file_path)
        mail.Display()
        messagebox.showinfo("Succes", "Outlook mail åbnet!")

def get_username():
    return simpledialog.askstring("Brugernavn", "Indtast brugernavn for at importere profiler:")

def get_profiles_dir():
    return os.path.join(os.getenv('APPDATA'), 'dynamictemplate', 'Profiler')

def get_shared_profiles_dir():
    return os.path.join('Q:\\DynamicTemplate\\Delte Profiler')

def import_profile():
    if not check_network_drive():
        return
    
    profiles_dir = get_profiles_dir()
    shared_profiles = get_shared_profiles_dir()
    
    while True:
        username = get_username()
        if username is None:  # User clicked cancel
            break
        if not username:
            messagebox.showerror("Fejl", "Brugernavn er påkrævet.")
            continue
        
        user_profiles_dir = os.path.join(shared_profiles, username)
        if not os.path.exists(user_profiles_dir):
            messagebox.showerror("Fejl", "Ingen profiler fundet for brugernavn " + username + ".")
            continue
        
        profiles = os.listdir(user_profiles_dir)
        if not profiles:
            messagebox.showerror("Fejl", "Ingen profiler fundet for brugernavn " + username + ".")
            continue
        
        import_window = tk.Toplevel()
        import_window.title("Vælg profiler til import")
        import_window.geometry("400x500")
        
        scroll_frame = ScrolledFrame(import_window)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        profile_vars = []
        for profile in profiles:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(scroll_frame.scrollable_frame, text=profile, variable=var)
            chk.pack(anchor='w')
            profile_vars.append((profile, var))
        
        def import_selected_profiles():
            for profile, var in profile_vars:
                if var.get():
                    file_path = os.path.join(user_profiles_dir, profile)
                    destination_path = os.path.join(profiles_dir, profile)
                    shutil.copy(file_path, destination_path)
            messagebox.showinfo("Succes", "Valgte profiler er importeret!")
            import_window.destroy()
        
        def select_all():
            for _, var in profile_vars:
                var.set(True)
        
        def deselect_all():
            for _, var in profile_vars:
                var.set(False)
        
        import_button = ttk.Button(import_window, text="Importér valgte profiler", command=import_selected_profiles)
        import_button.pack(pady=20)
        
        select_all_button = ttk.Button(import_window, text="Vælg alle", command=select_all)
        select_all_button.pack(pady=5)
        
        deselect_all_button = ttk.Button(import_window, text="Fravælg alle", command=deselect_all)
        deselect_all_button.pack(pady=5)
        
        cancel_button = ttk.Button(import_window, text="Annuller", command=import_window.destroy)
        cancel_button.pack(pady=20)
        
        import_window.bind("<Escape>", lambda event: import_window.destroy())
        break

def export_profile():
    if not check_network_drive():
        return
    
    username = os.getenv('USERNAME')
    export_dir = os.path.join('Q:\\DynamicTemplate\\Delte Profiler', username)
    try:
        os.makedirs(export_dir, exist_ok=True)
    except FileNotFoundError:
        messagebox.showerror("Netværksfejl", "Forbind til Tønder Kommunes netværk for at fortsætte.")
        return
    
    profiles_dir = os.path.join(os.getenv('APPDATA'), 'dynamictemplate', 'Profiler')
    local_profiles = os.listdir(profiles_dir)
    
    if local_profiles:
        export_window = tk.Toplevel()
        export_window.title("Vælg profiler til eksport")
        export_window.geometry("400x500")
        
        scroll_frame = ScrolledFrame(export_window)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        profile_vars = []
        for profile in local_profiles:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(scroll_frame.scrollable_frame, text=profile, variable=var)
            chk.pack(anchor='w')
            profile_vars.append((profile, var))
        
        def export_selected_profiles():
            for profile, var in profile_vars:
                if var.get():
                    file_path = os.path.join(profiles_dir, profile)
                    destination_path = os.path.join(export_dir, profile)
                    shutil.copy(file_path, destination_path)
            messagebox.showinfo("Succes", "Valgte profiler er eksporteret!")
            export_window.destroy()
        
        def select_all():
            for _, var in profile_vars:
                var.set(True)
        
        def deselect_all():
            for _, var in profile_vars:
                var.set(False)
        
        export_button = ttk.Button(export_window, text="Eksportér valgte profiler", command=export_selected_profiles)
        export_button.pack(pady=20)
        
        select_all_button = ttk.Button(export_window, text="Vælg alle", command=select_all)
        select_all_button.pack(pady=5)
        
        deselect_all_button = ttk.Button(export_window, text="Fravælg alle", command=deselect_all)
        deselect_all_button.pack(pady=5)
    else:
        messagebox.showerror("Fejl", "Ingen lokale profiler fundet.")

def create_gui():
    root = tk.Tk()
    root.title("Dynamic Template Profil Manager")
    root.geometry("400x200")

    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    import_button = ttk.Button(frame, text="Importer profil", command=import_profile)
    import_button.pack(pady=20)

    export_button = ttk.Button(frame, text="Eksporter profil", command=export_profile)
    export_button.pack(pady=20)

    root.mainloop()

create_gui()