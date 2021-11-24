#Minesweeper - Duncan Tasker

#import arcade for screen drawing routines and randint for mine placement
import arcade
import arcade.gui
from random import randint

#Screen setup variables
SCREEN_TITLE = "Minesweeper"

class GameView(arcade.View):
    #Main application Class
    
    def __init__(self):
        #call parent class and set up window
        super().__init__()
        self.center_on_screen()
        arcade.set_background_color([210,210,210])
        
        #Lists to keep track of sprites
        self.tile_list = None
        
        #Game variables
        self.playspace = []
        self.flagsleft = 0
        
    def setup(self, X_SIZE, Y_SIZE, mine_amount):
        #Set up game here, call function to restart game
        
        #Create Sprite Lists
        self.tile_list = arcade.SpriteList(use_spatial_hash=True)
                
        #create restart list of values for quick restarts
        self.restart_values = (X_SIZE, Y_SIZE, mine_amount)
        
        #set global variable for mine amount to be used in win check
        self.mine_amount = mine_amount
        self.X_SIZE = X_SIZE
        self.Y_SIZE = Y_SIZE
        
        self.winstate_text = ""
        
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
        arcade.draw_text(flag_count_text, 10, self.window.height - 35, arcade.color.BLACK, 20)
        
        arcade.draw_text(self.winstate_text, self.window.width // 2 - 75, self.window.height - 35, arcade.color.BLACK, 20)
        
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
            if _button == 1 and _modifiers == 0:
                self.left_click(corrected_x, corrected_y)
            elif _button == 4 or (_button == 1 and _modifiers == 2):
                self.right_click(corrected_x, corrected_y)
                
        #quick restart by pressing shift left click
        if _button == 1 and _modifiers == 1:
            self.setup(self.restart_values[0], self.restart_values[1], self.restart_values[2])
    
    
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
                    self.game_over()
                    return
                    
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
                if j[0] == 100 and j[1] == True:
                    flagged_mines += 1
                    
        if flagged_mines == self.mine_amount:
            self.allow_mouse_press = False
            self.winstate_text = "YOU WIN"
            
    
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
        self.winstate_text = "GAME OVER"
                
    def center_on_screen(self):
        #function centers the window on the screen
        screen_dimensions = arcade.get_display_size()
        
        _left = screen_dimensions[0] // 2 - self.window.width // 2
        _top = screen_dimensions[1] // 2 - self.window.height // 2
        self.window.set_location(_left, _top)
        
class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        
        #create ui manager for buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        #set background color
        arcade.set_background_color(arcade.color.GRAY)
        
        #create vbox to keep buttons centered on screen
        self.vbox = arcade.gui.UIBoxLayout()
        
        #add text widgit for button context
        ui_text_label = arcade.gui.UITextArea(text="Select Difficulty Option", width=330,height=40,font_size=24, font_name="Roboto")
        self.vbox.add(ui_text_label.with_space_around(bottom=5))
        
        #add subtitle to explain controls
        text = "Left click to reveal squares\nRight Click (two fingers) or Ctrl + Left Click to flag squares\nShift + Left Click to restart"
        ui_text_label = arcade.gui.UITextArea(text=text,width=370, height=110, font_size=18, font_name="Roboto", bold=True)
        self.vbox.add(ui_text_label.with_space_around(bottom=5))
        
        #create three buttons to use with difficulty selection and add to the ui manager
        easy_button = arcade.gui.UIFlatButton(text="Easy",width = 200)
        self.vbox.add(easy_button.with_space_around(bottom=20))
        
        med_button = arcade.gui.UIFlatButton(text="Medium",width = 200)
        self.vbox.add(med_button.with_space_around(bottom=20))
        
        hard_button = arcade.gui.UIFlatButton(text="Hard",width = 200)
        self.vbox.add(hard_button.with_space_around(bottom=20))
        
        #bind button click actions to a helper function
        easy_button.on_click = self.on_click_easy
        med_button.on_click = self.on_click_med
        hard_button.on_click = self.on_click_hard
        
        #bind ui manager to center x and y dimensions
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.vbox))
           
    #button click methods call the setup function with different dimensions and mine amounts
    def on_click_easy(self, event):
        self.start_game(8, 8, 10)
        
    def on_click_med(self, event):
        self.start_game(16, 16, 40)
        
    def on_click_hard(self, event):
        self.start_game(30, 16, 99)
    
    def start_game(self, x_size, y_size, mine_amount):
        
        #defining screen dimensions based on difficulty (playspace size and amount of mines)
        SCREEN_WIDTH = x_size * 50
        SCREEN_HEIGHT = (y_size + 1) * 50

        #adjust screen size to match that of the playspace
        self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        #disable buttons
        self.manager.disable()
        
        #call code to start the main minesweeper playspace
        start_view = GameView()
        start_view.setup(x_size, y_size, mine_amount)
        self.window.show_view(start_view)
        
    def on_draw(self):
        #draw the buttons
        arcade.start_render()
        self.manager.draw()
        
def main():    
    #call the difficulty screen setups and run
    window = arcade.Window(400, 450, "MINESWEEPER")
    start_view = IntroView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()