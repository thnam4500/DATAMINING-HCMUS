
from cgitb import text
from fileinput import filename
import tkinter as tk
from turtle import width
import pandas as pd
from tkinter import VERTICAL, ttk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
# import sklearn
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

global df

global X
global y

#-----------------------------------------------------------VIEW--------------------------------------------------------------------

top = tk.Tk()
top.title("VISUALIZE AND CLASSIFICATION")
top.geometry("1280x800")
top.pack_propagate(False)
top.resizable(0,0)

#PRINT DATA
frame1 = tk.LabelFrame(top, text="DỮ LIỆU")
frame1.place(relheight=0.5,relwidth=0.75)

# Describe frame
desc_frame = tk.LabelFrame(top, text="THÔNG TIN MÔ TẢ")
desc_frame.place(relheight=0.3,relwidth=0.75,rely=0.5)

desc_view = ttk.Treeview(desc_frame)
desc_view.place(relheight=1,relwidth=1)

desc_scrollx = tk.Scrollbar(desc_frame,orient="horizontal", command=desc_view.xview)

desc_view.configure(xscrollcommand=desc_scrollx.set)

desc_scrollx.pack(side="bottom",fill="x")



#OPEN FILE
file_frame = tk.LabelFrame(top, text="THAO TÁC FILE")
file_frame.place(relwidth=0.4,relheight=0.2,rely=0.8)


#Button for chose and open file

label_location = tk.Label(file_frame,text="Location: ")
label_location.grid(row=0,column=0,pady=(30,10),padx=(20,10))
file_name = tk.Entry(file_frame,text="No file selected",width=50)
file_name.grid(column=1,row=0,columnspan=2,pady=(30,10))

load_file_button = tk.Button(file_frame,text="Load file",width=10,command=lambda:load_file_data())
load_file_button.grid(row=1,column=1,pady=(10,10),padx=(20,10))

browse_button = tk.Button(file_frame,text="Chọn file",width=10, command=lambda:file_dialog())
browse_button.grid(row=1,column=2,pady=(10,10),padx=(10,10))




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
visual_frame.place(relx=0.75,relwidth=0.25,relheight=0.15)


# Drop down list
tkvar1 = tk.StringVar()
drop_down_field = ttk.Combobox(visual_frame,textvariable=tkvar1)
drop_down_field.pack(pady=(5,5))

# Drop down type chart
tkvar2 = tk.StringVar()
drop_down_type_chart = ttk.Combobox(visual_frame,textvariable=tkvar2)
drop_down_type_chart['value'] = ['Histogram','Pie chart','Bar chart']
drop_down_type_chart.pack(pady=(5,5))
drop_down_type_chart.current(0)

# Visual button
visual_button = tk.Button(visual_frame,text="Trực quan",command=lambda:visualize_data())
visual_button.pack(pady=(5,5))

# Model
train_frame = tk.LabelFrame(top, text="Huấn luyện mô hình")
# train_frame.grid(row=0, column=0,padx=(5,0))
train_frame.place(relx=0.75,rely=0.15,relwidth=0.25,relheight=1)



# input estimator

n_estimator_label = tk.Label(train_frame,text="N estimator")
n_estimator_label.grid(row=0,column=1,columnspan=1)
n_estimator_input = tk.Entry(train_frame,text="n estimator",state='disabled')
n_estimator_input.grid(row=1,column=0,columnspan=2,pady=(2,8),padx=(64,0))
n_estimate_var = tk.BooleanVar()
n_estimator_check = tk.Checkbutton(train_frame,command=lambda v=n_estimate_var,e=n_estimator_input:enable_input(v,e),variable=n_estimate_var)
n_estimator_check.grid(column=0,row=0,padx=(50,0))

max_depth_label = tk.Label(train_frame,text="Max depth")
max_depth_label.grid(row=2,column=1,columnspan=1)
max_depth_input = tk.Entry(train_frame,text="Max depth",state='disabled')
max_depth_input.grid(row=3,column=0,columnspan=2,pady=(2,8),padx=(64,0))
max_depth_var = tk.BooleanVar()
max_depth_check = tk.Checkbutton(train_frame,command=lambda v=max_depth_var,e=max_depth_input:enable_input(v,e),variable=max_depth_var)
max_depth_check.grid(column=0,row=2,padx=(50,0))

min_samples_leaf_label = tk.Label(train_frame,text="Min samples leaf")
min_samples_leaf_label.grid(row=4,column=1,columnspan=1)
min_samples_leaf_input = tk.Entry(train_frame,text="Min samples leaf",state='disabled')
min_samples_leaf_input.grid(row=5,column=0,columnspan=2,pady=(2,8),padx=(64,0))
min_samples_leaf_var = tk.BooleanVar()
min_samples_leaf_check = tk.Checkbutton(train_frame,command=lambda v=min_samples_leaf_var,e=min_samples_leaf_input:enable_input(v,e),variable=min_samples_leaf_var)
min_samples_leaf_check.grid(column=0,row=4,padx=(50,0))

min_samples_split_label = tk.Label(train_frame,text="Min samples split")
min_samples_split_label.grid(row=6,column=1,columnspan=1)
min_samples_split_input = tk.Entry(train_frame,text="Min samples split",state='disabled')
min_samples_split_input.grid(row=7,column=0,columnspan=2,pady=(2,8),padx=(64,0))
min_samples_split_var = tk.BooleanVar()
min_samples_split_check = tk.Checkbutton(train_frame,command=lambda v=min_samples_split_var,e=min_samples_split_input:enable_input(v,e),variable=min_samples_split_var)
min_samples_split_check.grid(column=0,row=6,padx=(60,0))

# Choose result field

result_field_label = tk.Label(train_frame,text="Cột kết quả:")
result_field_label.grid(column=0,row=8,pady=(10,10))
tkvar3 = tk.StringVar()
result_field = ttk.Combobox(train_frame,textvariable=tkvar3)
result_field.grid(column=1,row=8,columnspan=1,pady=(10,10))

# Train Model Button
train_button = tk.Button(train_frame,text="Train",command=lambda:train_model())
train_button.grid(column=0,row=9,pady=(10,10),padx=(90,10))

# predict 
predict_button = tk.Button(train_frame,text="Predict",command=lambda:predict())
predict_button.grid(column=1,row=9,pady=(10,10))

# logging box
log_box = tk.Text(train_frame,height=20,width=30,state='disabled')
log_box.place(relwidth=1,relheight=0.45,rely=0.4)

# result_train
result_frame = tk.LabelFrame(top, text="KẾT QUẢ")
result_frame.place(relx=0.4,rely=0.8,relwidth=0.35,relheight=0.2)
result_label = tk.Label(result_frame,text="Độ chính xác trung bình: ",font=('Arial',19))
result_label.pack(pady=(20,10))
result_output = tk.Label(result_frame,text="0.0",font=('Arial',20))
result_output.pack()




#---------------------------------------------------------END VIEW--------------------------------------------------------------------

def file_dialog():
    filename = filedialog.askopenfilename(initialdir='./', 
                                         title="Select a file",
                                         filetypes=(("csv files","*.csv"),("xlsx files","*.xlsx")))
    file_name.delete(0,tk.END)
    file_name.insert(0,filename)
    

def load_file_data():
    file_path = file_name.get()
    try:
        file = r"{}".format(file_path)
        file_type = file.split('.')[-1]
        if file_type == "csv":
            df = pd.read_csv(file)
            del_column = [x for x in df.keys() if "Unnamed" in x]
            df = df.drop(columns=del_column)
        elif file_type == 'xlsx':
            df = pd.read_excel(file)
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
    drop_down_field.current(0)
    result_field['values'] = Dataview["columns"]
    result_field.current(0)

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
    

def eval_kfold(model, X_fold, y, splits=3):
  # Khởi tạo kfold
    kfold = KFold(n_splits=splits)

    fold_idx = 1
    sum_acc = 0
    log_box.configure(state='normal')
    log_box.delete('1.0', tk.END)
    for train_ids, val_ids in kfold.split(X_fold, y):

        temp_model = model
        temp_model.fit(X_fold.iloc[train_ids], y.iloc[train_ids])
        # Test và in kết quả

        scores = temp_model.score(X_fold.iloc[val_ids], y.iloc[val_ids])
        log_box.insert(tk.END,f'Độ chính xác trên tập train: {model.score(X_fold.iloc[train_ids], y.iloc[train_ids]):.2f}\n')
        log_box.insert(tk.END,f'Độ chính xác trên tập validation: {scores:.2f}\n')
        log_box.insert(tk.END,"Đã train xong Fold\n\n", fold_idx)
        sum_acc += scores
        # Sang Fold tiếp theo
        fold_idx = fold_idx + 1
    result_label['text'] = f'Độ chính xác trung bình sau {fold_idx-1} lần là: '
    result_output['text']= f'{sum_acc/(fold_idx-1):.2f}\n'
    log_box.configure(state='disabled')




def enable_input(var,entry):
    if var.get()==True:
        entry.configure(state='normal')
    else:
        entry.configure(state='disabled')
    pass

def train_model():
    parametes = dict()
    if (n_estimate_var.get() == True):
        if n_estimator_input.get().isnumeric():
            parametes['n_estimators'] = int(n_estimator_input.get())
    if (max_depth_var.get() == True):
        if max_depth_input.get().isnumeric():
            parametes['max_depth'] = int(max_depth_input.get())
    if (min_samples_split_var.get() == True):
        if min_samples_split_input.get().isnumeric():
            parametes['min_samples_split'] = int(min_samples_split_input.get())
    if (min_samples_leaf_var.get() == True):
        if min_samples_leaf_input.get().isnumeric():
            parametes['min_samples_leaf'] = int(min_samples_leaf_input.get())

    global rfc_model
    rfc_model = RandomForestClassifier(**parametes)
    
    ## Delete column result
    X = data.drop(result_field.get(), axis=1)
    y = data[result_field.get()]
    ##

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    eval_kfold(rfc_model, X_train,y_train)
    
def predict():
    predict_win = tk.Tk()
    predict_win.title("Predict to file")
    
    predict_win.geometry("1024x140")
    predict_file_label = tk.Label(predict_win,text="File cần predict: ",width=25,anchor='w')
    predict_file_label.grid(row=0,column=0,padx=(20,10),pady=(10,10))
    result_file_label = tk.Label(predict_win,text="Lưu vào: ",anchor="w",width=25)
    result_file_label.grid(row=1,column=0,padx=(20,10),pady=(10,10))
    
    input_entry = tk.Entry(predict_win,width=100)
    input_entry.grid(row=0,column=1,padx=(20,20),pady=(10,10))

    output_entry = tk.Entry(predict_win,width=100)
    output_entry.grid(row=1,column=1,padx=(20,20),pady=(10,10))

    

    


    def read_file():

        filename = filedialog.askopenfilename(initialdir='./', 
                                          title="Select a file",
                                          filetypes=(("csv files","*.csv"),("xlsx files","*.xlsx")))
        input_entry.delete(0,tk.END)
        input_entry.insert(tk.END,filename)
        predict_win.focus_force()
        

    def save_file():
        filename = filedialog.asksaveasfilename()
        output_entry.delete(0,tk.END)
        output_entry.insert(tk.END,filename)
        predict_win.focus_force()
    

    
    open_button = tk.Button(predict_win,text="Open",command=lambda:read_file(),width=15)
    open_button.grid(row=0,column=3)

    save_button = tk.Button(predict_win,text="Save",command=lambda:save_file(),width=15)
    save_button.grid(row=1,column=3)

    start_predict = tk.Button(predict_win,text="Predict",width=15,command=lambda:predict_data())
    start_predict.grid(row=2, column=1)

    def predict_data():
        filename = input_entry.get()
        try:
            print(filename)
            file = r"{}".format(filename)
            file_type = file.split('.')[-1]
            print(file_type)
            global predict_data
            if  file_type == 'csv':
                predict_data = pd.read_csv(filename)
                del_column = [x for x in predict_data.keys() if "Unnamed" in x]
                predict_data = predict_data.drop(columns=del_column)
            elif file_type == 'xlsx':
                predict_data
                predict_data = pd.read_excel(filename)
                del_column = [x for x in predict_data.keys() if "Unnamed" in x]
                predict_data = predict_data.drop(columns=del_column)
            else:
                tk.messagebox.showerror("Information", "File bạn chọn không được hỗ trợ để mở")
        except ValueError:
            tk.messagebox.showerror("Information","File bạn chọn không tồn tại")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Information","No such file as {file_path}")
            return None
        # print(rfc_model.predict(predict_data))
        predict_data['predict']=rfc_model.predict(predict_data)
        predict_data.to_csv(output_entry.get())
        tk.messagebox.showinfo("Information","Dự đoán kết quả và lưu file thành công")
        predict_win.destroy()





top.mainloop()