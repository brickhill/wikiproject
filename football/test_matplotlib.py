import tkinter as tk


def clicked():
    print("BUTTON CLICKED")


root = tk.Tk()
root.title("Button Test")

button = tk.Button(
    root,
    text="CLICK ME"
)

button.pack(
    padx=100,
    pady=100
)

button.bind(
    "<Button-1>",
    lambda event: print("MOUSE CLICK DETECTED")
)

root.mainloop()