# 導入套件
import os
import sys
import pygame
import numpy as np

# 設定畫面更新速度 & 長寬 & 黑灰白三色
FPS = 10
WIDTH = 500
HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (128,128,128)
BLACK = (0, 0, 0)

# 遊戲初始化 & 創建視窗(長寬為(WIDTH, HEIGHT))
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 載入圖標 & 設定小圖標 & 更換小圖標
icon = pygame.image.load(os.path.join("Conways game.png")).convert()
mini_icon = pygame.transform.scale(icon,(25,25))
pygame.display.set_icon(icon)

# 預設為繪製狀態
edit_state = 1

# 定義細胞大小和顏色
cell_size = 10
cell_color = WHITE
dead_color = BLACK

# 定義初始地圖大小
map_width = 100
map_height = 100

# 設定視窗名稱 & 畫面刷新速度
pygame.display.set_caption("Conways game")
clock = pygame.time.Clock()

# 使用numpy定義目前地圖和下一代地圖
current_map = np.zeros((map_width, map_height), dtype=int)
next_map = np.zeros((map_width, map_height), dtype=int)

# 宣告繪製細胞函式
def draw_cell():
    global running
    if running:
        for x in range(map_width):
            for y in range(map_height):
                if current_map[x, y] == 1:
                    pygame.draw.rect(screen, cell_color, (x * cell_size, y * cell_size, cell_size, cell_size))
    else:
        pygame.quit()

# 宣告繪製地圖函式
def edit(key):
    edit=True
    mouse_down = False
    global edit_state
    global running
    if key == 'e':
        edit_state = 0
    else:
        edit_state = 1
        
    while edit:
        for event in pygame.event.get():
            #離開遊戲&結束編輯
            if event.type == pygame.QUIT:
                running = False
                print('trun off')
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('back')
                    return False
                key_char = pygame.key.name(event.key)
                if key_char == 'r':
                    print('running')
                    edit=False
                if key_char == 'w':
                    print('write')
                    edit_state = 1
                if key_char == 'e':
                    print('erase')
                    edit_state = 0
            #繪畫細胞
            a,b=pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            if mouse_down:
                if edit_state == 1:
                    if current_map[a // 10, b // 10] == 0:
                        current_map[a // 10, b // 10] = 1
                        pygame.draw.rect(screen,WHITE,pygame.Rect(a-a%10,b-b%10,10,10))
                if edit_state == 0:
                    if current_map[a // 10, b // 10] == 1:
                        current_map[a // 10, b // 10] = 0
                        pygame.draw.rect(screen,BLACK,pygame.Rect(a-a%10,b-b%10,10,10))

        draw_cell()
        pygame.display.update()

# 計算下一代細胞
def cell_renew():
    for x in range(map_width):
        for y in range(map_height):
            neighbors = np.sum(current_map[x - 1:x + 2, y - 1:y + 2]) - current_map[x, y]
            if current_map[x, y] == 1:
                # 活细胞规则
                if neighbors < 2 or neighbors > 3:
                    next_map[x, y] = 0
                else:
                    next_map[x, y] = 1
            else:
                # 死细胞规则
                if neighbors == 3:
                    next_map[x, y] = 1
                else:
                    next_map[x, y] = 0

# 預設遊戲迴圈進行
running = True
# 預設畫面為繪圖(write)狀態
if edit('w') == False :
    running = False
# 遊戲迴圈
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    # 判斷是否退出 or 進入繪圖狀態
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('trun off')
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print('trun off')
                running = False
                pygame.quit()
            key_char = pygame.key.name(event.key)
            if key_char == 'w' or key_char == 'e':
                edit(key_char)
    # 計算下一代細胞
    cell_renew()
    # 交換當前地圖和下一代地圖
    current_map = np.copy(next_map)
    # 清空下一代地圖
    next_map = np.zeros((map_width, map_height), dtype=int)                     
    # 繪製細胞
    draw_cell()                  
    # 畫面更新
    if running:
        pygame.display.update()
    else:
        pygame.quit()
        sys.exit()
pygame.quit()
sys.exit()    