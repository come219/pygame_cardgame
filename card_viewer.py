import pygame
import random

import cardgame  # Import the cardgame module

# Initialize Pygame
pygame.init()
# Screen dimensions 800x600 
display_Width = 1920
display_Height = 1080
WIDTH, HEIGHT = display_Width, display_Height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Viewer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
DARK_GREY = (69, 69, 69)
LIGHT_GREY = (211, 211, 211)


# Font
font = pygame.font.SysFont(None, 50)
image_default = pygame.image.load("assets/card_a.png")

class Card:
    def __init__(self, name, image_path, pos, ):
        self.name = name
        self.image_path = pygame.image.load(image_path).convert_alpha()
        self.image = image_default
        self.rect = self.image.get_rect()
        self.selected = False

    def toggle_select(self):
        self.selected = not self.selected
        if self.selected:
            self.image = pygame.transform.scale(self.image_path, (150, 150))
        else:
            self.image = image_default

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def is_tapped(self, x, y):
        return self.rect.collidepoint(x, y)
    

# card viewer 

# Load images
card_a_image = pygame.image.load("assets/card_a.png")
card_b_image = pygame.image.load("assets/card_b.png")
card_c_image = pygame.image.load("assets/card_c.png")

rock_img = pygame.image.load("assets/card_rock.png")
paper_img = pygame.image.load("assets/card_paper.png")
scissors_img = pygame.image.load("assets/card_scissors.png")
card_lizard_img = pygame.image.load("assets/card_lizard.png")
card_spock_img = pygame.image.load("assets/card_spock.png")
card_gun_img = pygame.image.load("assets/card_gun.png")
card_sponge_img = pygame.image.load("assets/card_sponge.png")
card_devil_img = pygame.image.load("assets/card_devil.png")
card_dragon_img = pygame.image.load("assets/card_dragon.png")
card_lightning_img = pygame.image.load("assets/card_lightning.png")
card_human_img = pygame.image.load("assets/card_human.png")
card_fire_img = pygame.image.load("assets/card_fire.png")
card_snake_img = pygame.image.load("assets/card_snake.png")
card_tree_img = pygame.image.load("assets/card_tree.png")
card_air_img = pygame.image.load("assets/card_air.png")
card_wolf_img = pygame.image.load("assets/card_wolf.png")
card_water_img = pygame.image.load("assets/card_water.png")
card_balance_img = pygame.image.load("assets/card_balance.png")
card_void_img = pygame.image.load("assets/card_void.png")
card_no_lose_img = pygame.image.load("assets/card_no_lose.png")
card_metal_img = pygame.image.load("assets/card_metal.png")
card_toon_metal_img = pygame.image.load("assets/card_toon_metal.png")
card_earth_img = pygame.image.load("assets/card_earth.png")
card_super_paper_img = pygame.image.load("assets/card_super_paper.png")
card_skissors_img = pygame.image.load("assets/card_skissors.png")
card_toon_angel_img = pygame.image.load("assets/card_toon_angel.png") # angel = tree
card_toon_fire_img = pygame.image.load("assets/card_toon_fire.png")
card_toon_water_img = pygame.image.load("assets/card_toon_water.png")
card_toon_earth_img = pygame.image.load("assets/card_toon_earth.png")
card_toon_snake_img = pygame.image.load("assets/card_toon_snake.png")
card_toon_lizard_img = pygame.image.load("assets/card_toon_lizard.png")
card_toon_spock_img = pygame.image.load("assets/card_toon_spock.png")
card_toon_gun_img = pygame.image.load("assets/card_toon_gun.png")
card_computer_img = pygame.image.load("assets/card_computer.png")
card_bear_img = pygame.image.load("assets/card_bear.png")
card_toon_dragon_img = pygame.image.load("assets/card_toon_dragon.png")
card_fundamentals_only = pygame.image.load("assets/card_fundamentals_only.png")    # fundamentals only card - only rock, paper, scissors, with derivative cards
card_non_core =  pygame.image.load("assets/card_non_core.png")   # non-core card - no rock, paper, scissors, and derivative cards
card_stop_card_img = pygame.image.load("assets/card_stop_card.png")
card_counter_stop_card_img = pygame.image.load("assets/card_counter_stop.png")

blue_eyes_white_dragon_img = pygame.image.load("assets/card_blue_eyes_white_dragon.png")
red_eyes_black_dragon_img = pygame.image.load("assets/card_red_eyes_black_dragon.png")
# dark_magician_img = pygame.image.load("assets/card_dark_magician.png")

pot_of_greed_img = pygame.image.load("assets/card_pot_of_greed.png")
exodia_the_forbidden_one_img = pygame.image.load("assets/card_exodia_the_forbidden_one.png")
left_arm_of_exodia_img = pygame.image.load("assets/card_left_arm_of_exodia.png")
right_arm_of_exodia_img = pygame.image.load("assets/card_right_arm_of_exodia.png")
right_leg_of_exodia_img = pygame.image.load("assets/card_right_leg_of_exodia.png")
left_leg_of_exodia_img = pygame.image.load("assets/card_left_leg_of_exodia.png")
tassets_of_exodia_img = pygame.image.load("assets/card_tassets_of_exodia.png")
part_of_exodia_img = pygame.image.load("assets/card_part_of_exodia.png")
full_exodia_img = pygame.image.load("assets/card_full_exodia.png")
shadow_of_exodia_img = pygame.image.load("assets/card_shadow_of_exodia.png")
stop_exodia_img = pygame.image.load("assets/card_stop_exodia.png")

silence_img = pygame.image.load("assets/silence_card.png")
greater_axe_img = pygame.image.load("assets/greater_axe_card.png")
black_hole_img = pygame.image.load("assets/blackhole_card.png")
mysticalspacetypoon_img = pygame.image.load("assets/mysticalspacetypoon_card.png")
swords_of_hope_img = pygame.image.load("assets/swords_of_hope_card.png")
whip_img = pygame.image.load("assets/whip_card.png")
trap_stun_img = pygame.image.load("assets/card_trap_stun.png")

moon_champion_img = pygame.image.load("assets/card_moon_champion.png")
soldier_of_lunar_light_img = pygame.image.load("assets/card_soldier_of_lunar_light.png")
void_bard_img = pygame.image.load("assets/card_void_bard.png")

holy_knight_img = pygame.image.load("assets/card_holy_knight.png")
holy_archer_img = pygame.image.load("assets/card_holy_archer.png")
holy_mage_img = pygame.image.load("assets/card_holy_mage.png")

castle_img = pygame.image.load("assets/card_castle.png")
keep_img = pygame.image.load("assets/card_keep.png")
footman_img = pygame.image.load("assets/card_footman.png")
rifleman_img = pygame.image.load("assets/card_rifleman.png")
knight_img = pygame.image.load("assets/card_knight.png")
ghoul_img = pygame.image.load("assets/card_ghoul.png")
grunt_img = pygame.image.load("assets/card_grunt.png")
burrow_img = pygame.image.load("assets/card_burrow.png")
stronghold_img = pygame.image.load("assets/card_stronghold.png")

barbed_armour_img = pygame.image.load("assets/card_barbed_armour.png")

card_back_image = pygame.image.load("assets/card_back.png")
card_info_image = pygame.image.load("assets/card_info.png")


card_a_img = pygame.transform.scale(card_a_image, (150, 150))
card_b_img = pygame.transform.scale(card_b_image, (150, 150))
card_c_img = pygame.transform.scale(card_c_image, (150, 150))

card_rock_img = pygame.transform.scale(rock_img, (150, 150))
card_paper_img = pygame.transform.scale(paper_img, (150, 150))
card_scissors_img = pygame.transform.scale(scissors_img, (150, 150))
card_lizard_img = pygame.transform.scale(card_lizard_img, (150, 150))
card_spock_img = pygame.transform.scale(card_spock_img, (150, 150))
card_gun_img = pygame.transform.scale(card_gun_img, (150, 150))
card_sponge_img = pygame.transform.scale(card_sponge_img, (150, 150))
card_devil_img = pygame.transform.scale(card_devil_img, (150, 150))
card_dragon_img = pygame.transform.scale(card_dragon_img, (150, 150))
card_lightning_img = pygame.transform.scale(card_lightning_img, (150, 150))
card_human_img = pygame.transform.scale(card_human_img, (150, 150))
card_fire_img = pygame.transform.scale(card_fire_img, (150, 150))
card_snake_img = pygame.transform.scale(card_snake_img, (150, 150))
card_water_img = pygame.transform.scale(card_water_img, (150, 150))
card_tree_img = pygame.transform.scale(card_tree_img, (150, 150))
card_air_img = pygame.transform.scale(card_air_img, (150, 150))
card_wolf_img = pygame.transform.scale(card_wolf_img, (150, 150))
card_balance_img = pygame.transform.scale(card_balance_img, (150, 150))
card_earth_img = pygame.transform.scale(card_earth_img, (150, 150))
card_super_paper_img = pygame.transform.scale(card_super_paper_img, (150, 150))
card_skissors_img = pygame.transform.scale(card_skissors_img, (150, 150))
card_toon_snake_img = pygame.transform.scale(card_toon_snake_img, (150, 150))
card_toon_lizard_img = pygame.transform.scale(card_toon_lizard_img, (150, 150))
card_toon_spock_img = pygame.transform.scale(card_toon_spock_img, (150, 150))
card_toon_gun_img = pygame.transform.scale(card_toon_gun_img, (150, 150))
card_computer_img = pygame.transform.scale(card_computer_img, (150, 150))
card_bear_img = pygame.transform.scale(card_bear_img, (150, 150))
card_void_img = pygame.transform.scale(card_void_img, (150, 150))
card_metal_img = pygame.transform.scale(card_metal_img, (150, 150))
card_toon_metal_img = pygame.transform.scale(card_toon_metal_img, (150, 150))
card_toon_angel_img = pygame.transform.scale(card_toon_angel_img, (150, 150)) # angel = tree
card_toon_fire_img = pygame.transform.scale(card_toon_fire_img, (150, 150))
card_toon_water_img = pygame.transform.scale(card_toon_water_img, (150, 150))
card_toon_earth_img = pygame.transform.scale(card_toon_earth_img, (150, 150))
card_toon_dragon_img = pygame.transform.scale(card_toon_dragon_img, (150, 150))
card_no_lose_img = pygame.transform.scale(card_no_lose_img, (150, 150))


card_fundamentals_only = pygame.transform.scale(card_fundamentals_only, (150, 150))
card_non_core = pygame.transform.scale(card_non_core, (150, 150))
card_stop_card_img = pygame.transform.scale(card_stop_card_img, (150, 150))
card_counter_stop_card_img = pygame.transform.scale(card_counter_stop_card_img, (150, 150))


pot_of_greed_img = pygame.transform.scale(pot_of_greed_img, (150, 150))
blue_eyes_white_dragon_img = pygame.transform.scale(blue_eyes_white_dragon_img, (150, 150))
red_eyes_black_dragon_img = pygame.transform.scale(red_eyes_black_dragon_img, (150, 150))
exodia_the_forbidden_one_img = pygame.transform.scale(exodia_the_forbidden_one_img, (150, 150))
left_arm_of_exodia_img = pygame.transform.scale(left_arm_of_exodia_img, (150, 150))
right_arm_of_exodia_img = pygame.transform.scale(right_arm_of_exodia_img, (150, 150))
right_leg_of_exodia_img = pygame.transform.scale(right_leg_of_exodia_img, (150, 150))
left_leg_of_exodia_img = pygame.transform.scale(left_leg_of_exodia_img, (150, 150))
tassets_of_exodia_img = pygame.transform.scale(tassets_of_exodia_img, (150, 150))
full_exodia_img = pygame.transform.scale(full_exodia_img, (150, 150))
shadow_of_exodia_img = pygame.transform.scale(shadow_of_exodia_img, (150, 150))
stop_exodia_img = pygame.transform.scale(stop_exodia_img, (150, 150))



# spell cards
barbed_armour_img = pygame.transform.scale(barbed_armour_img, (150, 150))
swords_of_hope_img = pygame.transform.scale(swords_of_hope_img, (150, 150)) 
whip_img = pygame.transform.scale(whip_img, (150, 150))
silence_img = pygame.transform.scale(silence_img, (150, 150))
greater_axe_img = pygame.transform.scale(greater_axe_img, (150, 150))
black_hole_img = pygame.transform.scale(black_hole_img, (150, 150))
mysticalspacetypoon_img = pygame.transform.scale(mysticalspacetypoon_img, (150, 150))
trap_stun_img = pygame.transform.scale(trap_stun_img, (150, 150))

moon_champion_img = pygame.transform.scale(moon_champion_img, (150, 150))
soldier_of_lunar_light_img = pygame.transform.scale(soldier_of_lunar_light_img, (150, 150))
void_bard_img = pygame.transform.scale(void_bard_img, (150, 150))
holy_knight_img = pygame.transform.scale(holy_knight_img, (150, 150))
holy_archer_img = pygame.transform.scale(holy_archer_img, (150, 150))
holy_mage_img = pygame.transform.scale(holy_mage_img, (150, 150))

castle_img = pygame.transform.scale(castle_img, (150, 150))
keep_img = pygame.transform.scale(keep_img, (150, 150))
knight_img = pygame.transform.scale(knight_img, (150, 150))
footman_img = pygame.transform.scale(footman_img, (150, 150))
rifleman_img = pygame.transform.scale(rifleman_img, (150, 150))
ghoul_img = pygame.transform.scale(ghoul_img, (150, 150))
grunt_img = pygame.transform.scale(grunt_img, (150, 150))
burrow_img = pygame.transform.scale(burrow_img, (150, 150))
stronghold_img = pygame.transform.scale(stronghold_img, (150, 150))


card_back_img = pygame.transform.scale(card_back_image, (150, 150))

# card info image
card_info_img = pygame.transform.scale(card_info_image, (600, 800))



# Function to display text
def display_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))


    # Function to display a card with a picture that can be tapped
    def display_card(image, x, y):
        screen.blit(image, (x, y))

    # Function to check if a card is tapped
    def is_card_tapped(x, y, card_x, card_y, card_width, card_height):
        return card_x <= x <= card_x + card_width and card_y <= y <= card_y + card_height


CURRENT_PAGE = 0
TOTAL_PAGES = 20

image_cards =[
    rock_img, paper_img, scissors_img,
    card_info_img,card_info_img,card_info_img,card_info_img,card_info_img,card_info_img,
    card_info_img,card_info_img,card_info_img,card_info_img,card_info_img,card_info_img,
    card_info_img,card_info_img,card_info_img,card_info_img,card_info_img,card_info_img,
]

cards = [card_rock_img, card_paper_img, card_scissors_img, card_snake_img, 
        card_human_img, card_dragon_img, card_wolf_img, card_devil_img, 
        card_lightning_img,  card_gun_img,  card_fire_img, card_water_img, card_air_img, card_sponge_img,card_tree_img,
        card_lizard_img, card_spock_img, card_toon_spock_img, card_toon_snake_img, card_toon_lizard_img, 
        card_metal_img, card_toon_metal_img, card_bear_img, card_toon_dragon_img, 
        card_earth_img, card_super_paper_img, card_skissors_img, card_computer_img, 
        card_toon_angel_img, card_toon_fire_img, card_toon_water_img, card_toon_earth_img,
        
        card_toon_gun_img, card_stop_card_img, card_counter_stop_card_img, 
        card_balance_img, card_void_img, card_no_lose_img, 
        card_fundamentals_only, card_non_core,
        
        
        exodia_the_forbidden_one_img, pot_of_greed_img,
        full_exodia_img, right_arm_of_exodia_img, tassets_of_exodia_img, left_arm_of_exodia_img,  
        stop_exodia_img, right_leg_of_exodia_img, shadow_of_exodia_img, left_leg_of_exodia_img, 
        
        holy_archer_img, holy_mage_img, holy_knight_img, castle_img, keep_img,
        footman_img, rifleman_img, knight_img,  stronghold_img, grunt_img, burrow_img, ghoul_img,
        blue_eyes_white_dragon_img, red_eyes_black_dragon_img,
        moon_champion_img, soldier_of_lunar_light_img, void_bard_img, trap_stun_img,
        barbed_armour_img, swords_of_hope_img, whip_img,

        silence_img, greater_axe_img, black_hole_img, mysticalspacetypoon_img,
        
        card_a_img, card_b_img, card_c_img,
        card_a_img, card_b_img, card_c_img,
        card_a_img, card_b_img, card_c_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        card_back_img, card_back_img, card_back_img, card_back_img,
        ]

def _page_0():
        # row 0
        screen.blit(cards[0], (250, 150))
        screen.blit(cards[1], (450, 150))
        screen.blit(cards[2], (650, 150))
        screen.blit(cards[3], (850, 150))
        # row 1
        screen.blit(cards[4], (250, 350))
        screen.blit(cards[5], (450, 350))
        screen.blit(cards[6], (650, 350))
        screen.blit(cards[7], (850, 350))
        # row 2
        screen.blit(cards[8], (250, 550))
        screen.blit(cards[9], (450, 550))
        screen.blit(cards[10], (650, 550))
        screen.blit(cards[11], (850, 550))
        
def _page_1():
        # row 0
        screen.blit(cards[12], (250, 150))
        screen.blit(cards[13], (450, 150))
        screen.blit(cards[14], (650, 150))
        screen.blit(cards[15], (850, 150))
        # row 1
        screen.blit(cards[16], (250, 350))
        screen.blit(cards[17], (450, 350))
        screen.blit(cards[18], (650, 350))
        screen.blit(cards[19], (850, 350))

        # row 2
        screen.blit(cards[20], (250, 550))
        screen.blit(cards[21], (450, 550))
        screen.blit(cards[22], (650, 550))
        screen.blit(cards[23], (850, 550))


def _page_2():
        screen.blit(cards[24], (250, 150))
        screen.blit(cards[25], (450, 150))
        screen.blit(cards[26], (650, 150))
        screen.blit(cards[27], (850, 150))
        # row 1
        screen.blit(cards[28], (250, 350))
        screen.blit(cards[29], (450, 350))
        screen.blit(cards[30], (650, 350))
        screen.blit(cards[31], (850, 350))
        # row 2
        screen.blit(cards[32], (250, 550))
        screen.blit(cards[33], (450, 550))
        screen.blit(cards[34], (650, 550))
        screen.blit(cards[35], (850, 550))

def _page_3():
        screen.blit(cards[36], (250, 150))
        screen.blit(cards[37], (450, 150))
        screen.blit(cards[38], (650, 150))
        screen.blit(cards[39], (850, 150))
        # row 1
        screen.blit(cards[40], (250, 350))
        screen.blit(cards[41], (450, 350))
        screen.blit(cards[42], (650, 350))
        screen.blit(cards[43], (850, 350))
        # row 2
        screen.blit(cards[44], (250, 550))
        screen.blit(cards[45], (450, 550))
        screen.blit(cards[46], (650, 550))
        screen.blit(cards[47], (850, 550))

def _page_4():
        screen.blit(cards[48], (250, 150))
        screen.blit(cards[49], (450, 150))
        screen.blit(cards[50], (650, 150))
        screen.blit(cards[51], (850, 150))
        # row 1
        screen.blit(cards[52], (250, 350))
        screen.blit(cards[53], (450, 350))
        screen.blit(cards[54], (650, 350))
        screen.blit(cards[55], (850, 350))
        # row 2
        screen.blit(cards[56], (250, 550))
        screen.blit(cards[57], (450, 550))
        screen.blit(cards[58], (650, 550))
        screen.blit(cards[59], (850, 550))

def _page_5():
        screen.blit(cards[60], (250, 150))
        screen.blit(cards[61], (450, 150))
        screen.blit(cards[62], (650, 150))
        screen.blit(cards[63], (850, 150))
        # row 1
        screen.blit(cards[64], (250, 350))
        screen.blit(cards[65], (450, 350))
        screen.blit(cards[66], (650, 350))
        screen.blit(cards[67], (850, 350))
        # row 2
        screen.blit(cards[68], (250, 550))
        screen.blit(cards[69], (450, 550))
        screen.blit(cards[70], (650, 550))
        screen.blit(cards[71], (850, 550))

def _page_6():
        screen.blit(cards[72], (250, 150))
        screen.blit(cards[73], (450, 150))
        screen.blit(cards[74], (650, 150))
        screen.blit(cards[75], (850, 150))
        # row 1
        screen.blit(cards[76], (250, 350))
        screen.blit(cards[77], (450, 350))
        screen.blit(cards[78], (650, 350))
        screen.blit(cards[79], (850, 350))
        # row 2
        screen.blit(cards[80], (250, 550))
        screen.blit(cards[81], (450, 550))
        screen.blit(cards[82], (650, 550))
        screen.blit(cards[83], (850, 550))

def _page_7():
        screen.blit(cards[84], (250, 150))
        screen.blit(cards[85], (450, 150))
        screen.blit(cards[86], (650, 150))
        screen.blit(cards[87], (850, 150))
        # row 1
        screen.blit(cards[88], (250, 350))
        screen.blit(cards[89], (450, 350))
        screen.blit(cards[90], (650, 350))
        screen.blit(cards[91], (850, 350))
        # row 2
        screen.blit(cards[92], (250, 550))
        screen.blit(cards[93], (450, 550))
        screen.blit(cards[94], (650, 550))
        screen.blit(cards[95], (850, 550))

b_selected = False
num_selected = 0

def show_card_info():
    # Display card information here
    # screen.blit(card_info_img, (1250, 100))

    if b_selected == True:
        screen.blit(image_cards[num_selected], (1100, 100))
    else:
        screen.blit(card_info_img, (1250, 100))
        


    pass

def is_button_tapped(x, y, card_x, card_y, card_width, card_height):
    return card_x <= x <= card_x + card_width and card_y <= y <= card_y + card_height

def is_card_tapped(x, y, card_x, card_y, card_width, card_height):
    return card_x <= x <= card_x + card_width and card_y <= y <= card_y + card_height

# Main game loop
def main():
    running = True

    global b_selected, num_selected
    

    global CURRENT_PAGE
    while running:
        screen.fill(BLACK)
        # Draw a grey rectangle menu bar at the top
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))
        pygame.draw.rect(screen, DARK_GREY, (200, 100, WIDTH/2, 700))
        
        if CURRENT_PAGE == 0:
            _page_0()

        elif CURRENT_PAGE == 1:
            _page_1()
        elif CURRENT_PAGE == 2:
            _page_2()
        elif CURRENT_PAGE == 3:
            _page_3()
        elif CURRENT_PAGE == 4:
            _page_4()
        elif CURRENT_PAGE == 5:
            _page_5()
        elif CURRENT_PAGE == 6:
            _page_6()
        elif CURRENT_PAGE == 7:
            _page_7()
        

        display_text(f"Card Viewer", BLUE, 860, 4)
        show_card_info()

    
        display_text(f"Page {CURRENT_PAGE} / 20", BLUE, 630, 860)
        # Draw a light grey box
        pygame.draw.rect(screen, LIGHT_GREY, (450, 850, 120, 80))
        pygame.draw.rect(screen, LIGHT_GREY, (850, 850, 120, 80))
        display_text(f"<", BLUE, 500, 860)
        display_text(f">", BLUE, 900, 860)
        if b_selected == True:
            pygame.draw.rect(screen, LIGHT_GREY, (1550, 850, 140, 80))
            display_text(f"CLEAR", BLUE, 1550, 860)
        

        display_text(f"Menu", BLUE, 50, 4)
        
        # event handling
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        cardgame.main()
                    if event.key == pygame.K_LEFT:
                        CURRENT_PAGE -= 1
                        if CURRENT_PAGE > 0:
                            CURRENT_PAGE -= 0
                    if event.key == pygame.K_RIGHT:
                        CURRENT_PAGE += 1
                        if CURRENT_PAGE < TOTAL_PAGES:
                            CURRENT_PAGE += 0
                    if event.key == pygame.K_c:
                        b_selected = False
                        num_selected = 0
                        print("Card selection cleared")
                        
                    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    # (450, 850, 120, 80))
                    if is_button_tapped(x, y, 450, 850, 120, 80):
                        CURRENT_PAGE -= 1
                        if CURRENT_PAGE > 0:
                            CURRENT_PAGE -= 0
                    if is_button_tapped(x, y, 850, 850, 120, 80):
                        CURRENT_PAGE += 1
                        if CURRENT_PAGE < TOTAL_PAGES:
                            CURRENT_PAGE += 0
                    if is_button_tapped(x, y, 1550, 850, 140, 80):
                        b_selected = False
                        num_selected = 0
                        print("Card selection cleared")


                    if is_card_tapped(x, y, 250, 150, 150, 150):
                        b_selected = True
                        print("Card A tapped")
                        if CURRENT_PAGE == 0:
                            print("Card A chosen")
                            num_selected = 0
                    elif is_card_tapped(x, y, 450, 150, 150, 150):
                        b_selected = True
                        print("Card B tapped")
                        if CURRENT_PAGE == 0:
                            print("Card B chosen")
                            num_selected = 1
                    elif is_card_tapped(x, y, 650, 150, 150, 150):
                        b_selected = True
                        print("Card C tapped")
                        if CURRENT_PAGE == 0:
                            print("Card C chosen")
                            num_selected = 2
                    elif is_card_tapped(x, y, 850, 150, 150, 150):
                        print("Card D tapped")
                    elif is_card_tapped(x, y, 1650, 150, 150, 150):
                        print("Card Info tapped")

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()
        