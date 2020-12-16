from tkinter.filedialog import askopenfile
import tkinter as tk
from tkinter import ttk
import cv2 as cv
from util.cvutil import *
from PIL import Image, ImageTk

def select_file():
    open_file = askopenfile()
    if open_file is not None:
        return open_file.name







