from tkinter import *
import win32api
import time
import threading
from win10toast import ToastNotifier
from pystray import MenuItem as item
import pystray
from PIL import Image
import sys
import datetime




def backgroundThreadRunner() :
    threading.Thread(target=start, daemon=True).start()

def start() :
    timer = timerStart()
    activityCheck()


# Logic :

promptInterval = 25*60;
breakDuration = 2*60;
idleThreshold = 10*60;
threads = 0;
startButton = True
absoluteAlertTime = 0;
absoluteBreakTime = 0;
timer = 0;
whatIsHappening = "nothing"

base_path = getattr(sys, '_MEIPASS','.')+'/'

def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) // 1000

n = ToastNotifier()


def eyeNotify() :

    idleTime = getIdleTime()
    if idleTime < idleThreshold :
        n.show_toast(
        title="eyeCare Time !", 
        msg="Time to take your eyes off the screen for " + (str(breakDuration/60) if breakDuration != 0 else "few") + " minutes", 
        duration = 5,
        icon_path =base_path + "eye.ico",
        threaded=True,
        )

        global absoluteBreakTime, whatIsHappening;
        absoluteBreakTime = datetime.datetime.now() + datetime.timedelta(seconds=breakDuration)

        whatIsHappening = "breakTimerCountDown"

        time.sleep(breakDuration)

        if breakDuration != 0 :
            n.show_toast(
            "Back to Work !", 
            "You can get back to work now", 
            duration = 5,
            icon_path =base_path + "eye.ico",
            threaded=True
            )
        global timer;
        whatIsHappening = "timerCountDown"
        timer = timerStart()
        activityCheck()
    else :
        timer.cancel()
        waitingForReset()

def timerStart(timeElapsed=0) :
    global timer, absoluteAlertTime;
    timer = threading.Timer(promptInterval-timeElapsed, eyeNotify)
    timer.start()
    absoluteAlertTime = datetime.datetime.now() + datetime.timedelta(seconds=promptInterval)
    return timer

def activityCheck() :
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
    
    
    global whatIsHappening;
    whatIsHappening = "standbyMode"

    while 1 :
        time.sleep(idleThreshold)
        idleTime = getIdleTime()

        if idleTime < idleThreshold :
            global timer;
            
            timer = timerStart(idleTime)

           
            whatIsHappening = "timerCountDown"
            activityCheck()

# GUI Link

def timerDisplay() :
    while 1 :
        timeRemaining = absoluteAlertTime - datetime.datetime.now()


        if timeRemaining.days >= 0 and whatIsHappening == "timerCountDown" :

            canvas.itemconfig(standbyPage, state='hidden')
            canvas.itemconfig(breakTimeRemainingText, state='hidden')
            canvas.itemconfig(hh, state='normal')
            canvas.itemconfig(mm, state='normal')
            canvas.itemconfig(ss, state='normal')
            canvas.itemconfig(background1, state='normal')
            canvas.itemconfig(timeRemainingText, state='normal')


            timeRemaining = timeRemaining.seconds

            minute,second = (timeRemaining // 60 , timeRemaining % 60)
            hour =0
            if minute > 60:
                hour , minute = (minute // 60 , minute % 60)

            canvas.itemconfig(hh, text=hour)
            canvas.itemconfig(mm, text=minute)
            canvas.itemconfig(ss, text=second)

            # print(hour, minute, second)

            window.update()

            time.sleep(1)
        elif whatIsHappening == "breakTimerCountDown" :

            canvas.itemconfig(standbyPage, state='hidden')
            canvas.itemconfig(timeRemainingText, state='hidden')
            canvas.itemconfig(hh, state='normal')
            canvas.itemconfig(mm, state='normal')
            canvas.itemconfig(ss, state='normal')
            canvas.itemconfig(background1, state='normal')
            canvas.itemconfig(breakTimeRemainingText, state='normal')

            breakTimeRemaining = (absoluteBreakTime - datetime.datetime.now()).seconds

            minute,second = (breakTimeRemaining // 60 , breakTimeRemaining % 60)
            hour =0
            if minute > 60:
                hour , minute = (minute // 60 , minute % 60)

            canvas.itemconfig(hh, text=hour)
            canvas.itemconfig(mm, text=minute)
            canvas.itemconfig(ss, text=second)

            # print(hour, minute, second)

            window.update()

            time.sleep(1)

        elif whatIsHappening == "standbyMode" :
            canvas.itemconfig(hh, state='hidden')
            canvas.itemconfig(mm, state='hidden')
            canvas.itemconfig(ss, state='hidden')
            canvas.itemconfig(background1, state='hidden')
            canvas.itemconfig(timeRemainingText, state='hidden')
            canvas.itemconfig(breakTimeRemainingText, state='hidden')
            canvas.itemconfig(standbyPage, state='normal')

            time.sleep(1)
        else :
            time.sleep(1)

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

        n.show_toast(
        title="eyeCare Timer Set", 
        msg="Your eyeCare timer is set \n You can close the program now and access it later in the system tray", 
        duration = 5,
        icon_path =base_path + "eye.ico",
        threaded=True,
    )

        canvas.itemconfig(background, state='hidden')
        canvas.itemconfig(entry0_bg, state='hidden')
        canvas.itemconfig(entry1_bg, state='hidden')
        canvas.itemconfig(entry2_bg, state='hidden')
        entry0.destroy()
        entry1.destroy()
        entry2.destroy()

        canvas.itemconfig(background1, state='normal')
        canvas.itemconfig(hh, state='normal')
        canvas.itemconfig(mm, state='normal')
        canvas.itemconfig(ss, state='normal')
        canvas.itemconfig(timeRemainingText, state='normal')

        # timerDisplay()
        global whatIsHappening
        whatIsHappening = "timerCountDown"
        threading.Thread(target=timerDisplay, daemon=True).start()
    else :
        window.destroy()


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



# Second page

background_img1 = PhotoImage(file = base_path + "background1.png")
background1 = canvas.create_image(
    293.5, 175.0,
    image=background_img1)
canvas.itemconfig(background1, state='hidden')

timeRemainingText = canvas.create_text(
    360, 233.5,
    text = "Time remaining :",
    fill = "#2f423f",
    font = ("Nunito-SemiBold", int(24.0)))
canvas.itemconfig(timeRemainingText, state='hidden')

breakTimeRemainingText = canvas.create_text(
365.0, 233.5,
text = "Break time remaining :",
fill = "#2f423f",
font = ("Nunito-SemiBold", int(24.0)))
canvas.itemconfig(breakTimeRemainingText, state='hidden')

hh = canvas.create_text(
    250.0, 290.5,
    text = "60",
    fill = "#2f423f",
    font = ("Nunito-SemiBold", int(48.0)))
canvas.itemconfig(hh, state='hidden')

mm = canvas.create_text(
    352.0, 290.5,
    text = "60",
    fill = "#2f423f",
    font = ("Nunito-SemiBold", int(48.0)))
canvas.itemconfig(mm, state='hidden')

ss = canvas.create_text(
    453.0, 290.5,
    text = "60",
    fill = "#2f423f",
    font = ("Nunito-SemiBold", int(48.0)))
canvas.itemconfig(ss, state='hidden')

# Third page (standby)

standby_img = PhotoImage(file = base_path + "StandbyBackground.png")
standbyPage = canvas.create_image(
    301.5, 180.0,
    image=standby_img)
canvas.itemconfig(standbyPage, state='hidden')

# Show in system tray

def quit_window(icon, item):
    icon.stop()
    window.destroy()

def show_window(icon, item):
    icon.stop()
    window.after(0,window.deiconify)


    global whatIsHappening
    timeRemaining = absoluteAlertTime - datetime.datetime.now()
    whatIsHappening = ("timerCountDown" if timeRemaining.days >= 0 else "breakTimerCountDown")
    

def withdraw_window():  
    window.withdraw()
    image = Image.open(base_path + "eye.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    global icon;
    icon = pystray.Icon("Smart eyeCare", image, "Smart eyeCare", menu)
    icon.run()

window.protocol('WM_DELETE_WINDOW', withdraw_window)

window.resizable(False, False)
window.mainloop()
