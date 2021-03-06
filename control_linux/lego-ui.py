import tkinter as tk
from gattlib import DiscoveryService
from gattlib import GATTRequester
from time import sleep

DELAY = 30

def run():
    global button_run
    button_run.after(DELAY, motor_run)

def stop():
    global button_stop
    button_stop.after(DELAY, motor_stop)

def connect():
    global button_disconnect
    button_disconnect.after(DELAY, smart_hub_connect)

def disconnect():
    global button_disconnect
    button_disconnect.after(DELAY, smart_hub_disconnect)

def up():
    global button_up
    button_up.after(DELAY, motor_up)

def down():
    global button_down
    button_down.after(DELAY, motor_down)

def motor_run():
    global req
    if req != None:
        req.write_by_handle(0x3d, str(bytearray([0x01, 0x01, 0x01, 0x64])))

def smart_hub_connect():
    service = DiscoveryService("hci0")
    devices = service.discover(2)

    for address, name in devices.items():
        if name != '' and '9' in name:
            label['text'] = address

            global button_run, button_stop, button_disconnect, req
            button_connect['state'] = 'disabled'
            button_run['state'] = 'normal'
            button_stop['state'] = 'normal'
            button_disconnect['state'] = 'normal'
            button_up['state'] = 'normal'
            button_down['state'] = 'normal'

            req = GATTRequester(address, True, "hci0")
            break

MAX_SPEED = 100
MIN_SPEED = 1
SPEED_CHANGE = 4

current_speed = 100
req = None

def motor_up():
    global req, current_speed
    if req != None:
        if current_speed == MAX_SPEED:
            return

        current_speed += SPEED_CHANGE
        req.write_by_handle(HANDLE, str(bytearray([0x01, 0x01, 0x01, current_speed])))
        sleep(WEDO_DELAY)

def motor_down():
    global req, current_speed
    if req != None:
        if current_speed == MIN_SPEED:
            return

        current_speed -= SPEED_CHANGE
        req.write_by_handle(HANDLE, str(bytearray([0x01, 0x01, 0x01, current_speed])))
        sleep(WEDO_DELAY)



BUTTON_WIDTH = 30

root = tk.Tk()
root.title("Lego Wedo 2.0 Motor Control")

label = tk.Label(root, fg="dark green", text='N/A')
label.pack()

button_connect = tk.Button(root, text='Connect Smart Hub', width=BUTTON_WIDTH, command=connect)
button_connect.pack()

button_disconnect = tk.Button(root, text='Disconnect Smart Hub', width=BUTTON_WIDTH, command=disconnect, state='disabled')
button_disconnect.pack()

button_run = tk.Button(root, text='Run motor', width=BUTTON_WIDTH, command=run, state='disabled')
button_run.pack()

button_up = tk.Button(root, text='Speed up', width=BUTTON_WIDTH, command=up, state='disabled')
button_up.pack()

button_down = tk.Button(root, text='Speed down', width=BUTTON_WIDTH, command=down, state='disabled')
button_down.pack()

button_stop = tk.Button(root, text='Stop motor', width=BUTTON_WIDTH, command=stop, state='disabled')
button_stop.pack()

root.mainloop()
