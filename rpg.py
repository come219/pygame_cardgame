import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1920,1080 # 1080, 720
TILE_SIZE = 32
PLAYER_SPEED = 5
CAMERA_LERP = 0.08

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- COLORS ---
COLORS = {
    0: (50, 200, 50),    # grass
    1: (20, 120, 20),    # forest
    2: (40, 80, 200),    # water
    3: (210, 200, 120),  # sand
    4: (130, 130, 130),  # mountain
    5: (255, 80, 0)      # lava
}

# --- LOAD MAP ---
def load_map(file):
    with open(file) as f:
        return [list(map(int, line.split())) for line in f]

game_map = load_map("map.txt")

MAP_W = len(game_map[0])
MAP_H = len(game_map)

# --- PLAYER ---
player = pygame.Rect(2500, 2500, 20, 20)

camera_x = 0
camera_y = 0

# --- MINIMAP ---
MINIMAP_SIZE = 200
minimap_scale_x = MINIMAP_SIZE / MAP_W
minimap_scale_y = MINIMAP_SIZE / MAP_H

def draw_minimap():
    minimap = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))

    for y in range(MAP_H):
        for x in range(MAP_W):
            color = COLORS[game_map[y][x]]
            px = int(x * minimap_scale_x)
            py = int(y * minimap_scale_y)
            minimap.set_at((px, py), color)

    # draw player on minimap
    px = int((player.x / TILE_SIZE) * minimap_scale_x)
    py = int((player.y / TILE_SIZE) * minimap_scale_y)
    pygame.draw.circle(minimap, (255, 0, 0), (px, py), 3)

    screen.blit(minimap, (WIDTH - MINIMAP_SIZE - 10, 10))


running = True
while running:
    dt = clock.tick(60)

    # --- INPUT ---
    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
    dy = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED

    player.x += dx
    player.y += dy

    # --- CAMERA ---
    target_x = player.centerx - WIDTH // 2
    target_y = player.centery - HEIGHT // 2

    camera_x += (target_x - camera_x) * CAMERA_LERP
    camera_y += (target_y - camera_y) * CAMERA_LERP

    screen.fill((0, 0, 0))

    # --- DRAW ONLY VISIBLE TILES ---
    start_x = int(camera_x // TILE_SIZE)
    start_y = int(camera_y // TILE_SIZE)

    end_x = start_x + (WIDTH // TILE_SIZE) + 2
    end_y = start_y + (HEIGHT // TILE_SIZE) + 2

    for y in range(start_y, min(end_y, MAP_H)):
        for x in range(start_x, min(end_x, MAP_W)):
            tile = game_map[y][x]

            rect = pygame.Rect(
                x * TILE_SIZE - camera_x,
                y * TILE_SIZE - camera_y,
                TILE_SIZE,
                TILE_SIZE
            )

            pygame.draw.rect(screen, COLORS[tile], rect)

    # --- PLAYER ---
    pygame.draw.rect(
        screen,
        (255, 50, 50),
        (player.x - camera_x, player.y - camera_y, 20, 20)
    )

    # --- MINIMAP ---
    draw_minimap()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                import cardgame
                cardgame.main()

        if event.type == pygame.QUIT:
            running = False
            

pygame.quit()
sys.exit()