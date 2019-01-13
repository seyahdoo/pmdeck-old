
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
        self.zconf = zeroconf.Zeroconf()
        self.Decks = {}
        # {
            # "ANDROID1":{
            #     "pass": "123456",
            #     "connected": "false"
            # }
        # }

        return

    def connector_listener(self):
        bind_ip = '0.0.0.0'
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((bind_ip, 0))
        self.server_socket.listen(5)  # max backlog of connections
        local_ip = ""
        port = self.server_socket.getsockname()[1]
        try:
            local_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
        except:
            print("exception on getting local ip")

        print('Listening on {}:{}'.format(local_ip, port))

        self.register_service(local_ip,port)

        while True:
            try:
                client_socket, address = self.server_socket.accept()
                print('Accepted connection from {}:{}'.format(address[0], address[1]))
                deck = Deck(client_socket, self)
                #self.on_connected(deck)
                deck._read()
            except Exception as e:
                print(e)
                return
        return

    def listen_connections(self):
        self.connector_thread:threading.Thread = threading.Thread(
            target=self.connector_listener
        ).start()

        return

    def stop_listening_connections(self):
        self.server_socket.close()
        return

    def register_service(self,local_ip,port):
        print("Registering Service")
        service_name = local_ip + ":" + str(port) + "._pmdeck._tcp.local."

        desc = {}
        info = zeroconf.ServiceInfo("_pmdeck._tcp.local.",
                                    service_name,
                                    socket.inet_aton(local_ip), port, 0, 0,
                                    desc, local_ip + ".")

        self.zconf.register_service(info)
        return

    def unregister_service(self):
        self.zconf.unregister_all_services()
        return

    def sync_new_device(self):
        return

    def stop_syncing(self):
        return

    def set_on_connected_callback(self, callback):
        self.connected_callback = callback
        return

    def on_connected(self, deck):
        # deck.reset()
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

    def __init__(self, client_socket: socket.socket, deviceManager:DeviceManager):

        self.id = None
        self.key_callback = None
        self.client_socket: socket.socket = client_socket;
        self.disconnected = False
        self.deviceManager = deviceManager
        return

    def __del__(self):
        return

    def _read(self):

        self.client_socket.settimeout(10)

        def listener():
            stream = ""
            while True:
                try:
                    data = self.client_socket.recv(1024)
                    stream = data.decode('utf-8')
                    print(stream)
                    for msg in list(filter(None, stream.split(';'))):
                        spl = msg.split(":")
                        cmd = spl[0]
                        if(cmd == "PONG"):
                            pass

                        elif(cmd == "BTNEVENT"):
                            args = spl[1].split(",")
                            self.on_key_status_change(args[0], args[1])

                        elif(cmd == "CONN"):
                            args = spl[1].split(",")
                            self.id = args[0]
                            password = self.deviceManager.Decks[self.id]["pass"]
                            self.client_socket.send("CONN:{};".format(password).encode("utf-8"))

                        elif(cmd == "CONNACCEPT"):
                            self.reset()
                            self.deviceManager.on_connected(self)

                        elif(cmd == "SYNCREQ"):
                            args = spl[1].split(",")
                            self.id = args[0]
                            self.client_socket.send("SYNCTRY:{};".format("123456").encode("utf-8"))

                        elif(cmd == "SYNCACCEPT"):
                            args = spl[1].split(",")
                            # self.deviceManager.Decks[self.id]["pass"] = args[0]
                            # self.deviceManager.Decks[self.id]["synced"] = True
                            self.client_socket.send("CONN:{};".format(args[0]).encode("utf-8"))
                            if self.id in self.deviceManager.Decks:
                                self.deviceManager.Decks[self.id]["pass"] = "123456"
                            else:
                                self.deviceManager.Decks[self.id] = {"connected":True, "pass":"123456"}


                except Exception as e:
                    print(e)
                    self.disconnect()
                    return

        threading.Thread(target=listener).start()

        def pinger():
            while True:
                try:
                    self.client_socket.send("PING;\n".encode('utf-8'))
                    time.sleep(3)
                except Exception as e:
                    print(e)
                    self.disconnect()
                    return

        threading.Thread(target=pinger).start()

        return

    def disconnect(self):
        if self.disconnected:
            return

        print("Deck Disconnected")
        # TODO

        self.disconnected = True
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
        encoded = ("IMAGE:" + str(key) + ",").encode('utf-8') + base64_string + ";\n".encode('utf-8')
        self.client_socket.send(encoded)
        return

    def set_key_callback(self, callback):
        self.key_callback = callback;
        return

    def on_key_status_change(self, key, status):
        if self.key_callback:
            self.key_callback(self, key, status)
        return


