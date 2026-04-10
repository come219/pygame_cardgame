import pygame
import sys

# shop.py - Pygame Card Shop Screen


# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Shop")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_GREY = (69, 69, 69)

# Font
font = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 30)

shop_icon_image = pygame.image.load("assets/shop_icon.png")
shop_icon_image_scaled = pygame.transform.scale(shop_icon_image, (250, 250))  

# Load images
card_images = {
    "Random_Common": pygame.image.load("assets/card_random.png"),
    "Random_Uncommon": pygame.image.load("assets/card_random.png"),
    "Random_Pack": pygame.image.load("assets/card_random.png"),
    "Random_Card": pygame.image.load("assets/card_random.png"),
    "Featured_Card": pygame.image.load("assets/card_random.png"),
    "Rock": pygame.image.load("assets/card_rock.png"),
    "Paper": pygame.image.load("assets/card_paper.png"),
    "Scissors": pygame.image.load("assets/card_scissors.png"),
    "Lizard": pygame.image.load("assets/card_lizard.png"),
    "Spock": pygame.image.load("assets/card_spock.png"),

}
for key in card_images:
    card_images[key] = pygame.transform.scale(card_images[key], (150, 150))

# Shop items
shop_items = [
    {"name": "Rock", "price": 100, "stock": 10, "image": card_images["Rock"]},
    {"name": "Paper", "price": 150, "stock": 10, "image": card_images["Paper"]},
    {"name": "Scissors", "price": 200, "stock": 10, "image": card_images["Scissors"]},
    {"name": "Lizard", "price": 1000, "stock": 5, "image": card_images["Lizard"]},
    {"name": "Spock", "price": 2000, "stock": 5, "image": card_images["Spock"]},

]

# card back
# card_accessories_shop_items = [
#     {"name": "Card Sleeve", "price": 50, "stock": 20, "image": card_images["Random_Card"]},
#     {"name": "Deck Box", "price": 100, "stock": 15, "image": card_images["Random_Card"]},
#     {"name": "Playmat", "price": 200, "stock": 10, "image": card_images["Random_Card"]},
#     {"name": "Card Stand", "price": 30, "stock": 25, "image": card_images["Random_Card"]},
#     {"name": "Dice Set", "price": 75, "stock": 20, "image": card_images["Random_Card"]},
# ]

random_shop_items = [

    {"name": "Random Common", "price": 10, "stock": 10, "image": card_images["Random_Common"]},
    {"name": "Random Uncommon", "price": 20, "stock": 5, "image": card_images["Random_Uncommon"]},
    {"name": "Random Booster Pack", "price": 999, "stock": 3, "image": card_images["Random_Pack"]},
    {"name": "Random Card", "price": 99, "stock": 10, "image": card_images["Random_Card"]},
    {"name": "Featured Card", "price": 999, "stock": 1, "image": card_images["Featured_Card"]},

]

# Player's currency
player_currency = 500

# Function to display text
def display_text(text, color, x, y, font=font):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))


shops_menu_toggle = True
selected_shop_menu = 1
def display_shops_menu():
    screen.fill(DARK_GREY)
    display_text("ESC - Return to Shop", GREY, 50, 20)
    display_text("Shops Menu", LIGHT_BLUE, WIDTH // 2 - 150, 80)

    shops = [
        "1. Card Shop",
        "2. Player Shop",
        "3. Item Shop",
        "4. Quest Shop",
        "5. [LOCKED] Rare Card Shop",
        "6. [LOCKED] Campaign Shop",
        "7. [LOCKED] HIDDEN Shop",
        "8. [LOCKED] HIDDEN Shop",
        "9. Lootbox Shop",
        "0. M.T.X. Shop"
    ]

    start_y = 250
    for i, shop in enumerate(shops):
        color = LIGHT_BLUE if i + 1 == selected_shop_menu else WHITE
        display_text(shop, color, WIDTH // 2 - 200, start_y + i * 50, font_small)

    # Highlight selected shop
    highlight_y = start_y + (selected_shop_menu - 1) * 50 - 10
    pygame.draw.rect(screen, LIGHT_BLUE, (WIDTH // 2 - 220, highlight_y, 420, 50), 3)

    # Instructions
    display_text("Use ↑ ↓  to navigate", GREY, WIDTH // 2 - 200, HEIGHT - 150, font_small) # ← →
    display_text("Press ENTER to select", GREY, WIDTH // 2 - 200, HEIGHT - 100, font_small)
    display_text("Press ESC to return", GREY, WIDTH // 2 - 200, HEIGHT - 50, font_small)



def display_card_shop():
    screen.fill(BLACK)
    display_text("ESC - Mainmenu", GREY, 50, 4)
    # Draw shop UI
    display_text("Card Shop", LIGHT_BLUE, WIDTH // 2 - 100, 4)
    screen.blit(shop_icon_image_scaled, (WIDTH // 2 - 200, 50))
    
    display_text(f"Player: _", WHITE, WIDTH - 400, 4)
    display_text(f"Balance: ${player_currency}", WHITE, WIDTH - 400, 50)
    display_text(f"MTX Balance: ◙ 0", WHITE, WIDTH - 400, 100)
    # Display shop items
    for i, item in enumerate(shop_items):
        x = 100 + i * 400
        y = 300
        screen.blit(item["image"], (x, y))
        display_text(item["name"], WHITE, x + 25, y + 160, font_small)
        display_text(f"Price: {item['price']}", WHITE, x + 25, y + 190, font_small)
        display_text(f"Stock: {item['stock']}", WHITE, x + 25, y + 220, font_small)
    # Instructions
    display_text("Press SPACE to claim free card pack!", GREY, 50, HEIGHT - 300)
    display_text("Press Q to view card packs", GREY, 50, HEIGHT - 250)
    display_text("Press O to open card pack", GREY, 50, HEIGHT - 200)
    display_text("Press V to View Cards", GREY, 50, HEIGHT - 150)
    display_text("Press D to View Deck Manager", GREY, 50, HEIGHT - 100)
    
    display_text("Press P to view Payments & Transactions", GREY, 50, HEIGHT - 50)

    if b_sell_toggle == False:
        display_text("Press B to Buy", GREY, 50, HEIGHT - 350)
    else:
        display_text("Press S to Sell", GREY, 50, HEIGHT - 350)

    
    display_text("Press I to View Collection", GREY, WIDTH/2, HEIGHT - 250)
    display_text("Page 0 / 20", WHITE, WIDTH/2, HEIGHT - 200)
    display_text("Press ← to see previous page", GREY, WIDTH/2, HEIGHT - 150) 
    display_text("Press → to see next page", GREY, WIDTH/2, HEIGHT - 100)
    display_text("Press Y to open shops menu", GREY, WIDTH/2, HEIGHT - 50)




# Main shop loop
def main():
    global player_currency, b_sell_toggle, shops_menu_toggle, selected_shop_menu
    running = True
    b_sell_toggle = True

    while running:

        if shops_menu_toggle:
            display_shops_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shops_menu_toggle = False
                    
                    if event.key == pygame.K_RETURN:
                        shops_menu_toggle = False
                        print(f"Entered shop menu {selected_shop_menu}")
                    if event.key == pygame.K_DOWN:
                        selected_shop_menu += 1
                        if selected_shop_menu > 9:
                            selected_shop_menu = 1
                    if event.key == pygame.K_UP:
                        selected_shop_menu -= 1
                        if selected_shop_menu < 1:
                            selected_shop_menu = 9

            pygame.display.flip()
            continue

        else:
            display_card_shop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        shops_menu_toggle = True

                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_s:
                        b_sell_toggle = not b_sell_toggle
                    if event.key == pygame.K_b:
                        b_sell_toggle = not b_sell_toggle
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, item in enumerate(shop_items):
                        x = 100 + i * 400
                        y = 300
                        if x <= mouse_pos[0] <= x + 150 and y <= mouse_pos[1] <= y + 150:
                            if player_currency >= item["price"]:
                                player_currency -= item["price"]
                                print(f"Purchased {item['name']}!")
                            else:
                                print("Not enough currency!")

        pygame.display.flip()

if __name__ == "__main__":
    main()