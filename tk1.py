import tkinter as tk
from tkinter import ttk  # new tkinter library that makes application look more native to Windows

# create a tk object, which is the main window
root = tk.Tk()

# create Label object in the ttk, pass the object to a parent (root)
# put the element into the window using pack
ttk.Label(root, text="Hello, world!").pack()

# create another Label with left-right and top-bottom padding of 30 and 10
ttk.Label(root, text="Great to see you!", padding=(30,10)).pack()

# start running the tk object (main window) indefinitely
# any code after this line won't run until the window is closed
root.mainloop()