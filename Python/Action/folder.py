
from Action.action import Action

class Folder:

    def __init__(self,deck):
        
        # List of Actions
        self.actions = [Action(deck)] * 15
        self.deck = deck

        return

    def set_action(self, space_index:int, action):
        if not 14 >= space_index >= 0:
            print("Space index error: "+ space_index)
            return
        self.actions[space_index] = action


    def open(self):

        # for each action in actions, draw action
        for i in range(0,len(self.actions)):
            if self.actions[i]:
                self.actions[i]._set_visible(i)

        # hook layout as current folder
        self.deck.current_folder = self
        return


    def button_pressed(self, space_index:int):
        if self.actions[int(space_index)]:
            self.actions[int(space_index)]._pressed()


    def button_released(self, space_index:int):
        if self.actions[int(space_index)]:
            self.actions[int(space_index)]._released()

