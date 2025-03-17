import tkinter as tk
from tkinter import ttk
from gui.profile_import import open_import_window
from gui.profile_export import open_export_window
import services.network as net
from tkinter import messagebox
import hashlib
import json
from services import filesystem, network
import os

class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Dynamic Template Profil Manager")
        root.geometry("400x200")

        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Importer profil", command=self.import_profile).pack(pady=10)
        ttk.Button(frame, text="Eksporter profil", command=self.export_profile).pack(pady=10)
        ttk.Button(frame, text="Synkroniser profiler", command=self.sync_profiles).pack(pady=10)

        self.metadata_file = os.path.join(network.resolve_local_profiles_dir(), "profile_metadata.json")
        self.load_metadata()

    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.profile_metadata = json.load(f)
        else:
            self.profile_metadata = {}

    def save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.profile_metadata, f, indent=4)

    def calculate_checksum(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def check_network(self) -> bool:
        if not net.network_drive_available():
            messagebox.showerror("Network Error", "Network drive unavailable.")
            return False
        return True

    def sync_profiles(self):
        if not self.check_network():
            return

        local_dir = network.resolve_local_profiles_dir()
        username = os.getenv('USERNAME')
        network_dir = network.get_user_shared_profiles(username)

        local_profiles = filesystem.list_xml_files(local_dir)
        network_profiles = filesystem.list_xml_files(network_dir)

        # Sync from local to network
        for profile in local_profiles:
            local_path = os.path.join(local_dir, profile)
            network_path = os.path.join(network_dir, profile)

            # Check if the profile was originally exported by the current user
            original_user = self.profile_metadata.get(profile)
            if original_user == username:
                if not os.path.exists(network_path) or (
                    self.calculate_checksum(local_path) != self.calculate_checksum(network_path) and
                    os.path.getmtime(local_path) > os.path.getmtime(network_path)
                ):
                    filesystem.copy_file(local_path, network_path)

        # Sync from network to local
        for profile in network_profiles:
            network_path = os.path.join(network_dir, profile)
            local_path = os.path.join(local_dir, profile)

            # Update metadata to track the origin of new profiles
            if profile not in self.profile_metadata:
                self.profile_metadata[profile] = username

            if not os.path.exists(local_path) or (
                self.calculate_checksum(network_path) != self.calculate_checksum(local_path) and
                os.path.getmtime(network_path) > os.path.getmtime(local_path)
            ):
                filesystem.copy_file(network_path, local_path)

        self.save_metadata()
        messagebox.showinfo("Synkronisering fuldført.", "Dine profiler er blevet synkroniseret.")

    def import_profile(self):
        if self.check_network():
            open_import_window(self.root)

    def export_profile(self):
        if self.check_network():
            open_export_window(self.root)