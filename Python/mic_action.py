

from action import Action


class MicAction(Action):

    def __init__(self, deck):
        super().__init__(deck)

        self.enabled = True
        self.image_path = "Assets/pressed-min.png"

        return

    def on_pressed(self):
        super(MicAction, self).on_pressed()

        print("pressed....")

        self.enabled = not self.enabled

        if self.enabled:
            self.set_image_path("Assets/pressed-min.png")
        else:
            self.set_image_path("Assets/released-min.png")

        return

