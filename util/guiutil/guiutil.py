import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from tkinter import font
from util.cvutil import read_img, get_shape, color_thresholding, convert_to_gray, view_img, getCanny
import numpy as np

##############################################################################################################
#### 1. FRAME TO LOAD AND VIEW IMAGE ####
##############################################################################################################
class SelectShowImageFrame(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.title = "Select and Show Image"

        ###################################### create variables ########################################
        self.img_filepath = tk.StringVar(value="")

        ###################################### create widgets ##########################################
        img_file_lbl_1 = ttk.Label(self, text="Select your image file: ")
        img_file_btn = ttk.Button(self, text="Select",
                                  command=self.open_image_file)
        img_file_lbl_2 = ttk.Label(self, text="Path of selected image: ")
        img_file_lbl_3 = ttk.Label(self, textvariable=self.img_filepath)
        self.img_frame = ShowImage(self)

        ##################################### position widgets #########################################
        img_file_lbl_1.grid(row=0, column=0, sticky='W')
        img_file_btn.grid(row=0, column=1, sticky='W')
        img_file_lbl_2.grid(row=1, column=0, sticky='W')
        img_file_lbl_3.grid(row=1, column=1, sticky='W')
        self.img_frame.grid(row=2, column=0, columnspan=2, sticky='EW')

        ################################# configure properties #########################################
        # set equal paddings for all widgets
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

        # change font size
        font.nametofont('TkDefaultFont').configure(size=11)

        # change font type
        font.nametofont('TkDefaultFont').configure(family='Arial')


    def open_image_file(self):
        img_filepath = fd.askopenfile()
        self.img_filepath.set(img_filepath.name)
        self.img_frame.update_img(img_filepath.name)

class ShowImage(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

    def update_img(self, img_path):
        self.img = ImageTk.PhotoImage(file=img_path)
        self.img_label = ttk.Label(self, image=self.img)
        self.img_label.grid()

##############################################################################################################
#### 2. FRAME TO LOAD AND VIEW IMAGE AND SELECT PIXEL LOCATION ####
##############################################################################################################
class SelectPixelFrame(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        ########################## create variables ####################################
        self.img_filepath = tk.StringVar(value="No selected image.")
        self.title = "Get Pixel Location"
        self.select_pixel_panel = None

        ############################### create widgets ################################
        img_file_lbl_1 = ttk.Label(self, text="Select image file: ")
        img_file_btn = ttk.Button(self, text="Select", command=self.update_select_pixel)
        img_file_lbl_2 = ttk.Label(self, text="Path of selected image: ")
        img_file_lbl_3 = ttk.Label(self, textvariable=self.img_filepath)
        separator = ttk.Separator(self)


        ############################### position widgets ##############################
        self.columnconfigure(index=0, weight=0)
        self.columnconfigure(index=1, weight=1)

        img_file_lbl_1.grid(row=0, column=0, sticky='W')
        img_file_btn.grid(row=0, column=1, sticky='W')
        img_file_lbl_2.grid(row=1, column=0, sticky='W')
        img_file_lbl_3.grid(row=1, column=1, sticky='W')
        separator.grid(row=2, column=0, columnspan=2, sticky='EW')

        ############################### configure window #############################
        # set font size and type
        font.nametofont("TkDefaultFont").configure(size=11, family="Arial")

        # set equal padding for all
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def update_select_pixel(self):
        img_filepath = fd.askopenfile()
        self.img_filepath.set(img_filepath.name)

        # create SelectPixel panel
        if self.select_pixel_panel is not None:
            self.select_pixel_panel.grid_forget()

        self.select_pixel_panel = SelectPixelPanel(self, img_filepath.name)
        self.select_pixel_panel.grid(row=3, column=0, columnspan=2, sticky='EW')


class SelectPixelPanel(tk.Frame):
    def __init__(self, container, img_path, **kwargs):
        super().__init__(container, **kwargs)

        self.img_path = img_path
        self.img = ImageTk.PhotoImage(file=self.img_path)

        # get image height and width
        self.height, self.width, _ = get_shape(read_img(self.img_path))

        ################## create variable ##################
        self.selected_pixel = tk.StringVar(value="")

        ################## create widgets ###################
        self.img_canvas = tk.Canvas(self, height=self.height, width=self.width)
        self.img_canvas.create_image(0,0, image=self.img, anchor='nw')
        pixel_label = ttk.Label(self, text="Location of selected pixel: ")
        pixel_display = ttk.Label(self, textvariable=self.selected_pixel)

        ################## position widgets #################
        self.columnconfigure(index=0, weight=0)
        self.columnconfigure(index=1, weight=1)
        self.img_canvas.grid(row=0, column=0, columnspan=2, sticky='EW')
        pixel_label.grid(row=1, column=0, sticky='W')
        pixel_display.grid(row=1, column=1, sticky='W')

        ################## event binding to canvas ###############
        self.img_canvas.bind("<Button-1>", self.click_to_locate)
        self.img_canvas.bind("<Motion>", self.change_cursor)

    def click_to_locate(self,event):
        selected_x, selected_y = event.x, event.y
        self.selected_pixel.set(f"x: {selected_x}, y: {selected_y}")

    def change_cursor(self, event):
        if (event.x < self.width and event.y < self.height):
            self.img_canvas.config(cursor="tcross")
        else:
            self.img_canvas.config(cursor="")

#####################################################################################################################
#### 3. LOAD AND VIEW IMAGE; SELECT COLOR PIXEL; PERFORMING COLOR THRESHOLDING; RETURN FINAL IMAGE ####
#####################################################################################################################
class ColorThresholdingFrame(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        ######################################### configure properties ###################################
        self.columnconfigure(index=0, weight=1)

        ######################################### create variables #######################################
        self.final_img = self.img_threshold_frame = None
        self.R_low = self.R_up = self.G_low = self.G_up = self.B_low = self.B_up = None

        ######################################### create widgets #########################################
        self.create_file_selection_frame()

    def create_file_selection_frame(self):
        self.file_selection_frame = ttk.Frame(self)
        self.file_selection_frame.grid(row=0, column=0, sticky='EW')

        ############################### Add widgets to frame #############################################
        selection_lbl = ttk.Label(self.file_selection_frame, text="Select image file: ")
        selection_lbl.grid(row=0, column=0, sticky='W')

        selection_btn = ttk.Button(self.file_selection_frame, text="Select", command=self.create_img_threshold_frame)
        selection_btn.grid(row=0, column=1, sticky='W')

    def create_img_threshold_frame(self):
        self.select_img_file() # 1. allow user select and open image file

        if self.img_threshold_frame is not None:
            self.img_threshold_frame.grid_forget()

        self.img_threshold_frame = ttk.Frame(self) # create the frame for thresholding process
        self.img_threshold_frame.grid(row=1, column=0, sticky='EW')

        ################################### Add widgets here #############################################
        ### 1. Add image canvas
        img_height, img_width, _ = get_shape(read_img(self.img_filepath))
        self.img_canvas = tk.Canvas(self.img_threshold_frame, height=img_height, width=img_width)
        self.img_on_canvas = self.img_canvas.create_image(0,0,
                                image=self.img, anchor='nw')
        self.img_canvas.grid(row=0, column=0, columnspan=2, sticky='EW')

        ### 2. Add display for selected pixel values
        loc_lbl = ttk.Label(self.img_threshold_frame, text="Location of selected pixel: ")
        loc_lbl.grid(row=1, column=0, sticky='W')

        self.pixel_loc = tk.StringVar()
        loc_display = ttk.Label(self.img_threshold_frame, textvariable=self.pixel_loc)
        loc_display.grid(row=1, column=1, sticky='W')

        ### 3. Add display for RGB-values of selected pixel
        pix_val_lbl = ttk.Label(self.img_threshold_frame, text="RGB value of selected pixel: ")
        pix_val_lbl.grid(row=2, column=0, sticky='W')

        self.pixel_value = tk.StringVar()
        pix_val_display = ttk.Label(self.img_threshold_frame, textvariable=self.pixel_value)
        pix_val_display.grid(row=2, column=1, sticky='W')

        ### 4. Add spin for range of RGB values
        self.R_low_upper_container = LowerUpperContainer(self.img_threshold_frame, "R-range: ", 0, 255)
        self.R_low_upper_container.grid(row=3, column=0, columnspan=2, sticky='W')

        self.G_low_upper_container = LowerUpperContainer(self.img_threshold_frame, "G-range: ", 0, 255)
        self.G_low_upper_container.grid(row=4, column=0, columnspan=2, sticky='W')

        self.B_low_upper_container = LowerUpperContainer(self.img_threshold_frame, "B-range: ", 0, 255)
        self.B_low_upper_container.grid(row=5, column=0, columnspan=2, sticky='W')

        ############################### CALLBACKS #############################################################
        ### 5. Bind callback to spinning event of the spinbox
        self.R_low_upper_container.get_low_spinbox()["command"]=self.threshold_and_update_img
        self.R_low_upper_container.get_up_spinbox()["command"] = self.threshold_and_update_img
        self.G_low_upper_container.get_low_spinbox()["command"] = self.threshold_and_update_img
        self.G_low_upper_container.get_up_spinbox()["command"] = self.threshold_and_update_img
        self.B_low_upper_container.get_low_spinbox()["command"] = self.threshold_and_update_img
        self.B_low_upper_container.get_up_spinbox()["command"] = self.threshold_and_update_img

        ### 6. Bind callback to pressing enter on the spinbox
        self.R_low_upper_container.get_low_spinbox().bind('<Return>', lambda event: self.threshold_and_update_img())
        self.R_low_upper_container.get_up_spinbox().bind('<Return>', lambda event: self.threshold_and_update_img())
        self.G_low_upper_container.get_low_spinbox().bind('<Return>', lambda event: self.threshold_and_update_img())
        self.G_low_upper_container.get_up_spinbox().bind('<Return>', lambda event: self.threshold_and_update_img())
        self.B_low_upper_container.get_low_spinbox().bind('<Return>', lambda event: self.threshold_and_update_img())
        self.B_low_upper_container.get_up_spinbox().bind('<Return>', lambda event: self.threshold_and_update_img())


        ### 6. Bind events to the canvas ############
        self.img_canvas.bind("<Button-1>", self.click_to_locate)
        self.img_canvas.bind("<Motion>", lambda event: self.change_cursor(event, img_height, img_width))


    ############################## CONTROLLER ###################################
    def select_img_file(self):
        img_filepath = fd.askopenfile()
        if img_filepath is not None:
            self.img_filepath = img_filepath.name
            self.img = ImageTk.PhotoImage(file=self.img_filepath)
            self.imgcv = read_img(img_filepath.name)
            self.imgcv_original = read_img(img_filepath.name)
        else:
            pass

    def click_to_locate(self, event):
        self.pixel_loc.set(f"x: {event.x}, y: {event.y}")

        self.r_value, self.g_value, self.b_value = self.imgcv[event.y, event.x, :]
        self.pixel_value.set(f"R: {self.r_value}, G: {self.g_value}, B: {self.b_value}")


    def change_cursor(self, event, img_height, img_width):
        if (event.x < img_width and event.y < img_height):
            self.img_canvas.config(cursor="tcross")
        else:
            self.img_canvas.config(cursor="")

    def threshold_and_update_img(self):
        RGB_low = (self.R_low_upper_container.get_low_value(),
                   self.G_low_upper_container.get_low_value(),
                   self.B_low_upper_container.get_low_value())
        RGB_up = (self.R_low_upper_container.get_up_value(),
                   self.G_low_upper_container.get_up_value(),
                   self.B_low_upper_container.get_up_value())

        self.imgcv = color_thresholding(self.imgcv_original, RGB_low, RGB_up)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.imgcv))
        self.img_canvas.itemconfig(self.img_on_canvas,
                                   image=self.img)

class LowerUpperContainer(ttk.Frame):
    def __init__(self, container, name, min, max, **kwargs):
        super().__init__(container, **kwargs)
        self.name = name
        self.low_value = tk.IntVar(value=0)
        self.up_value = tk.IntVar(value=0)

        ################## create widget #################
        name_lbl = ttk.Label(self, text=f"{self.name}: From ")
        name_lbl.grid(row=0, column=0, sticky='W')

        self.low_spinbox = tk.Spinbox(self, from_=min, to=max,
                                 increment=1.0, wrap=True,
                                 textvariable=self.low_value)
        self.low_spinbox.grid(row=0, column=1, sticky='W')

        to_lbl = ttk.Label(self, text=" to ")
        to_lbl.grid(row=0, column=2, sticky='W')

        self.up_spinbox = tk.Spinbox(self, from_=min, to=max,
                                increment=1.0, wrap=True,
                                textvariable=self.up_value)
        self.up_spinbox.grid(row=0, column=3, sticky='W')

    def get_low_value(self):
        return self.low_value.get()

    def get_up_value(self):
        return self.up_value.get()

    def get_low_spinbox(self):
        return self.low_spinbox

    def get_up_spinbox(self):
        return self.up_spinbox

class GetCannyEdge(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        ############# declare variables #######################
        self.functional_frame=None
        #######################################################

        self.select_img_file()
        self.selection_frame.grid(row=0, column=0, sticky='EW')

    def select_img_file(self):
        self.selection_frame = ttk.Frame(self)

        ###################### add widgets to frame ######################
        selection_lbl= ttk.Label(self.selection_frame, text="Select image: ")
        selection_lbl.grid(row=0, column=0, sticky='W')

        selection_btn = ttk.Button(self.selection_frame, text="Select",
                                   command=self.create_canny_edge_frame)
        selection_btn.grid(row=0, column=1, sticky='W')

    def create_canny_edge_frame(self):
        # create functional frame
        if self.functional_frame is not None:
            self.functional_frame.grid_forget()

        self.functional_frame = ttk.Frame(self)
        self.functional_frame.grid(row=1, column=0, sticky='EW')

        # activate dialog to select image file
        self.select_img()

        # get image height and width
        img_height, img_width, _ = get_shape(self.imgcv)

        # create image canvas
        self.canvas = tk.Canvas(self.functional_frame, height=img_height,
                                width=img_width)
        self.canvas_img = self.canvas.create_image(0,0, anchor='nw',
                                                   image=self.img)
        self.canvas.grid(row=0, column=0, sticky='EW')

        # create scale frame for lower threshold
        self.scale_frame_low = ScrollForValueContainer(self.functional_frame, 0, 255,
                                title="Lower threshold", discrete=True)
        self.scale_frame_low.scale_bar['command'] = lambda event : self.get_canny_edge()
        self.scale_frame_low.grid(row=1, column=0, sticky='EW')

        # create scale frame for higher threshold
        self.scale_frame_high = ScrollForValueContainer(self.functional_frame, 0, 255,
                                                        title="Higher threshold", discrete=True)
        self.scale_frame_high.scale_bar['command'] = lambda event : self.get_canny_edge()
        self.scale_frame_high.grid(row=2, column=0, sticky='EW')

    def select_img(self):
        img_filepath = fd.askopenfile()
        if img_filepath is not None:
            self.img_filepath = img_filepath.name
            self.imgcv = convert_to_gray(read_img(img_filepath.name), reshape=True)
            self.imgcv_original = convert_to_gray(read_img(img_filepath.name), reshape=True)
            self.img = ImageTk.PhotoImage(Image.fromarray(self.imgcv))
        else:
            pass

    def get_canny_edge(self):
        min_val = int(self.scale_frame_low.get_scale_bar().get())
        max_val = int(self.scale_frame_high.get_scale_bar().get())
        self.imgcv = getCanny(self.imgcv_original, min_val, max_val)
        self.img = ImageTk.PhotoImage(Image.fromarray(self.imgcv))

        self.canvas.itemconfig(self.canvas_img,
                                   image=self.img)


    def show_value_low(self):
        self.current_value_low.set(str(self.scale_bar_low.get()))

    def show_value_high(self):
        self.current_value_high.set(str(self.scale_bar_high.get()))


class ScrollForValueContainer(ttk.Frame):
    def __init__(self, container, low_val, up_val, title=None, discrete=True, **kwargs):
        super().__init__(container, **kwargs)
        self.title = title
        self.low_val = low_val
        self.up_val = up_val
        self.discrete = discrete

        if self.discrete:
            self.low_val = int(np.round(self.low_val))
            self.up_val = int(np.round(self.up_val))

        ############## create widget here ##############
        row_index = 0
        if self.title is not None:
            self.title_lbl = ttk.Label(self, text=f"Variable name: {self.title}")
            self.title_lbl.grid(row=row_index, column=0, columnspan=2, sticky='W')
            row_index += 1

        self.scale_bar = ttk.Scale(self, from_=self.low_val, to=self.up_val)
        self.scale_bar.grid(row=row_index, column=0, columnspan=2, sticky='EW')
        row_index += 1

        self.display_title = ttk.Label(self, text="Current value: ")
        self.display_title.grid(row=row_index, column=0, sticky='W')

        self.display_value = ttk.Label(self)
        self.display_value.grid(row=row_index, column=1, sticky='W')

    # def get_display(self, event):
    #     self.accept_integer()
    #     self.display.set(f"{self.scale_bar.get():.3f}")
    #
    # def accept_integer(self):
    #     value = self.scale_bar.get()
    #     if self.discrete:
    #         if int(value) != value:
    #             self.scale_bar.set(round(value))
    #     else:
    #         pass

    def get_scale_bar(self):
        return self.scale_bar

    def get_display_value(self):
        return self.display_value


if __name__ == "__main__":

    # root = tk.Tk()
    # root.columnconfigure(index=0, weight=1)
    # select_pixel_panel = SelectPixelFrame(root)
    # select_pixel_panel.grid(row=0, column=0, sticky='EW')
    # root.title(select_pixel_panel.title)
    # root.mainloop()

    # root = tk.Tk()
    # root.configure(background='#ffffff')
    # color_threshold_frame = ColorThresholdingFrame(root)
    # color_threshold_frame.grid()
    # root.mainloop()


    # def add_lower():
    #     total.set(some_spinbox_1.get_low_value() +
    #               some_spinbox_2.get_low_value())
    #
    # root = tk.Tk()
    # some_spinbox_1 = LowerUpperContainer(root, "R-value", 0, 255)
    # some_spinbox_1.get_low_spinbox()["command"]=add_lower
    # some_spinbox_1.get_low_spinbox().bind("<Return>", lambda event: add_lower())
    # some_spinbox_1.grid()
    # some_spinbox_2 = LowerUpperContainer(root, "G-value", 0, 255)
    # some_spinbox_2.get_low_spinbox()["command"] = add_lower
    # some_spinbox_2.get_low_spinbox().bind("<Return>", lambda event: add_lower())
    # some_spinbox_2.grid()
    # total = tk.IntVar(value=0)
    # some_label = ttk.Label(root, textvariable=total)
    # some_label.grid()
    # root.mainloop()

    root = tk.Tk()
    get_canny = GetCannyEdge(root)
    get_canny.grid()
    root.mainloop()


