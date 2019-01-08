from Action.action import Action
import subprocess

class TestAction(Action):

    def initialize(self):
        self.set_image_path("Assets/Keys/test-key.png")
        return

    def on_pressed(self):
        subprocess.call(["C:/Program Files/AutoHotkey/AutoHotkey.exe", "C:/AHK/Functions/test.ahk"])
        return

