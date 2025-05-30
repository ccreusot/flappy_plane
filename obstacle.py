import pygame
import random

class Obstacle:
    def __init__(self, sprite, position):
        self.sprite = sprite
        self.position = position
        self.y_default = position.y # Store the default y position

    def update(self, dt, screen):
        self.position.x -= 100 * dt  # Move the obstacle to the left
        if self.position.x < -self.sprite.get_width():
            self.position.x = screen.get_width()  # Reset the obstacle to the right side of the screen when it reaches the left side
            # Randomize the Obstacle y position
            # Make sure the obstacle is not too close to the player
            if self.y_default <= 0:
                start = int(min(self.y_default, self.y_default - self.sprite.get_height() // 3))
                stop = int(max(self.y_default, self.y_default - self.sprite.get_height() // 3))
            else:
                start = int(min(self.y_default, self.y_default + self.sprite.get_height() // 3))
                stop = int(max(self.y_default, self.y_default + self.sprite.get_height() // 3))
            self.position.y = random.randint(start, stop)
            global score_updated
            score_updated = False

    def draw(self, screen):
        screen.blit(self.sprite, self.position)