#Minesweeper - Duncan Tasker

#import arcade for screen drawing routines and randint for mine placement
import arcade
from random import randint

#Screen setup variables
SCREEN_TITLE = "Minesweeper"

class MyGame(arcade.Window):
    #Main application Class
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        #call parent class and set up window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        arcade.set_background_color([210,210,210])
        
        #Lists to keep track of sprites
        self.tile_list = None
                
        self.X_SIZE = 0
        self.Y_SIZE = 0
        
        #Game variables
        self.playspace = []
        self.flagsleft = 0
        
    def setup(self, X_SIZE, Y_SIZE, mine_amount):
        #Set up game here, call function to restart game
        
        #Create Sprite Lists
        #self.player_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList(use_spatial_hash=True)
        
        #set global variables for size to be used in drawing the flag counter on the top (probably better ways to do it but idk)
        self.X_SIZE = X_SIZE
        self.Y_SIZE = Y_SIZE
        
        #set global variable for mine amount to be used in win check
        self.mine_amount = mine_amount
        
        #Fill playspace with squares
        for i in range(0, self.Y_SIZE):
            for j in range(0, self.X_SIZE):
                tile = arcade.Sprite("assets/blank.png")
                tile.center_x = (j * 50) + 25
                tile.center_y = (i * 50) + 25
                self.tile_list.append(tile)
                
        #Set up arrays to store game data
        self.playspace = [[[0] for i in range(self.Y_SIZE)]for j in range(self.X_SIZE)]
            
        #fill playspace with randomly placed mines
        self.flag_count = self.mine_amount
        temp_mine_total = self.mine_amount
        while temp_mine_total > 0:
            mine_x = randint(0,self.X_SIZE - 1)
            mine_y =randint(0,self.Y_SIZE - 1)
            
            if self.playspace[mine_x][mine_y][0] != 100:
                self.playspace[mine_x][mine_y] = [100, False, False]
                temp_mine_total -= 1
        
        #basically just iterate through each square ot see what the tiles immediately around it look like
        mine_check = lambda x, y: 1 if self.playspace[x][y][0] == 100 else 0
        for j in range(0,self.Y_SIZE):
            for i in range(0,self.X_SIZE):
                #only check the stuff below if the current space is not a bomb
                if (self.playspace[i][j][0] != 100):
                    
                    mine_prox = 0
                    for r in range(max(0,j-1), min(j+2, len(self.playspace[i]))):
                        for c in range(max(0,i-1), min(i+2, len(self.playspace))):
                            mine_prox += mine_check(c,r)
                    #data is stored as [mines nearby, flagged, clicked]
                    self.playspace[i][j] = [mine_prox, False, False]

        self.allow_mouse_press = True
        
    def on_draw(self):
        #render the screen
        arcade.start_render()
        
        #code to draw screen goes here
        self.tile_list.draw()
        
        #Drawing the flag counter in the top row
        flag_count_text = f" Flags: {self.flag_count}"
        arcade.draw_text(flag_count_text, 10, ((self.Y_SIZE + 1) * 50) - 35, arcade.color.BLACK, 20)        
        
    def my_round(self, rounding_val, factor):
        #rounds rounding_val to the nearest factor i.e rounds x coordinate to the nearest 50 pixels
        rounded_val = factor * round(rounding_val/factor)
        return rounded_val
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        #handles mouse interactions with the playfield
        
        #rounds mouse clicks to the nearest tile center
        corrected_x = self.my_round(_x - 25, 50) + 25
        corrected_y = self.my_round(_y - 25, 50) + 25
        
        #checks to see if mouse clicks are permitted at this time
        if self.allow_mouse_press == True:
            #call appropriate function for click
            if _button == 1:
                self.left_click(corrected_x, corrected_y)
            elif _button == 4:
                self.right_click(corrected_x, corrected_y)
    
    
    def left_click(self, corrected_x, corrected_y):
        #Left click actions
        #show tile value when clicked
        for idx, val in enumerate(self.tile_list):
            if val.position == (corrected_x, corrected_y):
                
                #get value of tile, check if tile is mine, convert int to string
                tile_val = self.playspace[corrected_x // 50][corrected_y // 50]
                
                # if tile has already been clicked, return from this function
                if tile_val[2] == True:
                    return
                
                #if tile value is a mine call game_over function
                #elif value has been flagged, increment the flag to account for its removal and remove flag in playspace array
                if tile_val[0] == 100:
                    tile_val[0] = "mine"
                    self.game_over()
                    
                elif tile_val[1] == True:
                    self.flag_count += 1
                    self.playspace[corrected_x // 50][corrected_y // 50][1] = False
                
                
                #replace blank tile with tile with appropriate number at same position in tile list
                tile = arcade.Sprite("assets/"+str(tile_val[0])+".png")
                tile.position = val.position
                self.tile_list.remove(val)
                self.tile_list.insert(idx, tile)
                
                #change clicked indicator to indicate tile has been revealed
                self.playspace[corrected_x // 50][corrected_y // 50][2] = True
                
                
                #if tile_val is 0, click the 8 surrounding tiles
                if tile_val[0] == 0:
                    for r in range(max(0, (corrected_y // 50) - 1), min((corrected_y // 50) + 2, len(self.playspace[corrected_x // 50]))):
                        for c in range(max(0, (corrected_x // 50) - 1), min((corrected_x // 50) + 2, len(self.playspace))):
                            self.left_click((c * 50) + 25, (r * 50) + 25)
                    
            
                
    def right_click(self, corrected_x, corrected_y):
        #Right click actions
        #Add flag to current square. current flaw: cannot place flags on squares with value of 0 due to flag detection system
        for idx, val in enumerate(self.tile_list):
            if val.position == (corrected_x, corrected_y):
                #check to see if space has been revealed already
                if self.playspace[corrected_x // 50][corrected_y // 50][2] == True:
                    return
                
                #Add flag if selected position does not have flag (value > 0)
                if self.playspace[corrected_x // 50][corrected_y // 50][1] == False:
                    #only allow flags to be placed if there are flags remaining
                    if self.flag_count > 0:
                        #multiply value by -1 to remove flag indication
                        self.playspace[corrected_x // 50][corrected_y // 50][1] = True
                        
                        #replacing tile at position with flagged tile
                        tile = arcade.Sprite("assets/flagged.png")
                        tile.position = val.position
                        self.tile_list.remove(val)
                        self.tile_list.insert(idx, tile)
                        
                        #increment flag count when removed
                        self.flag_count -= 1
                
                #remove flag if selected position has flag already (value < 0)
                elif self.playspace[corrected_x // 50][corrected_y // 50][1] == True:
                    #multiply value by -1 to indicate flag
                    self.playspace[corrected_x // 50][corrected_y // 50][1] = False
                    
                    #replacing the flag with blank tile again
                    tile = arcade.Sprite("assets/blank.png")
                    tile.position = val.position
                    self.tile_list.remove(val)
                    self.tile_list.insert(idx, tile)
                    
                    #decrement flag count after flag is placed
                    self.flag_count += 1
                        
            #if all flags have been placed run the win check function
            if self.flag_count == 0:
                self.win_check()
                        
    def win_check(self):
        #iterate through playspace to see if the amount of unflagged mines = total mines
        flagged_mines = 0
        for i in self.playspace:
            for j in i:
                if j == -100:
                    flagged_mines += 1
                    
        if flagged_mines == self.mine_amount:
            self.allow_mouse_press = False
            print("You Win!")
    
    def game_over(self):
        #iterate through playspace array and reveal bombs then print
        self.allow_mouse_press = False
        for idx, val in enumerate(self.tile_list):
            #reveal all mines
            if self.playspace[val.center_x // 50][val.center_y // 50][0] == 100:
                #replacing tile at position with flag
                tile = arcade.Sprite("assets/mine.png")
                tile.position = val.position
                self.tile_list.remove(val)
                self.tile_list.insert(idx, tile)
        print("Game Over") 
                        
    
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