import os
import tkinter as tk
from tkinter.constants import *


def tree_pack():
    frame_tree.pack(anchor=NE, fill=NONE, side=RIGHT)
    btn_exit.pack(anchor=SW, fill=X, side=BOTTOM)
    scrollbar_tree.pack(side=RIGHT, fill=Y)
    label_path.pack(side=TOP, anchor=NW, fill=X)
    list_box_tree.pack(side=LEFT, fill=Y)


def file_pack():
    frame_file.pack(side=LEFT, anchor=NW)
    btn_close.pack(side=RIGHT, anchor=NE, fill=Y)
    text_file.pack(side=LEFT, anchor=NW, expand=YES)


def mouse_on(event=None):
    global window, sense_bar, window_status
    sense_bar.pack_forget()
    if window_status == 1:
        size_position = '%dx%s+%s+0' % (tree_width, window_height, window.winfo_screenwidth() - tree_width)
        window.geometry(size_position)
    elif window_status == 2:
        size_position = '%dx%s+%s+0' % (
        tree_width + file_width, window_height, window.winfo_screenwidth() - (tree_width + file_width))
        window.geometry(size_position)
        file_pack()
    tree_pack()


def mouse_off(event=None):
    global window_status
    global window
    frame_tree.pack_forget()
    frame_file.pack_forget()
    size_position = '%dx%s+%s+0' % (bar_width, window_height, window.winfo_screenwidth() - bar_width)
    window.geometry(size_position)
    sense_bar.pack()


def click_tree(event=None):
    global window, list_box_tree, root_path, cur_path
    file_index = list_box_tree.curselection()
    if file_index == '':
        return
    file_name = list_box_tree.get(file_index)
    if file_name == '..':
        file_path = '/'.join(cur_path.split('/')[:-1])
    else:
        file_path = os.path.join(cur_path, file_name)
    if os.path.isfile(file_path):
        show_file(file_path)
    elif os.path.isdir(file_path):
        show_tree(file_path)


def show_tree(file_dir):
    global window, list_box_tree, cur_path, string_path
    cur_path = file_dir
    string_path.set(cur_path)
    list_box_tree.delete(0, END)
    if cur_path != root_path:
        list_box_tree.insert(END, '..')
    files = os.listdir(cur_path)
    files.sort()
    for file in files:
        list_box_tree.insert(END, file)


def show_file(file_path):
    global window, tree_width, file_width, window_height, frame_file, btn_close, text_file, text_file, window_status
    window_status = 2
    size_position = '%dx%s+%s+0' % (
    tree_width + file_width, window_height, window.winfo_screenwidth() - (tree_width + file_width))
    window.geometry(size_position)
    file_pack()
    text_file.delete('0.0', END)
    with open(file_path, 'r') as rf:
        for line in rf:
            text_file.insert(END, line)


def close_file():
    global window, tree_width, window_height, frame_file, window_status
    window_status = 1
    size_position = '%dx%s+%s+0' % (tree_width, window_height, window.winfo_screenwidth() - tree_width)
    window.geometry(size_position)
    frame_file.pack_forget()


font_style = 'ubuntu'
window_status = 1

window = tk.Tk()
window.attributes('-topmost', True)
window.overrideredirect(True)
window.title('file manager')
window.resizable(0, 0)
window.bind('<FocusOut>', mouse_off)

bar_width = 15
tree_width = 250
file_width = 700
window_height = window.winfo_screenheight()
size_position = '%dx%s+%s+0' % (bar_width, window_height, window.winfo_screenwidth() - bar_width)
window.geometry(size_position)

sense_bar = tk.Frame(window, height=window_height, width=bar_width, bg='green')
sense_bar.bind('<Enter>', mouse_on)
sense_bar.pack_propagate(0)
sense_bar.pack()

root_path = '/home/wuyuhao/CodeLibrary'
cur_path = root_path
frame_file = tk.Frame(window, height=window_height, width=file_width, bg='pink')
frame_file.pack_propagate(0)
btn_close = tk.Button(frame_file, text='>>', command=close_file, height=window_height)
text_file = tk.Text(frame_file, width=file_width, height=window_height, yscrollcommand='auto', font=(font_style, 16))
text_file.pack_propagate(0)

frame_tree = tk.Frame(window, height=window_height, width=tree_width, bg='white')
frame_tree.pack_propagate(0)
btn_exit = tk.Button(frame_tree, text='退出', command=window.quit, height=7, font=(font_style, 18))
scrollbar_tree = tk.Scrollbar(frame_tree)
string_path = tk.StringVar()
string_path.set(cur_path)
label_path = tk.Label(frame_tree, textvariable=string_path, font=(font_style, 12), justify=LEFT)
list_box_tree = tk.Listbox(frame_tree, width=tree_width-2, font=(font_style, 18), selectforeground='red',
                           yscrollcommand=scrollbar_tree.set)
scrollbar_tree.config(command=list_box_tree.yview)
list_box_tree.bind('<ButtonRelease-1>', click_tree)

files = os.listdir(cur_path)
files.sort()
for file in files:
    list_box_tree.insert(END, file)


window.mainloop()
