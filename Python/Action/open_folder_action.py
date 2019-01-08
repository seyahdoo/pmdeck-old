
from Action.action import Action
from Action.folder import Folder


class OpenFolderAction(Action):

    def __init__(self, folder):
        super().__init__()
        self.folder: Folder = folder

        return

    def on_pressed(self):
        self.folder.open()

        return


