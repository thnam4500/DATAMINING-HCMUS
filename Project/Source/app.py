from ast import Global
from cgitb import text
import tkinter as tk
from turtle import width
from numpy import pad, size
import pandas as pd
from tkinter import VERTICAL, ttk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

global df

#-----------------------------------------------------------VIEW--------------------------------------------------------------------

top = tk.Tk()
top.geometry("1024x768")
top.pack_propagate(False)
top.resizable(0,0)

#PRINT DATA
frame1 = tk.LabelFrame(top, text="Dữ liệu")
frame1.place(relheight=0.5,relwidth=0.75)

# Describe frame
desc_frame = tk.LabelFrame(top, text="Thông tin mô tả")
desc_frame.place(relheight=0.3,relwidth=0.75,rely=0.5)

desc_view = ttk.Treeview(desc_frame)
desc_view.place(relheight=1,relwidth=1)

desc_scrollx = tk.Scrollbar(desc_frame,orient="horizontal", command=desc_view.xview)

desc_view.configure(xscrollcommand=desc_scrollx.set)

desc_scrollx.pack(side="bottom",fill="x")


#OPEN FILE
file_frame = tk.LabelFrame(top, text="THAO TÁC FILE")
file_frame.place(relwidth=0.75,relheight=0.2,rely=0.85)


#Button for chose and open file
file_name = tk.Label(file_frame,text="No file selected")
file_name.place(rely=0.1,relx=0.1)

load_file_button = tk.Button(file_frame,text="Load file",width=10,command=lambda:load_file_data())
load_file_button.place(relx=0.1, rely=0.4)

browse_button = tk.Button(file_frame,text="Chọn file",width=10, command=lambda:file_dialog())
browse_button.place(relx=0.3,rely=0.4)




# Data view
Dataview = ttk.Treeview(frame1)
Dataview.place(relheight=1,relwidth=1)

Data_scrolly = tk.Scrollbar(frame1,orient="vertical",command=Dataview.yview)
Data_scrollx = tk.Scrollbar(frame1,orient="horizontal", command=Dataview.xview)

Dataview.configure(xscrollcommand=Data_scrollx.set, yscrollcommand=Data_scrolly.set)

Data_scrollx.pack(side="bottom",fill="x")
Data_scrolly.pack(side="right",fill="y")

# Visualization
visual_frame = tk.LabelFrame(top)
visual_frame.place(relx=0.75)
# Drop down list
list_field = []
tkvar = tk.StringVar(top)
drop_down = tk.OptionMenu(visual_frame,tkvar,"a","b")
drop_down.pack()

#---------------------------------------------------------END VIEW--------------------------------------------------------------------

    

def file_dialog():
    filename = filedialog.askopenfilename(initialdir='./', 
                                         title="Select a file",
                                         filetypes=(("csv files","*.csv"),("xlsx files","*.xlsx")))
    file_name["text"] = filename
    

def load_file_data():
    file_path = file_name["text"]
    try:
        file = r"{}".format(file_path)
        if file.split('.')[-1] == 'csv':
            df = pd.read_csv(file)
            del_column = [x for x in df.keys() if "Unnamed" in x]
            df = df.drop(columns=del_column)
            
        else:
            tk.messagebox.showerror("Information", "File bạn chọn không được hỗ trợ để mở")
    except ValueError:
        tk.messagebox.showerror("Information","File bạn chọn không tồn tại")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information","No such file as {file_path}")
        return None

    clear_data()
    # Print data
    Dataview["columns"] = list(df.columns)
    Dataview["show"] = "headings"
    for column in Dataview["columns"]:
        Dataview.heading(column,text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        Dataview.insert("","end",values=row)

    # Print describe
    desc_info = df.describe().reset_index()
    desc_info = desc_info.rename(columns={'index':'info'})
    desc_view["columns"] = list(desc_info.columns)
    desc_view["show"] = "headings"
    for column in desc_view["columns"]:
        desc_view.heading(column,text=column)
    df_rows = desc_info.to_numpy().tolist()
    for row in df_rows:
        desc_view.insert("","end",values=row)

    return None

def clear_data():
    Dataview.delete(*Dataview.get_children())
    desc_view.delete(*desc_view.get_children())

top.mainloop()