from pmdeck import pmdeck
from threading import Event

from folder import Folder
from action import Action
from mic_action import MicAction

current_folder = None

def key_callback(deck, key, status):

    global current_folder

    if status == "0":
        # deck.set_key_image_path(key,"Assets/pressed-min.png")
        current_folder.button_pressed(key)
    else:
        #deck.set_key_image_path(key,"Assets/released-min.png")
        current_folder.button_released(key)
    return


def on_connected_callback(deck):
    deck.set_key_callback(key_callback)

    root_folder = Folder(deck)

    global current_folder
    current_folder = root_folder

    root_folder.set_action(0, MicAction(deck))
    root_folder.open()

    return


if __name__ == "__main__":

    manager = pmdeck.DeviceManager()

    manager.set_on_connected_callback(on_connected_callback)


    Event().wait()