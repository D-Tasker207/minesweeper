#Minesweeper - Duncan Tasker

import arcade
from random import randint

#Screen setup variables
SCREEN_TITLE = "Minesweeper"

class MyGame(arcade.Window):
    #Main application Class
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        #call parent class and set up window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        arcade.set_background_color([128, 128, 128])
        
        #Lists to keep track of sprites
        self.wall_list = None
                
        self.X_SIZE = 0
        self.Y_SIZE = 0
        
        #Game variables
        self.playspace = []
        self.flagsleft = 0
        
    def setup(self, X_SIZE, Y_SIZE, mine_amount):
        #Set up game here, call function to restart game
        
        #Create Sprite Lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        
        self.X_SIZE = X_SIZE
        self.Y_SIZE = Y_SIZE
        
        #Fill playspace with squares
        for i in range(0, self.Y_SIZE):
            for j in range(0, self.X_SIZE):
                wall = arcade.Sprite(":resources:gui_basic_assets/window/grey_panel.png", 0.5)
                wall.center_x = (j * 50) + 25
                wall.center_y = (i * 50) + 25
                self.wall_list.append(wall)
                
        #Set up arrays to store game data
        self.playspace = [[0 for i in range(self.Y_SIZE)]for j in range(self.X_SIZE)]
            
        #fill playspace with randomly placed mines
        self.flag_count = mine_amount
        temp_mine_total = mine_amount
        while temp_mine_total > 0:
            mine_x = randint(0,self.X_SIZE - 1)
            mine_y =randint(0,self.Y_SIZE - 1)
            
            if self.playspace[mine_x][mine_y] != 100:
                self.playspace[mine_x][mine_y] = 100
                temp_mine_total -= 1
        
        #theres a better way to do this but its like 1am, i can't be bothered to think about it
        #it also only runs at the start of each game so it shouldn't be a that much of a problem
        mine_check = lambda x, y: 1 if self.playspace[x][y] == 100 else 0
        for j in range(0,self.Y_SIZE):
            for i in range(0,self.X_SIZE):
                if (self.playspace[i][j] != 100):
                    #only check the stuff below if the current space is not a bomb
                
                    #top right corner
                    if [i,j] == [self.X_SIZE - 1, self.Y_SIZE - 1]:
                        mine_prox = mine_check(i-1,j)
                        mine_prox += mine_check(i,j-1)
                        mine_prox += mine_check(i-1,j-1)
                        self.playspace[i][j] = mine_prox
            
                    #top left corner
                    elif [i, j] == [0, self.Y_SIZE - 1]:
                        mine_prox = mine_check(i+1,j)
                        mine_prox += mine_check(i,j-1)
                        mine_prox += mine_check(i+1,j-1)
                        self.playspace[i][j] = mine_prox
            
                    #bottom right corner
                    elif [i, j] == [self.X_SIZE - 1, 0]:
                        mine_prox = mine_check(i-1,j)
                        mine_prox += mine_check(i,j+1)
                        mine_prox += mine_check(i-1,j+1)
                        self.playspace[i][j] = mine_prox
            
                    #bottom left corner
                    elif [i, j] == [0, 0]:
                        mine_prox = mine_check(i+1,j)
                        mine_prox += mine_check(i,j+1)
                        mine_prox += mine_check(i+1,j+1)
                        self.playspace[i][j] = mine_prox
            
                    #left edge
                    elif i == 0:
                        mine_prox = mine_check(i+1,j)
                        mine_prox += mine_check(i,j+1)
                        mine_prox += mine_check(i,j-1)
                        mine_prox += mine_check(i+1,j+1)
                        mine_prox += mine_check(i+1,j-1)
                        self.playspace[i][j] = mine_prox
            
                    #right edge
                    elif i == self.X_SIZE - 1:
                        mine_prox = mine_check(i-1,j)
                        mine_prox += mine_check(i,j+1)
                        mine_prox += mine_check(i,j-1)
                        mine_prox += mine_check(i-1,j+1)
                        mine_prox += mine_check(i-1,j-1)
                        self.playspace[i][j] = mine_prox
            
                    #top edge
                    elif j == self.Y_SIZE - 1:
                        mine_prox = mine_check(i+1,j)
                        mine_prox += mine_check(i-1,j)
                        mine_prox += mine_check(i,j-1)
                        mine_prox += mine_check(i+1,j-1)
                        mine_prox += mine_check(i-1,j-1)
                        self.playspace[i][j] = mine_prox
            
                    #bottom edge
                    elif j == 0:
                        mine_prox = mine_check(i+1,j)
                        mine_prox += mine_check(i-1,j)
                        mine_prox += mine_check(i,j+1)
                        mine_prox += mine_check(i+1,j+1)
                        mine_prox += mine_check(i-1,j+1)
                        self.playspace[i][j] = mine_prox
                
                    #central squares
                    else:
                        mine_prox = mine_check(i+1,j)
                        mine_prox += mine_check(i-1,j)
                        mine_prox += mine_check(i,j+1)
                        mine_prox += mine_check(i,j-1)
                        mine_prox += mine_check(i+1,j+1)
                        mine_prox += mine_check(i-1,j+1)
                        mine_prox += mine_check(i+1,j-1)
                        mine_prox += mine_check(i-1,j-1)
                        self.playspace[i][j] = mine_prox
                                    
        
    def on_draw(self):
        #render the screen
        arcade.start_render()
        
        #code to draw screen goes here
        self.wall_list.draw()
        
        #Drawing the flag counter in the top row
        flag_count_text = f" Flags: {self.flag_count}"
        arcade.draw_text(flag_count_text, 10, ((self.Y_SIZE + 1) * 50) - 35, arcade.color.WHITE, 20)        
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        #handles mouse interactions with the playfield
        
        #rounds mouse clicks to the nearest tile center
        myround = lambda x, y: y * round(x/y)
        corrected_x = myround(_x - 25, 50) + 25
        corrected_y = myround(_y - 25, 50) + 25
        
        if _button == 1:
            #Left click actions
            for idx, val in enumerate(self.wall_list):
                if val.position == (corrected_x, corrected_y):
                    wall = arcade.Sprite(":resources:images/tiles/dirt.png", 1, 0, 0, 48, 48)
                    wall.position = val.position
                    self.wall_list.remove(val)
                    self.wall_list.insert(idx, wall)
                    print(corrected_x // 50, corrected_y // 50, self.playspace[corrected_x // 50][corrected_y // 50])
                    
                    if (self.playspace[corrected_x // 50][corrected_y // 50] == 100) or (self.playspace[corrected_x // 50][corrected_y // 50] == -100):
                        print("Game Over")
                        arcade.exit()
                    
        if _button == 4:
            #Right click actions 
            for idx, val in enumerate(self.wall_list):
                if val.position == (corrected_x, corrected_y):
                    #Add flag if selected position does not have flag (value > 0)
                    if self.playspace[corrected_x // 50][corrected_y // 50] > 0:
                        #multiply value by -1 to remove flag indication
                        self.playspace[corrected_x // 50][corrected_y // 50] *= -1
                        
                        #replacing tile at position with flag
                        wall = arcade.Sprite(":resources:images/tiles/grass.png", 1, 0, 0, 48, 48)
                        wall.position = val.position
                        self.wall_list.remove(val)
                        self.wall_list.insert(idx, wall)
                        
                        #increment flag count when removed
                        self.flag_count -= 1
                        
                    
                    #remove flag if selected position has flag already (value < 0)
                    elif self.playspace[corrected_x // 50][corrected_y // 50] < 0:
                        #multiply value by -1 to indicate flag
                        self.playspace[corrected_x // 50][corrected_y // 50] *= -1
                        
                        #replacing the flag with blank tile again
                        wall = arcade.Sprite(":resources:images/tiles/brickGrey.png", 1, 0, 0, 48, 48)
                        wall.position = val.position
                        self.wall_list.remove(val)
                        self.wall_list.insert(idx, wall)
                        
                        #decrement flag count after flag is placed
                        self.flag_count += 1
        
    
def main():
    #difficulty selection screen before game is launched
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
    
    #defining screen dimensions based on difficulty (playspace size and amount of mines)
    SCREEN_WIDTH = X_SIZE * 50
    SCREEN_HEIGHT = (Y_SIZE + 1) * 50
    
    #calling the arcade class to draw screen
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup(X_SIZE, Y_SIZE, mine_amount)
    arcade.run()

if __name__ == "__main__":
    main()