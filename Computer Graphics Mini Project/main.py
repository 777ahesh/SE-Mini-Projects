import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load images
RED_SPACE_SHIP = pygame.image.load("redship.png")
GREEN_SPACE_SHIP = pygame.image.load("greenship.png")
ufo1 = pygame.image.load("alien.png")
ufo2 = pygame.image.load("spaceship.png")

# Player player
YELLOW_SPACE_SHIP = pygame.image.load("spacelader.png")

# Lasers
RED_LASER = pygame.image.load("redlaser.png")
GREEN_LASER = pygame.image.load("greenlaser.png")

YELLOW_LASER = pygame.image.load("bullet.png")

# Background
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

# Laser Class Controls the lasers that the space ships shoot
class Laser:
    # constructor
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # Initializing the Game Window
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Controls motion of the Lasers so that the laser can travel from one point to another
    def move(self, vel):
        self.y += vel

    # Removes the Opponent Spaceship out of the player window
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    # Function Call for initiating the collision condition.
    # That is when Laser hits the spaceship
    def collision(self, obj):
        return collide(self, obj)


class Ship:
    # Delay between 2 consecutive laser beams
    COOLDOWN = 30

    # Constructor Of the Base Class
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Displays Space ship on the Player Window
    def draw(self, window):
        # Blit = Makes Image appear on the screen
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Checks Collision Condition and Makes required changes
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            # If the player laser hits the Opponent the Opp space ship Disappears
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            # If opponent laser hits Player then The Player Health Reduces by 10
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # Keeps the delay constant toggles between 0-30 and 30-0
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # If cooldown Counter == 0 then a laser will be shot at the space ship
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Returns Spaceship width
    def get_width(self):
        return self.ship_img.get_width()

    # Returns Spaceship Height
    def get_height(self):
        return self.ship_img.get_height()


# Derived Class Player
# Base class Ship
class Player(Ship):
    # Constructor
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    # Moves lasers for Player
    # 2 conditions
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            # If laser is going out of the screen remove laser
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    # If collision Occurs then remove opp spaceship
                    # removes the laser as well
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # Displays Health bar of the Player as well as the Player Image
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    # Maintains the Health Bar of the Player
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


# Enemy SpaceShip Derived Class
# Base Class = Ship
class Enemy(Ship):

    # Maintains Enemy Ship Colours onscreen and associates Enemy ships with specific laser colours
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "orange":(ufo1,RED_LASER),
                "pink":(ufo2,GREEN_LASER)
                
                }

    # Constructor
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Moves the Enemy Ship
    def move(self, vel):
        self.y += vel

    # Shoots Laser from the Enemy Spaceship
    def shoot(self):
        if self.cool_down_counter == 0:
            # makes sure that laser gets dispatched from the center of the spaceship
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            # prevents major delay of lasers being shot by the enemy ship
            self.cool_down_counter = 1


# Checks if the Lasers have Hit the Space ship or not and makes required chenges
# Takes care of:
# Enemy Laser Hitting Player Spaceship
# Player Laser Hitting Enemy Spaceship
# Player SpaceShip Hits the Enemy or vice versa
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# Driver code Initializes Window
def main():
    # While Run == True Player Keeps playing
    run = True
    # Frames per sec
    FPS = 60
    # Maintains the level of the player
    level = 0
    # Maintains Life of player
    # If life == 0 Game will end
    # Life Reduces when:
    #    1. Enemy Escape the Window
    #    2. Health Bar Becomes 0
    lives = 5

    # Styling of Text on Playing Window
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    # Maintains the enemy spaceships on the screen
    enemies = []
    # Number of enemy spaceships that will come in every instance will be 5
    # The time gap between arrival of the Spaceships will Decrease as levels go on Increasing
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    # Initialize Player with pos(300, 630)
    player = Player(300, 630)

    clock = pygame.time.Clock()

    # If lost == True Game will be over
    lost = False
    lost_count = 0

    # Resets the screen everytime the player wishes to play he game
    def redraw_window():
        WIN.blit(BG, (0,0))
        # Keeps track of the Lives of player and Level the player has reached
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # Display the 5 Enemies on the Player Window
        for enemy in enemies:
            enemy.draw(WIN)

        # Displays the Player on the Window
        player.draw(WIN)

        # Renders the window when player loses the game
        # Displays That You Have Lost
        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        # Updates the player window
        pygame.display.update()

    while run:
        # To smoothen the game
        clock.tick(FPS)
        redraw_window()
        # Checking all the conditions where game will end

        # Checks If player has life left if yes continue
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        # If lost condition == True break game
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # If we kill all the enemies on the window then the player level goes up
        # and rate at which the enemy appears Increases
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green","orange","pink"]))
                enemies.append(enemy)

        # Allows Player To quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Controls :
        # W = Player Moves Up
        # A = Player moves Left
        # S = Player moves Down
        # D = Player Moves Right
        # SpaceBar = Player Shoots Laser
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Defines the Movement of the enemies
        # All enemies will be retrieved from the window
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            # If player spaceship gets hit reduce player health
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            # If enemy escapes reduce player life
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Makes enemy laser move downwards
        player.move_lasers(-laser_vel, enemies)

# Driver code 2:
# Starts the game
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()

# A Project By- 
# Mahesh Gaikwad
# Prathamesh Bhise
# Pranav Gaikwad
