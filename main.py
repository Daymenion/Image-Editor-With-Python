import tkinter as tk
from tkinter import ttk
from interface import Interface
from InterfaceFunctions import InterfaceFunctions


class Main(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.filename = ""
        self.more_imageFilename = ""
        self.original_image = None
        self.processed_image = None
        self.rotating_image = None
        self.drawing_cache = list()
        self.more_image = None
        self.is_image_selected = False
        self.is_draw_state = False
        self.is_crop_state = False
        self.is_paste_state = False
        self.num_rows, self.num_cols = None, None
        self.filtering_frame = None
        self.adjusting_frame = None
        self.edge_detection_frame = None

        self.title("Image Editor by Daymenion")

        self.interface = Interface(master=self)
        separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        self.interface_functions = InterfaceFunctions(master=self)

        self.interface.pack(fill=tk.BOTH)
        separator1.pack(fill=tk.X, padx=10, pady=5)
        self.interface_functions.pack(fill=tk.BOTH, padx=10, pady=10, expand=1)
