import pygame
import math
import cardgame

pygame.init()
HEIGHT = 1080
WIDTH = 1920
window = pygame.display.set_mode((1920, 1080))
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

coin = pygame.Surface((160, 160), pygame.SRCALPHA)
pygame.draw.circle(coin, (255, 255, 0), (80, 80), 80, 10)
pygame.draw.circle(coin, (128, 128, 0), (80, 80), 75)
cointext_heads = pygame.font.SysFont(None, 80).render("HEADS", True, (255, 255, 0))
cointext_tails = pygame.font.SysFont(None, 80).render("TAILS", True, (255, 255, 0))
cointext = pygame.font.SysFont(None, 80).render("10", True, (255, 255, 0))

coin.blit(cointext, cointext.get_rect(center = coin.get_rect().center))
coin_rect = coin.get_rect(center = window.get_rect().center)
angle = 0

run = True
while run:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:                                                 
                if event.key == pygame.K_ESCAPE:
                    print('Return to mainmenu!')
                    cardgame.main()  # Import the cardgame module

    window.fill(0)    
    new_width = round(math.sin(math.radians(angle)) * coin_rect.width) 
    angle += 2
    rot_coin = coin if new_width >= 0 else pygame.transform.flip(coin, True, False) 
    rot_coin = pygame.transform.scale(rot_coin, (abs(new_width), coin_rect.height))
    window.blit(rot_coin, rot_coin.get_rect(center = coin_rect.center))

    heads_counter_text = font.render(f"Heads Count: {angle // 360}", True, (255, 255, 255))
    window.blit(heads_counter_text, (50, HEIGHT - 250))
    tails_counter_text = font.render(f"Tails Count: {(angle // 360) // 2}", True, (255, 255, 255))
    window.blit(tails_counter_text, (50, HEIGHT - 100))

    mainmenu_text= font.render(f"Press ESC to return to the mainmenu", True, (255, 255, 255))
    window.blit(mainmenu_text, (50, 4))

    
    coin_flip_text= font.render(f"Coin Flip", True, (255, 255, 255))
    window.blit(coin_flip_text, (WIDTH/2, 4))

    pygame.display.flip()

pygame.quit()
exit()