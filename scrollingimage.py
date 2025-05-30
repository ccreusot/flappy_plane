import pygame

class ScrollingImage:
    def __init__(self, image, scroll_speed, position, scale_factor = 1.0):
        self.position = position
        self.scroll_speed = scroll_speed
        self.scale_factor = scale_factor
        self.background = pygame.transform.scale(image, (image.get_width() * scale_factor, image.get_height() * scale_factor))

    def update(self, dt):
        self.position.x -= self.scroll_speed * dt
        if self.position.x < -self.background.get_width():
            self.position.x = 0  # Reset the background to the right side of the screen when it reaches the left side

    def draw(self, screen):
        screen.blit(self.background, (self.position.x, self.position.y))
        screen.blit(self.background, (self.position.x + self.background.get_width(), self.position.y))

