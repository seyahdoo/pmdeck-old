

class Action:

    def __init__(self,deck):

        self.image_path = "Assets/pressed-min.png"
        self.is_visible = False
        self.current_space = 0
        self.is_pressed = False
        self.deck = deck
        
        return

    def set_visible(self,space):
        self.is_visible = True
        self.current_space = space
        self.draw()

    def set_invisible(self):
        self.is_visible = False

    def set_image_path(self, image_path):
        self.image_path = image_path
        self.draw()

    def draw(self):
        if self.is_visible:
            self.deck.set_key_image_path(self.current_space, self.image_path)

        return

    def on_pressed(self):
        self.is_pressed = True
        return

    def on_released(self):
        self.is_pressed = False
        return

    

    