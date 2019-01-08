

class Action:

    def __init__(self,deck):
        self.image_path = "Assets/empty.png"
        self.is_visible = False
        self.current_space = 0
        self.is_pressed = False
        self.deck = deck
        self.initialize()
        return

    def _set_visible(self, space):
        self.is_visible = True
        self.current_space = space
        self.on_visible()
        self._draw()
        return

    def _set_invisible(self):
        self.is_visible = False
        self.on_invisible()
        return

    def set_image_path(self, image_path):
        self.image_path = image_path
        self._draw()
        return

    def _draw(self):
        if self.is_visible:
            self.deck.set_key_image_path(self.current_space, self.image_path)
        return

    def _pressed(self):
        self.is_pressed = True
        self.on_pressed()
        return

    def _released(self):
        self.is_pressed = False
        self.on_released()
        return


    def initialize(self):
        return

    def on_visible(self):
        return

    def on_invisible(self):
        return

    def on_pressed(self):
        return

    def on_hold_down(self):
        return

    def on_released(self):
        return

    def on_update_sec(self):
        return

    def on_update(self):
        return

    def on_exit(self):
        return



    

    