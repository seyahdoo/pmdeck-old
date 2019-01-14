from pmdeck import pmdeck
from threading import Event

from Action.folder import Folder
from Action.Actions.mic_action import MicAction
from Action.Actions.test_action import TestAction

import atexit
import threading
import time
import sys
import os

import pystray
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import time

def key_callback(deck, key, status):

    if status == "0":
        # deck.set_key_image_path(key,"Assets/pressed-min.png")
        deck.current_folder.button_pressed(key)
    else:
        #deck.set_key_image_path(key,"Assets/released-min.png")
        deck.current_folder.button_released(key)
    return


def on_connected_callback(deck):
    deck.set_key_callback(key_callback)

    root_folder = Folder(deck)
    root_folder.set_action(12, MicAction(deck))
    # for i in range(1,15,2):
    #     root_folder.set_action(i, TestAction(deck))
    root_folder.open()

    return

# Decorators


def callback(icon):
    image = Image.new('RGBA', (128,128), (255,255,255,255)) # create new image
    percent = 100
    while True:
        img = image.copy()
        d = ImageDraw.Draw(img)
        d.rectangle([0, 128, 128, 128-(percent * 128) / 100], fill='blue')
        icon.icon = img
        time.sleep(1)
        percent -= 5
        if percent < 0:
            percent = 100

if __name__ == "__main__":

    manager = pmdeck.DeviceManager()

    manager.set_on_connected_callback(on_connected_callback)

    manager.listen_connections()

    state = False


    def on_clicked(icon, item):
        global state
        print("Blah")
        state = not state


    # Update the state in `on_clicked` and return the new state in
    # a `checked` callable
    Icon('test', Image.new('RGBA', (128,128), (255,255,255,255)), menu=Menu(
        MenuItem(
            'Sync New',
            on_clicked),
        MenuItem(
            'Restart',
            on_clicked,
            default=True),
        MenuItem(
            'Quit',
            on_clicked,
            checked=lambda item: state) )
        ).run()


