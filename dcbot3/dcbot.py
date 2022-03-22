import threading
import mouse
import keyboard
import sys
import os
from pathlib import Path
import pickle
import time
import datetime
import tkinter as tk
from tkinter import X, BOTTOM, TOP, Entry, Frame
from tkinter.ttk import Label, Button
        
class Custommove():
    def record():
        global frame
        global homeframe
        global mousepos
        global mouse_events
        global keyboard_events

        try:
            frame.destroy()
            homeframe.destroy()
            findfileframe.destroy()

        except NameError:
            pass
        
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
        global filefindframe
        global recordframe

        try:
            filefindframe.destroy()
            recordframe.destroy()

        except NameError:
            pass
        
        root.title('Playing...')

        playframe = Frame(root)
        playframe.pack(side = 'top', expand = True, fill = 'both')
        
        k_thread = threading.Thread(target = lambda :keyboard.play(keyboard_events))
        k_thread.start()

        m_thread = threading.Thread(target = lambda :mouse.play(mouse_events))
        mouse.move(-2000, -2000, absolute=False, duration=0.01)
        mouse.move(1000, 59, absolute=False, duration=0.01)
        m_thread.start()

        k_thread.join()
        m_thread.join()

        skip = Label(playframe, text = 'You can skip in 1 second', font = ("Arial", 14))
        skip.pack()

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

        skip.destroy()

        Custommove.play()
    
    def save():
        global saveframe
        global nameframe
        global mouse_events
        global keyboard_events
        global mousepos

        root.title('Saving It...')
        
        del keyboard_events[-1]

        check = 'Home from save()'

        savename = name.get()
        savenametxt = savename + '.txt'

        nameframe.destroy()

        saveframe = Frame(root)
        saveframe.pack(side = 'top', expand = True, fill = 'both')

        situation = Label(saveframe, text = 'Saving it...', font = ("Arial", 14))
        situation.pack()

        b1 = Button(saveframe, text = "Play", command = Custommove.play)
        b1.pack(ipadx= 20, ipady = 20, fill = X, expand = False, side = BOTTOM)
        b2 = Button(saveframe, text = "Home", command = lambda m = check: homepage(m))
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
        global nameframe
        global confirmframe
        global name

        root.title('Asking Name...')
        
        confirmframe.destroy()

        nameframe = Frame(root)
        nameframe.pack(side = 'top', expand = True, fill = 'both')
        
        askname = Label(nameframe, text = "Type the name you want to save it as...", font = ("Arial", 15))
        askname.pack()
        name = Entry(nameframe, width = 50)
        name.pack()
        enter = Button(nameframe, text = "Enter", command = Custommove.save)
        enter.pack(ipady = 20, fill = X, expand = False, side = BOTTOM)
            
    def confirm():
        global recordframe
        global confirmframe

        root.title('Confirming Save...')
        
        recordframe.destroy()

        confirmframe = Frame(root)
        confirmframe.pack(side = 'top', expand = True, fill = 'both')
        
        ask = Label(confirmframe, text = 'Do you want to save the recording...', font = ('Arial', 15))
        ask.pack()
        
        no = Button(confirmframe, text="No", command = Custommove.play)
        yes = Button(confirmframe, text="Yes", command = Custommove.name)
        no.pack(ipadx = 50, ipady = 20, fill = X, expand=False, side = BOTTOM)
        yes.pack(ipadx = 50, ipady = 20, fill = X, expand=False, side = BOTTOM)

    def findfile(button_press):
        global savedframe
        global keyboard_events
        global mouse_events
        global mousepos
        global findfileframe
        
        os.chdir("Saved Recordings")
        os.chdir(button_press)

        savedframe.destroy()

        findfileframe = Frame(root)
        findfileframe.pack(side = 'top', expand = True, fil = 'both')
                
        with open('Mouse Recordings.txt', 'rb') as filehandle:
            mouse_events = pickle.load(filehandle)

        with open('Keyboard Recordings.txt', 'rb') as filehandle:
            keyboard_events = pickle.load(filehandle)
                
        with open('Mouse Position.txt', 'rb') as filehandle:
            mousepos = pickle.load(filehandle)

        play = Button(findfileframe, text = 'Play', command = Custommove.play)
        play.pack(ipadx = 20, ipady = 20, fill = X, expand = False, side = TOP)
            
def saved():
    global frame
    global homeframe
    global savedframe

    root.title('Saved Recordings...')

    try:
        frame.destroy()
        homeframe.destroy()

    except NameError:
        pass

    savedframe = Frame(root)
    savedframe.pack(side = "top", expand = True, fill = 'both')

    check = 'Home from saved()'
    
    b1 = Button(savedframe, text = "Home", command = lambda m = check: homepage(m))
    b1.pack(ipadx= 10, ipady = 10, fill = X, expand = False, side = TOP)

    incase = Label(savedframe, text = 'If this appears empty either you have no saved recordings.\nIf you do relaunch the application...', font = ("Arial", 14))
    incase.pack()

    dirs = os.listdir("Saved Recordings")

    for files in dirs:
        name = files
        button = Button(savedframe, text = name, command = lambda m = name: Custommove.findfile(m))
        button.pack(ipadx = 20, ipady = 20, fill = X, expand = False, side = BOTTOM)

def homepage(button_press):
    global homeframe
    global playframe
    global savedframe
    global saveframe

    root.title('Home')

    homeframe = Frame(root)
    homeframe.pack(side="top", expand=True, fill="both")

    if button_press == 'Home from saved()':
        savedframe.destroy()

    if button_press == 'Home from save()':
        saveframe.destroy()
        
    l1 = Label(homeframe, text="Press the button to record and press the esc button when you are done recording.\nTo exit the bot while it is running just right click when it tells you to.", font = ("Arial", 14))
        
    b1 = Button(homeframe, text = "Record", command = Custommove.record)
    b2 = Button(homeframe, text = "Saved", command = saved)

    b1.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)
    b2.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)

    l1.pack()
    
if not os.path.exists("Saved Recordings"):
    path = Path.cwd() / "Saved Recordings"
    path.mkdir()
    
root = tk.Tk()
root.geometry('800x400')
root.resizable(True,  True)
root.title('Home')

frame = Frame(root)
frame.pack(side = "top", expand = True, fill = "both")

l1 = Label(frame, text="Press the button to record and press the esc button when you are done recording.\nTo exit the bot while it is running just right click when it tells you to.", font = ("Arial", 14))

b1 = Button(frame, text = "Record", command = Custommove.record)
b2 = Button(frame, text = "Saved", command = saved)

b1.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)
b2.pack(ipadx = 10, ipady = 15, fill=X, expand=False, side=BOTTOM)

l1.pack()

root.mainloop()
