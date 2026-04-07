import pygame
import random
import pygame
import json
import os

GREEN = (5, 130, 5)
GREEN_LIGHT = (55, 130, 55)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
BLACK = (0, 0, 0)


class Player():

    def __init__(self, _name, _stack):
        self.name = _name
        self.stack = _stack

class Bet():

    def __init__(self, _player, _spot, _wager):
        self.player = _player
        self.spot = _spot
        self.wager = _wager

    def payout(self, _ball):
        if _ball in self.spot.numbers:
            _payout = self.spot.pay_rate * self.wager
            return _payout
        
        else:
            return False

class Spot():

    def __init__(self, _name, _pay_rate, _numbers, _origin_x=0, _origin_y=0, _width=35, _height=35, _child=None):
        self.name = _name
        self.pay_rate = _pay_rate
        self.numbers = _numbers
        self.origin_x = _origin_x
        self.origin_y = _origin_y
        self.width = _width
        self.height = _height
        self.child = _child

class Button():

    def __init__(self, _table, _type, _text_bool, _box_bool, _origin_x, _origin_y, _width, _height, _text=None, _child=None, _input=None, _color=WHITE, _hover_color=GREY, _is_active=True):
        self.table = _table
        self.type = _type
        self.text = _text
        self.text_bool = _text_bool
        self.box_bool = _box_bool

        self.origin_x = _origin_x
        self.origin_y = _origin_y
        self.width = _width
        self.height = _height

        self.child = _child
        self.input = _input
        self.color = _color

        self.is_active = _is_active
        self.hover_color = _hover_color
        self.is_clicked = False
        self.player = None

        if self.type == "spot":
            self.width = self.child.width * self.table.width_win
            self.height = self.child.height * self.table.height_win 
        
    def origin(self):

        if self.type == "spot" and self.child:
            x = int(self.child.origin_x * self.table.width_win)
            y = int(self.child.origin_y * self.table.height_win)

        else:
            x = int(self.origin_x * self.table.width_win)
            y = int(self.origin_y * self.table.height_win)

        return (x, y)
        

    def isHover(self, _mouse):
        x, y = self.origin()
        _test = x < _mouse[0] < x + self.width and y < _mouse[1] < y + self.height

        if _test and self.is_active:
            color = self.hover_color

            if self.type == "spot" and self.table.bet_lock:
                self.text_bool = True
                self.box_bool = True

            if self.type == "spin" or self.type == "player":
                self.text_bool = True
                self.box_bool = True

            if self.table.is_click:                                                    # click listener passthrough
                self.clickResponse()
                
        else:                                                                  # un-hover button
            color = self.color
            if self.type == "spot" or self.type == "spin":
                self.text_bool = False
                self.box_bool = False
            if self.type == "player" and self.child != self.table.current_player:
                self.box_bool = False

        return color, x, y

    def clickResponse(self):
        if self.table.current_player:  
            _text = self.table.current_player.name
        else:
            _text = None

        if self.type == "textBox":
            self.table.key_catch = True
            self.table.input_select = self
            self.color = GREY

        if self.type == "Add Player":
            self.table.key_catch = False
            if self.table.input_select:
                self.table.addPlayer(self.table.input_select.text)
                self.table.input_select.clearText()
                self.child.color = WHITE
            
        if self.type == "Bet":
            self.table.key_catch = False
            if self.table.input_select and self.table.input_select.text.isnumeric():
                self.table.current_wager = int(self.table.input_select.text)
                self.child.color = GREEN
                self.table.bet_lock = True

        if self.type == "spin":
            self.table.key_catch = False
            self.table.wheel.spin()
            self.table.input_select = None

        if self.type == "payout":
            self.box_bool = False
            self.text_bool = False
            self.is_active = False
            self.text = []
            for button in self.table.buttons:
                if button.type != "payout":
                    button.is_active = True

        if self.type == "spot":
            self.table.key_catch = False
            if self.table.current_wager and self.table.current_player:
                self.table.spot_select = self.child
                self.table.addBet(self.child)
                for button in self.table.buttons:
                    if button.type == "player":
                        button.text = "{}:    ${}".format(button.child.name, button.child.stack)

        if self.type == "player":
            if self.table.current_player != self.child:
                self.table.current_player = self.child
                for button in self.table.buttons:
                    if button.type == "player":
                        self.box_bool = False
                self.box_bool = True

    def clearText(self):
        self.color = WHITE
        self.input = None
        self.text = None
        self.text_bool = False
        self.table.input_select = None
        self.table.key_catch = False


class Table(pygame.sprite.Sprite):

    def __init__(self, _height_table, _height_win, _width_table, _width_win):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('assets', 'roulette_table_trans.png'))

        # input variables
        self.height_table = _height_table
        self.height_win = _height_win
        self.width_table = _width_table
        self.width_win = _width_win

        # prescribed variables
        self.players = []
        self.current_player = None
        self.current_wager = 0
        self.bets = []
        self.bet_lock = False
        self.key_catch = False
        self.is_click = False
        self.input_select = None # holds textbox button to recieve input keys
        self.spot_select = None
        self.wheel = None
        self.payouts = []               

        self.bet_input = Button(self, "textBox", False, True, 0.5, 0.5, 100, 50)
        self.player_input = Button(self, "textBox", False, True, 0.5, 0.4, 150, 50)                            
        self.bet_button = Button(self, "Bet", True, True, 0.8, 0.5, 150, 50, "Bet", self.bet_input)
        self.add_player_button = Button(self, "Add Player", True, True, 0.8, 0.4, 150, 50, _text="Add Player", _child=self.player_input)
        self.spin_button = Button(self, "spin", False, False, 0.1, 0.2, 250, 100, "SPIN")
        self.payout_button = Button(self, "payout", False, False, 0.25, 0.9, int(0.5*self.width_win), int(0.05*self.height_win), [] , _is_active=False)
        self.buttons = [self.bet_input, 
                        self.player_input, 
                        self.bet_button, 
                        self.add_player_button,
                        self.spin_button,
                        self.payout_button] 
                    
    def addWheel(self, _wheel):
        if not self.wheel: 
            self.wheel = _wheel

    def addPlayer(self, _name, _stack=100):
        _player = Player(_name, _stack)
        self.players.append(_player)
        self.current_player = _player
        self.buttons.append(Button(self, "player", True, True, 0.6, 0.05*len(self.players), 0.35*self.width_win, 0.05*self.height_win, "{}:    ${}".format(_player.name, _player.stack), _player))
        self.payout_button.origin_y = 1 - (0.05*len(self.players))
        self.payout_button.height = int(0.05*len(self.players)*self.height_win)

    def addBet(self, _spot):
        _wager = self.current_wager

        if self.current_player and self.current_player.stack > _wager:
            self.current_player.stack -= int(_wager)
            _bet = Bet(self.current_player, _spot, _wager)
            self.bets.append(_bet)
            self.bet_lock = False

        self.bet_input.clearText()

    def calculateWinnings(self, _ball):
        _winnings = {}

        for bet in self.bets:
            _payout = bet.payout(_ball)
            if bet.player.name in list(_winnings.keys()):
                _name = bet.player.name

            else:
                _name = bet.player.name
                _winnings[_name] = {"Bets": 0,
                                    "Wins": 0}
            _winnings[_name]["Bets"] += bet.wager
            
            if _payout:
                _winnings[_name]["Wins"] += _payout
                bet.player.stack += _payout + bet.wager
                self.payouts.append(bet)
        return _winnings

    def payout(self, _ball):
        for button in self.buttons:
            button.is_active = False
        self.payout_info = {}
        self.payouts = []
        if len(self.bets) > 0:
            _winnings = self.calculateWinnings(_ball)
            for player in self.players:
                if player.name in list(_winnings.keys()):
                    _wins = _winnings[player.name]["Wins"]
                    _bets = _winnings[player.name]["Bets"]
                    _text = "{} wagered {} and won {}".format(player.name, _bets, _wins)
                    self.payout_button.text.append(_text)

            self.bets = []
            self.payout_button.box_bool = True
            self.payout_button.text_bool = True
            self.payout_button.is_active = True


class Wheel(pygame.sprite.Sprite):

    def __init__(self, _table, _spin_speed=10, _delay_max=300):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('assets', 'roulette_wheel.png'))
        self.table = _table
        self.ball = None
        self.is_spinning = False
        self.spin_speed = _spin_speed
        self.delay_max = _delay_max
        self.delay_current = 0
        self.angle = 0

        self.spots = {}

        with open('spots.json') as f: # add spots from json library
            _spots = json.load(f)
        for spot, values in _spots.items():
            self.spots[spot] = Spot(spot, values['pay_rate'], 
                                    values['numbers'])
            if 'origin' in list(values.keys()):
                _spot = self.spots[spot]
                _spot.origin_x = values['origin']['x']
                _spot.origin_y = values['origin']['y']
                _spot.width = values['size']['x']
                _spot.height = values['size']['y']

                # _preview_wid = 0.1*self.table.width_win
                # _preview_hig = 0.1*self.table.height_win
                # _preview_x = _spot.origin_x - _preview_wid//2
                # _preview_y = _spot.origin_x - _preview_hig//2
                # _spot.child = Button(self.table, "preview", False, False, _preview_x, _preview_y, _preview_wid, _preview_hig, None, None, False)
                self.table.buttons.append(Button(self.table, "spot", False, True, _spot.origin_x, _spot.origin_y, _spot.width, _spot.height, None, _spot))

        for spot in range(1,37):
            self.spots[str(spot)] = Spot(str(spot), _pay_rate=35, _numbers=[spot])
            _spot = self.spots[str(spot)]
            _spot.width = 0.058
            line_width = 0.0058
            _spot.height = 0.068

            _spot.num = _spot.numbers[0]
            _spot.text = str(_spot.num)
            _spot.column = (_spot.num - .333) // 3

            _spot.origin_x = 0.105 + (_spot.column * _spot.width) + (_spot.column * line_width)
            

            if _spot.numbers[0] % 3 == 1:
                _spot.origin_y = 0.763

            elif _spot.numbers[0] % 3 == 2:
                _spot.origin_y = 0.69

            elif _spot.numbers[0] % 3 == 0:
                _spot.origin_y = 0.615

            self.table.buttons.append(Button(self.table, "spot", True, True, _spot.origin_x, _spot.origin_y, _spot.width, _spot.height, _text=_spot.text, _child=_spot))


    def spin(self):
        # if self.delay_current == 0:
        # self.is_spinning = False
        self.ball = random.randint(0,37)
        self.table.payout(self.ball)
        for button in self.table.buttons:
                    if button.type == "player":
                        button.text = "{}:    ${}".format(button.child.name, button.child.stack)

        # else:
        #     self.angle += self.spin_speed
        #     delay_current -= 1

WIDTH, HEIGHT = 800, 700
TABLE_WIDTH, TABLE_HEIGHT = 750, 300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette")

GREEN = (5, 130, 5)
GREEN_LIGHT = (55, 130, 55)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
BLACK = (0, 0, 0)

FPS = 60

TABLE = Table(TABLE_HEIGHT, HEIGHT, TABLE_WIDTH, WIDTH)
WHEEL = Wheel(TABLE)
TABLE.addWheel(WHEEL)

TABLE.image = pygame.transform.scale(TABLE.image, (TABLE_WIDTH, TABLE_HEIGHT))
WHEEL.image = pygame.transform.scale(WHEEL.image, (WIDTH//2,WIDTH//2))


def drawButtons():
    mouse = pygame.mouse.get_pos()

    for button in TABLE.buttons:
        if button.is_active:
            color, x, y = button.isHover(mouse)  # button hover listener
            if button.type == "payout":
                button.text_bool = True

            if button.box_bool: # draw button rectangle
                pygame.draw.rect(WIN, color, [x, y, button.width, button.height])

            if button.text_bool: # draw button text
                if button.type == "payout":
                    i = 0
                    for _text in button.text:
                        _font = pygame.font.SysFont('Corbel',35)
                        text = _font.render(_text, True, BLACK)
                        (_x, _y) = button.origin()
                        _y_offset = 0.05*TABLE.height_win*i
                        _y = _y + _y_offset
                        WIN.blit(text, (_x, _y))
                        i += 1
                else:
                    _text = button.text
                    _font = pygame.font.SysFont('Corbel',35)
                    text = _font.render(_text, True, BLACK)
                    WIN.blit(text, button.origin())


def drawWindow():
    # draw table
    WIN.fill(GREEN)
    WIN.blit(TABLE.image, ((WIDTH/2-TABLE_WIDTH/2), (HEIGHT-TABLE_HEIGHT)))
    WIN.blit(WHEEL.image, (1,1))

    # draw bets
    if len(TABLE.bets) > 0:
        _string = "Bets: {}".format(len(TABLE.bets))
        _font = pygame.font.SysFont('Corbel',35)
        _text = _font.render(_string, True, WHITE)
        WIN.blit(_text, (0, 0))

    # draw stacks
    # if len(TABLE.players) > 0:
    #     count = 0
    #     for player in TABLE.players:
    #         count += 1
    #         _font = pygame.font.SysFont('Corbel',35)
    #         _name = _font.render(player.name+": ", True, WHITE)
    #         _stack = _font.render("$"+str(player.stack), True, WHITE)
    #         WIN.blit(_name,(WIDTH//2+50, 50*count))
    #         WIN.blit(_stack,(WIDTH//2+250, 50*count))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    is_click = False
    
    while run:
        clock.tick(FPS)
        TABLE.is_click = False
        if len(TABLE.players) > 0 and not TABLE.current_player:
            TABLE.current_player = TABLE.players[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN: # mouse click listener
                TABLE.is_click = True

            if event.type == pygame.KEYDOWN: # key listener
                key = pygame.key.name(event.key)

                if TABLE.key_catch and TABLE.input_select:
                    TABLE.input_select.text_bool = True

                    if len(key) == 1:
                        if TABLE.input_select.input:
                            TABLE.input_select.input += key

                        else:
                            TABLE.input_select.input = key

                    elif key == "backspace":
                        if TABLE.input_select.input:
                            TABLE.input_select.input = TABLE.input_select.input[:-1]

                        else:
                            TABLE.input_select.input = None

                    TABLE.input_select.text = TABLE.input_select.input
            

        drawWindow()
        drawButtons()

        pygame.display.update()

    pygame.quit()

if __name__=="__main__":
    main()