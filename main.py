import tkinter as tk
from tkinter import messagebox
from gui.main_window import MainWindow
import services.network as net
from config import get_config

CONFIG = get_config()

def show_splash_screen(root):
    """Create and display a splash screen."""
    splash = tk.Toplevel(root)
    splash.title("Indlæser...")
    splash.geometry("300x100")
    splash_label = tk.Label(splash, text="Indlæser Dynamic Template Profil Manager...", font=("Arial", 12))
    splash_label.pack(expand=True, fill=tk.BOTH)
    splash.update()
    return splash

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window during the splash screen

    # Show splash screen
    splash = show_splash_screen(root)

    # Perform network check
    if not net.network_drive_available():
        splash.destroy()  # Close the splash screen
        messagebox.showerror(
            "Netværksfejl",
            f"Netværksdrevet er utilgængeligt. Forbind til {CONFIG['local_organization_name']}s netværk og prøv igen."
        )
        return  # Exit the program if the network is unavailable

    # Close splash screen and show the main window
    splash.destroy()
    root.deiconify()  # Show the main window
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()