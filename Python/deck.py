
class DeviceManager:

    decks = []

    def find_all(self):
        return

    def on_connected(self, deck):
        return

    def on_disconnected(self, deck):
        return



class Deck:

    KEY_COUNT = 15
    KEY_COLS = 5
    KEY_ROWS = 3

    KEY_PIXEL_WIDTH = 72
    KEY_PIXEL_HEIGHT = 72
    KEY_PIXEL_DEPTH = 3
    KEY_PIXEL_ORDER = "BGR"

    KEY_IMAGE_SIZE = KEY_PIXEL_WIDTH * KEY_PIXEL_HEIGHT * KEY_PIXEL_DEPTH

    def __init__(self):

        return

    def __del__(self):

        return

    def _read(self):

        return

    def set_key_image_path(self, key, image_path):

        return

    def set_key_image(self, key, image_buffer):

        return

    def set_key_callback(self, callback):

        return


