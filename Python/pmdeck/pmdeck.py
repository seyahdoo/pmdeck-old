
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



        # name = "_pmdeck._tcp."
        # regtype = "_pmdeck._tcp."
        #
        # def register_callback(sdRef, flags, errorCode, name, regtype, domain):
        #     if errorCode == pybonjour.kDNSServiceErr_NoError:
        #         print('Registered service:')
        #         print('  name    = '+ name)
        #         print('  regtype = '+ regtype)
        #         print('  domain  = '+ domain)
        #         print("Local mDNS is started, domain is " + local_ip)
        #
        # sdRef = pybonjour.DNSServiceRegister(name=name,
        #                                      regtype=regtype,
        #                                      port=port,
        #                                      callBack=register_callback,
        #                                      host=local_ip,
        #                                      domain=regtype)
        #
        # def register_listener():
        #     try:
        #         try:
        #             while True:
        #                 ready = select.select([sdRef], [], [])
        #                 if sdRef in ready[0]:
        #                     pybonjour.DNSServiceProcessResult(sdRef)
        #         except KeyboardInterrupt:
        #             pass
        #     finally:
        #         sdRef.close()
        #
        # threading.Thread(target=register_listener).start()

        while True:
            client_sock, address = server_socket.accept()
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
        encoded = (str(key) + ";").encode('utf-8') + base64_string + "\n".encode('utf-8')
        self.client_sock.send(encoded)
        return

    def set_key_callback(self, callback):
        self.key_callback = callback;
        return

    def on_key_status_change(self, key, status):
        if self.key_callback:
            self.key_callback(self, key, status)
        return

