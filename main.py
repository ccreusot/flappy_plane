import pygame
import xml.etree.ElementTree as ET
import random
import ia
from scrollingimage import ScrollingImage
from obstacle import Obstacle
from player import Player

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
# player = Player([planes["planeBlue1.png"], planes["planeBlue2.png"], planes["planeBlue3.png"]], pygame.Vector2(screen.get_width() / 2 - planes["planeBlue1.png"].get_width() / 2, screen.get_height() / 2 - planes["planeBlue1.png"].get_height() / 2))
obstacles = [
    Obstacle(sheet["rock.png"], pygame.Vector2(screen.get_width() + sheet["rock.png"].get_width(), screen.get_height() - sheet["rock.png"].get_height())),
    Obstacle(sheet["rockDown.png"], pygame.Vector2(screen.get_width() + sheet["rockDown.png"].get_width(), 0))
    ]

# idk, some name
learner_count = 100

# cohorte_count
# cohorte_size
# update_pct_range

ai_array = []
player_arr = []


def generate_player():
    return Player([planes["planeBlue1.png"], planes["planeBlue2.png"], planes["planeBlue3.png"]], pygame.Vector2(screen.get_width() / 2 - planes["planeBlue1.png"].get_width() / 2, screen.get_height() / 2 - planes["planeBlue1.png"].get_height() / 2))    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not playable:
        if len(player_arr) > 0 and all(not player.canPlay for player in player_arr):
            ai_array.sort(key=lambda ai: player_arr[ai.id].score, reverse=True)
            new_ai_array = []
            ai_count = 0
            for ai in ai_array[:10]:
                ai.id = ai_count
                new_ai_array.append(ai)
                ai_count += 1
                for i in range(9):
                    new_ai = ia.IA.from_ia(ai)
                    new_ai.id = ai_count
                    new_ai_array.append(new_ai)
                    ai_count += 1
            ai_array = new_ai_array
        else:
            # if [player_arr] is empty
            # init randomly (uniform) [cohorte_count] x [cohorte_size] AI
            # else
            # keep the [cohorte_count] best
            # for each generate [cohorte_size - 1] new AI that use the parent weight with random update in the range +/-[update_pct_range]%
            ai_array = [ia.IA(i) for i in range(learner_count)]
        # give each AI a player
        player_arr = [generate_player() for _ in range(len(ai_array))]
        playable = True

    if playable:
        # AI decision

        for i, bot in enumerate(ai_array):
            linked_player = player_arr[i]
            pipe_hole = pygame.Vector2(obstacles[0].position.x, obstacles[0].position.y + obstacles[0].sprite.get_height())
            pipe_distance = linked_player.position.distance_to(pipe_hole)
            if bot.should_flap(linked_player.position.y, pipe_distance):
                linked_player.move_up()

        background.update(dt)
        ground.update(dt)
        for player in player_arr:
            player.update(dt)

        for obstacle in obstacles:
            obstacle.update(dt, screen)
            for i, player in enumerate(player_arr):
                if player.collide(obstacle, screen):
                    player.canPlay = False
                    #print(f"Player({i}): {player.score}")

        if all(not player.canPlay for player in player_arr):
            # Find the 10 players that have the hightest score
            # Generate the 9 from the top 10
            playable = False
            obstacles = [
                Obstacle(sheet["rock.png"], pygame.Vector2(screen.get_width() + sheet["rock.png"].get_width(), screen.get_height() - sheet["rock.png"].get_height())),
                Obstacle(sheet["rockDown.png"], pygame.Vector2(screen.get_width() + sheet["rockDown.png"].get_width(), 0))
            ]
            continue

        # Update score
        # if not score_updated and player.position.x > obstacles[0].position.x + obstacles[0].sprite.get_width() // 2:
        #     score += 1
        #     score_updated = True        

    screen.fill("purple")

    # background full screen
    background.draw(screen)
    ground.draw(screen)
    for player in player_arr:
        player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    # Display score centered on top of the screen
    score_text = pygame.font.SysFont("Arial", 42).render(f"{score}", True, (0, 0, 0))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()