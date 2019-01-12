
import socket
import threading
import base64
import zeroconf
# from pmdeck import pybonjour
import atexit
import sys
import time

class DeviceManager:

    def __init__(self):
        self.connected_callback = None
        self.disconnected_callback = None
        return

    def start(self):
        threading.Thread(
            target=self.connector_listener
        ).start()
        return

    def connector_listener(self):
        bind_ip = '0.0.0.0'
        # bind_port = 23997

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((bind_ip, 0))
        server_socket.listen(5)  # max backlog of connections
        local_ip = ""
        port = server_socket.getsockname()[1]
        try:
            local_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
        except:
            print("expttt")

        print('Listening on {}:{}'.format(local_ip, port))

        desc = {}
        info = zeroconf.ServiceInfo("_pmdeck._tcp.local.",
                            "PMDeck._pmdeck._tcp.local.",
                                    socket.inet_aton(local_ip), port, 0, 0,
                                    desc, local_ip +".")

        z = zeroconf.Zeroconf()
        z.register_service(info)

        @atexit.register
        def _unregister():
            print("unregistering")
            z.unregister_all_services()

        print("registered")

        while True:
            client_socket, address = server_socket.accept()
            print('Accepted connection from {}:{}'.format(address[0], address[1]))
            deck = Deck(client_socket)
            self.on_connected(deck)
            deck._read()

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

    def __init__(self, client_socket: socket.socket):

        self.id = None
        self.key_callback = None
        self.client_socket: socket.socket = client_socket;

        return

    def __del__(self):
        return

    def _read(self):

        def listener():
            stream = ""
            while True:
                try:
                    data = self.client_socket.recv(1024)
                    stream = data.decode('utf-8')
                    for cmd in list(filter(None, stream.split(';'))):
                        spl = cmd.split(',')
                        self.on_key_status_change(spl[0], spl[1])

                except Exception as e:
                    print(e)
                    self.disconnect()
                    return

        threading.Thread(target=listener).start()
        return

    def disconnect(self):
        print("Deck Disconnected")
        # TODO
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
        encoded = (str(key) + ";").encode('utf-8') + base64_string + "\n".encode('utf-8')
        self.client_socket.send(encoded)
        return

    def set_key_callback(self, callback):
        self.key_callback = callback;
        return

    def on_key_status_change(self, key, status):
        if self.key_callback:
            self.key_callback(self, key, status)
        return


