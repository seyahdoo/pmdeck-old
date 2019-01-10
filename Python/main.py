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


if __name__ == "__main__":

    manager = pmdeck.DeviceManager()

    manager.set_on_connected_callback(on_connected_callback)

    Event().wait()


