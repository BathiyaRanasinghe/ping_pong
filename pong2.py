# Pong v2
# 
# Pong is a game where two players try to bounce a moving ball into the oponents side
# The ball bounces off the walls and if it hits the oponents side the player gets a score
# The players use their paddles to stop and bounce the ball around
# First person to get to 11 points wins
#
# v2 requirements:
# The second version should add a scoreboard that is updated based on the rules of the game
# and the game should end according to the rules of the game - when a score reaches 11. 
# In addition, the ball should now bounce off the front side of each paddle but go through
# the back side of each paddle.

# imports the pygame module
import pygame

# User-defined fucntions

def main():
   # initialize all pygame modules 
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

      # === general game objects 
      self.surface = surface
      self.window_width = window_width
      self.window_height = window_height
      self.bg_color = pygame.Color('black')      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects   
   
      # Paddles specifications
      self.paddle_margin_wall = 100
      self.paddle_width = 12
      self.paddle_height = 50      
      self.paddle_color = pygame.Color('white')
      self.paddle_position_top = self.window_height //2 - self.paddle_height // 2
      self.left_paddle_position_left = self.paddle_margin_wall   
      self.right_paddle_position_left = self.window_width - self.paddle_width \
                                        - self.paddle_margin_wall
       
      # left paddle specifications               
      self.left_paddle_params = pygame.Rect(self.left_paddle_position_left, \
                                self.paddle_position_top, self.paddle_width, self.paddle_height)
      
      # right paddle specifications
      self.right_paddle_params = pygame.Rect(self.right_paddle_position_left, \
                                 self.paddle_position_top, self.paddle_width, self.paddle_height)  
      
      # create the left and right paddles
      self.left_paddle = Paddle(self.paddle_color ,self.left_paddle_params, surface)
      self.right_paddle = Paddle(self.paddle_color ,self.right_paddle_params, surface)
      
      # balls specifications
      self.ball_radius = 6
      self.ball_colour = 'white'    
      self.x_velocity = 9
      self.y_velocity = 3
      self.center = [window_width // 2 - 7, window_height // 2 - 7]
       
      # create the ball   
      self.ball = Ball(self.ball_colour, self.ball_radius, self.center, \
                  [self.x_velocity, self.y_velocity], self.left_paddle, self.right_paddle, surface)
      
      # create scoreboard values
      self.score_left, self.score_right = 0, 0 

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
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
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display
      
   def draw_score(self):
      # render scoreboards text to screen
      text_color = pygame.Color('white')        
      text_font = pygame.font.SysFont("", 72)      
      left_scoreboard_position = (0, 0)      
      left_scoreboard = text_font.render(str(self.score_left), True, text_color)
      self.surface.blit(left_scoreboard , left_scoreboard_position)        
      right_scoreboard = text_font.render(str(self.score_right), True, text_color)   
      right_scoreboard_position = (self.window_width - right_scoreboard.get_width(), 0)
      self.surface.blit(right_scoreboard, right_scoreboard_position)  

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update      
      self.ball.move()
      self.ball.collision_paddle(self.left_paddle_params,self.right_paddle_params)
      
      # check if the ball hit the left or right wall and discribute points accordingly
      if self.center[0] < self.ball_radius:  
         self.score_right = self.score_right + 1       
      if self.center[0] + self.ball_radius > self.window_width:  
         self.score_left = self.score_left + 1
                
   def decide_continue(self):
      # Decides game end condition
      if self.score_left >= 11 or self.score_right >= 11:
         self.continue_game = False

class Ball:
   # An object in this class represents a Ball that that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, left_paddle, right_paddle, surface):
      # Initialize the ball.
      # - self is the Ball to initialize
      # - color is the pygame.Color of the Ball
      # - center is a list containing the x and y int
      #   coords of the center of the Ball
      # - radius is the int pixel radius of the Ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object
      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.left_padle = left_paddle
      self.right_paddle = right_paddle
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
      
   def collision_paddle(self, left_paddle, right_paddle):  
      # check if ball bounced on the  front of each paddle
      if left_paddle.collidepoint(self.center[0] - 6, self.center[1]) and self.velocity[0] < 0 \
         or right_paddle.collidepoint(self.center[0] + 6, self.center[1]) and self.velocity[0] > 0: \
         self.velocity[0] = -self.velocity[0]   

class Paddle:
   # An object in this class represents a paddle  
   
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
