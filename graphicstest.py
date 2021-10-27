# Arcade library tests

import arcade
import random
import warnings

#Screen setup variables
SCREEN_TITLE = "Minesweeper"

#Sprite Scaling
#CHARACTER_SCALING = 1
TILE_SCALING = 0.5

warnings.filterwarnings("ignore")

class MyGame(arcade.Window):
    #Main application Class
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        #call parent class and set up window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        print(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        arcade.set_background_color([128, 128, 128])
        
        #Lists to keep track of sprites
        self.wall_list = None
        #self.player_list = None
        
        #Game variables
        self.heatmap = []
        self.playspace = []
        self.flagsleft = 0
    def setup(self, X_SIZE, Y_SIZE, mine_amount):
        #Set up game here, call function to restart game
        
        #Create Sprite Lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        
        #Fill playspace with squares
        for i in range(0, Y_SIZE):
            for j in range(0, X_SIZE):
                wall = arcade.Sprite(":resources:gui_basic_assets/window/grey_panel.png", TILE_SCALING)
                wall.center_x = (j * 50) + 25
                wall.center_y = (i * 50) + 25
                self.wall_list.append(wall)
                
        #Set up arrays to store game data
        self.playspace = [[0 for i in range(Y_SIZE)]for j in range(X_SIZE)]
        
        print(self.playspace)
            
        #fill playspace with randomly placed mines
        self.flagsleft = mine_amount
        temp_mine_total = mine_amount
        while temp_mine_total > 0:
            mine_x = random.randint(0,X_SIZE - 1)
            mine_y = random.randint(0,Y_SIZE - 1)
            
            print(temp_mine_total, self.playspace[mine_x][mine_y], mine_x, mine_y)
            
            if self.playspace[mine_x][mine_y] != "B":
                self.playspace[mine_x][mine_y] = "B"
                temp_mine_total -= 1
                print(self.playspace)
        
        
    def on_draw(self):
        #render the screen
        arcade.start_render()
        
        #code to draw screen goes here
        self.wall_list.draw()
        #self.player_list.draw()
        
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        #handles mouse interactions with the playfield
        
        #rounds mouse clicks to the nearest tile center
        myround = lambda x, y: y * round(x/y)
        corrected_x = myround(_x - 25, 50) + 25
        corrected_y = myround(_y - 25, 50) + 25
        
        if _button == 1:
            #Left click actions
            for i in self.wall_list:
                if i.position == (corrected_x, corrected_y):
                    wall = arcade.Sprite(":resources:images/tiles/dirt.png", 1, 0, 0, 48, 48)
                    wall.position = i.position
                    self.wall_list.remove(i)
                    self.wall_list.append(wall)
                    print(corrected_x // 50, corrected_y // 50)
                    print(self.playspace[corrected_x // 50][corrected_y // 50])
                    
        if _button == 4:
            #Right click actions
            for i in self.wall_list:
                if i.position == (corrected_x, corrected_y):
                    wall = arcade.Sprite(":resources:images/tiles/grass.png", 1, 0, 0, 48, 48)
                    wall.position = i.position
                    self.wall_list.remove(i)
                    self.wall_list.append(wall)

def testfunction():
    print("hello world")
    
def main():
    
    
    difficulty_selection_is_valid = False
    while difficulty_selection_is_valid == False:
        difficulty_selection = input("Select (E)asy, (M)edium, or (H)ard :: ")
        if difficulty_selection == "E":
            X_SIZE = 8
            Y_SIZE = 8
            mine_amount = 10
            difficulty_selection_is_valid = True
        elif difficulty_selection == "M":
            X_SIZE = 16
            Y_SIZE = 16
            mine_amount = 40
            difficulty_selection_is_valid = True
        elif difficulty_selection == "H":
            X_SIZE = 30
            Y_SIZE = 16
            mine_amount = 99
            difficulty_selection_is_valid = True
        elif difficulty_selection == "T":
            X_SIZE = 3
            Y_SIZE = 3
            mine_amount = 1
            difficulty_selection_is_valid = True
        else:
            print("Please input E, M, or H for corrosponding difficulty level")
    
    SCREEN_WIDTH = X_SIZE * 50
    SCREEN_HEIGHT = (Y_SIZE + 1) * 50
    
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup(X_SIZE, Y_SIZE, mine_amount)
    arcade.run()

if __name__ == "__main__":
    main()