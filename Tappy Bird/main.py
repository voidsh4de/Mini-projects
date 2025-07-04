import random
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True
high_score = 0
font = pygame.font.SysFont("ariel", 40, True)
pygame.display.set_caption("Tappy bird")
game_on = False
score = 0
pipe_count = 0

#key change info
Key_Options = [[pygame.K_a, "a"], [pygame.K_s, "s"], [pygame.K_k, "k"], [pygame.K_l, "l"], [pygame.K_SPACE, "space"]]
current_key = Key_Options[-1]
def change_key(Key_Options, current_key):
    new_keys = [k for k in Key_Options if k[0] != current_key[0]]
    return random.choice(new_keys)


try:
    with open("GAME.save") as save_file:
        high_score = high_score + int(save_file.read())
except:
    with open("GAME.save", "w") as save_file:
        save_file.write("0")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def MakeButton(x, y, width, height, text, color, hover_color, font_size = 50):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            #click_sfx.play()
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, pygame.font.SysFont("Special Gothic", font_size), (255, 255, 255), x + (width // 2) - (font.size(text)[0] // 2), y + (height // 2) - (font.size(text)[1] // 2))
    return False

class Player():
    def __init__(self, x, y, fall_rate, size, colour):
        self.x = x
        self.y = y
        self.fall_rate = fall_rate
        self.width, self.height = size[0], size[1]
        self.colour = colour
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
    def fall(self):
        self.y += self.fall_rate
    def jump(self):
        self.y -= (self.fall_rate * 2) + 100
    def Load_img(self):
        try:
            self.img = pygame.transform.scale(pygame.image.load("BIRD.png"), (self.width, self.height))
        except:
            self.img = pygame.Surface((self.width, self.height))
            self.img.fill(self.colour)
    

class pipe():
    def __init__(self, x, y, gap=200):
        self.x = x
        self.y = y
        self.width = 40
        self.gap = gap
        self.colour = (0, 255, 0)
        self.update_rects()
    
    def update_rects(self):
        self.top = (self.x, 0, self.width, self.y)
        self.bot = (self.x, self.y + self.gap, self.width, 800 - (self.y + self.gap))
    
    def draw(self):
        self.update_rects()
        pygame.draw.rect(screen, self.colour, self.top)
        pygame.draw.rect(screen, self.colour, self.bot)

pipes = [pipe(800, 300)]

bird = Player(30, 400, 2, (50, 50), (0,0,0))
bird.Load_img()

def new_pipe(): 
    piper = pipe(800, random.randint(200, 600))
    pipes.append(piper)

def move_pipes(speed, item, pipe_count=pipe_count):
    global score, running   
    adjust = 0          
    for pipe in range(len(item)):
        if item[pipe - adjust].x < -40:
            item.pop(pipe)
            score += 1
            adjust += 1
            
        item[pipe - adjust].x -= speed
        item[pipe - adjust ].draw()
    if any(pygame.Rect(bird.x, bird.y, bird.width, bird.height).colliderect(pipea.top) for pipea in pipes) or any(pygame.Rect(bird.x, bird.y, bird.width, bird.height).colliderect(pipea.bot) for pipea in pipes):
        running = False



    if pipe_count % 100 == 0:
        new_pipe()

def jump_manage(keys, current_key, Key_Options, bird):
    if keys[current_key[0]]:
        temp_list = [k for k in Key_Options if k[0] != current_key[0]]
        if not any(keys[k[0]] for k in temp_list):
            bird.jump()
            current_key = change_key(Key_Options, current_key)
    return current_key

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys =  pygame.key.get_pressed()

    screen.fill("lightblue")

    # RENDER YOUR GAME HERE
    bird.draw()
    if game_on == False:
        draw_text("Press ENTER to start", font, (255, 255, 255), 20, 400)
        draw_text("HighScore = " + str(high_score), font, (255,255,255), 0, 0)
        if keys[pygame.K_RETURN]:
            game_on = True
    else:
        pipe_count += 1
        bird.fall()
        bird.fall_rate = (score / 3) + 1      
        current_key = jump_manage(keys, current_key, Key_Options, bird)

        if bird.y < 0 or bird.y > 800 - bird.height:
            running = False
        move_pipes(4, pipes, pipe_count)
        draw_text("Score = " + str(score), font, (255,255,255), 0, 0)
        draw_text(str(current_key[1]), font, (0,0,0), 0, 800 - 40)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

if score > high_score:
    with open("GAME.save", "w") as save_file:
        save_file.write(str(score))
pygame.quit()