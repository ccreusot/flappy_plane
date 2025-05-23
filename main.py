import pygame
import xml.etree.ElementTree as ET
import random


def load_sprites_sheet(file_name):
    sprites_atlas = file_name + ".xml"
    sprites_sheet = file_name + ".png"

    sprites_sheet_image = pygame.image.load(sprites_sheet).convert_alpha()
    sprites_tree = ET.parse(sprites_atlas)
    sprites_root = sprites_tree.getroot()
    sprites = {}
    for sprite in sprites_root.findall("SubTexture"):
        sprite_name = sprite.attrib["name"]
        sprite_rect = pygame.Rect(
            int(sprite.attrib["x"]),
            int(sprite.attrib["y"]),
            int(sprite.attrib["width"]),
            int(sprite.attrib["height"])
        )
        sprite_image = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
        sprite_image.blit(sprites_sheet_image, (0, 0), sprite_rect)
        sprites[sprite_name] = sprite_image
    return sprites

def floor(value):
    return int(value)

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

class Player:
    def __init__(self, sprites, position):
        self.sprites = sprites
        self.position = position
        self.upward_vector = pygame.Vector2(0, 0)
        self.current_frame = 0
        self.rotation = 0  # Player rotation in degrees

    def update(self, dt):
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

    def collide(self, obstacle):
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
        return player_rect.colliderect(obstacle_rect) or player_rect.colliderect(pygame.Rect(0, screen.get_height() - 50, screen.get_width(), screen.get_height()))

class Obstacle:
    def __init__(self, sprite, position):
        self.sprite = sprite
        self.position = position
        self.y_default = position.y # Store the default y position

    def update(self, dt):
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

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((360, 640))
clock = pygame.time.Clock()
running = True
playable = False
score_updated = False

planes = load_sprites_sheet("ressources/planes")
sheet = load_sprites_sheet("ressources/sheet")
scale_factor = 1.4
dt = 0
score = 0

background = ScrollingImage(sheet["background.png"], 100, pygame.Vector2(0, 0), scale_factor)
ground = ScrollingImage(sheet["groundDirt.png"], 60, pygame.Vector2(0, screen.get_height() - sheet["groundDirt.png"].get_height()))
player = Player([planes["planeBlue1.png"], planes["planeBlue2.png"], planes["planeBlue3.png"]], pygame.Vector2(screen.get_width() / 2 - planes["planeBlue1.png"].get_width() / 2, screen.get_height() / 2 - planes["planeBlue1.png"].get_height() / 2))
obstacles = [
    Obstacle(sheet["rock.png"], pygame.Vector2(screen.get_width() + sheet["rock.png"].get_width(), screen.get_height() - sheet["rock.png"].get_height())),
    Obstacle(sheet["rockDown.png"], pygame.Vector2(screen.get_width() + sheet["rockDown.png"].get_width(), 0))
    ]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not playable:
                    playable = True
                player.move_up()

    if playable:
        background.update(dt)
        ground.update(dt)
        player.update(dt)
        for obstacle in obstacles:
            obstacle.update(dt)
            if player.collide(obstacle):
                playable = False
                player = Player([planes["planeBlue1.png"], planes["planeBlue2.png"], planes["planeBlue3.png"]], pygame.Vector2(screen.get_width() / 2 - planes["planeBlue1.png"].get_width() / 2, screen.get_height() / 2 - planes["planeBlue1.png"].get_height() / 2))
                obstacles = [
                    Obstacle(sheet["rock.png"], pygame.Vector2(screen.get_width() + sheet["rock.png"].get_width(), screen.get_height() - sheet["rock.png"].get_height())),
                    Obstacle(sheet["rockDown.png"], pygame.Vector2(screen.get_width() + sheet["rockDown.png"].get_width(), 0))
                    ]
                
        # Update score
        if not score_updated and player.position.x > obstacles[0].position.x + obstacles[0].sprite.get_width() // 2:
            score += 1
            score_updated = True

    screen.fill("purple")

    # background full screen
    background.draw(screen)
    ground.draw(screen)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
        # player.collide(obstacle)

    # Display score centered on top of the screen
    score_text = pygame.font.SysFont("Arial", 42).render(f"{score}", True, (0, 0, 0))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()