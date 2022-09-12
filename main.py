import random
import pygame

# Initialized pygame module
pygame.mixer.init()
pygame.init()

# Setting the screen and font
screen_width = 800
screen_height = 600
game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game by Prathamesh Patil")
font = pygame.font.SysFont("Comic Sans", 30)

# Game specific initializations
game_over = False
exit_game = False
open_maze = False
white = (255, 255, 255)
pink = (244, 194, 194)
red = (255, 0, 0)
black = (0, 0, 0)
green = (50, 200, 50)
scoreFile = None


# Started Background music
pygame.mixer.music.load("backgroundMusic.mp3")
pygame.mixer.music.play()

# Opening High-Score file to read high score if exists, else 0 (zero) is the initial high-score
try:
    scoreFile = open("score.bin", "r")
    high_score = scoreFile.readline()
    high_score = int(high_score)
    scoreFile.close()
except FileNotFoundError:
    high_score = 0


# Function to print score on the screen
def print_screen(text,  color,  x,  y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x,y])


# Function to show Pause Resume controls
def show_pause_resume():
    f = pygame.font.SysFont("Comic sans",15)
    game_window.blit(f.render("Arrow Keys to control direction, Esc : Pause, Space: Resume", True, black), [200, 580])


# Function to draw snake on the screen
def draw_snake(game_window, color, snake_nodes_list, snake_size):
    for node in snake_nodes_list:
        pygame.draw.rect(game_window, color, [node[0], node[1], snake_size, snake_size])


# Function to show starting screen
def start_screen():
    global open_maze
    game_window.fill(black)
    print_screen("Snake Game by Prathamesh Patil", white, 160, 230)
    print_screen("Press O For Open Maze", white, 210, 270)
    print_screen("Press C For Closed Maze", white, 205, 310)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    open_maze = True
                    game_loop()
                if event.key == pygame.K_c:
                    open_maze = False
                    game_loop()



# Function containing Main Game Loop
def game_loop():
    # Initializing Variables
    global game_over
    global exit_game
    global high_score
    score = 0
    velocity_x = 0
    velocity_y = 0
    direction = ""
    speed = 8
    snake_x = 50
    snake_y = 60
    snake_size = 20
    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    food_size = 15
    fps = 30
    clock = pygame.time.Clock()

    snake_nodes_list = []
    head = [snake_x, snake_y]
    snake_nodes_list.append(head)
    snake_length = 1

    # --------------- Main Game Loop ---------------- #
    while not exit_game:
        # Checking Game Over to stop game
        if game_over:
            pygame.mixer.music.load('gameover.mp3')
            pygame.mixer.music.play()
            game_window.fill(pink)

            # Setting new high-score, if player scores more than previous high-score
            if score > high_score:
                print_screen("New High Score !!!", red, 270, 150)
                high_score = score

                # Storing the new high-score in file
                with open("score.bin", "w") as scoreFile:
                    # Writing High Score
                    scoreFile.write(str(high_score))
            print_screen("Game Over!!!", red, 300, 200)
            print_screen("Score: "+str(score), red, 310, 250)
            print_screen("Press Enter to Start New Game", red, 200, 300)
            pygame.display.update()

            # Waiting for Game Over Screen input
            while not exit_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            game_over = False
                            # Restart Background Music
                            pygame.mixer.music.load("backgroundMusic.mp3")
                            pygame.mixer.music.play()
                            game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # Actual control setup for our snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    velocity_y = -speed
                    velocity_x = 0
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    velocity_y = speed
                    velocity_x = 0
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    velocity_x = -speed
                    velocity_y = 0
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    velocity_x = speed
                    velocity_y = 0
                    direction = "RIGHT"
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    while paused:
                        for e in pygame.event.get():
                            if e.key == pygame.K_SPACE:
                                paused = False
                                break

        snake_x += velocity_x
        snake_y += velocity_y

        # Checking the food proximity with snake's head
        if abs(snake_x-food_x) < snake_size and abs(snake_y-food_y) < snake_size:
            pygame.mixer.Sound("point.mp3").play()
            score += 10
            snake_length += 2
            food_x = random.randint(20, screen_width - 20)
            food_y = random.randint(20, screen_height - 20)


        # Logic to grow the snake size
        snake_nodes_list.append([snake_x, snake_y])
        if len(snake_nodes_list) > snake_length:
            snake_nodes_list.pop(0)

        # Checking game over when snake head touches its body
        if [snake_x, snake_y] in snake_nodes_list[:-1]:
            game_over = True

        # Checking Boundary Game over
        if open_maze:
            if snake_x > screen_width-5:
                snake_x = 0
            elif snake_x < 0:
                snake_x = screen_width
            elif snake_y > screen_height:
                snake_y = 0
            elif snake_y < 0:
                snake_y = screen_height
        else:
            if snake_x > screen_width or snake_y > screen_height or snake_x < 0 or snake_y < 0:
                game_over = True

        game_window.fill(pink)     # setting background pink
        print_screen("Score: " + str(score), black, 10, 10)      # Printing Score
        print_screen("High Score: " + str(high_score), black, 450, 10)  # Printing Score
        pygame.draw.rect(game_window, red, [food_x, food_y, food_size, food_size])  # Drawing food
        draw_snake(game_window, green,  snake_nodes_list, snake_size)   # Drawing Snake Body
        show_pause_resume()     # Showing Pause Resume controls
        pygame.display.update()
        clock.tick(fps)     # setting frame rate

# Starting Screen
start_screen()
pygame.quit()
quit()
