# Importing arcade module
import arcade
  
# Creating MainGame class       
class MainGame(arcade.Window):
    def __init__(self):
        super().__init__(600, 600, title="Keyboard Inputs")
  
        # Starting location of player
        self.x = 100
        self.y = 100
  
    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()
  
        # Drawing our player
        arcade.draw_circle_filled(self.x, self.y,25,
                                     arcade.color.GREEN )
          
    # Creating function to check the position
    # of the mouse
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.x = x
        self.y = y
      
    # Creating function to check the mouse clicks
    def on_mouse_press(self, x, y, button, modifiers):
        print("Mouse button is pressed")
                
# Calling MainGame class       
MainGame()
arcade.run()