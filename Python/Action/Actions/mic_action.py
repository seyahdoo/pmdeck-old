from Action.action import Action
import subprocess


class MicAction(Action):

    def initialize(self):
        self.enabled = True
        self.set_image_path("Assets/Keys/mic-on.png")
        return

    def on_pressed(self):
        self.enabled = not self.enabled

        if self.enabled:
            self.set_image_path("Assets/Keys/mic-on.png")
            subprocess.call(["C:/Program Files/AutoHotkey/AutoHotkey.exe", "C:/AHK/Functions/unmute_mic.ahk"])
        else:
            self.set_image_path("Assets/Keys/mic-off.png")
            subprocess.call(["C:\\Program Files\\AutoHotkey\\AutoHotkey.exe", "C:\\AHK\\Functions\\mute_mic.ahk"])
        return

