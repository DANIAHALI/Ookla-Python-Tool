from tkinter import *
import time
import Ookla_Tool


print('Processing Start Please Wait!')
master = Tk()
master.title('RF Activities Automation')
master.geometry("632x440")
master.resizable(width=False, height=False)
master.iconbitmap("Images\\huawei_icon.ico")
icon1 = PhotoImage(file="Images\\edureka.png")


Img_ico = Label(master, image=icon1)
Img_ico.place(x = 0, y = 0)
subject_lab = Label(master, text="Count of previous days for data retrieval/ Keep blank for all days")
subject_lab.place(x = 140, y = 240)
# To_lab = Label(master, text="Password: ")
# To_lab.place(x = 40, y = 280)
# msg_lab = Label(master, text="Message: ")
# msg_lab.place(x = 40, y = 310)


c2 = Entry(master)
# c3 = Entry(master)
# c4 = Entry(master)


c2.insert(20, "")
# c3.insert(300, "")
# c4.insert(100, "")


c2.place(x = 145, y = 280, height = 25, width = 340)
# c3.place(x = 120, y = 280, height = 25, width = 420)
# c4.place(x = 120, y = 310, height = 25, width = 420)

# variable = StringVar(master)
# variable.set("3G")  # Info :3G Variable set
#
# OptionMenu(master, variable, "4G", "3G").place(x = 470, y = 120, height = 35, width = 65)

Button(master, text='START', width=15, bg='white', command=lambda: Ookla_Tool.main_(c2.get())).place(x = 250, y = 330, height = 35, width = 115)
Label(master, text="For Support : Danish Ali WX854280    Contact : 00971508552942 ").place(x = 140, y = 410)
mainloop()
