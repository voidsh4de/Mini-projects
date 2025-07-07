import random, pygame

pygame.init()
screen = pygame.Surface((800, 800))
win = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
running = True
game_on = False
grid_size = 25
pygame.display.set_caption("Drunk Snake")
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x, y))

snake_length = 1
# Start with 1 segment, all others will follow it
snake_tail = [[0, 0]]
direction = [1, 0]  # right
position_history = []
drunkness = 0
shakey = 0
beer_loc = []

try: 
    beer = pygame.image.load("BEER.png")
except:
    beer = pygame.Surface((grid_size, grid_size))
pygame.display.set_icon(beer)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    win.fill("black")
    if game_on:
        if len(beer_loc) != 1:
            beer_loc.append([random.randint(0, 32), random.randint(0, 32)])
        try:
            shakey += drunkness
            shakey = shakey % (drunkness * 30)
        except:
            shakey = 0
        # Direction control
        if keys[pygame.K_DOWN]:
            direction = [0, 1]
        elif keys[pygame.K_RIGHT]:
            direction = [1, 0]
        elif keys[pygame.K_UP]:
            direction = [0, -1]
        elif keys[pygame.K_LEFT]:
            direction = [-1, 0]

        # Move head
        head = snake_tail[0][:]
        head[0] += direction[0] * grid_size
        head[1] += direction[1] * grid_size

        # Add current head to history
        position_history.insert(0, head[:])

        # Add head to front of tail
        snake_tail.insert(0, head)

        # Keep tail at desired length
        if len(snake_tail) > snake_length:
            snake_tail.pop()
        temp_bx, temp_by = beer_loc[0][0] * 25, beer_loc[0][1] * 25
        copy_snake = snake_tail[:]
        copy_snake.pop(0)
        for peice in copy_snake:
            if peice == head:
                game_on = False
        if [temp_bx, temp_by] == head:
            drunkness += 1
            snake_length += 1
            beer_loc.pop(0)

        if head[0] > 800 - grid_size or head[0] < 0:
            game_on = False
        if head[1] > 800 - grid_size or head[1] < 0:
            game_on = False
        # Draw
        screen.fill("purple")
        screen.blit(beer, (temp_bx, temp_by))
        for piece in snake_tail:
            pygame.draw.rect(screen, (0, 200, 0), (piece[0] % 800, piece[1] % 800, grid_size, grid_size))
        try:
            win.blit(pygame.transform.scale(screen, (900 - shakey, 900 - shakey)), (shakey / 2 + (random.choice(range(drunkness * 10))), shakey / 2+ (random.choice(range(drunkness * 10)))))
        except:
            win.blit(pygame.transform.scale(screen, (900, 900)), (0, 0))
        if drunkness > 5:
            win.blit(pygame.transform.scale(screen, (900 - shakey * 2, 900 - shakey * 2)), (shakey / 2 + (random.choice(range(drunkness * 30))), shakey / 2+ (random.choice(range(drunkness * 30)))))
    else:
        draw_text("press enter to start", pygame.font.SysFont("Ariel", 30), (255,255,255), 400, 30)
        if keys[pygame.K_RETURN]:
            game_on = True
            snake_length = 1
            # Start with 1 segment, all others will follow it
            snake_tail = [[0, 0]]
            direction = [1, 0]  # right
            position_history = []
            drunkness = 0
            shakey = 0
            beer_loc = []
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
