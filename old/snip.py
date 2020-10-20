import pyautogui
import tkinter as tk

root=tk.Tk()

root.geometry("200x200")
root.title("snip")

def takess():
    img = pyautogui.screenshot("new-img.png")

def quitApp():
    root.destroy()

button1=tk.Button(root, text="Take Picture", command=takess)
button1.place(x=20, y=50)

button1=tk.Button(root, text="Quit", command=takess)
button1.place(x=20, y=100)

root.mainloop()