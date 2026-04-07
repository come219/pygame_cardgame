import pygame
import sys

def init():
    # Initialize pygame
    pygame.init()

def main():
    # Screen dimensions
    WIDTH, HEIGHT = 1920, 1080

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Balanced Card Game | Auto CS")
    title_font = pygame.font.Font(None, 74)  # Use default font with size 74
    font = pygame.font.Font(None, 32)  # Use default font
    small_font = pygame.font.Font(None, 18)  # Use default font

    
    cs_office_img = pygame.image.load("assets/cs_cs_office.png")
    cs_office_img = pygame.transform.scale(cs_office_img, (150, 150))
    de_train_img = pygame.image.load("assets/cs_de_train.png")
    de_train_img = pygame.transform.scale(de_train_img, (150, 150))
    de_nuke_img = pygame.image.load("assets/cs_de_nuke.png")
    de_nuke_img = pygame.transform.scale(de_nuke_img, (150, 150))
    de_inferno_img = pygame.image.load("assets/cs_de_inferno.png")
    de_inferno_img = pygame.transform.scale(de_inferno_img, (150, 150))
    de_mirage_img = pygame.image.load("assets/cs_de_mirage.png")
    de_mirage_img = pygame.transform.scale(de_mirage_img, (150, 150))
    de_dust_2_img = pygame.image.load("assets/cs_de_dust2.png")
    de_dust_2_img = pygame.transform.scale(de_dust_2_img, (150, 150))
    de_dust_2_tga_img = pygame.image.load("assets/cs_de_dust2_tga.png")
    de_dust_2_tga_img = pygame.transform.scale(de_dust_2_tga_img, (300, 300))

    # Main loop
    running = True
    choose_side = True
    knife_round = False
    preliminary_round = False
    round_start = False
    round_switch = False
    round = 1
    global b_is_ct, b_is_t, round_result
    round_result = False
    b_t_win = False
    b_ct_win = False
    b_is_ct = False
    b_is_t = False
    CURRENT_MAP = 0
    CURRENT_SELECTION = 0
    CURRENT_PLAY_STYLE = 0
    CURRENT_ECONOMY_STYLE = 0
    CURRENT_ARMOR_STYLE = 0

    num_total_money = 4000
    num_divided_money = 800

    global num_in_a, num_in_long_a, num_in_short_a, num_in_b, num_in_mid, num_in_spawn
    num_in_a = 0
    num_in_long_a = 0
    num_in_short_a = 0
    num_in_b = 0
    num_in_mid = 0
    num_in_spawn = 5
    global list_a, list_mid, list_b
    list_a = []
    list_mid = []
    list_b = []

    def reset_positions():
        global num_in_a, num_in_long_a, num_in_short_a, num_in_b, num_in_mid, num_in_spawn
        num_in_a = 0
        num_in_long_a = 0
        num_in_short_a = 0
        num_in_b = 0
        num_in_mid = 0
        num_in_spawn = 5
        list_a.clear()
        list_mid.clear()
        list_b.clear()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        import cardgame  # Import the cardgame module
                        cardgame.main()
                    if event.key == pygame.K_c:
                        choose_side = False
                        knife_round = True
                        b_is_ct = True
                        b_is_t = False
                    if event.key == pygame.K_t:
                        choose_side = False
                        knife_round = True
                        b_is_ct = False
                        b_is_t = True
                    
                    if event.key == pygame.K_LEFT:
                            CURRENT_MAP = CURRENT_MAP - 1
                    if event.key == pygame.K_RIGHT:
                            CURRENT_MAP = CURRENT_MAP + 1
                    
                    
                    if round_result == True:
                        if event.key == pygame.K_RETURN:
                            knife_round = False
                            preliminary_round = True
                            
                    if event.key == pygame.K_RETURN:
                        round_result = True
                        # assign bot positions
                        if num_in_a == 5:
                            b_t_win = True
                        if num_in_b == 5:
                            b_t_win = True
                        if num_in_mid == 5:
                            b_ct_win = True

                    
                    if round_result == True:
                        if event.key == pygame.K_PERIOD:
                            knife_round = False
                            preliminary_round = False

                            if b_ct_win:
                                if b_is_ct:
                                    num_total_money = num_total_money + 3250
                                    num_divided_money = num_divided_money + 3250
                            if b_t_win:
                                if b_is_t:
                                    num_total_money = num_total_money + 3250
                                    num_divided_money = num_divided_money + 3250

                            
                    if event.key == pygame.K_PERIOD:
                        round = round + 1
                        # assign bot positions
                        if num_in_a == 5:
                            b_t_win = True
                        if num_in_b == 5:
                            b_t_win = True
                        if num_in_mid == 5:
                            b_ct_win = True
                        

                    if event.key == pygame.K_s:
                        b_is_ct = b_is_ct
                        b_is_t = b_is_t
                        preliminary_round = False
                        round_start = True
                        
                    if event.key == pygame.K_x:
                        b_is_ct = not b_is_ct
                        b_is_t = not b_is_t
                        preliminary_round = False
                        round_start = True
                                    
                        


                    if event.key == pygame.K_1:
                        if num_in_spawn > 0:
                            num_in_a = num_in_a + 1
                            num_in_long_a = num_in_long_a + 1
                            num_in_spawn = num_in_spawn - 1
                            list_a.append((CURRENT_PLAY_STYLE, CURRENT_ECONOMY_STYLE, CURRENT_ARMOR_STYLE))

                    if event.key == pygame.K_2:
                        if num_in_spawn > 0:
                            num_in_a = num_in_a + 1
                            num_in_short_a = num_in_short_a + 1
                            num_in_spawn = num_in_spawn - 1

                    if event.key == pygame.K_3:
                        if num_in_spawn > 0:
                            num_in_mid = num_in_mid + 1
                            num_in_spawn = num_in_spawn - 1
                            list_mid.append((CURRENT_PLAY_STYLE, CURRENT_ECONOMY_STYLE, CURRENT_ARMOR_STYLE))

                    if event.key == pygame.K_4:
                        if num_in_spawn > 0:
                            num_in_b = num_in_b + 1
                            num_in_spawn = num_in_spawn - 1
                            list_b.append((CURRENT_PLAY_STYLE, CURRENT_ECONOMY_STYLE, CURRENT_ARMOR_STYLE))

                    if event.key == pygame.K_5:
                        reset_positions()


                    
                    
                    
                    if event.key == pygame.K_UP:
                        CURRENT_SELECTION = CURRENT_SELECTION - 1
                        if CURRENT_SELECTION < 0:
                            CURRENT_SELECTION = 2
                        
                    if event.key == pygame.K_DOWN:
                        CURRENT_SELECTION = CURRENT_SELECTION + 1
                        if CURRENT_SELECTION > 3:
                            CURRENT_SELECTION = 0
                
                    if CURRENT_SELECTION == 0:
                        if event.key == pygame.K_LEFT:
                            CURRENT_PLAY_STYLE = CURRENT_PLAY_STYLE - 1
                        if event.key == pygame.K_RIGHT:
                            CURRENT_PLAY_STYLE = CURRENT_PLAY_STYLE + 1
                    
                    if CURRENT_SELECTION == 1:
                        if event.key == pygame.K_LEFT:
                            CURRENT_ECONOMY_STYLE = CURRENT_ECONOMY_STYLE - 1
                        if event.key == pygame.K_RIGHT:
                            CURRENT_ECONOMY_STYLE = CURRENT_ECONOMY_STYLE + 1
                    
                    if CURRENT_SELECTION == 2:
                        if event.key == pygame.K_LEFT:
                            CURRENT_ARMOR_STYLE = CURRENT_ARMOR_STYLE - 1
                        if event.key == pygame.K_RIGHT:
                            CURRENT_ARMOR_STYLE = CURRENT_ARMOR_STYLE + 1
                        

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Set the top window bar to dark grey
        pygame.display.get_surface().fill((50, 50, 50), pygame.Rect(0, 0, WIDTH, 30))
        menu_text = font.render("Menu", True, (255, 255, 255))  # White color
        menu_text_rect = menu_text.get_rect(center=(50, 20))  # Center the text
        screen.blit(menu_text, menu_text_rect)

        title_text = font.render("Auto CS", True, (255, 255, 255))  # White color
        title_text_rect = title_text.get_rect(center=(WIDTH / 2, 20))  # Center the text
        screen.blit(title_text, title_text_rect)
        
        
        if choose_side == True:
            text = title_font.render("Auto CS - Automatic Search & Destroy", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 -50))  # Center the text
            screen.blit(text, text_rect)
            
            # pick ct or t
            text = title_font.render("Pick T or CT", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Map: _", True, (255, 255, 255))  # White color
            if CURRENT_MAP == 5:
                text = title_font.render("Map: de_office", True, (255, 255, 255))  # White color
            if CURRENT_MAP == 4:
                text = title_font.render("Map: de_train", True, (255, 255, 255))  # White color
            if CURRENT_MAP == 3:
                text = title_font.render("Map: de_nuke", True, (255, 255, 255))  # White color
            if CURRENT_MAP == 2:
                text = title_font.render("Map: de_inferno", True, (255, 255, 255))  # White color
            if CURRENT_MAP == 1:
                text = title_font.render("Map: de_mirage", True, (255, 255, 255))  # White color
            if CURRENT_MAP == 0:
                text = title_font.render("Map: de_dust2", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, 80))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render("<", True, (0, 0, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 300, 80))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(">", True, (0, 0, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 300, 80))  # Center the text
            screen.blit(text, text_rect)

            
            if CURRENT_MAP == 5:
                screen.blit(cs_office_img, (WIDTH // 2 - 75, 150))
            if CURRENT_MAP == 4:
                screen.blit(de_train_img, (WIDTH // 2 - 75, 150))
            if CURRENT_MAP == 3:
                screen.blit(de_nuke_img, (WIDTH // 2 - 75, 150))
            if CURRENT_MAP == 2:
                screen.blit(de_inferno_img, (WIDTH // 2 - 75, 150))

            if CURRENT_MAP == 1:
                screen.blit(de_mirage_img, (WIDTH // 2 - 75, 150))
            if CURRENT_MAP == 0:
                screen.blit(de_dust_2_img, (WIDTH // 2 - 75, 150))



        if  knife_round == True:
            text = title_font.render("Map: de_dust2", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 400,  60))  # Center the text
            screen.blit(text, text_rect)
            screen.blit(de_dust_2_img, (WIDTH // 2 - 475, 120))
            screen.blit(de_dust_2_tga_img, (WIDTH // 2 - 945, 40))
            
            text = title_font.render("CT Wins: 0 | T Wins: 0", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2  - 350))  # Center the text
            screen.blit(text, text_rect)
            
            if round_result == True:
                if b_ct_win == True:
                    text = title_font.render("CT Wins", True, (0, 255, 0))  # White color
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))  # Center the text
                    screen.blit(text, text_rect)
                if b_t_win == True:
                    text = title_font.render(" T Wins", True, (0, 255, 0))  # White color
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))  # Center the text
                    screen.blit(text, text_rect)


        # show economy, round
        if knife_round == True:
            text = title_font.render("Round: 0 - Knife Round", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 400))  # Center the text
            screen.blit(text, text_rect)


            text = title_font.render(f"1. Long A : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 - 750, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"2. Short A : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"3. Mid : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"4. B : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"5. Spawn : 5", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 650, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"1. Long A : {num_in_long_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 750, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"2. Short A : {num_in_short_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"3. Mid : {num_in_mid}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"4. B : {num_in_b}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"5. Spawn : {num_in_spawn}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 650, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
        
            text = small_font.render(f"[A] : {num_in_a} : {list_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 350))  # Center the text
            screen.blit(text, text_rect)
            
            text = small_font.render(f"Mid : {num_in_mid} : {list_mid}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 200))  # Center the text
            screen.blit(text, text_rect)

            text = small_font.render(f"[B] : {num_in_b} : {list_b}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 100))  # Center the text
            screen.blit(text, text_rect)


            
            if b_is_t == True:
                text = title_font.render("Current Side: Terrorists (T)", True, (212,85,0))  # t color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)

            
            if b_is_ct == True:
                text = title_font.render("Current Side: Counter-Terrorists (CT)", True, 	(58,71,106))  # ct color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)
                        


            text = title_font.render(f"Random {CURRENT_PLAY_STYLE}", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 0:
                text = title_font.render("Advantageous Hold", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 1:
                text = title_font.render("Aggressive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 2:
                text = title_font.render("Anchor", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 3:
                text = title_font.render("Passive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 4:
                text = title_font.render("Rush", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 5:
                text = title_font.render("Lurk", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 6:
                text = title_font.render("Hold Corner", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 7:
                text = title_font.render("Float", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 8:
                text = title_font.render("Flow", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE >= 9:
                text = title_font.render("_", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Playstyle:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Center the text
            screen.blit(text, text_rect)

            if CURRENT_SELECTION == 0:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)

            
            text = title_font.render("Economy:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 330))  # Center the text
            screen.blit(text, text_rect)

            
            if CURRENT_SELECTION == 1:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)

            text = title_font.render("knives only", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 380))  # Center the text
            screen.blit(text, text_rect)

            if round_result == True:
                text = title_font.render("Press Enter for Preliminaries", True, (255, 255, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))  # Center the text
                screen.blit(text, text_rect)
            else: 
                text = title_font.render("Press Enter to Ready Up", True, (255, 255, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))  # Center the text
                screen.blit(text, text_rect)
            
            text = title_font.render("Press '5' to Reset", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 600, HEIGHT - 50))  # Center the text
            screen.blit(text, text_rect)
        
        if preliminary_round == True:
            text = title_font.render("Preliminary Round", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, 150))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Stay or switch sides?", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, 250))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Press s to stay", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 250))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render("Press x to switch", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 150))  # Center the text
            screen.blit(text, text_rect)
            
            if b_is_t == True:
                text = title_font.render("Current Side: Terrorists (T)", True, (212,85,0))  # t color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)

            
            if b_is_ct == True:
                text = title_font.render("Current Side: Counter-Terrorists (CT)", True, 	(58,71,106))  # ct color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)


        if round_start == True and round == 1:
            text = title_font.render(f"Round: {round} - Pistol Round", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, 150))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"1. Long A : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 - 750, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"2. Short A : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"3. Mid : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"4. B : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"5. Spawn : 5", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 650, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"1. Long A : {num_in_long_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 750, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"2. Short A : {num_in_short_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"3. Mid : {num_in_mid}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"4. B : {num_in_b}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"5. Spawn : {num_in_spawn}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 650, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)

            text = small_font.render(f"[A] : {num_in_a} : {list_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 350))  # Center the text
            screen.blit(text, text_rect)
            
            text = small_font.render(f"Mid : {num_in_mid} : {list_mid}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 200))  # Center the text
            screen.blit(text, text_rect)

            text = small_font.render(f"[B] : {num_in_b} : {list_b}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 100))  # Center the text
            screen.blit(text, text_rect)



            if b_is_t == True:
                text = title_font.render("Current Side: Terrorists (T)", True, (212,85,0))  # t color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)

            
            if b_is_ct == True:
                text = title_font.render("Current Side: Counter-Terrorists (CT)", True, 	(58,71,106))  # ct color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)


            # text = title_font.render("Playstyle: Advantageous Hold/Aggressive/Anchor/Passive/Rush", True, (255, 255, 255))  # White color
            text = title_font.render(f"Random {CURRENT_PLAY_STYLE}", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 0:
                text = title_font.render("Advantageous Hold", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 1:
                text = title_font.render("Aggressive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 2:
                text = title_font.render("Anchor", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 3:
                text = title_font.render("Passive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 4:
                text = title_font.render("Rush", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 5:
                text = title_font.render("Lurk", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 6:
                text = title_font.render("Hold Corner", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 7:
                text = title_font.render("Float", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 8:
                text = title_font.render("Flow", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE >= 9:
                text = title_font.render("_", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Playstyle:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Center the text
            screen.blit(text, text_rect)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Center the text
            screen.blit(text, text_rect)


            if CURRENT_SELECTION == 0:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)

            
            text = title_font.render(f"Total Balance:  ${num_total_money}", True, (0, 255, 0))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT // 2 + 230))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"Balance: ~${num_divided_money} / Player", True, (0, 255, 0))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT // 2 + 330))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Economy:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 330))  # Center the text
            screen.blit(text, text_rect)

            
            if CURRENT_SELECTION == 1:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)
            
            # text = title_font.render("armor/eco. pistol/luxury pistols/utility/save", True, (255, 255, 255))  # White color
            text = title_font.render("Default Pistol", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 0:
                text = title_font.render("Default Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 1:
                text = title_font.render("Eco. Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 2:
                text = title_font.render("Luxury Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 3:
                text = title_font.render("Utility + Pistol", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 4:
                text = title_font.render("Utility", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 5:
                text = title_font.render("Save", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 6:
                text = title_font.render("Drop Eco. Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 7:
                text = title_font.render("Drop Luxury Pistol", True, (255, 255, 255))  # White color

            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 380))  # Center the text
            screen.blit(text, text_rect)

            if CURRENT_SELECTION == 2:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 430))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 430))  # Center the text
                screen.blit(text, text_rect)


            text = title_font.render("Armor:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 430))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render("No Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 0:
                text = title_font.render("No Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 1:
                text = title_font.render("Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 2:
                text = title_font.render("Kit", True, (255, 255, 255))  # White color

            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 480))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Press . to see result", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT - 50))  # Center the text
            screen.blit(text, text_rect)

        elif round_switch == True:
            text = title_font.render(f"Round: {round} - Switch Round", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, 150))  # Center the text
            screen.blit(text, text_rect)
            

            text = title_font.render("Press Enter to continue", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))  # Center the text
            screen.blit(text, text_rect)
        


        if round == 16:
            text = title_font.render(f"Round: {round} - Pistol Round", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, 150))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"1. Long A : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 - 750, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"2. Short A : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"3. Mid : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"4. B : 0", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"5. Spawn : 5", True, (255, 0, 0))  # red color
            text_rect = text.get_rect(center=(WIDTH // 2 + 650, HEIGHT // 2 - 150))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"1. Long A : {num_in_long_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 750, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"2. Short A : {num_in_short_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"3. Mid : {num_in_mid}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render(f"4. B : {num_in_b}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render(f"5. Spawn : {num_in_spawn}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2 + 650, HEIGHT // 2))  # Center the text
            screen.blit(text, text_rect)

            text = small_font.render(f"[A] : {num_in_a} : {list_a}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 350))  # Center the text
            screen.blit(text, text_rect)
            
            text = small_font.render(f"Mid : {num_in_mid} : {list_mid}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 200))  # Center the text
            screen.blit(text, text_rect)

            text = small_font.render(f"[B] : {num_in_b} : {list_b}", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(250, HEIGHT - 100))  # Center the text
            screen.blit(text, text_rect)



            if b_is_ct == True:
                text = title_font.render("Current Side: Terrorists (T)", True, (212,85,0))  # t color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)

            
            if b_is_t == True:
                text = title_font.render("Current Side: Counter-Terrorists (CT)", True, 	(58,71,106))  # ct color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Center the text
                screen.blit(text, text_rect)


            # text = title_font.render("Playstyle: Advantageous Hold/Aggressive/Anchor/Passive/Rush", True, (255, 255, 255))  # White color
            text = title_font.render(f"Random {CURRENT_PLAY_STYLE}", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 0:
                text = title_font.render("Advantageous Hold", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 1:
                text = title_font.render("Aggressive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 2:
                text = title_font.render("Anchor", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 3:
                text = title_font.render("Passive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 4:
                text = title_font.render("Rush", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 5:
                text = title_font.render("Lurk", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 6:
                text = title_font.render("Hold Corner", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 7:
                text = title_font.render("Float", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 8:
                text = title_font.render("Flow", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE >= 9:
                text = title_font.render("_", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Playstyle:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Center the text
            screen.blit(text, text_rect)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Center the text
            screen.blit(text, text_rect)


            if CURRENT_SELECTION == 0:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)

            
            text = title_font.render(f"Total Balance:  ${num_total_money}", True, (0, 255, 0))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT // 2 + 230))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"Balance: ~${num_divided_money} / Player", True, (0, 255, 0))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT // 2 + 330))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Economy:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 330))  # Center the text
            screen.blit(text, text_rect)

            
            if CURRENT_SELECTION == 1:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)
            
            # text = title_font.render("armor/eco. pistol/luxury pistols/utility/save", True, (255, 255, 255))  # White color
            text = title_font.render("Default Pistol", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 0:
                text = title_font.render("Default Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 1:
                text = title_font.render("Eco. Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 2:
                text = title_font.render("Luxury Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 3:
                text = title_font.render("Utility + Pistol", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 4:
                text = title_font.render("Utility", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 5:
                text = title_font.render("Save", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 6:
                text = title_font.render("Drop Eco. Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 7:
                text = title_font.render("Drop Luxury Pistol", True, (255, 255, 255))  # White color

            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 380))  # Center the text
            screen.blit(text, text_rect)

            if CURRENT_SELECTION == 2:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 430))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 430))  # Center the text
                screen.blit(text, text_rect)


            text = title_font.render("Armor:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 430))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render("No Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 0:
                text = title_font.render("No Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 1:
                text = title_font.render("Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 2:
                text = title_font.render("Kit", True, (255, 255, 255))  # White color

            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 480))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Press . to see result", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT - 50))  # Center the text
            screen.blit(text, text_rect)


        elif round >= 2:
            text = title_font.render(f"Round: {round} - Normal Round", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, 150))  # Center the text
            screen.blit(text, text_rect)


            text = title_font.render(f"Random {CURRENT_PLAY_STYLE}", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 0:
                text = title_font.render("Advantageous Hold", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 1:
                text = title_font.render("Aggressive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 2:
                text = title_font.render("Anchor", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 3:
                text = title_font.render("Passive", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 4:
                text = title_font.render("Rush", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 5:
                text = title_font.render("Lurk", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 6:
                text = title_font.render("Hold Corner", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 7:
                text = title_font.render("Float", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE == 8:
                text = title_font.render("Flow", True, (255, 255, 255))  # White color
            if CURRENT_PLAY_STYLE >= 9:
                text = title_font.render("_", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))  # Center the text
            screen.blit(text, text_rect)

            text = title_font.render("Playstyle:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Center the text
            screen.blit(text, text_rect)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Center the text
            screen.blit(text, text_rect)


            if CURRENT_SELECTION == 0:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 200))  # Center the text
                screen.blit(text, text_rect)

            
            text = title_font.render(f"Total Balance:  ${num_total_money}", True, (0, 255, 0))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT // 2 + 230))  # Center the text
            screen.blit(text, text_rect)
            text = title_font.render(f"Balance: ~${num_divided_money} / Player", True, (0, 255, 0))  # White color
            text_rect = text.get_rect(center=(WIDTH - 400, HEIGHT // 2 + 330))  # Center the text
            screen.blit(text, text_rect)


            text = title_font.render("Economy:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 330))  # Center the text
            screen.blit(text, text_rect)

            if CURRENT_SELECTION == 1:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 330))  # Center the text
                screen.blit(text, text_rect)
            

            text = title_font.render("Save", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 0:
                text = title_font.render("Auto Buy Guns", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 1:
                text = title_font.render("Eco. Weapons", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 2:
                text = title_font.render("Luxury Weapons", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 3:
                text = title_font.render("Utility + Eco. Weapons", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 4:
                text = title_font.render("Utility + Luxury Weapons", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 5:
                text = title_font.render("Save", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 6:
                text = title_font.render("AWP", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 7:
                text = title_font.render("Utility + AWP", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 8:
                text = title_font.render("Utility + Luxury Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 9:
                text = title_font.render("Utility + Eco. Pistols", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 10:
                text = title_font.render("Utility", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 11:
                text = title_font.render("Eco. SMG", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 12:
                text = title_font.render("Luxury SMG", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 13:
                text = title_font.render("Shotgun", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 14:
                text = title_font.render("Negev", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 15:
                text = title_font.render("Auto Sniper", True, (255, 255, 255))  # White color
            if CURRENT_ECONOMY_STYLE == 16:
                text = title_font.render("Zeus", True, (255, 255, 255))  # White color
        

            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 380))  # Center the text
            screen.blit(text, text_rect)

            if CURRENT_SELECTION == 2:
                text = title_font.render("<", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 430))  # Center the text
                screen.blit(text, text_rect)
                text = title_font.render(">", True, (0, 0, 255))  # White color
                text_rect = text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 430))  # Center the text
                screen.blit(text, text_rect)


            text = title_font.render("Armor:", True, (255, 255, 255))  # White color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 430))  # Center the text
            screen.blit(text, text_rect)
            
            text = title_font.render("No Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 0:
                text = title_font.render("Auto Buy Armor + Kit", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 1:
                text = title_font.render("Armor + Helmet + Kit", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 2:
                text = title_font.render("Armor + Helmet", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 3:
                text = title_font.render("Armor + Kit", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 4:
                text = title_font.render("Armor", True, (255, 255, 255))  # White color
            if CURRENT_ARMOR_STYLE == 5:
                text = title_font.render("Kit", True, (255, 255, 255))  # White color

            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 480))  # Center the text
            screen.blit(text, text_rect)
        


        # how many b, how many a, how many mid?
        # pick economy

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    init()
    main()