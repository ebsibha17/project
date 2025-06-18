import os
from tkinter import *
from PIL import Image,ImageTk
images=[]
index=0
def load_images():
    image_folder="images"
    supported=(".jpg",".jpeg",".png",".bmp")
    for file in os.listdir(image_folder):
        if file.lower().endswith(supported):
            images.append(os.path.join(image_folder,file))

    if images:
        show_image()
    else:
        label.config(text="No images found in 'images' folder")

def show_image():
    img=Image.open(images[index])
    img=img.resize((980,650),Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img,text="")
    label.image=tk_img

def next_image():
    global index 
    if index < len(images)-1:
        index+=1
        show_image()
    
def previous_image():
    global index 
    if index > 0:
        index-=1
        show_image()


window = Tk()
window.title("Image Viewer")
window.geometry("1000x750")

label = Label(window,text = "Loading images")
label.pack(pady=10)

btn_frame = Frame(window)
btn_frame.pack()

Button(btn_frame,text="<< Prev",command=previous_image).grid(row=0, column=0, padx=5)
Button(btn_frame,text="Exit",command=window.quit).grid(row=0, column=1, padx=10, pady=10)
Button(btn_frame,text="Next >>",command=next_image).grid(row=0, column=2, padx=5)

load_images()

window.mainloop()