
import socket
import threading


class DeviceManager:

    def __init__(self):

        self.connected_callback = None

        threading.Thread(
            target=self.connector_listener
        ).start()

        return

    def connector_listener(self):
        bind_ip = '0.0.0.0'
        bind_port = 23997

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((bind_ip, bind_port))
        server.listen(5)  # max backlog of connections
        print('Listening on {}:{}'.format(bind_ip, bind_port))

        while True:
            client_sock, address = server.accept()
            print('Accepted connection from {}:{}'.format(address[0], address[1]))
            client_handler = threading.Thread(
                target=self.deck_listener,
                args=(client_sock,)
                # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
            )
            client_handler.start()

        return

    def deck_listener(self, client_socket):

        deck = Deck()
        self.on_connected(deck)

        while True:
            try:
                data = client_socket.recv(1024)
                msg = data.decode('utf-8')
                cmd = msg.split(';')
                deck.on_key_status_change(cmd[0], cmd[1])
            except Exception as e:
                print(e)
                self.on_disconnected(deck)
                return

        return

    def set_on_connected_callback(self, callback):
        self.connected_callback = callback
        return

    def on_connected(self, deck):
        print("Connected")
        self.connected_callback()
        return



    def on_disconnected(self, deck):
        print("Disconnected")
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

    def __init__(self, socket):

        self.socket = socket;

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

    def on_key_status_change(self, key, status):
        print("Key Status {}, {}".format(key, status));
        return

