import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Classic theme
style = ttk.Style(root)
style.theme_use("classic")

combobox = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
combobox.pack()

# Blue theme
style = ttk.Style(root)
style.theme_use("alt")
style.configure("TCombobox", fieldbackground="light blue")

combobox = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
combobox.pack()

root.mainloop()
