from tkinter import *
import win32api
import time
import threading
from win10toast import ToastNotifier
from pystray import MenuItem as item
import pystray
from PIL import Image
import sys




def backgroundThreadRunner() :
    threading.Thread(target=start, daemon=True).start()

def start() :
    activityCheck(timerStart())


# Logic :

promptInterval = 25*60;
breakDuration = 2*60;
idleThreshold = 10*60;
threads = 0;
startButton = True

base_path = getattr(sys, '_MEIPASS','.')+'/'

def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0

n = ToastNotifier()


def eyeNotify() :

    n.show_toast(
    title="EYE CARE TIME !", 
    msg="Give your eyes some rest, breath in and relax or go for a walk", 
    duration = 5,
    icon_path =base_path + "eye.ico",
    threaded=True,
    )
    print("here now")
    time.sleep(breakDuration)

    if breakDuration != 0 :
        n.show_toast(
        "BACK TO WORK !", 
        "You can get back to work now", 
        duration = 5,
        icon_path =base_path + "eye.ico",
        threaded=True
        )

    activityCheck(timerStart())

def timerStart(timeElapsed=0) :
    timer = threading.Timer(promptInterval-timeElapsed, eyeNotify)
    timer.start()
    return timer

def activityCheck(timer) :
    # print(promptInterval, breakDuration, idleThreshold)
    global stopThread;
    global threads;
    while 1 :
        # print("threads running : ", threading.active_count())
            
        time.sleep(idleThreshold)

        idleTime = getIdleTime()
        if idleTime >= idleThreshold :
            timer.cancel()
            # print("Found not working")
            waitingForReset()

def waitingForReset() :
    while 1 :
        time.sleep(idleThreshold)
        idleTime = getIdleTime()

        if idleTime < idleThreshold :
            activityCheck(timerStart(idleTime))



# GUI Link


def startButtonClicked():
    global startButton
    if startButton == True :
        startButton = False
        # print("Start")
        # print(float(entry0.get()), float(entry1.get()), float(entry2.get()))
        b0.configure(image=img2)

        global promptInterval, breakDuration, idleThreshold
        promptInterval = float(entry0.get())*60;
        breakDuration = float(entry1.get())*60;
        idleThreshold = float(entry2.get())*60;

        # activityCheck(timerStart())

        backgroundThreadRunner()
        withdraw_window()
    else :
        icon.stop()
        window.destroy()

# def resetButtonClicked():
#     # print("reset")
#     entry0.delete(0, 'end')
#     entry0.insert(END, '25')
#     entry1.delete(0, 'end')
#     entry1.insert(END, '2')
#     entry2.delete(0, 'end')
#     entry2.insert(END, '10')

# GUI


window = Tk()

window.wm_title("Smart eyeCare")
window.iconbitmap(base_path + "eye.ico")

window.geometry("703x500")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 500,
    width = 703,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

entry0_img = PhotoImage(file = base_path +"img_textBox0.png")
entry0_bg = canvas.create_image(
    458.5, 190.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#f59b1f",
    highlightthickness = 0,
    fg="#ffffff",
    font="Nunito 22 bold")

entry0.place(
    x = 434.7890625, y = 170,
    width = 57.421875,
    height = 38)

entry0.insert(END, '25')

entry1_img = PhotoImage(file = base_path + "img_textBox1.png")
entry1_bg = canvas.create_image(
    458.5, 266.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#f59b1f",
    highlightthickness = 0,
    fg="#ffffff",
    font="Nunito 22 bold")

entry1.place(
    x = 434.7890625, y = 246,
    width = 57.421875,
    height = 38)

entry1.insert(END, '2')

entry2_img = PhotoImage(file = base_path + "img_textBox2.png")
entry2_bg = canvas.create_image(
    458.5, 341.0,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#f59b1f",
    highlightthickness = 0,
    fg="#ffffff",
    font="Nunito 22 bold")

entry2.place(
    x = 434.7890625, y = 321,
    width = 57.421875,
    height = 38)

entry2.insert(END, '10')

img2 = PhotoImage(file = base_path + "img2.png")
img0 = PhotoImage(file = base_path + "img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = startButtonClicked,
    relief = "flat")

b0.place(
    x = 291, y = 415,
    width = 121,
    height = 42)

# img1 = PhotoImage(file = f"img1.png")
# b1 = Button(
#     image = img1,
#     borderwidth = 0,
#     highlightthickness = 0,
#     command = resetButtonClicked,
#     relief = "flat")

# b1.place(
#     x = 429, y = 415,
#     width = 71,
#     height = 42)


background_img = PhotoImage(file = base_path + "background.png")
background = canvas.create_image(
    316.0, 175.0,
    image=background_img)



# Show in system tray

def quit_window(icon, item):
    icon.stop()
    window.destroy()

def show_window(icon, item):
    icon.stop()
    window.after(0,window.deiconify)

def withdraw_window():  
    window.withdraw()
    image = Image.open(base_path + "eye.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    global icon;
    icon = pystray.Icon("name", image, "Smart eyeCare", menu)
    icon.run()

window.protocol('WM_DELETE_WINDOW', withdraw_window)

window.resizable(False, False)
window.mainloop()
