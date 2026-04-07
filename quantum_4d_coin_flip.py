import pygame
import math
import cardgame
import random

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
roll_value = 360
roll_result = 'None'

def roll_coin_flip():
    global roll_value
    global roll_result
    roll_value = random.randint(0, 360)

    # HEADS/TAILS/CENTER

    if roll_value == 0 or roll_value == 360:
        roll_result = 'Center'
    elif roll_value < 180:
        roll_result = 'Heads'
    else:
        roll_result = 'Tails'




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
                if event.key == pygame.K_1:
                    roll_coin_flip()
                if event.key == pygame.K_2:
                    roll_coin_flip()
                if event.key == pygame.K_3:
                    roll_coin_flip()
    

    window.fill(0)    
    new_width = round(math.sin(math.radians(angle)) * coin_rect.width) 
    angle += 2
    rot_coin = coin if new_width >= 0 else pygame.transform.flip(coin, True, False) 
    rot_coin = pygame.transform.scale(rot_coin, (abs(new_width), coin_rect.height))
    window.blit(rot_coin, rot_coin.get_rect(center = coin_rect.center))


    roll_value_text = font.render(f"Roll value: {roll_value}", True, (255, 255, 255))
    window.blit(roll_value_text, (50, HEIGHT / 2 - 150))
    
    roll_result_text = font.render(f"Result: {roll_result}", True, (255, 255, 255))
    window.blit(roll_result_text, (50, HEIGHT / 2 - 50))
    
    history_log_text = font.render(f"Histroy Log", True, (255, 255, 255))
    window.blit(history_log_text, (50, HEIGHT / 2 + 50))


    player_wins_text = font.render(f"Player Wins: 0", True, (255, 255, 255))
    window.blit(player_wins_text, (WIDTH - 900, HEIGHT - 250))
    draws_no_wins_text = font.render(f"Draws/No Wins: 0", True, (255, 255, 255))
    window.blit(draws_no_wins_text, (WIDTH - 650, HEIGHT - 250))
    computer_wins_text = font.render(f"Computer Wins: 0", True, (255, 255, 255))
    window.blit(computer_wins_text, (WIDTH - 350, HEIGHT - 250))

    heads_counter_text = font.render(f"Heads: 0/0", True, (255, 255, 255))
    window.blit(heads_counter_text, (50, HEIGHT - 250))
    center_counter_text = font.render(f"Center: 0/0", True, (255, 255, 255))
    window.blit(center_counter_text, (350, HEIGHT - 250))
    tails_counter_text = font.render(f"Tails: 0/0", True, (255, 255, 255))
    window.blit(tails_counter_text, (650, HEIGHT - 250))
    heads_counter_text = font.render(f"Predict Heads", True, (255, 255, 255))
    window.blit(heads_counter_text, (50, HEIGHT - 150))
    center_counter_text = font.render(f"Predict Center", True, (255, 255, 255))
    window.blit(center_counter_text, (350, HEIGHT - 150))
    tails_counter_text = font.render(f"Predict Tails", True, (255, 255, 255))
    window.blit(tails_counter_text, (650, HEIGHT - 150))

    heads_counter_text = font.render(f"Heads Count: {angle // 360}", True, (255, 255, 255))
    window.blit(heads_counter_text, (WIDTH - 900, HEIGHT - 150))
    center_counter_text = font.render(f"Center Count: {(angle // 360) % 2}", True, (255, 255, 255))
    window.blit(center_counter_text, (WIDTH - 600, HEIGHT - 150))
    tails_counter_text = font.render(f"Tails Count: {(angle // 360) // 2}", True, (255, 255, 255))
    window.blit(tails_counter_text, (WIDTH - 350, HEIGHT - 150))



    mainmenu_text= font.render(f"Press ESC to return to the mainmenu", True, (255, 255, 255))
    window.blit(mainmenu_text, (50, 4))

    
    coin_flip_text= font.render(f"Quantum 4D Coin Flip", True, (255, 255, 255))
    window.blit(coin_flip_text, (WIDTH/2, 4))

    pygame.display.flip()

pygame.quit()
exit()