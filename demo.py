import pygame
import sys

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("音量控制")

# 初始化mixer模块
pygame.mixer.init()

# 载入音乐文件
bgm = pygame.mixer.music.load('./assets/Zoltraak - Evan Call.mp3')  # 替换为你的音乐文件路径

pygame.mixer.music.play(-1)  # -1 表示无限循环

# 设置初始音量（0.5 表示50%的音量）
volume = 0.5
pygame.mixer.music.set_volume(volume)

# 定义音量条的属性
volume_bar_x = 50
volume_bar_y = 50
volume_bar_width = 200
volume_bar_height = 20
volume_bar_color = (0, 0, 0)  # 音量条的颜色
volume_bar_fill_color = (255, 0, 0)  # 音量条填充的颜色

# 定义音量条的当前位置
volume_bar_pos = int(volume_bar_width * volume)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标点击是否在音量条上
            if volume_bar_x <= event.pos[0] <= volume_bar_x + volume_bar_width and volume_bar_y <= event.pos[1] <= volume_bar_y + volume_bar_height:
                # 计算新的音量值
                new_volume = (event.pos[0] - volume_bar_x) / volume_bar_width
                pygame.mixer.music.set_volume(new_volume)
                volume = new_volume
                volume_bar_pos = int(volume_bar_width * volume)

    screen.fill((255, 255, 255))  # 填充背景色

    # 绘制音量条
    pygame.draw.rect(screen, volume_bar_color, (volume_bar_x, volume_bar_y, volume_bar_width, volume_bar_height))
    pygame.draw.rect(screen, volume_bar_fill_color, (volume_bar_x, volume_bar_y, volume_bar_pos, volume_bar_height))

    # 更新屏幕显示
    pygame.display.flip()

    # 控制游戏刷新速度
    pygame.time.Clock().tick(30)

# 退出pygame
pygame.quit()
sys.exit()