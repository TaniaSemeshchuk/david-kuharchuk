import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 720, 600
fps = 60

# paddle settings
paddle_w = 200
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# ball settings
ball_radius = 20
ball_speed = 4
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# blocks settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(6) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(6) for j in range(4)]

# Initialize pygame
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background image and scale to full screen
img = pygame.image.load('1.jpg').convert()
img = pygame.transform.scale(img, (WIDTH, HEIGHT))  # Scale image to fit the screen

# Set up font for game over message
font = pygame.font.SysFont('Arial', 72)

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

# Function to display "Game Over" message
def show_game_over():
    game_over_text = font.render('КІНЕЦЬ ГРИ', True, (255, 0, 0))
    sc.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait 3 seconds before closing the game
    exit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Draw background
    sc.blit(img, (0, 0))  # Blit the scaled background image onto the screen

    # Draw blocks, paddle, and ball
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # Move ball
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # Collision with left and right walls
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx

    # Collision with top wall
    if ball.centery < ball_radius:
        dy = -dy

    # Collision with paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    # Collision with blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        
        # Special effect on block hit
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2

    # Check if the ball is below the paddle (Game Over)
    if ball.bottom > HEIGHT:
        show_game_over()

    # Win condition if no blocks remain
    elif not len(block_list):
        print('WIN!!!')
        exit()

    # Paddle movement
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # Update display
    pygame.display.flip()
    clock.tick(fps)
