# imgcode_gui v0.1 08/04/2019
# utility for CNC lasers image etching
# developed by M. "Vidmo" Widomski  
# github.com/vidmo91
# hackaday.io/vidmo91
# 
# graphic user interface overlay for imgcode. use with imgcode_cli4gui, which has simplified UI
# 
# 
# 

# Copyright 2019 M.Widomski
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tkinter import *
import tkinter.filedialog
import subprocess
import os
output=""
errors=""
img_file_name="lena.png"
gcode_file_name="test.nc"


root = Tk()
show_preview_var=IntVar()

root.iconbitmap('icon.ico')
root.title("imgcode GUI")
def load_image_click():  
    global show_preview_var
    global img_file_name
    img_file_name = tkinter.filedialog.askopenfilename(
        parent=root,
        title='choose image',
        filetypes=[('images', '.png .jpg .jpeg .gif .png'),
                   ('png images', '.png'),
                   ('jpeg images', '.jpg .jpeg'),
                   ('gif images', '.gif'),
                   ('bitmap images', '.bmp'),
                   ('all files', '.*')]
        )
        
    if(show_preview_var.get()==1):
        new_window = Toplevel(root)
        new_window.iconbitmap('icon.ico')
        image = PhotoImage(file=img_file_name)
        l1 = Label(new_window, image=image)
        l1.image = image
        l1.pack()

load_image_button = Button(root, text='load image', command=load_image_click)  
load_image_button.pack(fill='x')

def save_gcode_click():  
    global gcode_file_name
    gcode_file_name = tkinter.filedialog.asksaveasfilename(
        parent=root,
        title='choose gcode file',
        filetypes=[('gcode nc file', '.nc'),
                   ('text file', '.txt'),
                   ('don\'t know, don\'t care', '.*')],
        defaultextension="*.*"
        )


save_gcode_button = Button(root, text='choose gcode file', command=save_gcode_click)  
save_gcode_button.pack(fill='x')

def run_button_click():
    p = subprocess.Popen(".\env_imGcode\Scripts\python.exe .\imgcode_cli4gui.py "+img_file_name+" "+gcode_file_name+" "+x_offset_entry.get()+" "+y_offset_entry.get()+" "+output_size_entry.get()+" "+pixel_size_entry.get()+" "+feed_rate_entry.get()+" "+laser_power_entry.get()+" "+colours_entry.get() ,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#    p = subprocess.Popen(".\imgcode_cli4gui.exe "+img_file_name+" "+gcode_file_name+" "+x_offset_entry.get()+" "+y_offset_entry.get()+" "+output_size_entry.get()+" "+pixel_size_entry.get()+" "+feed_rate_entry.get()+" "+laser_power_entry.get()+" "+colours_entry.get() ,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    global output
    global show_preview_var
    output = p.communicate()
    text.pack()
    text.delete(1.0,END)
    text_var="imgcode_cli4gui "+img_file_name+" "+gcode_file_name+" "+x_offset_entry.get()+" "+y_offset_entry.get()+" "+output_size_entry.get()+" "+pixel_size_entry.get()+" "+feed_rate_entry.get()+" "+laser_power_entry.get()+" "+colours_entry.get()+"\n\n\n"
    text.pack()
    text.insert(END,text_var)    
    text.pack()
    text.insert(END,output)
    text_var = "\n\n"
    text.pack()
    text.insert(END,text_var)
    
    if(show_preview_var.get()==1):
        new_window = Toplevel(root)
        image = PhotoImage(file="out_img.png")
        l1 = Label(new_window, image=image)
        l1.image = image
        l1.pack()


def num_chk(input):
    if input=="":
        return True
    else:
        try:
            float(input)
            return True
        except ValueError:
            return False


reg_num_chk=root.register(num_chk)


x_offset_label=Label(root,text="x offset [mm]")
x_offset_label.pack()
x_offset_entry=Entry(root)
x_offset_entry.pack()
x_offset_entry.insert(INSERT,"0")
x_offset_entry.config(validate="key", validatecommand=(reg_num_chk, '%P'))



y_offset_label=Label(root,text="y offset [mm]")
y_offset_label.pack()
y_offset_entry=Entry(root)
y_offset_entry.pack()
y_offset_entry.insert(INSERT,"0")
y_offset_entry.config(validate="key", validatecommand=(reg_num_chk, '%P'))


output_size_label=Label(root,text="output image horizontal size [mm]")
output_size_label.pack()
output_size_entry=Entry(root)
output_size_entry.pack()
output_size_entry.insert(INSERT,"100")
output_size_entry.config(validate="key", validatecommand=(reg_num_chk, '%P'))

pixel_size_label=Label(root,text="pixel size [mm]")
pixel_size_label.pack()
pixel_size_entry=Entry(root)
pixel_size_entry.pack()
pixel_size_entry.insert(INSERT,"0.1")
pixel_size_entry.config(validate="key", validatecommand=(reg_num_chk, '%P'))

feed_rate_label=Label(root,text="feed rate [mm/min]")
feed_rate_label.pack()
feed_rate_entry=Entry(root)
feed_rate_entry.pack()
feed_rate_entry.insert(INSERT,"100")
feed_rate_entry.config(validate="key", validatecommand=(reg_num_chk, '%P'))

laser_power_label=Label(root,text="maximum laser power")
laser_power_label.pack()
laser_power_entry=Entry(root)
laser_power_entry.pack()
laser_power_entry.insert(INSERT,"255")
laser_power_entry.config(validate="key", validatecommand=(reg_num_chk, '%P'))

colours_label=Label(root,text="number of colours (2 >= no. of colours >= 255)")
colours_label.pack()
colours_entry=Entry(root)
colours_entry.pack()
colours_entry.insert(INSERT,"2")
colours_entry.config(validate="key", validatecommand=(reg_num_chk, '%P'))

show_preview_button=Checkbutton(root,text="show preview images",variable=show_preview_var, onvalue=1, offvalue=0)
show_preview_button.pack()
show_preview_button.select()

empty_label=Label(root,text="")
empty_label.pack()

run_button= Button(root,text='run', command=run_button_click)
run_button.pack(fill='x')

text = Text(root)
text.pack()
text.insert(END, output)
root.mainloop()


