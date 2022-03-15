
from cgitb import text
import tkinter as tk
from turtle import width
import pandas as pd
from tkinter import VERTICAL, ttk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
# import sklearn
import seaborn as sns

global df

#-----------------------------------------------------------VIEW--------------------------------------------------------------------

top = tk.Tk()
top.geometry("1024x768")
top.pack_propagate(False)
top.resizable(0,0)

#PRINT DATA
frame1 = tk.LabelFrame(top, text="DỮ LIỆU")
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
visual_frame = tk.LabelFrame(top,text="TRỰC QUAN HOÁ")
visual_frame.place(relx=0.75,relwidth=0.25,relheight=1)


# Drop down list
tkvar1 = tk.StringVar()
drop_down_field = ttk.Combobox(visual_frame,textvariable=tkvar1)
drop_down_field.pack()

# Drop down type chart
tkvar2 = tk.StringVar()
drop_down_type_chart = ttk.Combobox(visual_frame,textvariable=tkvar2)
drop_down_type_chart['value'] = ['Histogram','Pie chart','Bar chart']
drop_down_type_chart.pack()

# Visual button
visual_button = tk.Button(visual_frame,text="Trực quan",command=lambda:visualize_data())
visual_button.pack()

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
    global data
    data = df
    Dataview["columns"] = list(df.columns)
    Dataview["show"] = "headings"
    for column in Dataview["columns"]:
        Dataview.heading(column,text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        Dataview.insert("","end",values=row)

    # Add option for visualize 
    drop_down_field['values'] = Dataview["columns"]

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

def visualize_data():
    visual_col = drop_down_field.get()
    type_chart = drop_down_type_chart.get()
    if type_chart == 'Histogram':
        sns.histplot(data=data,x=visual_col)
    elif type_chart == 'Pie chart':
        process_data = data[visual_col].value_counts()
        plt.pie(process_data,labels=process_data.keys(),autopct='%.2f')
        plt.title(visual_col+" "+type_chart)
    elif type_chart == 'Bar chart':
        process_data = data[visual_col].value_counts()
        plt.bar(process_data.keys(),process_data)
        plt.title(visual_col+" "+type_chart)
    elif type_chart == 'Box plot':
        pass
    plt.show()
    

top.mainloop()