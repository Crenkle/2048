import pygame
import random

ANIMATION_SPEED = 18    # How many ticks it takes for a slide animation to complete

class AnimatingTile:
    def __init__(self, x_animate_pos, y_animate_pos, x_target_pos, y_target_pos, value):
        # animate_pos begins as initial location of tile, but updates to the current
        # position during animation
        self.x_animate_pos = x_animate_pos
        self.y_animate_pos = y_animate_pos
        
        # target_pos is the destination of the tile during animation
        self.x_target_pos = x_target_pos
        self.y_target_pos = y_target_pos

        self.value = value

#region Drawing/Animating Functions

def init_board(ttt):
    # Set up the background surface
    background = pygame.Surface(ttt.get_size())
    background = background.convert()

    return background

def show_board(ttt, board):   
    global animating, animate_tiles

    board.fill((195, 245, 255))

    # Draw the grid lines
    for x in range(5):
        pygame.draw.line(board, (128, 128, 128), (4 + 109 * x, 0), (4 + 109 * x, 445), 9)
        pygame.draw.line(board, (128, 128, 128), (0, 4 + 109 * x), (445, 4 + 109 * x), 9)
    
    if (animating > 0):
        for tile in animate_tiles: 
            if (tile.value > 0):
                x_pos = 9 + (109 * tile.x_animate_pos)
                y_pos = 9 + (109 * tile.y_animate_pos)
                pygame.draw.rect(board, get_tile_colour(tile.value), (x_pos, y_pos, 100, 100), 0)
                text = font.render(str(tile.value), 1, (10, 10, 10))
                rect = text.get_rect()
                board.blit(text, (x_pos + 50 - (rect.width / 2), y_pos + 50 - (rect.height / 2)))
    else:
        for x in range (4):
            for y in range (4):
                tile_value = tile_grid[x][y]
                if (tile_value > 0):
                    x_pos = 9 + (109 * x)
                    y_pos = 9 + (109 * y)
                    pygame.draw.rect(board, get_tile_colour(tile_value), (y_pos, x_pos, 100, 100), 0)
                    text = font.render(str(tile_value), 1, (10, 10, 10))
                    rect = text.get_rect()
                    board.blit(text, (y_pos + 50 - (rect.width / 2), x_pos + 50 - (rect.height / 2)))

    if (fail):
        text = fail_font.render("FAIL", 1, (255, 0, 0))
        rect = text.get_rect()
        board.blit(text, (222 - (rect.width / 2), 222 - (rect.height / 2)))

    ttt.blit(board, (0, 0))
    pygame.display.flip()

def get_tile_colour(value):
    return {
        2:      (160, 224, 255),
        4:      (150, 210, 255),
        8:      (140, 196, 255),
        16:     (130, 182, 255),
        32:     (120, 168, 255),
        64:     (110, 154, 255),
        128:    (100, 140, 255),
        256:    (90,  126, 255),
        512:    (80,  112, 255),
        1024:   (70,  98,  255),
        2048:   (60,  84,  255),
        4096:   (50,  70,  255),
        8092:   (40,  56,  255),
        16184:  (30,  42,  255),
        32368:  (20,  28,  255),
        64736:  (10,  14,  255),
        129472: (0,   0,   255),
    }[value]

#endregion

#region Business Functions

def place_tile():
    global blank_tile_count

    placeNewTile = random.randrange(blank_tile_count)	# When placeNewTile == 0 place tile and exit
    for x in range(4):
        for y in range(4):
            if (tile_grid[x][y] == 0):
                if (placeNewTile == 0):
                    if (random.randrange(10) == 9):	# 10% chance of new tile having 4 value instead of 2
                        tile_grid[x][y] = 4
                    else:
                        tile_grid[x][y] = 2
                    blank_tile_count = blank_tile_count - 1 # Placing tile means 1 more tile is unavailable
                    return
                else:
                    placeNewTile = placeNewTile - 1
    return
                
def move_function(direction):
    global animate_tiles

    if (direction == pygame.K_w):
        is_x_diff = False
        start = 0
    elif (direction == pygame.K_d):
        is_x_diff = True
        start = -3
    elif (direction == pygame.K_s):
        is_x_diff = False
        start = -3
    elif (direction == pygame.K_a):
        is_x_diff = True
        start = 0
    else:
        return

    for i in range(4):
        values = [None] * 4
        for j in range(4):
            if (is_x_diff):
                values[j] = tile_grid[abs(start + i)][abs(start + j)]
            else:
                values[j] = tile_grid[abs(start + j)][abs(start + i)]
        
        animate_row = calculate_row(values)

        for j in range(4):
            if (is_x_diff):
                tile_grid[abs(start + i)][abs(start + j)] = values[j]
                if (animate_row[j].value > 0):
                    animate_tile = animate_row[j]
                    diff = animate_tile.x_target_pos - j

                    animate_tile.x_animate_pos = abs(start + j)
                    animate_tile.y_animate_pos = abs(start + i)
                    
                    animate_tile.x_target_pos = abs(start + j + diff)
                    animate_tile.y_target_pos = abs(start + i)

                    animate_tiles.append(animate_tile)
            else:
                tile_grid[abs(start + j)][abs(start + i)] = values[j]
                if (animate_row[j].value > 0):
                    animate_tile = animate_row[j]
                    diff = animate_tile.x_target_pos - j

                    animate_tile.x_animate_pos = abs(start + i)
                    animate_tile.y_animate_pos = abs(start + j)
                    
                    animate_tile.x_target_pos = abs(start + i)
                    animate_tile.y_target_pos = abs(start + j + diff)

                    animate_tiles.append(animate_tile)

# Accepts a row of tiles of length 4 and attempts to shift all tiles left
def calculate_row(tiles):
    global blank_tile_count, moved_tiles
    
    available_pos = 0   # Position tile will be moved to if available. Prevents double merge 
                        # cases e.g. [2, 2, 4, 0] => [8, 0, 0, 0], should become [4, 4, 0, 0]

    # Only x_animate_pos and value fields are given values in calculate_row()
    # animate_pos/target_pos fields are properly calculated in move_function()
    animate_row = [AnimatingTile(0, 0, 0, 0, 0) for x in range(w)]

    if (tiles[0] > 0):
        animate_row[0].x_animate_pos, animate_row[0].x_target_pos, animate_row[0].value = 0, 0, tiles[0]

    for x in range(1, 4):
        value = tiles[x]
        if (value == 0):
            continue    # Skip empty tiles

        if (tiles[available_pos] == 0):
            tiles[available_pos] = value
            tiles[x] = 0

            animate_row[x].x_animate_pos, animate_row[x].x_target_pos, animate_row[x].value = x, available_pos, value
            moved_tiles = True
        elif (tiles[available_pos] == value):
            tiles[available_pos] *= 2   # Merge tiles
            tiles[x] = 0
            blank_tile_count += 1       # Merging tiles means 1 more tile is available

            animate_row[x].x_animate_pos, animate_row[x].x_target_pos, animate_row[x].value = x, available_pos, value
            available_pos += 1
            moved_tiles = True
        else:
            available_pos += 1
            if (available_pos != x):    # Shifted tile is not eligible for merge but does need to be moved
                tiles[available_pos] = value
                tiles[x] = 0
                moved_tiles = True
            # else tile is already in the correct spot
            animate_row[x].x_animate_pos, animate_row[x].x_target_pos, animate_row[x].value = x, available_pos, value
        
    return animate_row

# Check for adjacent tiles that are equal in value, thus permitting a move in that direction
# Tiles equal in value but multiple spaces apart don't need to be checked for since all grid spaces are filled, 
# meaning that there would be a tile with a different value in between them, making the move invalid
def check_loss():
    for x in range(3):
        for y in range(4):
            if (tile_grid[x][y] == tile_grid[x + 1][y] or tile_grid[y][x] == tile_grid[y][x + 1]):
                return 0
    return 1

#endregion

#region Initilisation

pygame.init()
ttt = pygame.display.set_mode((445, 445))
pygame.display.set_caption('2048')
font = pygame.font.Font('ClearSans-Bold.ttf', 30)
fail_font = pygame.font.Font('ClearSans-Bold.ttf', 60)
clock = pygame.time.Clock()

w, h = 4, 4
tile_grid = [[0 for x in range(w)] for y in range(h)] 

blank_tile_count = 16

# Place the first two tiles
place_tile()
place_tile()

# Create the game board
board = init_board(ttt)

#endregion

#region Main Event Loop

running = 1
fail = False
animating = 0
animate_tiles = []
moved_tiles = False

# Temporary Unit Tests
# test1 = calculate_row([0, 0, 0, 0])
# test2 = calculate_row([2, 0, 2, 0])
# test3 = calculate_row([2, 4, 0, 2])
# test4 = calculate_row([2, 4, 2, 0])
# test5 = calculate_row([2, 2, 4, 0])
# test6 = calculate_row([2, 2, 4, 4])

while (running == 1):
    if (animating == 0):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = 0
                pygame.event.clear()
                break   # Only accept first valid key input
            elif (event.type == pygame.KEYDOWN and event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d) and fail == False):
                animate_tiles = []
                move_function(event.key)
                if (blank_tile_count > 0 and moved_tiles == True):
                    place_tile()
                else:
                    if (check_loss()):
                        fail = True
                moved_tiles = False
                animating = ANIMATION_SPEED - 1
                pygame.event.clear()
                break   # Only accept first valid key input
    else:   # else disable user input until animation completes
        for tile in animate_tiles:
            if (tile.x_animate_pos != tile.x_target_pos):
                diff = tile.x_animate_pos - tile.x_target_pos
                diff /= ((animating + 1) / ANIMATION_SPEED)
                diff *= (animating / ANIMATION_SPEED)
                tile.x_animate_pos = tile.x_target_pos + diff
                if (abs(diff) < 0.001):     # Ensures floating point number arithmetic doesn't cause equality comparison failures in tiles that should be still
                    tile.x_animate_pos = tile.x_target_pos
            elif (tile.y_animate_pos != tile.y_target_pos):
                diff = tile.y_animate_pos - tile.y_target_pos
                diff /= ((animating + 1) / ANIMATION_SPEED)
                diff *= (animating / ANIMATION_SPEED)
                tile.y_animate_pos = tile.y_target_pos + diff
                if (abs(diff) < 0.001):     # See above comment
                    tile.y_animate_pos = tile.y_target_pos

        animating -= 1
        if (animating == 0):
            pygame.event.clear()
            pygame.event.clear()

    # Update the display
    show_board(ttt, board)
    clock.tick(60)  # Game runs at 60 ticks/s. Animation speed is tied to tick rate

#endregion
