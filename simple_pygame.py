import sys, pygame, random

pygame.init()

WIDTH = 800
HEIGHT = 600

player_colour = (255,0,0)
enemy_colour =  (0,0,255)
BACKGROUND_COLOUR = (0,0,0)
FONT_COLOUR =  (255,25,0)

player_size = 50
player_position = [WIDTH/2, HEIGHT-2*player_size]

enemy_size = 25
enemy_position = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_position]

speed =  10
score = 0

screen = pygame.display.set_mode((WIDTH,HEIGHT))

game_over = False
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, speed):
    if (score % 20 == 0) and (score>=20):
        speed += 0.5
    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        pygame.draw.rect(screen, enemy_colour, (enemy[0], enemy[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for i, enemy in enumerate(enemy_list):
        if enemy[1] >=0 and enemy[1] < HEIGHT:
            enemy[1] += speed

        else:
            enemy_list.pop(i)
            score += 1
    return score

def collision_check(enemy_list, player_position):
    for enemy in enemy_list:
        if detect_collision(enemy, player_position):
            return True
    return False

# Detect collisions
def detect_collision(player_position, enemy_position):
    p_x = player_position[0]
    p_y = player_position[1]

    e_x = enemy_position[0]
    e_y = enemy_position[1]

    if ((e_x >= p_x) and (e_x < p_x+player_size)) or ((p_x >= e_x) and (p_x < e_x+enemy_size)):
        if ((e_y >= p_y) and (e_y < p_y+player_size)) or ((p_y >= e_y) and (p_y < e_y+enemy_size)):
            return True
    return False

while not game_over:

    # event log
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_position[0]
            y = player_position[1]
            
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size
            
            player_position = [x,y]
    
    screen.fill(BACKGROUND_COLOUR)

    if detect_collision(player_position, enemy_position):
            game_over = True
            break

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    text = "Score: " + str(score)
    label = myFont.render(text, 1, FONT_COLOUR)
    screen.blit(label, (WIDTH-200, HEIGHT-40))
    
    speed = set_level(score, speed)

    if collision_check(enemy_list, player_position):
        game_over = True
    draw_enemies(enemy_list)
    
    pygame.draw.rect(screen, player_colour, (player_position[0], player_position[1], player_size, player_size)) # Rect(left top width height)
    

    clock.tick(30) #fps

    

    pygame.display.update()