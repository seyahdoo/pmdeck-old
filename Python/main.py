
import pmdeck
from threading import Event


def key_callback(deck, key, status):

    if status == "0":
        deck.set_key_image_path(key,"Assets/pressed-min.png")
    else:
        deck.set_key_image_path(key,"Assets/released-min.png")

    return


def on_connected_callback(deck):
    deck.set_key_callback(key_callback)
    return


if __name__ == "__main__":

    manager = pmdeck.DeviceManager()

    manager.set_on_connected_callback(on_connected_callback)


    Event().wait()