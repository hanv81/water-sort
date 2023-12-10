# import critical modules - random for board generation, copy for being able to restart, pygame for framework
import copy
import random
import pygame

# initialize pygame
pygame.init()

# initialize game variables
WIDTH = 500
HEIGHT = 550
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Water Sort PyGame')
font = pygame.font.Font('freesansbold.ttf', 24)
fps = 60
timer = pygame.time.Clock()
color_choices = 'red', 'darkorange2', 'deepskyblue4', 'dark blue', 'dark green', 'hotpink', 'purple', 'darkslateblue','burlywood4', 'light green', 'yellow', 'white'
tubes = []
initial_colors = []
# 10 - 14 tubes, always start with two empty
tubes = 10
new_game = True
selected = False
tube_rects = []
select_rect = 100
win = False

# select a number of tubes and pick random colors upon new game setup
def generate_start():
    tubes_number = random.randint(8, 12)
    colors = [i//4 for i in range(tubes_number*4)]
    random.shuffle(colors)

    return [colors[i*4: i*4+4] for i in range(tubes_number)] + [[], []]

# draw all tubes and colors on screen, as well as indicating what tube was selected
def draw_tubes(tubes):
    tubes_num = len(tubes)
    tube_boxes = []
    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        offset = True
    spacing = WIDTH / tubes_per_row
    for i in range(tubes_per_row):
        for j in range(len(tubes[i])):
            pygame.draw.rect(screen, color_choices[tubes[i][j]], [5 + spacing * i, 200 - (50 * j), 65, 50], 0, 3)
        box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 50, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [5 + spacing * i, 50, 65, 200], 3, 5)
        tube_boxes.append(box)
    if offset:
        for i in range(tubes_per_row - 1):
            for j in range(len(tubes[i + tubes_per_row])):
                pygame.draw.rect(screen, color_choices[tubes[i + tubes_per_row][j]],
                                 [(spacing * 0.5) + 5 + spacing * i, 450 - (50 * j), 65, 50], 0, 3)
            box = pygame.draw.rect(screen, 'blue', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 3, 5)
            tube_boxes.append(box)
    else:
        for i in range(tubes_per_row):
            for j in range(len(tubes[i + tubes_per_row])):
                pygame.draw.rect(screen, color_choices[tubes[i + tubes_per_row][j]], [5 + spacing * i,
                                                                                          450 - (50 * j), 65, 50], 0, 3)
            box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [5 + spacing * i, 300, 65, 200], 3, 5)
            tube_boxes.append(box)
    return tube_boxes


# determine the top color of the selected tube and destination tube,
# as well as how long a chain of that color to move
def calc_move(colors, selected_rect, destination):
    chain = True
    color_on_top = 100
    length = 1
    color_to_move = 100
    if len(colors[selected_rect]) > 0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1, len(colors[selected_rect])):
            if chain:
                if colors[selected_rect][-1 - i] == color_to_move:
                    length += 1
                else:
                    chain = False
    if 4 > len(colors[destination]):
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        for i in range(length):
            if len(colors[destination]) < 4:
                if len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop(-1)
    print(colors, length)
    return colors


# check if every tube with colors is 4 long and all the same color. That's how we win
def check_victory(tubes):
    def check_tube_done(tube):
        if len(tube) == 0: return True
        return False if len(tube) < 4 or any(tube[i] != tube[-1] for i in range(len(tube)-1)) else True
    
    return False if any(not check_tube_done(tube) for tube in tubes) else True

# main game loop
run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    # generate game board on new game, make a copy of the colors in case of restart
    if new_game:
        tubes = generate_start()
        initial_colors = copy.deepcopy(tubes)
        new_game = False
    # draw tubes every cycle
    else:
        tube_rects = draw_tubes(tubes)

    # event handling - Quit button exits, clicks select tubes, enter and space for restart and new board
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tubes = copy.deepcopy(initial_colors)
            elif event.key == pygame.K_RETURN:
                new_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        selected = True
                        select_rect = item
            else:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        tubes = calc_move(tubes, select_rect, dest_rect)
                        selected = False
                        select_rect = 100

    if check_victory(tubes):
        victory_text = font.render('You Won! Press Enter for a new board!', True, 'white')
        screen.blit(victory_text, (30, 265))

    restart_text = font.render('Stuck? Space-Restart, Enter-New Board!', True, 'white')
    screen.blit(restart_text, (10, 10))

    # display all drawn items on screen, exit pygame if run == False
    pygame.display.flip()

pygame.quit()