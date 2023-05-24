
import tkinter as tk

def show_selected(option):
    print(f"Selected option: {option}")

root = tk.Tk()
root.geometry("200x100")

options = ["Option 1", "Option 2", "Option 3"]
selected_option = tk.StringVar(root)
selected_option.set(options[0])

option_menu = tk.OptionMenu(root, selected_option, *options)
option_menu.pack(pady=10)

button = tk.Button(root, text="Select", command=lambda: show_selected(selected_option.get()))
button.pack()

root.mainloop()
