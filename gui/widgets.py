import tkinter as tk
from tkinter import ttk

class ScrolledFrame(ttk.Frame):
    def __init__(self, parent, width=400, height=300, **kwargs):
        super().__init__(parent, **kwargs)

        # Create a canvas with a specified width/height and white background
        self.canvas = tk.Canvas(self, width=width, height=height, background='white', highlightthickness=0)
        
        # Vertical scrollbar linked to canvas yview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Frame configuration event binding for scrollbar activation
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Window inside canvas used to host the scrollable frame
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Linking canvas scrolling to scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Geometry management
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Ensuring canvas resizes properly
        self.canvas.bind('<Configure>', self._resize_frame)

    def _resize_frame(self, event):
        # Resizes the internal frame to fit the available horizontal space within the canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)