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

# Load images
card_images = {
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
    {"name": "Rock", "price": 100, "image": card_images["Rock"]},
    {"name": "Paper", "price": 150, "image": card_images["Paper"]},
    {"name": "Scissors", "price": 200, "image": card_images["Scissors"]},
    {"name": "Lizard", "price": 1000, "image": card_images["Lizard"]},
    {"name": "Spock", "price": 2000, "image": card_images["Spock"]},
]

# Player's currency
player_currency = 500

# Function to display text
def display_text(text, color, x, y, font=font):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Main shop loop
def main():
    global player_currency, b_sell_toggle
    running = True
    b_sell_toggle = True

    while running:
        screen.fill(BLACK)
        display_text("Menu", GREY, 50, 4)
        # Draw shop UI
        display_text("Card Shop", LIGHT_BLUE, WIDTH // 2 - 100, 4)
        display_text("Page 0 / 20", GREY, WIDTH // 2 - 100, 200)
        display_text(f"Player: _", WHITE, WIDTH - 400, 4)
        display_text(f"Balance: {player_currency}", WHITE, WIDTH - 400, 50)

        # Display shop items
        for i, item in enumerate(shop_items):
            x = 100 + i * 400
            y = 300
            screen.blit(item["image"], (x, y))
            display_text(item["name"], WHITE, x + 25, y + 160, font_small)
            display_text(f"Price: {item['price']}", WHITE, x + 25, y + 190, font_small)

        # Instructions
        display_text("Press I to check collection", GREY, 50, HEIGHT - 50)
        
        if b_sell_toggle == False:
            display_text("Press B to Buy", GREY, 50, HEIGHT - 350)
        else:
            display_text("Press S to Sell", GREY, 50, HEIGHT - 350)
        
        display_text("Press ESC to return to the main game", GREY, WIDTH/2, HEIGHT - 350)
        display_text("Press < to see previous page", GREY, WIDTH/2, HEIGHT - 100)
        display_text("Press > to see next page", GREY, WIDTH/2, HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_s:
                    b_sell_toggle = not b_sell_toggle
                if event.key == pygame.K_b:
                    b_sell_toggle = not b_sell_toggle
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, item in enumerate(shop_items):
                    x = 200 + i * 400
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