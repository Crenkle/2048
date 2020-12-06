import pygame
import random

#region Drawing/Animating Functions

def init_board(ttt):
    # Set up the background surface
    background = pygame.Surface(ttt.get_size())
    background = background.convert()

    return background

def show_board(ttt, board):   
    board.fill((205,193,180))

    # Draw the grid lines
    for x in range(5):
        pygame.draw.line (board, (187,173,160), (4 + 109 * x, 0),(4 + 109 * x, 445), 9)
        pygame.draw.line (board, (187,173,160), (0, 4 + 109 * x),(445, 4 + 109 * x), 9)
    
    for x in range (4):
        for y in range (4):
            tile_value = tile_grid[x][y]
            if (tile_value > 0):
                x_pos = 9 + (109 * x)
                y_pos = 9 + (109 * y)
                pygame.draw.rect(board, (255, 255, 255), (x_pos, y_pos, 100, 100), 0)
                text = font.render(str(tile_value), 1, (10, 10, 10))
                rect = text.get_rect()
                board.blit(text, (x_pos + 50 - (rect.width / 2), y_pos + 50 - (rect.height / 2)))

    if (fail):
        text = fail_font.render("FAIL", 1, (255, 0, 0))
        rect = text.get_rect()
        board.blit(text, (222 - (rect.width / 2), 222 - (rect.height / 2)))

    ttt.blit(board, (0, 0))
    pygame.display.flip()

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
    if (direction == pygame.K_w):
        for x in range(4):
            values = [None] * 4
            values[0] = tile_grid[x][0]
            values[1] = tile_grid[x][1]
            values[2] = tile_grid[x][2]
            values[3] = tile_grid[x][3]
            calculate_row(values)
            tile_grid[x][0] = values[0]
            tile_grid[x][1] = values[1]
            tile_grid[x][2] = values[2]
            tile_grid[x][3] = values[3]
    elif (direction == pygame.K_d):
        for x in range(4):
            values = [None] * 4
            values[0] = tile_grid[3][x]
            values[1] = tile_grid[2][x]
            values[2] = tile_grid[1][x]
            values[3] = tile_grid[0][x]
            calculate_row(values)
            tile_grid[3][x] = values[0]
            tile_grid[2][x] = values[1]
            tile_grid[1][x] = values[2]
            tile_grid[0][x] = values[3]
    elif (direction == pygame.K_s):
        for x in range(4):
            values = [None] * 4
            values[0] = tile_grid[x][3]
            values[1] = tile_grid[x][2]
            values[2] = tile_grid[x][1]
            values[3] = tile_grid[x][0]
            calculate_row(values)
            tile_grid[x][3] = values[0]
            tile_grid[x][2] = values[1]
            tile_grid[x][1] = values[2]
            tile_grid[x][0] = values[3]
    elif (direction == pygame.K_a):
        for x in range(4):
            values = [None] * 4
            values[0] = tile_grid[0][x]
            values[1] = tile_grid[1][x]
            values[2] = tile_grid[2][x]
            values[3] = tile_grid[3][x]
            calculate_row(values)
            tile_grid[0][x] = values[0]
            tile_grid[1][x] = values[1]
            tile_grid[2][x] = values[2]
            tile_grid[3][x] = values[3]

# Accepts a row of tiles of length 4 and attempts to shift all tiles left
def calculate_row(tiles):
    global blank_tile_count
    
    available_pos = 0   # Position tile will be moved to if available. Prevents double merge 
                        # cases e.g. [2, 2, 4, 0] -> [8, 0, 0, 0], should become [4, 4, 0, 0]

    for x in range(1, 4):
        value = tiles[x]
        if (value == 0):
            continue    # Skip empty tiles

        if (tiles[available_pos] == 0):
            tiles[available_pos] = value
            tiles[x] = 0
        elif (tiles[available_pos] == value):
            tiles[available_pos] *= 2   # Merge tiles
            available_pos += 1
            blank_tile_count += 1   # Merging tiles means 1 more tile is available
            tiles[x] = 0
        else:   # Shifted tile is not eligible for merge but does need to be moved
            available_pos += 1
            if (available_pos != x):
                tiles[available_pos] = value
                tiles[x] = 0
            # else tile is already in the correct spot
        
    return tiles

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

# Temporary Unit Tests
# test1 = calculate_row([0, 0, 0, 0])
# test2 = calculate_row([2, 0, 2, 0])
# test3 = calculate_row([2, 4, 0, 2])
# test4 = calculate_row([2, 4, 2, 0])
# test5 = calculate_row([2, 2, 4, 0])
# test6 = calculate_row([2, 2, 4, 4])

while (running == 1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        elif (event.type == pygame.KEYDOWN and fail == False):
            move_function(event.key)
            if (blank_tile_count > 0):
                place_tile()
            else:
                if (check_loss()):
                    fail = True

        # update the display
        show_board(ttt, board)

#endregion
