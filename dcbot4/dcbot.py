import threading
import mouse
import keyboard
import sys
import os
from pathlib import Path
from subprocess import Popen
import requests
import pickle
import time
import datetime
import tkinter as tk
from tkinter import X, BOTTOM, TOP, Entry, Text, Frame, messagebox
from tkinter.ttk import Label, Button

VERSION = 4
        
class Custommove():
    def record():
        global mousepos
        global mouse_events
        global keyboard_events

        for widgets in frame.winfo_children():
            widgets.destroy()
        
        root.title('3')
        time.sleep(1)
        root.title('2')
        time.sleep(1)
        root.title('1')
        time.sleep(1)
        root.title('Recording...')

        mouse_events = []

        mousepos = mouse.get_position()
        mouse.hook(mouse_events.append)
        keyboard.start_recording()

        keyboard.wait('esc')
        mouse.unhook(mouse_events.append)
        keyboard_events = keyboard.stop_recording()
        Custommove.confirm()

    def play():
        for widgets in frame.winfo_children():
            widgets.destroy()
        
        root.title('Playing...')
        
        k_thread = threading.Thread(target = lambda :keyboard.play(keyboard_events))
        k_thread.start()

        m_thread = threading.Thread(target = lambda :mouse.play(mouse_events))
        mouse.move(-2000, -2000, absolute=False, duration=0.01)
        mouse.move(1000, 59, absolute=False, duration=0.01)
        m_thread.start()

        k_thread.join()
        m_thread.join()

        x = datetime.datetime.now()
        x = x.second
        if x == 59:
            x = 58

        futurex = x+1

        while x != futurex:
            x = datetime.datetime.now()
            x = x.second
            if mouse.is_pressed('right') == True:
                root.destroy()
                sys.exit()

        Custommove.play()
    
    def save():
        global name
        global mouse_events
        global keyboard_events
        global mousepos

        savename = name.get()
        savenametxt = savename + '.txt'

        for widgets in frame.winfo_children():
            widgets.destroy()

        root.title('Saving It...')
        
        del keyboard_events[-1]

        situation = Label(frame, text = 'Saving it...', font = ("Arial", 14))
        situation.pack()

        b1 = Button(frame, text = "Play", command = Custommove.play)
        b1.pack(ipadx= 20, ipady = 20, fill = X, expand = False, side = BOTTOM)
        b2 = Button(frame, text = "Home", command = homepage)
        b2.pack(ipadx= 20, ipady = 20, fill = X, expand = False, side = BOTTOM)

        try:
            os.chdir("Saved Recordings")
            path = Path.cwd() / savename
            path.mkdir()
            os.chdir(savename)
            Path(savenametxt).touch()
            path = Path(savenametxt)
            path.write_text(savename)
            Path("Mouse Recordings.txt").touch()
            
            with open('Mouse Recordings.txt', 'wb') as filehandle:
                pickle.dump(mouse_events, filehandle)
                    
            Path("Keyboard Recordings.txt").touch()
            
            with open('Keyboard Recordings.txt', 'wb') as filehandle:
                pickle.dump(keyboard_events, filehandle)
                
            Path("Mouse Position.txt").touch()
            
            with open('Mouse Position.txt', 'wb') as filehandle:
                pickle.dump(mousepos, filehandle)

            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)
            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)

            situation.config(text = "Your recording has been saved...")
            root.title('It Has Been Saved...')

        except FileExistsError:
            situation.config(text = "This name already exists please change it...")
            root.title('There Was An Error While Saving')
        
    def name():
        global name

        for widgets in frame.winfo_children():
            widgets.destroy()

        root.title('Asking Name...')
        
        askname = Label(frame, text = "Type the name you want to save it as...", font = ("Arial", 15))
        askname.pack()
        name = Entry(frame, width = 50)
        name.pack()
        enter = Button(frame, text = "Enter", command = Custommove.save)
        enter.pack(ipady = 20, fill = X, expand = False, side = BOTTOM)
            
    def confirm():
        for widgets in frame.winfo_children():
            widgets.destroy()

        root.title('Confirming Save...')
        
        ask = Label(frame, text = 'Do you want to save the recording...', font = ('Arial', 15))
        ask.pack()
        
        no = Button(frame, text="No", command = Custommove.play)
        yes = Button(frame, text="Yes", command = Custommove.name)
        no.pack(ipadx = 50, ipady = 20, fill = X, expand=False, side = BOTTOM)
        yes.pack(ipadx = 50, ipady = 20, fill = X, expand=False, side = BOTTOM)

    def findfile(button_press):
        global keyboard_events
        global mouse_events
        global mousepos

        root.title('Play')

        for widgets in frame.winfo_children():
            widgets.destroy()
        
        os.chdir("Saved Recordings")
        os.chdir(button_press)
                
        with open('Mouse Recordings.txt', 'rb') as filehandle:
            mouse_events = pickle.load(filehandle)

        with open('Keyboard Recordings.txt', 'rb') as filehandle:
            keyboard_events = pickle.load(filehandle)
                
        with open('Mouse Position.txt', 'rb') as filehandle:
            mousepos = pickle.load(filehandle)

        play = Button(frame, text = 'Play', command = Custommove.play)
        play.pack(ipadx = 20, ipady = 20, fill = X, expand = False, side = TOP)

def check_updates():
    for widgets in frame.winfo_children():
        widgets.destroy()

    root.title('Checking for updates...')

    b1 = Button(frame, text = "Back", command = homepage)
    b1.pack(ipadx= 10, ipady = 10, fill = X, expand = False, side = TOP)

    checkupdate = Label(frame, text = "Looking for updates", font = ("Arial", 14))
    checkupdate.pack()
    
    try:
        link = "https://raw.githubusercontent.com/DoduCode/dcbot/main/Update/version.txt"
        check = requests.get(link)
        
        if float(VERSION) < float(check.text):
            mb1 = messagebox.askyesno('Update Available', 'There is an update available. Click yes to update.')
            if mb1 is True:
                filename = os.path.basename(sys.argv[0])
                savedrecordings = "Saved Recordings"

                for file in os.listdir():
                    if file == filename:
                        pass

                    elif file == savedrecordings:
                        pass

                    else:
                        os.remove(file)

                exename = f'dcbot{float(check.text)}.exe'
                code = requests.get("https://raw.githubusercontent.com/DoduCode/dcbot/main/Update/dcbot.exe", allow_redirects = True)
                open(exename, 'wb').write(code.content)

                root.destroy()
                os.remove(sys.argv[0])
                sys.exit()
                
            elif mb1 == 'No':
                pass
            
        else:
            messagebox.showinfo('Updates Not Available', 'No updates are available')

    except Exception as e:
        pass
            
def saved():
    for widgets in frame.winfo_children():
        widgets.destroy()

    root.title('Saved Recordings...')
    
    b1 = Button(frame, text = "Home", command = homepage)
    b1.pack(ipadx= 10, ipady = 10, fill = X, expand = False, side = TOP)

    incase = Label(frame, text = 'If this appears empty either you have no saved recordings.', font = ("Arial", 14))
    incase.pack()

    dirs = os.listdir("Saved Recordings")

    for files in dirs:
        name = files
        button = Button(frame, text = name, command = lambda m = name: Custommove.findfile(m))
        button.pack(ipadx = 20, ipady = 20, fill = X, expand = False, side = BOTTOM)

def homepage():
    for widgets in frame.winfo_children():
        widgets.destroy()

    root.title('Home')
        
    l1 = Label(frame, text="Press the button to record and press the esc button when you are done recording.\nTo exit the bot while it is running just right click when it tells you to.", font = ("Arial", 14))
        
    b1 = Button(frame, text = "Record", command = Custommove.record)
    b2 = Button(frame, text = "Saved", command = saved)
    b3 = Button(frame, text = "Check For Updates", command = check_updates)

    b1.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)
    b2.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)
    b3.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)

    l1.pack()
    
if not os.path.exists("Saved Recordings"):
    path = Path.cwd() / "Saved Recordings"
    path.mkdir()
    
root = tk.Tk()
root.geometry('800x400')
root.resizable(True,  True)
root.title('Checking for updates...')
    
try:
    link = "https://raw.githubusercontent.com/DoduCode/dcbot/main/Update/version.txt"
    check = requests.get(link)
        
    if float(VERSION) < float(check.text):
        mb1 = messagebox.showinfo('Update Available', 'There is an update available. Click Check For Updates and click yes after that.')

    else:
        pass

except Exception as e:
    pass

root.title('Home')

frame = Frame(root)
frame.pack(side = "top", expand = True, fill = "both")

l1 = Label(frame, text="Press the button to record and press the esc button when you are done recording.\nTo exit the bot while it is running just right click when it tells you to.", font = ("Arial", 14))

b1 = Button(frame, text = "Record", command = Custommove.record)
b2 = Button(frame, text = "Saved", command = saved)
b3 = Button(frame, text = "Check For Updates", command = check_updates)

b1.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)
b2.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)
b3.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)

l1.pack()

root.mainloop()
