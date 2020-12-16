import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import cv2 as cv
from util.cvutil import read_img, get_shape, getCanny
from util.guiutil.container_class import SelectFileContainer, ScaleBarContainer, ImageCanvasContainer
from util.guiutil.controller import *

class GetCannyEdge(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        ############### create class attributes ##################
        self.selected_img_file = None


        ############## create class widgets #####################
        # 1. create container to select image file
        self.file_select_frame = SelectFileContainer(self, title="Select image file: ", btn_title="Select")
        self.file_select_frame.selection_btn['command'] = self.btn_command
        self.file_select_frame.grid(row=0, column=0, sticky='EW')

        # 2. create image canvas frame
        self.img_canvas_frame = ImageCanvasContainer(self)
        self.img_canvas_frame.grid(row=1, column=0, sticky='EW')

        # 3. create two scale bars
        self.low_scalebar = ScaleBarContainer(self, 0, 255, title="Lower threshold",
                                              callbacks=[self.scale_command])
        self.low_scalebar.grid(row=2, column=0, sticky='EW')

        self.high_scalebar = ScaleBarContainer(self, 0, 255, title="Upper threshold",
                                               callbacks=[self.scale_command])
        self.high_scalebar.grid(row=3, column=0, sticky='EW')

    def btn_command(self):
        self.selected_img_file = select_file()

        # renew image when new file is selected
        if self.selected_img_file is not None:
            self.cv_img_original = read_img(self.selected_img_file)
            self.update_img(self.cv_img_original)

    def scale_command(self):
        if self.cv_img_original is not None:
            min_val = self.low_scalebar.scale_val.get()
            max_val = self.high_scalebar.scale_val.get()
            self.cv_img = getCanny(self.cv_img_original, min_val, max_val)
            self.cv_img = reshape_2D_img(self.cv_img)
            self.update_img(self.cv_img)
        else:
            pass

    def update_img(self, cv_img):
        self.img_canvas_frame.tk_img = ImageTk.PhotoImage(Image.fromarray(cv_img))
        self.img_canvas_frame.canvas['height'], self.img_canvas_frame.canvas['width'], _ = get_shape(
            cv_img
        )
        self.img_canvas_frame.canvas.itemconfig(self.img_canvas_frame.canvas_controller,
                                                image=self.img_canvas_frame.tk_img)

if __name__=="__main__":
    root = tk.Tk()
    GetCannyEdge(root).grid()
    root.mainloop()
