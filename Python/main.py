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

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize


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


def show_tray():

    def pri():
        print("hola")

    trayIconMenu = QMenu()
    trayIconMenu.addAction(pri)
    trayIconMenu.addAction(pri)
    trayIconMenu.addAction(pri)
    trayIconMenu.addSeparator()
    trayIconMenu.addAction(pri)

    trayIcon = QSystemTrayIcon()
    trayIcon.show()


if __name__ == "__main__":

    manager = pmdeck.DeviceManager()

    manager.set_on_connected_callback(on_connected_callback)

    manager.listen_connections()

    app = QApplication(sys.argv)
    show_tray()
    sys.exit(app.exec())



