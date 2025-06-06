import pygame
import numpy as np
import random

class Obstacle:
    def __init__(self, top_sprite, bottom_sprite, position, gap_size=200):
        self.top_sprite = top_sprite
        self.bottom_sprite = bottom_sprite
        self.position = position
        self.gap_size = gap_size
        self.y_default = position.y # Store the default y position

    def update(self, dt, screen):
        self.position.x -= 100 * dt  # Move the obstacle to the left
        if self.position.x < -max(self.top_sprite.get_width(), self.bottom_sprite.get_width()):
            self.position.x = screen.get_width()  # Reset the obstacle to the right side of the screen when it reaches the left side
            # Randomize the gap size between 150 and 250
            self.gap_size = random.randint(150, 250)
            
            # Randomize the Obstacle y position
            # Make sure the obstacle is not too close to the player
            # The y_position will be the top of the gap
            min_y = 50  # Minimum distance from the top of the screen
            max_y = screen.get_height() - 150 - self.gap_size  # Maximum position considering gap and ground
            self.position.y = np.random.uniform(min_y, max_y)
            global score_updated
            score_updated = False

    def draw(self, screen):
        # Draw the top obstacle (hanging from the top)
        top_position = pygame.Vector2(self.position.x, self.position.y - self.top_sprite.get_height())
        screen.blit(self.top_sprite, top_position)
        
        # Draw the bottom obstacle (standing from the bottom)
        bottom_position = pygame.Vector2(self.position.x, self.position.y + self.gap_size)
        screen.blit(self.bottom_sprite, bottom_position)
    
    def get_sprite(self):
        # For compatibility with collision detection
        return self.top_sprite  # Return one of the sprites for size calculations
        
    def get_top_rect(self):
        return pygame.Rect(
            self.position.x,
            self.position.y - self.top_sprite.get_height(),
            self.top_sprite.get_width(),
            self.top_sprite.get_height()
        )
        
    def get_bottom_rect(self):
        return pygame.Rect(
            self.position.x,
            self.position.y + self.gap_size,
            self.bottom_sprite.get_width(),
            self.bottom_sprite.get_height()
        )

    def get_gap_center(self):
        """Returns the center point of the gap between obstacles"""
        return pygame.Vector2(
            self.position.x + max(self.top_sprite.get_width(), self.bottom_sprite.get_width()) / 2,
            (self.position.y + self.top_sprite.get_height()) + self.gap_size / 2
        )
    
    def get_pike_position_top(self):
        return self.position.y + self.top_sprite.get_height()
    
    def get_pike_position_bottom(self):
        return self.position.y + self.gap_size