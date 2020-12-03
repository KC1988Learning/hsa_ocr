import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from util.cvutil import read_img, get_shape

# root = tk.Tk()
# frame = ttk.Frame(root)
# image = ImageTk.PhotoImage(file=r"C:\Users\KC_Cheng\Documents\hsa_ocr\util\img\puppy.jpg")
# img_label = ttk.Label(frame, image=image)
# img_label.pack()
# frame.pack()
# root.mainloop()

# class ShowImage(ttk.Frame):
#     def __init__(self, container, **kwargs):
#         super().__init__(container, **kwargs)
#
#         self.image = ImageTk.PhotoImage(file=r"C:\Users\KC_Cheng\Documents\hsa_ocr\util\img\puppy.jpg")
#         img_label = ttk.Label(self, image=self.image)
#         img_label.pack()
#
# root = tk.Tk()
# showImg_frame = ShowImage(root)
# showImg_frame.pack()
# root.mainloop()

def callback(event):
    print("clicked at, ", event.x, event.y)

def check_cursor(event):
    height, width = int(canvas['height']), int(canvas['width'])
    if (event.x < width and event.y < height):
        canvas.config(cursor="tcross")
    else:
        canvas.config(cursor="")


root = tk.Tk()
img = ImageTk.PhotoImage(file=r"C:\Users\KC_Cheng\Documents\hsa_ocr\util\img\puppy.jpg")
img_cv = read_img(r"C:\Users\KC_Cheng\Documents\hsa_ocr\util\img\puppy.jpg")
height, width, _ = get_shape(img_cv)
canvas = tk.Canvas(root, bg="white", height=height, width=width)
canvas.create_image(0,0, image=img, anchor='nw')
print(canvas["height"])
print(canvas["width"])
canvas.bind("<Button-1>", callback)
canvas.bind("<Motion>", check_cursor)
canvas.pack()
root.mainloop()
