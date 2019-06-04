import tkinter
import pynput
import os
import logging
from time import time
from time import sleep
from pynput.keyboard import Key
from pynput.keyboard import KeyCode

# ======== GLOBAL VARS ======
text_stopKeyPlay = "esc"
text_stopKeyRec = "esc"
mouse_recording = False
keyboard_recording = False
stopped_playing = False
# ========= END GLOBAL VARS ====
# ======================= COMMANDS ==========================

def KeyNameforUser(key):
    # key is something like "f" or Key.space
    key=str(key)
    if len(key)==3:
        return key[1]
    if key[0]=="K" and key[1]=="e" and key[2]=="y" and key[3]==".":
        new_key = ""
        for i in range(4, len(key)):
            new_key += key[i]
        return new_key
    print("SOMETHING IS WRONG WRONG WRONG WRONG WRONG")
def keyNameforMachine(key):
    if len(key) == 1:
        return KeyCode.from_char(key)
    if len(key) > 1:
        return eval("Key." + key)
def on_releaseStopkeyPlay(key):
    key = KeyNameforUser(key)
    button01_2.config(text=key, command=StopKeyPlay)
    normalizeAllObjects()
    return False
def on_releaseStopkeyRec(key):
    key = KeyNameforUser(key)
    button11_2.config(text=key, command=StopKeyRecord)
    normalizeAllObjects()
    return False
def disableObject(object):
    object.config(state=tkinter.DISABLED)
def disableObjectsExcept(object):
    buttons=[button01_1, button01_2, button10_2, button11_1, button11_2, optionMenu00_1, entry00_2, entry10_1]
    for button in buttons:
        if not button == object:
            disableObject(button)
def disableAllObjects():
    buttons = [button01_1, button01_2, button10_2, button11_1, button11_2, optionMenu00_1, entry00_2, entry10_1]
    for button in buttons:
        disableObject(button)
def normalizeObject(object):
    object.config(state=tkinter.NORMAL)
def normalizeObjectsExcept(object):
    buttons=[button01_1, button01_2, button10_2, button11_1, button11_2, optionMenu00_1, entry00_2, entry10_1]
    for button in buttons:
        if not button == object:
            normalizeObject(button)
def normalizeAllObjects():
    buttons = [button01_1, button01_2, button10_2, button11_1, button11_2, optionMenu00_1, entry00_2, entry10_1]
    for button in buttons:
        normalizeObject(button)
def StopKeyPlay():
    global text_stopKeyPlay
    text_stopKeyPlay = button01_2.cget('text')
    disableObjectsExcept(button01_2)
    button01_2.config(text='[    ]')
    keyboard_listener1 = pynput.keyboard.Listener(on_release=on_releaseStopkeyPlay)
    button01_2.config(command=None)
    keyboard_listener1.start()
    pass
def StopKeyRecord():
    global text_stopKeyRec
    text_stopKeyRec = button11_2.cget('text')
    disableObjectsExcept(button11_2)
    button11_2.config(text='[    ]')
    keyboard_listener2 = pynput.keyboard.Listener(on_release=on_releaseStopkeyRec)
    button11_2.config(command=None)
    keyboard_listener2.start()
    pass
def getsavesList():
    os.chdir(os.getcwd() + "/saves")
    list = os.listdir(os.getcwd())
    savelist = []
    for file in list:
        l = len(file)
        if file[l - 4] == '.' and file[l - 3] == 't' and file[l - 2] == 'x' and file[l - 1] == 't':
            savelist.append(file)
    os.chdir('..')
    return savelist
def on_press_play(key):
    global stopped_playing
    if key == keyNameforMachine(button01_2):
        stopped_playing == True
        return False
def Play():
    global stopped_playing
    amount = int(entry00_2.get())
    if amount == 0:
        amount = 2147483648
    keyboard_listener_play = pynput.keyboard.Listener(on_press = on_press_play)
    stopped_playing = False
    for i in range(amount):
        file = open("saves/"+SelectedSave.get(), "r")
        mouse_controller=pynput.mouse.Controller()
        keyboard_controller=pynput.keyboard.Controller()
        last_time = -1
        shift_pressed =False
        for line in file:
            line_list=line.split(" ")
            line_list.remove(line_list[len(line_list)-1])
            if last_time==-1:
                last_time=float(line_list[1])
            else:
                now_time=float(line_list[1])
                sleep((now_time-last_time))
                last_time=now_time
                task=line_list[0]
                if task=='move':
                    mouse_controller.position=(line_list[2],line_list[3])
                elif task=='scroll':
                    mouse_controller.scroll(line_list[2],line_list[3])
                elif task=='click':
                    if line_list[2]=='pressed':
                        mouse_controller.position = (line_list[4], line_list[5])
                        if line_list[3]=='Button.left':
                            mouse_controller.press(pynput.mouse.Button.left)
                        elif line_list[3]=='Button.middle':
                            mouse_controller.press(pynput.mouse.Button.middle)
                        elif line_list[3]=='Button.right':
                            mouse_controller.press(pynput.mouse.Button.right)
                        else:
                            print("Error 404")
                    elif line_list[2]=='released':
                        mouse_controller.position = (line_list[4], line_list[5])
                        if line_list[3]=='Button.left':
                            mouse_controller.release(pynput.mouse.Button.left)
                        elif line_list[3]=='Button.middle':
                            mouse_controller.release(pynput.mouse.Button.middle)
                        elif line_list[3]=='Button.right':
                            mouse_controller.release(pynput.mouse.Button.right)
                        else:
                            print("Error 405")
                    else:
                        print("There is a fucking mistake in choice")
                elif task=='press':
                    if len(line_list[2])==3:
                        drucke=line_list[2][1]
                        if shift_pressed:
                            with keyboard_controller.pressed(Key.shift):
                                keyboard_controller.press(drucke)
                        else:
                            keyboard_controller.press(drucke)
                    elif line_list[2]=="Key.shift_r" or line_list[2]=="Key.shift_l" or line_list[2]=="Key.shift":
                        shift_pressed=True
                    else:
                        drucke=line_list[2]
                        if drucke[0]=='K' and drucke[1]=='e' and drucke[2]=='y' and drucke[3]=='.':
                            drucke=eval(drucke)
                        if shift_pressed:
                            with keyboard_controller.pressed(Key.shift):
                                keyboard_controller.press(drucke)
                        else:
                            keyboard_controller.press(drucke)

                elif task=='release':
                    if len(line_list[2])==3:
                        drucke=line_list[2][1]
                        if shift_pressed:
                            with keyboard_controller.pressed(Key.shift):
                                keyboard_controller.release(drucke)
                        else:
                            keyboard_controller.release(drucke)
                    elif line_list[2]=="Key.shift_r" or line_list[2]=="Key.shift_l" or line_list[2]=="Key.shift":
                        shift_pressed=False
                    else:
                        drucke=line_list[2]
                        if drucke[0]=='K' and drucke[1]=='e' and drucke[2]=='y' and drucke[3]=='.':
                            drucke=eval(drucke)
                        if shift_pressed:
                            with keyboard_controller.pressed(Key.shift):
                                keyboard_controller.release(drucke)
                        else:
                            keyboard_controller.release(drucke)
        if stopped_playing:
            break


def Createfile(filename):
    path = os.getcwd() + "/saves"
    os.chdir(path)

    file = open(filename + ".txt", "w+")
    file.close()
    os.chdir('..')
def updateOptionMenu():
    saves = getsavesList()
    menu = optionMenu00_1['menu']
    menu.delete(0, 'end')
    for save in saves:
        menu.add_command(label = save,
                         command = lambda value = save:
                         SelectedSave.set(value)
                         )
def on_move(x, y):
    global mouse_recording
    if not keyboard_recording:
        mouse_recording = False
        StopRecord()
        return False

    logging.info('move {0} {1} {2} end'.format(time(), x, y))

def on_click(x, y, button, pressed):
    global mouse_recording
    if not keyboard_recording:
        mouse_recording = False
        StopRecord()
        return False
    logging.info('click {0} {1} {2} {3} {4} end'.format(
        time(),
        'pressed' if pressed else 'released',
        button,
        x,
        y))
def on_scroll(x, y, dx, dy):
    global mouse_recording
    if not keyboard_recording:
        mouse_recording = False
        StopRecord()
        return False
    logging.info('scroll {0} {1} {2} end'.format(
        time(),
        dx,
        dy))

def on_press(key):
    global keyboard_recording
    if not mouse_recording:
        keyboard_recording = False
        StopRecord()
        return False

    print(key, button11_2.cget('text'), keyNameforMachine(button11_2.cget('text')))
    logging.info('press {0} {1} end'.format(time(), key))
    if key == keyNameforMachine(button11_2.cget('text')):
        button11_1.config(command=Record)
        keyboard_recording = False
        return False


def on_release(key):
    global keyboard_recording
    if not mouse_recording:
        StopRecord()
        return False
    logging.info('release {0} {1} end'.format(time(), key))
def start_record(file):
    global mouse_recording
    global keyboard_recording
    logging.basicConfig(filename="saves/"+file+".txt", level=logging.DEBUG, format="%(message)s")
    mouse_listener_record = pynput.mouse.Listener(on_move=on_move,
                                                  on_click=on_click,
                                                  on_scroll=on_scroll)
    keyboard_listener_record = pynput.keyboard.Listener(on_press=on_press,
                                                        on_release=on_release)
    mouse_recording = True
    keyboard_recording = True
    mouse_listener_record.start()
    keyboard_listener_record.start()
def Record():
    filename = entry10_1.get()
    Createfile(filename)
    disableObjectsExcept(button11_1)
    start_record(filename)




    button11_1.configure(image=stopRecordImg, command=StopRecord)
    pass
def StopRecord():
    global keyboard_recording
    global mouse_recording
    if keyboard_recording:
        pynput.keyboard.Listener.stop
        keyboard_recording = False
    if mouse_recording:
        pynput.mouse.Listener.stop
        mouse_recording = False
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    normalizeAllObjects()
    updateOptionMenu()
    button11_1.config(image=recordImg, command=Record)
def Credits():
    credit_window = tkinter.Toplevel(root)
    name = tkinter.Label(credit_window, text="Mateusz Pełechaty")
    email = tkinter.Label(credit_window, text="sshozye@gmail.com")
    name.pack()
    email.pack()
    pass

root = tkinter.Tk()


root.resizable(False,False)
root.iconbitmap('photos\icon.ico')
root.title('Repeater')
saveList = getsavesList()
# ========================= Creating WIDGETS ======================

clickImg = tkinter.PhotoImage(file="photos/click.png")
playImg = tkinter.PhotoImage(file="photos/playimg.png")
recordImg = tkinter.PhotoImage(file="photos/record.png")
endlessImg = tkinter.PhotoImage(file="photos/infinite-symbol.png")
stopRecordImg = tkinter.PhotoImage(file="photos/stoprecord.png")
# main-one-frame is frame[row][col]
# widget[row][col]_[how-many-in-main-one-frame]

frame00 = tkinter.Frame(root)
label00_1 = tkinter.Label(frame00, text="File to repeat:")
frame00_1 = tkinter.Frame(frame00)
SelectedSave = tkinter.StringVar(root)
SelectedSave.set(saveList[0])
optionMenu00_1 = tkinter.OptionMenu(frame00_1, SelectedSave, *saveList)
frame00_2 = tkinter.Frame(frame00)
label00_2 = tkinter.Label(frame00_2, text="Play")
entry00_2 = tkinter.Entry(frame00_2, width=5)
label00_3 = tkinter.Label(frame00_2, text="times")
frame00_3= tkinter.Frame(frame00)
label00_4 = tkinter.Label(frame00_3, text="0 for")
label00_5 = tkinter.Label(frame00_3, image=endlessImg)


frame01 = tkinter.Frame(root)
button01_1 = tkinter.Button(frame01, image=playImg, command=Play)
frame01_1 = tkinter.Frame(frame01)
label01_1 = tkinter.Label(frame01_1, text="To stop:")
button01_2 = tkinter.Button(frame01_1, text="esc", command=StopKeyPlay)


frame10 = tkinter.Frame(root)
label10_1 = tkinter.Label(frame10, text="Type a filename to record")
frame10_1 = tkinter.Frame(frame10)
entry10_1 = tkinter.Entry(frame10_1, width=22)

label10_2 = tkinter.Label(frame10, text="")
button10_2 = tkinter.Button(frame10, text="Credits", command=Credits)

frame11 = tkinter.Frame(root)
button11_1 = tkinter.Button(frame11, image=recordImg, command=Record)
frame11_1 = tkinter.Frame(frame11)
label11_1 = tkinter.Label(frame11_1, text="To stop:")
button11_2 = tkinter.Button(frame11_1, text="esc", command=StopKeyRecord)

# ========================== END Creating WIDGETS =======================
# ========================== Positioning Widgets ========================

frame00.grid(row=0, column=0)
label00_1.pack(anchor=tkinter.NW)
frame00_1.pack(anchor=tkinter.NW)
optionMenu00_1.pack(side=tkinter.LEFT)
frame00_2.pack()
label00_2.pack(side=tkinter.LEFT)
entry00_2.pack(side=tkinter.LEFT)
label00_3.pack(side=tkinter.LEFT)
frame00_3.pack()
label00_4.pack(side=tkinter.LEFT)
label00_5.pack(side=tkinter.LEFT)

frame01.grid(row=0, column=1)
button01_1.pack()
frame01_1.pack()
label01_1.pack(side=tkinter.LEFT)
button01_2.pack(side=tkinter.LEFT)

frame10.grid(row=1, column=0)
label10_1.pack(anchor=tkinter.NW)
frame10_1.pack(anchor=tkinter.NW)
entry10_1.pack(side=tkinter.LEFT)
label10_2.pack(anchor=tkinter.NW)
button10_2.pack(anchor=tkinter.SE)

frame11.grid(row=1, column=1)
button11_1.pack()
frame11_1.pack()
label11_1.pack(side=tkinter.LEFT)
button11_2.pack(side=tkinter.LEFT)

# ======================== END POSITIONING WIDGETS ===========================
root.mainloop()