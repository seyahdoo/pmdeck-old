

from action import Action
import subprocess


class MicAction(Action):

    def __init__(self, deck):
        super().__init__(deck)

        self.enabled = True
        self.image_path = "Assets/Keys/mic-on.png"

        return

    def on_pressed(self):
        super(MicAction, self).on_pressed()

        self.enabled = not self.enabled

        if self.enabled:
            self.set_image_path("Assets/Keys/mic-on.png")
            subprocess.call(["C:/Program Files/AutoHotkey/AutoHotkey.exe", "C:/AHK/Functions/unmute_mic.ahk"])
        else:
            self.set_image_path("Assets/Keys/mic-off.png")
            subprocess.call(["C:\\Program Files\\AutoHotkey\\AutoHotkey.exe", "C:\\AHK\\Functions\\mute_mic.ahk"])
        return

