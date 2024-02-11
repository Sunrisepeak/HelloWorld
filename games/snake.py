import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('双人贪吃蛇')

# 设置颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 设置帧率
FPS = 4
fps_change = 0
clock = pygame.time.Clock()

# 蛇和食物设置
SNAKE_SIZE = 20
FOOD_SIZE = 20
SNAKE_SPEED = 20

# 初始化玩家位置和方向
player1_pos = [[SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2]]
player2_pos = [[SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2]]
player1_direction = 'RIGHT'
player2_direction = 'LEFT'

# 初始化食物位置
# 初始化食物位置
food_positions = [[random.randrange(1, (SCREEN_WIDTH//FOOD_SIZE)) * FOOD_SIZE,
                   random.randrange(1, (SCREEN_HEIGHT//FOOD_SIZE)) * FOOD_SIZE] for _ in range(4)]
food_spawn = [True] * 4

# 游戏结束函数
def check_game_over(player_pos):
    if (player_pos[0][0] >= SCREEN_WIDTH or player_pos[0][0] < 0 or
        player_pos[0][1] >= SCREEN_HEIGHT or player_pos[0][1] < 0):
        return True
    for block in player_pos[1:]:
        if player_pos[0] == block:
            return True
    return False

# 检查玩家是否碰撞
def check_collision(pos1, pos2):
    for p1_body in pos1:
        if p1_body in pos2:
            return True
    return False

# 显示胜利玩家
def display_winner(winner):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Player {winner} wins!', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    pygame.display.flip()
    # 等待一段时间
    pygame.time.wait(2000)

# 更新蛇的位置
def update_snake(player_pos, player_direction):
    if player_direction == 'UP':
        new_head = [player_pos[0][0], player_pos[0][1] - SNAKE_SPEED]
        if new_head[1] < 0:
            new_head[1] = SCREEN_HEIGHT - SNAKE_SIZE
    elif player_direction == 'DOWN':
        new_head = [player_pos[0][0], player_pos[0][1] + SNAKE_SPEED]
        if new_head[1] >= SCREEN_HEIGHT:
            new_head[1] = 0
    elif player_direction == 'LEFT':
        new_head = [player_pos[0][0] - SNAKE_SPEED, player_pos[0][1]]
        if new_head[0] < 0:
            new_head[0] = SCREEN_WIDTH - SNAKE_SIZE
    elif player_direction == 'RIGHT':
        new_head = [player_pos[0][0] + SNAKE_SPEED, player_pos[0][1]]
        if new_head[0] >= SCREEN_WIDTH:
            new_head[0] = 0
    player_pos.insert(0, new_head)

# 重新开始游戏
def restart_game():
    global player1_pos, player2_pos, player1_direction, player2_direction, food_position, food_spawn
    player1_pos = [[SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2]]
    player2_pos = [[SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2]]
    player1_direction = 'RIGHT'
    player2_direction = 'LEFT'
    food_position = [random.randrange(1, (SCREEN_WIDTH//FOOD_SIZE)) * FOOD_SIZE,
                     random.randrange(1, (SCREEN_HEIGHT//FOOD_SIZE)) * FOOD_SIZE]
    food_spawn = True

# 主游戏循环
running = True
food_color = RED
winner = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            fps_change += 0.05
            if event.key == pygame.K_w and player1_direction != 'DOWN':
                player1_direction = 'UP'
            if event.key == pygame.K_s and player1_direction != 'UP':
                player1_direction = 'DOWN'
            if event.key == pygame.K_a and player1_direction != 'RIGHT':
                player1_direction = 'LEFT'
            if event.key == pygame.K_d and player1_direction != 'LEFT':
                player1_direction = 'RIGHT'
            if event.key == pygame.K_UP and player2_direction != 'DOWN':
                player2_direction = 'UP'
            if event.key == pygame.K_DOWN and player2_direction != 'UP':
                player2_direction = 'DOWN'
            if event.key == pygame.K_LEFT and player2_direction != 'RIGHT':
                player2_direction = 'LEFT'
            if event.key == pygame.K_RIGHT and player2_direction != 'LEFT':
                player2_direction = 'RIGHT'

    # 更新蛇的位置
    update_snake(player1_pos, player1_direction)
    update_snake(player2_pos, player2_direction)

    # 检查是否吃到食物
    for i, food_position in enumerate(food_positions):
        if player1_pos[0] == food_position:
            food_spawn[i] = False
        if player2_pos[0] == food_position:
            food_spawn[i] = False

    # 如果食物被吃掉，重新生成食物
    for fspawn in food_spawn:
        if not fspawn:
            food_position = [random.randrange(1, (SCREEN_WIDTH//FOOD_SIZE)) * FOOD_SIZE,
                            random.randrange(1, (SCREEN_HEIGHT//FOOD_SIZE)) * FOOD_SIZE]
            fspawn = True

    # 检查两个玩家是否碰撞
    if check_collision(player1_pos, player2_pos) and False:
        running = False
        winner = 'Player 2' if check_game_over(player1_pos) else 'Player 1'
        display_winner(winner)

    # 填充背景
    screen.fill(BLACK)

    # 画出食物
    if food_color == RED:
        food_color = WHITE
    else:
        food_color = RED
    for food_position in food_positions:
        pygame.draw.rect(screen, food_color, pygame.Rect(food_position[0], food_position[1], FOOD_SIZE, FOOD_SIZE))

    # 画出蛇
    for pos in player1_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

    for pos in player2_pos:
        pygame.draw.rect(screen, BLUE, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

    # 刷新屏幕
    pygame.display.flip()

    # 控制游戏刷新速度
    clock.tick(FPS + fps_change)

# 显示重新开始的按钮
font = pygame.font.Font(None, 36)
text = font.render('Press R to Restart', True, WHITE)
text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
screen.blit(text, text_rect)
pygame.display.flip()

# 等待玩家重新开始或退出游戏
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                waiting = False
                restart_game()
                running = True

# 结束游戏
pygame.quit()
sys.exit()