import tkinter as tk
from tkinter import ttk

def greet():
    print("Hello world!")

def ask():
    print("How are you?")

root = tk.Tk()

greet_button = ttk.Button(root, text="Greet", command=greet)

# by default, the element will be contained within a horizontal strip anchored to the next available top position
# you can change this default behaviour by specifying the side parameter
# when side takes 'left', the element will be contained within a vertical strip instead
greet_button.pack(side="left")

#while the vertical strip spans across the entire height, the button does not
# to make the button fill up the wasted vertical space, set fill parameter to the y dimension
ask_button = ttk.Button(root, text="How are you?", command=ask)
ask_button.pack(side="right", fill="y")

# close the window upon clicking the button by setting command as root.destroy
quit_button = ttk.Button(root, text="Quit", command=root.destroy)
# make the button fill up the entire horizontal strip that contains it
quit_button.pack(side="top", fill="x")


root.mainloop()