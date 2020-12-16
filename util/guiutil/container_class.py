import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import cv2 as cv
from util.cvutil import *
import numpy as np

class ImageCanvasContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        ############# create default class widgets ##########################
        self.height, self.width = 200, 200
        self.canvas = tk.Canvas(self, height=self.height, width=self.width)
        self.tk_img = ImageTk.PhotoImage(Image.fromarray(np.zeros((self.height,self.width,3), dtype=np.uint8)))
        self.canvas_controller = self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
        self.canvas.grid(row=0, column=0, sticky='EW')

    def update_image_canvas(self):
        self.canvas = tk.Canvas(self, height = self.img_height, width=self.img_width)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
        self.canvas.grid(row=0, column=0, sticky='EW')

class SelectFileContainer(ttk.Frame):
    def __init__(self, container, title=None, btn_title=None, **kwargs):
        super().__init__(container, **kwargs)

        ############### create class attributes #################
        if title is None:
            self.title = "Select file: "
        else:
            self.title=title

        if btn_title is None:
            self.btn_title = "Select"
        else:
            self.btn_title=btn_title

        self.selected_file = None
        # self.btn_command_list = [self.select_file]

        ############### create widgets ##########################
        self.title_lbl = ttk.Label(self, text=self.title)
        self.title_lbl.grid(row=0, column=0, sticky='W')

        self.selection_btn = ttk.Button(self, text=self.btn_title)
        self.selection_btn.grid(row=0, column=1, sticky='W')

        ############### configure properties ###################
        self.rowconfigure(index=0, weight=1)
        self.grid_configure(sticky='EW')

    # def select_file(self):
    #     open_file = askopenfile()
    #     if open_file is not None:
    #         self.selected_file = open_file.name
    #
    # def btn_command(self):
    #     for func in self.btn_command_list:
    #         func()

class ScaleBarContainer(ttk.Frame):
    def __init__(self, container, min_val, max_val, title=None, discrete=True,
                 callbacks=[], **kwargs):
        super().__init__(container, **kwargs)

        ################ create class attributes ################
        if title is None:
            self.title=""
        else:
            self.title=title

        self.min_val = min_val
        self.max_val = max_val
        self.discrete=discrete
        self.callbacks= callbacks + [self.validate_and_display]

        ################ create widget variables ##############
        self.display_val = tk.StringVar()
        self.scalebar = None
        if discrete:
            self.scale_val = tk.IntVar()
        else:
            self.scale_val = tk.DoubleVar()

        ################ create widgets here #################
        # 1. create quantity label
        self.quantity_lbl = ttk.Label(self, text="Quantity: ")
        self.quantity_lbl.grid(row=0, column=0, sticky='W')

        # 2. input title as the quantity to be displayed
        self.title_lbl = ttk.Label(self, text=self.title)
        self.title_lbl.grid(row=0, column=1, sticky='W')

        # 3. create label for minimum value
        self.min_lbl = ttk.Label(self, text=f"{self.min_val}")
        self.min_lbl.grid(row=1, column=0, sticky='W')

        # 4. create scale bar
        self.scalebar = ttk.Scale(self, from_=self.min_val, to=self.max_val,
                                  command=lambda event : self.scale_bar_callbacks(),
                                  variable=self.scale_val)
        self.scalebar.grid(row=1, column=1, sticky='E')

        # 5. create label for maximum value
        self.max_lbl = ttk.Label(self, text=f"{self.max_val}")
        self.max_lbl.grid(row=1, column=2, sticky='W')

        # 6. create current value label
        self.current_val_lbl = ttk.Label(self, text="Current value: ")
        self.current_val_lbl.grid(row=2, column=0, sticky='W')

        # 7. create label to display current value
        self.display_current_lbl = ttk.Label(self, textvariable=self.display_val)
        self.display_current_lbl.grid(row=2, column=1, sticky='W')

    ############### define callbacks ####################
    def validate_and_display(self):
        if self.discrete:
            current_value = int(self.scalebar.get())
        else:
            current_value = round(self.scalebar.get(),2)

        self.display_val.set(current_value)
        self.scale_val.set(current_value)

    def scale_bar_callbacks(self):
        for func in self.callbacks:
            func()




if __name__=="__main__":
    root = tk.Tk()
    ScaleBarContainer(root, 0, 255, discrete=True).grid()
    root.mainloop()