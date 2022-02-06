# Pong v1
# 
# Pong is a game where two players try to bounce a moving ball into the oponents side
# The ball bounces off the walls and if it hits the oponents side the player gets a score
# The players use their paddles to stop and bounce the ball around
# First person to get to 11 points wins
#
# v1 requirements:
# The first version must display the ball and both paddles, with the ball  bouncing from the
# window edges. The ball should also not bounce off the paddles. Instead it should go through 
# the paddles. The paddles do not move and no score is kept so the game does not end until the 
# player closes the window.

import pygame

# User-defined fucntions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   window_width = 500
   window_height = 400
   pygame.display.set_mode((window_width, window_height))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 

   # create a game object
   game = Game(w_surface, window_width, window_height)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 
   
# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface, window_width, window_height):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects   
      
      # balls specifications
      ball_radius = 7
      x_starting_position = window_width // 2 - 7
      y_starting_position = window_height // 2 - 7
      x_velocity = 9
      y_velocity = 2     
      self.ball = Ball('white', ball_radius, [x_starting_position,y_starting_position], [x_velocity, y_velocity], surface) 
      
      # general paddle specifications
      paddle_margin_wall = 100
      paddle_width = 12
      paddle_height = 50      
      paddle_color = pygame.Color('white')
      paddle_position_top = window_height //2 - paddle_height // 2
      
      # left paddle specifications
      left_paddle_position_left = paddle_margin_wall      
      left_paddle_params = pygame.Rect(left_paddle_position_left, paddle_position_top,\
                           paddle_width, paddle_height)
      
      # right paddle specifications
      right_paddle_position_left = window_width - paddle_width - paddle_margin_wall
      right_paddle_params = pygame.Rect(right_paddle_position_left, paddle_position_top,\
                            paddle_width, paddle_height)      
      
      # create the left and right paddles
      self.left_paddle = Paddle(paddle_color ,left_paddle_params, surface)
      self.right_paddle = Paddle(paddle_color ,right_paddle_params, surface)

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()            
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      self.left_paddle.draw()
      self.right_paddle.draw()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update      
      self.ball.move()
      
   def decide_continue(self):
      pass

class Ball:
   # An object in this class represents a Ball that that moves 
   
   def __init__(self, Ball_color, Ball_radius, Ball_center, Ball_velocity, surface):
      # Initialize the ball.
      # - self is the Ball to initialize
      # - color is the pygame.Color of the Ball
      # - center is a list containing the x and y int
      #   coords of the center of the Ball
      # - radius is the int pixel radius of the Ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object
      self.color = pygame.Color(Ball_color)
      self.radius = Ball_radius
      self.center = Ball_center
      self.velocity = Ball_velocity
      self.surface = surface
           
   def move(self):
      # Change the location of the Ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Ball
      # move our Ball based on its velocity. If it comes in contact
      # with any of the four walls, reverse its direction of motion.
      size = self.surface.get_size()
      for index in range(0, len(size)):
         self.center[index] = (self.center[index] + self.velocity[index])
         if (self.center[index] < self.radius \
             or self.center[index] > size[index] - self.radius):
            self.velocity[index] = -self.velocity[index]
                             
   def draw(self):
      # Draw the Ball on the surface
      # - self is the Ball      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)

class Paddle:
   # An object in this class represents a Ball that that moves 
   
   def __init__(self, paddle_color, paddle_params, surface):
      # Initialize the paddle
      # - self is the paddle to initialize
      # - paddle_color is the Color of the paddle
      # - rect_params give the values of rect_left, rect_top, rect_width, rect_height
      # - surface is the window's pygame.Surface object
      self.paddle_color = paddle_color
      self.rect_params = paddle_params      
      self.surface = surface
          
   def draw(self):
      # Draw the paddle on the surface
      # - self is the paddle    
      pygame.draw.rect(self.surface, self.paddle_color, self.rect_params)

main()
