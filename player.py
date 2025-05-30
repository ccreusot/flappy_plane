import pygame
import random

def floor(value):
    return int(value)
    
class Player:
    def __init__(self, sprites, position):
        self.sprites = sprites
        self.position = position
        self.upward_vector = pygame.Vector2(0, 0)
        self.current_frame = 0
        self.rotation = 0  # Player rotation in degrees
        self.canPlay = True
        self.score = 0

    def update(self, dt):
        if not self.canPlay:
            return
        self.score+=1
        # Update player position
        if self.upward_vector.y < 0:
            self.position += self.upward_vector * dt  # Apply the upward vector to the player position
            self.upward_vector.y += 500 * dt  # Apply gravity to the player position when going upwards
            if self.rotation < 35:
                self.rotation += 70 * dt
        else: # Get the original sprite
            self.position.y += 200 * dt  # Move the player down the screen
            # Update player rotation
            if self.rotation > -35:
                self.rotation -= 100 * dt  # Rotate the player by 5 degrees per second


        # Last operation updating the player frame position
        self.current_frame = (self.current_frame + 10 * dt) % len(self.sprites)

    def draw(self, screen):
        if not self.canPlay:
            return
        # Get the original sprite
        original_sprite = self.sprites[floor(self.current_frame)]
        
        # Rotate the sprite around its center
        rotated_sprite = pygame.transform.rotate(original_sprite, self.rotation)
        
        # Get the rect of the rotated sprite
        rotated_rect = rotated_sprite.get_rect()
        
        # Set the center of the rotated rect to the center of the original position
        original_center = (self.position.x + original_sprite.get_width() // 2, 
                        self.position.y + original_sprite.get_height() // 2)
        rotated_rect.center = original_center
        
        # Draw the rotated sprite
        screen.blit(rotated_sprite, rotated_rect)

    def move_up(self):
        self.upward_vector.y = -250  # Move the player upwards

    def collide(self, obstacle, screen):
        # Check if the player and the obstacle collide
        # Create a rect for the player (using the center point for better collision)
        original_sprite = self.sprites[floor(self.current_frame)]
        player_center = (self.position.x + original_sprite.get_width() // 2, 
                        self.position.y + original_sprite.get_height() // 2)
        
        # Create a smaller collision circle for the player (using a rect as approximation)
        collision_radius = min(original_sprite.get_width(), original_sprite.get_height()) // 3
        player_rect = pygame.Rect(
            player_center[0] - collision_radius,
            player_center[1] - collision_radius,
            collision_radius * 2,
            collision_radius * 2
        )
        
        # Create a rect for the obstacle
        obstacle_rect = pygame.Rect(
            obstacle.position.x + obstacle.sprite.get_width() / 2, 
            obstacle.position.y, 
            obstacle.sprite.get_width() / 4, 
            obstacle.sprite.get_height()
        )

        # pygame.draw.rect(screen, (255, 0, 0), obstacle_rect)
        
        # Check for collision
        return player_rect.colliderect(obstacle_rect)\
        or self.position.y < 0\
        or self.position.y > screen.get_height() - 100
