import pygame
import random
import string

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alphabet Catcher")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game variables
letters = []
score = 0
missed = 0
speed = 1
font = pygame.font.Font(None, 36)

class Letter:
    def __init__(self, char):
        self.char = char
        self.x = random.randint(0, WIDTH - 30)
        self.y = 0

    def move(self):
        self.y += speed

    def draw(self):
        text = font.render(self.char, True, BLACK)
        screen.blit(text, (self.x, self.y))

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

def game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over!", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 100))
    
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(final_score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
    
    draw_button("Restart", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GREEN)
    draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50, RED)
    
    pygame.display.flip()

def reset_game():
    global letters, score, missed, speed
    letters = []
    score = 0
    missed = 0
    speed = 1

clock = pygame.time.Clock()
spawn_timer = 0

running = True
game_active = True

while running:
    if game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()
                for letter in letters[:]:
                    if key == letter.char:
                        letters.remove(letter)
                        score += 1
                        break
                else:
                    score = max(0, score - 1)

        spawn_timer += clock.get_time()
        if spawn_timer > 1000:
            if score >= 15:
                letters.extend([Letter(random.choice(string.ascii_uppercase)) for _ in range(2)])
            else:
                letters.append(Letter(random.choice(string.ascii_uppercase)))
            spawn_timer = 0

        screen.fill(WHITE)

        for letter in letters[:]:
            letter.move()
            letter.draw()
            if letter.y > HEIGHT:
                letters.remove(letter)
                missed += 1

        score_text = font.render(f"Score: {score}", True, BLACK)
        missed_text = font.render(f"Missed: {missed}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(missed_text, (10, 50))

        if missed >= 5:
            game_active = False

        pygame.display.flip()
        clock.tick(60)

        speed = 1 + score // 10

    else:
        game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 < mouse_pos[0] < WIDTH // 2 + 100:
                    if HEIGHT // 2 + 50 < mouse_pos[1] < HEIGHT // 2 + 100:
                        reset_game()
                        game_active = True
                    elif HEIGHT // 2 + 120 < mouse_pos[1] < HEIGHT // 2 + 170:
                        running = False

pygame.quit()