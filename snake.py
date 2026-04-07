import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox

WIDTH = 1920
HEIGHT = 1080

# Increase the playable area and grid size
width = 600  # Increased from 500
height = 600  # Increased from 500

cols = 35  # Increased from 25
rows = 30  # Increased from 20

class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(0,255,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        

class cube_food():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(0,255,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


class snake():
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        #pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_ESCAPE]:
                    import cardgame
                    cardgame.main()
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

            # Wrap around logic
            if c.pos[0] >= rows:
                c.pos = (0, c.pos[1])
            elif c.pos[0] < 0:
                c.pos = (rows - 1, c.pos[1])
            if c.pos[1] >= rows:
                c.pos = (c.pos[0], 0)
            elif c.pos[1] < 0:
                c.pos = (c.pos[0], rows - 1)

    def move_screen_death(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_ESCAPE]:
                    import cardgame
                    cardgame.main()
                if keys[pygame.K_p]:
                    print('pause game')
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



def redrawWindow():

    global win
    win.fill((0,0,0))
    
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    font = pygame.font.SysFont('', 35)
    score_text = font.render(f'Score: {len(s.body)}', True, (255, 0, 0))
    menu_text = font.render(f'Press ESC to return to the mainmenu', True, (255, 0, 0))
    cash_out_text = font.render(f'Press C to Cash out', True, (255, 0, 0))
    pause_text = font.render(f'Press P to Pause', True, (255, 0, 0))
    paused__text = font.render(f'Game is paused.', True, (0, 255, 0))
    game_type_text = font.render(f'Press G to Change Game Type', True, (255, 0, 0))
    food_text = font.render(f'Food: x, y', True, (255, 0, 0))
    balance_num = len(s.body) % 10
    balance_text = font.render(f'Balance: ${balance_num}', True, (0, 255, 0))
    text_rect0 = score_text.get_rect(center=(WIDTH // 5, HEIGHT - 200))
    text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT - 250))
    text_rect2 = menu_text.get_rect(center=(WIDTH // 5, HEIGHT - 150))
    text_rect3 = pause_text.get_rect(center=(WIDTH // 8, HEIGHT - 250))
    text_rect4 = paused__text.get_rect(center=(WIDTH // 8, 500))
    text_rect5 = food_text.get_rect(center=(WIDTH // 2, HEIGHT - 150))
    text_rect6 = balance_text.get_rect(center=(WIDTH - 300, HEIGHT - 250))
    text_rect7 = game_type_text.get_rect(center=(WIDTH - 300, HEIGHT - 150))
    win.blit(cash_out_text, text_rect0)
    win.blit(score_text, text_rect)
    win.blit(menu_text, text_rect2)
    win.blit(pause_text, text_rect3)
    win.blit(food_text, text_rect5)
    win.blit(balance_text, text_rect6)
    win.blit(game_type_text, text_rect7)
    
    
    pygame.display.update()
    pass



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (128,128,128), (x, 0),(x,w))
        pygame.draw.line(surface, (128,128,128), (0, y),(w,y))

    
    
def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, cols - 1)  # Use updated cols
        y = random.randrange(1, rows - 1)  # Use updated rows
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

def randomSnack_old(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
                continue
        else:
                break

    return (x,y)


def main():

    global s, snack, win
    
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    s = snake((255,0,0), (10,10))
    s.addCube()
    snack = cube(randomSnack(rows,s), color=(255,0,0))
    flag = True
    clock = pygame.time.Clock()
    pygame.font.init()
    

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        
        headPos = s.head.pos
        if headPos[0] >= cols or headPos[0] < 0 or headPos[1] >= rows or headPos[1] < 0:
            print("Score:", len(s.body))
            s.reset((10, 10))

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(255,0,0))
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print("Score:", len(s.body))
                s.reset((10,10))
                break
            
        redrawWindow()
    

main()
    

    