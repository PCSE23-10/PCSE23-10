# -*- coding: utf-8 -*-


from tkinter import *

import cv2
import numpy as np
from PIL import ImageGrab, Image, ImageTk
from tensorflow.keras.models import load_model

l1 = []
l2 = []
l3 = []
l4 = []
final_number = 0
binary_number = 0
octal_number = 0 
hexadecimal_number = 0
temp = 0
model = load_model('trained_model.h5')
image_folder = "img/"

root = Tk()
root.resizable(0, 0)
root.title("Handwritten Digit Recognition")

lastx, lasty = None, None
image_number = 0

cv = Canvas(root, width=640, height=480, bg='white')
cv.grid(row=0, column=0, pady=2, sticky=W, columnspan=2)


def clear_widget():
    global cv
    cv.delete('all')


def draw_lines(event):
    global lastx, lasty
    x, y = event.x, event.y
    cv.create_line((lastx, lasty, x, y), width=10, fill='black', capstyle=ROUND, smooth=TRUE, splinesteps=12)
    lastx, lasty = x, y


def activate_event(event):
    global lastx, lasty
    cv.bind('<B1-Motion>', draw_lines)
    lastx, lasty = event.x, event.y


cv.bind('<Button-1>', activate_event)


def Recognize_Digit():
    def copy():
        root.clipboard_clear()
        root.clipboard_append(T.get())
    def set_text(text):
        T.configure(state='normal')
        T.delete(0,END)
        T.insert(0,text)
        T.configure(state='disabled', disabledbackground='white', disabledforeground='black')
        return
    global image_number
    global l1
    global l2
    global l3
    global l4
    global final_number
    global temp
    global binary_number
    global octal_number
    global hexadecimal_number
    l1 = []
    l2 = []
    l3 = []
    temp = 0
    filename = f'img_{image_number}.png'
    widget = cv
    
    x = root.winfo_rootx() + widget.winfo_x()      
    y = root.winfo_rooty() + widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    print(x, y, x1, y1)
    
    # get image and save
    ImageGrab.grab().crop((x, y, x1, y1)).save(image_folder + filename)

    image = cv2.imread(image_folder + filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    print(contours)
#     print(contours[0][0])
#     print(contours[1][0])
#     print(contours[2][0])
#     print(contours[3][0])
#     print(contours[4][0])

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # make a rectangle box around each curve
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping out the digit from the image corresponding to the current contours in the for loop
        digit = th[y:y + h, x:x + w]
        # cv2.imshow('digit',digit)
        
        # Resizing that digit to (18, 18)
        resized_digit = cv2.resize(digit, (18, 18))
        
        # cv2.imshow('resize',resized_digit)
        
        # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
        padded_digit = np.pad(resized_digit, ((5, 5), (5, 5)), "constant", constant_values=0)
        
        # cv2.imshow('final_padded',padded_digit)
        
        digit = padded_digit.reshape(1, 28, 28, 1) #first 1 because 1 digit to be recognized currently in this loop and second 1 
                                                   #because there is empty dimension as digit image is grayscale
        digit = digit / 255.0
        
        # print(digit)
        temp = model([digit])
        pred = temp[0] # model([digit])[0] #model.predict changed to model because of tensorflow warning
        final_pred = np.argmax(pred)
        temp_pred = np.argmax(temp)
#         print("temp ",temp)
#         print("pred ",pred)
#         print("final_pred ",final_pred)
#         print("temp_pred ",temp_pred)
        l1.append(final_pred) #to add digits to list

        data = str(final_pred) + ' ' + str(int(max(pred) * 100)) + '%'
        # print(data)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        color = (0, 0, 255)
        thickness = 1
        cv2.putText(image, data, (x, y - 5), font, fontScale, color, thickness)
    for i in range(0,len(l1)):
        l2.append(contours[i][0][0][0])
#     for i in range(0,len(l1)):
#         l4.append(contours[i][0][0][1])
    print(l1)
    print(l2)
#     print(l4)
    l3 = [l1 for _,l1 in sorted(zip(l2,l1))]
    print(l3)
    final_number = int("".join(list(map(str,l3))))
    print(final_number)
    np_image = np.array(image)
    ###########################################################
    # MAIN MAIN MAIN MAIN cv2.imshow('Predicted Output', image)
    # MAIN MAIN MAIN MAIN cv2.waitKey(0)
    new_window = Toplevel(root)
    new_window.title('Predicted Output')
    new_window.geometry("855x580")
    new_window.resizable(0,0)
    photo = ImageTk.PhotoImage(image = Image.fromarray(np_image))
    panel = Label(new_window, image=photo)
    panel.image = photo
#     panel.pack()
    panel.grid(row=0, column=1)
    ctb = Button(new_window,text='Convert to Binary', command=lambda:set_text(format(final_number, "b")))
    ctb.grid(row=2, column=0, pady=1, padx=1)
#     if t=="Button-1 Clicked":
#         T.delete(0,END)
#         T.insert(0,text)
#     ctb.pack()
    cto = Button(new_window,text='Convert to Octal', command=lambda:set_text(format(final_number, "o")))
    cto.grid(row=2, column=2, pady=1, padx=1)
#     cto.pack()
    cthd = Button(new_window,text='Convert to Hexadecimal', command=lambda:set_text(format(final_number, "X")))
    cthd.grid(row=2, column=1, pady=1, padx=1)
#     cthd.pack()      
    T = Entry(new_window, width = 32) #T = Text(new_window, height = 2, width = 32) 
#     T.insert(END, binary_number)
    l = Label(new_window,text='Converted Number')
    l.grid(row=4, column=1)
    T.grid(row=5, column=1)
    copy_btn = Button(new_window,text='COPY', command=copy)
    copy_btn.place(x=535,y=534)

        
btn_save = Button(text='Recognize Number', command=Recognize_Digit)
btn_save.grid(row=2, column=0, pady=1, padx=1)
button_clear = Button(text='Clear Canvas', command=clear_widget)
button_clear.grid(row=2, column=1, pady=1, padx=1)

root.mainloop()

