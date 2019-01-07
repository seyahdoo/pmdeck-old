
import socket
import threading
import base64


class DeviceManager:

    def __init__(self):

        self.connected_callback = None
        self.disconnected_callback = None



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

        deck = Deck(client_socket)
        self.on_connected(deck)
        stream = ""

        while True:
            try:
                data = client_socket.recv(1024)
                stream = data.decode('utf-8')
                print(stream)
                for cmd in list(filter(None, stream.split(';'))):
                    spl = cmd.split(',')
                    deck.on_key_status_change(spl[0], spl[1])

            except Exception as e:
                print(e)
                self.on_disconnected(deck)
                return

        return

    def set_on_connected_callback(self, callback):
        self.connected_callback = callback
        return

    def on_connected(self, deck):
        deck.reset()
        if self.connected_callback:
            self.connected_callback(deck)
        return

    def set_on_disconnected_callback(self, callback):
        self.disconnected_callback = callback
        return

    def on_disconnected(self, deck):
        if self.disconnected_callback:
            self.disconnected_callback(deck)
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

    def __init__(self, client_sock: socket.socket):

        self.key_callback = None
        self.client_sock: socket.socket = client_sock;

        return

    def __del__(self):
        return

    def _read(self):

        return

    def reset(self):
        for i in range(0, 15):
            self.set_key_image_path(str(i), "Assets/empty.png")
        return

    def set_key_image_path(self, key, image_path: str):
        if image_path.endswith(".png"):
            encoded = base64.b64encode(open(image_path, "rb").read())
            self.set_key_image_base64(key,encoded)
        else:
            print("please give a png file")
        return

    def set_key_image_base64(self, key, base64_string):
        encoded = (key + ";").encode('utf-8') + base64_string + "\n".encode('utf-8')
        self.client_sock.send(encoded)
        return

    def set_key_callback(self, callback):
        self.key_callback = callback;
        return

    def on_key_status_change(self, key, status):
        print("Key Status {}, {}".format(key, status));
        if self.key_callback:
            self.key_callback(self, key, status)
        return

