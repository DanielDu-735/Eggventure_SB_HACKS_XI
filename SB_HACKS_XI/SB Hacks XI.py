import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
EGG_RADIUS = 20  # Make the egg smaller
START_OBSTACLE_SPEED = 1  # Slower obstacle speed
MAX_OBSTACLE_SPEED = 10
SPEED_UP_DURATION = 15  # Speed will increase over 15 seconds

# Colors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
CORAL = (255, 165, 0)
LIGHT_YELLOW = (255, 255, 0)
SKY_BLUE = (0, 128, 255)
HOT_PINK = (255, 105, 180)
RED_ORANGE = (255, 69, 0)
DEEP_PINK = (255, 20, 147)
LIGHT_SKY_BLUE = (135, 206, 250)
LIGHT_SEA_GREEN = (32, 178, 170)
DARK_ORANGE = (255, 140, 0)
INDIGO = (75, 0, 130)
LEMON_YELLOW = (255, 239, 0)
LAVENDER_BLUSH = (255, 240, 245)
LIGHT_GREEN = (144, 238, 144)
CYAN = (0, 255, 255)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)

# List of 24 color options with names
colors = [
    (GREEN, "Green"), (BLUE, "Blue"), (RED, "Red"), (ORANGE, "Orange"), (YELLOW, "Yellow"),
    (MAGENTA, "Magenta"), (CORAL, "Coral"), (WHITE, "White"), (LIGHT_YELLOW, "Light Yellow"),
    (SKY_BLUE, "Sky Blue"), (HOT_PINK, "Hot Pink"), (RED_ORANGE, "Red Orange"), (DEEP_PINK, "Deep Pink"),
    (LIGHT_SKY_BLUE, "Light Sky Blue"), (LIGHT_SEA_GREEN, "Light Sea Green"), (DARK_ORANGE, "Dark Orange"),
    (INDIGO, "Indigo"), (LEMON_YELLOW, "Lemon Yellow"), (LAVENDER_BLUSH, "Lavender Blush"),
    (LIGHT_GREEN, "Light Green"), (CYAN, "Cyan"), (SILVER, "Silver"), (GRAY, "Gray")
]

# Initialize the screen object globally
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Font for text
font = pygame.font.SysFont(None, 24)  # Smaller font for color names
title_font = pygame.font.SysFont(None, 50)  # Larger font for the title screen

# Sound Effects
collision_sound = pygame.mixer.Sound("collision_sound.mp3")
bg_music = pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.play(-1, 0.0)  # Loop background music

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action, color=(0, 128, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 255, 0), self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        label = font.render(self.text, True, (0, 0, 0))
        screen.blit(label, (self.rect.centerx - label.get_width() // 2, self.rect.centery - label.get_height() // 2))

    def is_clicked(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            self.action()  # Don't pass self, just call action directly

# Egg class
class Egg:
    def __init__(self, color):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.speed = 5
        self.color = color
        self.invincible = False
        self.invincible_time = 0  # Timer for invincibility
        self.last_collision_time = time.time()  # Track the last collision time

    def move(self, keys):
        if not self.invincible:  # Only allow movement if not invincible
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= self.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += self.speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y -= self.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y += self.speed

        # Keep the egg inside the screen
        self.x = max(EGG_RADIUS, min(self.x, WIDTH - EGG_RADIUS))
        self.y = max(EGG_RADIUS, min(self.y, HEIGHT - EGG_RADIUS))

    def become_invincible(self, duration=2):
        self.invincible = True
        self.invincible_time = time.time() + duration  # Set the invincible time duration

    def update_invincibility(self):
        if self.invincible and time.time() > self.invincible_time:
            self.invincible = False  # End invincibility when the time is up

    def draw(self, screen):
        if self.invincible:
            # Flash the egg color if invincible
            color = (255, 255, 255) if int(time.time() * 5) % 2 == 0 else self.color
        else:
            color = self.color
        pygame.draw.circle(screen, color, (self.x, self.y), EGG_RADIUS)

# Obstacle class
class Obstacle:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 50)
        self.y = -50  # Start from the top of the screen
        self.size = random.randint(30, 80)
        self.speed = speed
        self.color = random.choice([GREEN, BLUE, RED, ORANGE, YELLOW])

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

# Triangle class (new)
class Triangle:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 30)
        self.y = -30  # Start from the top of the screen
        self.size = 30
        self.speed = speed

    def move(self):
        self.y += self.speed  # Slow speed

    def draw(self, screen):
        points = [(self.x, self.y), (self.x + self.size, self.y), (self.x + self.size // 2, self.y + self.size)]
        pygame.draw.polygon(screen, (255, 0, 255), points)


# Color selection page
def color_selection_page():
    screen.fill(BLUE)
    
    # Display the message asking the player to choose an egg color
    color_selection_message = font.render("Please choose your favorite color for your egg.", True, (0, 0, 0))
    screen.blit(color_selection_message, (WIDTH // 2 - color_selection_message.get_width() // 2, 50))  # Centered at the top of the page
    
    color_buttons = []
    button_positions = [(x * 120 + 20, y * 60 + 100) for x in range(6) for y in range(4)]  # Increased spacing
    
    # Create color buttons
    def set_egg_color(color):
        global egg_color
        egg_color = color  # Set the egg color to the button's color
        start_page()  # Show the start page after color selection

    for (x, y), (color, color_name) in zip(button_positions, colors):
        # Make color names smaller and fit inside buttons
        button = Button(x, y, 100, 50, color_name, lambda color=color: set_egg_color(color), color)
        color_buttons.append(button)
    
    # Draw buttons
    for button in color_buttons:
        button.draw(screen, pygame.mouse.get_pos())

    pygame.display.flip()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Check for button clicks
        for button in color_buttons:
            if mouse_click:
                button.is_clicked(mouse_pos, mouse_click)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


# Title screen
def title_screen():
    screen.fill(WHITE)
    
    # Title text
    title_text = title_font.render("Welcome to the Egg Game!", True, (0, 0, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4 - 37))  # Moved up by ~1 cm (~37 pixels)
    
    # Authors' names and emails on separate lines
    authors_text = font.render(
        "Daniel Du", True, (0, 0, 0)
    )
    screen.blit(authors_text, (WIDTH // 2 - authors_text.get_width() // 2, HEIGHT // 3 - 37))  # Moved up by ~1 cm (~37 pixels)
    
    email_text = font.render(
        "danieldu@ucsb.edu", True, (0, 0, 0)
    )
    screen.blit(email_text, (WIDTH // 2 - email_text.get_width() // 2, HEIGHT // 3 + 30 - 37))  # 30px space between name and email
    
    authors_text_2 = font.render(
        "Yuxi Ji", True, (0, 0, 0)
    )
    screen.blit(authors_text_2, (WIDTH // 2 - authors_text_2.get_width() // 2, HEIGHT // 3 + 60 - 37))  # Moved up by ~1 cm (~37 pixels)
    
    email_text_2 = font.render(
        "yuxi_ji@ucsb.edu", True, (0, 0, 0)
    )
    screen.blit(email_text_2, (WIDTH // 2 - email_text_2.get_width() // 2, HEIGHT // 3 + 90 - 37))  # 30px space between name and email
    
    # Event name and date (move down slightly)
    event_text = font.render("SB Hacks XI", True, (0, 0, 0))
    screen.blit(event_text, (WIDTH // 2 - event_text.get_width() // 2, HEIGHT // 2 - 37 + 40))  # Moved down by ~40px

    date_text = font.render("Jan 11, 2025", True, (0, 0, 0))
    screen.blit(date_text, (WIDTH // 2 - date_text.get_width() // 2, HEIGHT // 2 + 30 - 37 + 40))  # Moved down by ~40px
    
    # Start button
    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100 - 37 + 40, 200, 50, "Start Game", color_selection_page)
    start_button.draw(screen, pygame.mouse.get_pos())
    
    pygame.display.flip()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if mouse_click:
            start_button.is_clicked(mouse_pos, mouse_click)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False







# Start page
def start_page():
    screen.fill(WHITE)
    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "START", game)
    start_button.draw(screen, pygame.mouse.get_pos())
    pygame.display.flip()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if mouse_click:
            start_button.is_clicked(mouse_pos, mouse_click)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

# Main game loop
def game():
    global highest_score
    egg = Egg(egg_color)  # Set the egg's color
    obstacles = []
    triangles = []  # New list to hold triangle objects
    game_over = False
    health = 100  # Start with 100% health
    hatch_rate = 0  # Initialize hatching progress
    start_time = time.time()
    level_start_time = time.time()  # Time when the level started
    level = 1  # Start with Level 1
    obstacle_speed = START_OBSTACLE_SPEED  # Initial obstacle speed
    background_color = random.choice([color[0] for color in colors])  # Initial random background color
    last_bg_change_time = time.time()  # Track the last time the background color changed
    last_hit_time = time.time()  # Time when the last obstacle hit happened (used for health recovery)

    while not game_over:
        current_time = time.time()

        # Change the background color every 5 seconds
        if current_time - last_bg_change_time >= 5:
            background_color = random.choice([color[0] for color in colors])  # Randomly change background color
            last_bg_change_time = current_time  # Update the time when the background color last changed

        # Update the level and speed every 10 seconds
        if current_time - level_start_time >= 10:
            level += 1
            obstacle_speed += 1  # Increase obstacle speed every level
            level_start_time = current_time  # Reset the level start time

        screen.fill(background_color)

        # Generate obstacles with increased density
        if random.randint(0, 15) == 0:  # Increased the frequency of obstacles (lowered the random range)
            obstacle = Obstacle(obstacle_speed)
            obstacles.append(obstacle)

        # Generate triangles
        if random.random() < 0.01:  # 1% chance to add a triangle
            triangles.append(Triangle(obstacle_speed))

        # Move obstacles
        for obstacle in obstacles[:]:
            if obstacle.color != background_color:  # Remove obstacles with the same color as the background
                obstacle.move()
                if obstacle.y > HEIGHT:
                    obstacles.remove(obstacle)
                obstacle.draw(screen)

        # Move and draw triangles
        for triangle in triangles[:]:
            triangle.move()
            triangle.draw(screen)

        # Check for collision with obstacles
        hit_occurred = False  # To check if the egg hit any obstacle
        for obstacle in obstacles:
            if (egg.x - obstacle.x)**2 + (egg.y - obstacle.y)**2 < (EGG_RADIUS + obstacle.size // 2)**2:
                if not egg.invincible:
                    health -= 25  # Decrease health by 25% on collision
                    collision_sound.play()
                    egg.become_invincible()
                    hit_occurred = True
                    if health <= 0:
                        health = 0  # Ensure health doesn't go negative

        # If no hit occurred, check health recovery
        if not hit_occurred and current_time - last_hit_time >= 5:
            health = min(100, health + 25)  # Recover 25% health, but max health is 100
            last_hit_time = current_time  # Update the time of the last hit event

        # Check for collision with triangles
        for triangle in triangles[:]:
            if (egg.x - triangle.x)**2 + (egg.y - triangle.y)**2 < (EGG_RADIUS + triangle.size // 2)**2:
                triangles.remove(triangle)  # Remove the triangle after collision
                hatch_rate += 10  # Increase hatching progress by 10%
                if hatch_rate >= 100:
                    game_over = True  # End game if hatching progress reaches 100%

        # Move the egg
        keys = pygame.key.get_pressed()
        egg.move(keys)
        egg.update_invincibility()

        # Timer and Score
        time_elapsed = current_time - start_time
        lambda_factor = 0.00254
        score = round(100 * math.exp(-lambda_factor * time_elapsed), 3)

        # Draw the egg and health
        egg.draw(screen)

        # Display health, hatching progress, score, level, and time
        health_text = font.render(f"Health: {health}%", True, (0, 0, 0))
        hatch_text = font.render(f"Hatch Progress: {hatch_rate}%", True, (0, 0, 0))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        level_text = font.render(f"Level {level}", True, (0, 0, 0))
        time_text = font.render(f"Time: {time_elapsed:.3f}s", True, (0, 0, 0))
        
        screen.blit(health_text, (10, 10))
        screen.blit(hatch_text, (10, 40))  # Show hatch progress below health
        screen.blit(score_text, (10, 70))  # Show score below hatch progress
        screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))  # Position level at the top-right
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 10))  # Position time at the top center

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = True

        pygame.time.Clock().tick(60)

        # End game if health reaches 0%
        if health == 0:
            game_over = True
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.fill((0, 0, 0))  # Fill screen with black for GAME OVER screen
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

            # Display the "Try Again" and "Quit" buttons immediately
            try_again_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Try Again", restart_game)
            quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50, "Quit", quit_game)

            try_again_button.draw(screen, pygame.mouse.get_pos())
            quit_button.draw(screen, pygame.mouse.get_pos())
            pygame.display.flip()

            running = True
            while running:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()[0]

                if mouse_click:
                    try_again_button.is_clicked(mouse_pos, mouse_click)
                    quit_button.is_clicked(mouse_pos, mouse_click)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        running = False

    # End the game if hatching progress reaches 100%
    if hatch_rate >= 100:
        end_page(score, time_elapsed)  # Show the end page when hatching reaches 100%





# End page
def end_page(score, time_elapsed):
    screen.fill(WHITE)
    # Add "CONGRATULATIONS" text
    congrats_text = font.render("CONGRATULATIONS! You've got a chick.", True, (0, 0, 0))
    screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - 100))  # Positioned above other elements
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    time_text = font.render(f"Time: {int(time_elapsed)}s", True, (0, 0, 0))
    
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2))
    

    try_again_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Try Again", restart_game)
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50, "Quit", quit_game)

    try_again_button.draw(screen, pygame.mouse.get_pos())
    quit_button.draw(screen, pygame.mouse.get_pos())
    pygame.display.flip()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if mouse_click:
            try_again_button.is_clicked(mouse_pos, mouse_click)
            quit_button.is_clicked(mouse_pos, mouse_click)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

# Restart the game
def restart_game():
    global egg_color
    egg_color = GREEN
    color_selection_page()

# Quit the game
def quit_game():
    pygame.quit()
    quit()

# Start the game by showing the title screen
title_screen()