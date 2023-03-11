#################################################
#################################################
####    Sebastian St Johnston - come219      ####
####    Untitled Card Game Version 0.02      ####
####                                         ####
####    Patch notes:                         ####
####    0.01: created gameloop, menus actv   ####
####    0.02: working deck of cards visually ####
####                                         ####
####                                         ####
####                                         ####
####                                         ####
####                                         ####
#################################################



##
#
#   INCLUDES for different apis, developments and libraries

##
#   pygame: Game Engine and Graphical display capabilities
##
from pygame_functions import *







#   END OF INCLUDE
##





########################
##  DEFINED COLOURS   ##
########################


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
newblue = (86,86,239)





##########################
#   Display parameters   #
##########################

#initalize pygame
pygame.init()

#display size constants
display_Width = 1920
display_Height = 1080

#gameDisplay defined
#tuple paramater for screen display size
gameDisplay = pygame.display.set_mode((display_Width,display_Height))

#display title
pygame.display.set_caption('Card Game')

#define time
clock = pygame.time.Clock()

#font defintion
#font=x(a, fontsize)
font = pygame.font.SysFont(None, 25)
font2 = pygame.font.SysFont(None, 50)
font3 = pygame.font.SysFont(None, 70)

#################################
#   message-to-screen functions #
#################################
def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [100, 100])

pass

def message_to_screen2(msg, color, x, y):
    screen_text = font2.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])

pass


def message_title(msg, color):
    screen_text = font3.render(msg, True, color)
    gameDisplay.blit(screen_text, [100, 100])

pass







#Loading in images into pygame variables
mainMenuBackgroundImg = pygame.image.load('mainmenubackground.png').convert()
mainmenubarImg = pygame.image.load('mainmenubar.png').convert()
playgamebuttonImg = pygame.image.load("playgamebutton.png").convert()
changedeckbuttonImg = pygame.image.load("changedeckbutton.png").convert()
settingsbuttonImg = pygame.image.load("settingsbutton.png").convert()
quitgamebuttonImg = pygame.image.load("quitgamebutton.png").convert()

changedeckbackgroundImg = pygame.image.load('changedeckbackground.png').convert()
changedeckbackgroundImg2 = pygame.image.load('changedeckbackgroundedit.png').convert()


oneroundImg = pygame.image.load('1round.png').convert()


#with open('currentdeck.txt') as currentdeckData:
currentdeckData = open("currentdeck.txt")
currentdecktext = currentdeckData.read()


#cardgame_
sizeofdeck = currentdecktext[9:]

newdeck = open('newdeck.txt')

#currentdecktxt = currentdeck.read()
#newdecktxt = newdeck.read()


cardaImg = pygame.image.load('carda.png').convert()
cardbImg = pygame.image.load('cardb.png').convert()
cardcImg = pygame.image.load('cardc.png').convert()

cardaImg = pygame.transform.scale(cardaImg, (100, 150))
cardbImg = pygame.transform.scale(cardbImg, (100, 150))
cardcImg = pygame.transform.scale(cardcImg, (100, 150))


#####################################
#   draw image function             #
#####################################
def drawImage(pygameimage, x, y):

    gameDisplay.blit(pygameimage,(x,y))

pass




###################################
#   quitgamebutton function     #
###################################
def quitgamebutton(x, y):

    gameDisplay.blit(quitgamebuttonImg,(x, y))
    
   
pass




#####################################
#   mainMenuBackground function     #
#####################################
def changedeckbackground(x, y):

    

    if(editdeckchange) == True:
        gameDisplay.blit(changedeckbackgroundImg2,(x, y))
    else:
        gameDisplay.blit(changedeckbackgroundImg,(x, y))
    

    
pass

#####################################
#   mainMenuBackground function     #
#####################################
def oneroundicon(x, y):

    gameDisplay.blit(oneroundImg,(x, y))

    
pass










#########################
#   drawCards function  #
#########################


#deck area coordinates
changedeckcardpos = [(100,100), (250,100), (400,100), (550,100),(700,100), (850,100), (1000,100), (1150,100),
                     (100,300), (250,300), (400,300), (550,300),(700,300), (850,300), (1000,300), (1150,300)]

#collection area coordinates
collectioncardpos =  [(100,800), (250,800), (400,800), (550,800),(700,800), (850,800), (1000,800), (1150,800)]


def drawCards(card, cardpos):

    if(card == 'a'):
        
        gameDisplay.blit(cardaImg, cardpos)
        
    elif(card == 'b'):
        
        gameDisplay.blit(cardbImg, cardpos)
        
    elif(card == 'c'):
        
        gameDisplay.blit(cardcImg, cardpos)



pass











##############################################################################################################################################
##############################################################################################################################################

##                                              GAME MENU CYCLE FUNCTIONS                                                                  ##

##############################################################################################################################################
##############################################################################################################################################





#########################
#   gameLoop function   #
#########################
def gameLoop():


    #print('gameLoop')

    #gameLoop parameters
    #gameRunning = True



##    #!main loop
##    while gameRunning:
##
##
##            #!event check
##            for event in pygame.event.get():
##                
##                #print(event)
##
##               if event.type == pygame.QUIT:
##                   #gameRunning = False
##                   isRunning = False
##                  
##                   
##               if event.type == pygame.KEYDOWN:
##            
##                    if event.key == pygame.K_q:
##                        #gameRunning = False
##                        isRunning = False
##                    if event.key == pygame.K_ESCAPE:
##                        #gameRunning = False
##                        isRunning = False
                        


            #!gameLoop instanced functions
            #gameBackground fill
            gameDisplay.fill(white)
            


        
pass







#############################
#   changeDeck function     #
#############################

#changedeck function boolean menu variables
editdeckchange = False
noteditingdeckchange = False
clearselectdeckchange = False

olddeck = []





def changeDeckMenu():

    #print('changedeckmenu')

    global gameMenu
    global sizeofdeck
    global editdeckchange
    global noteditingdeckchange
    global clearselectdeckchange
    

    
    #print(olddeck)

    
    
    #!event check
    for event in pygame.event.get():
                            
                        #print(event)

        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()




        elif event.type == pygame.MOUSEBUTTONDOWN:

            if(editdeckchange) == True:

                pos = pygame.mouse.get_pos()

                print(pos)

                if 
                            
                                  
                                   




        elif event.type == pygame.KEYDOWN:



            #If actively editing
            if(editdeckchange) == True:
                
                if event.key == pygame.K_s:
                    
                    noteditingdeckchange = True
                    editdeckchange = False
                    clearselectdeckchange = False

                    
                    #save new edit

                    #write sizeofdeck to the text file

                    
                    print('saved selection!')
                    


                if event.key == pygame.K_c:
                    
                    noteditingdeckchange = False
                    clearselectdeckchange = True

                    sizeofdeck = ""
                    #move the deck to 
                    
                    print('clear selection')





                if event.key == pygame.K_z:
                    
                    noteditingdeckchange = False
                    clearselectdeckchange = False
                    editdeckchange = False


                    #undo previous action    --> which requires to save the action made --> save old sizeofdeck into an array that it may refer back to
                    sizeofdeck = olddeck[0]
                    
                    
                    print('cancel edit!')



                
                
                          










            #initate Editing or quit editing
                    
            if event.key == pygame.K_ESCAPE:

                #are u sure u want to quit / save
                
                
                sizeofdeck = currentdecktext[9:]  #wrong command ?
                
                editdeckchange = False
                noteditingdeckchange = False
                clearselectdeckchange = False

                print('Return to gameMenu')

                
                gameMenu = 1
                                                           
            if event.key == pygame.K_e:
                
                editdeckchange = True
                noteditingdeckchange = False
                clearselectdeckchange = False

                olddeck.append(sizeofdeck)
                
                print('edit selection')
    
            
                






    
    #read decks
    #read cards in deck
    #read card collection
    
    #currentdeck.read(1, len(currentdeck))

    #for i in currentdecktext.len():
        
    
    
    #create new deck in edit
    #newdeck.write()
    
    #move cards around
                
    #change decks, ask to save

    #calculate deck statss
                
    #only replace deck in save
    



    #gameBackground fill
    gameDisplay.fill(black)


    
    
    #mainmenu background
    changedeckbackground(0, 0)


    #draw cards in the deck
    for i, d in enumerate(sizeofdeck):

        p = changedeckcardpos[i]
        drawCards(d,p)
        #print(d)


    #draw cards in the collection
    



    if(editdeckchange) == True:
        message_to_screen2("Editing Deck:", newblue, 1400, 500)

    if(noteditingdeckchange) == True:
        message_to_screen2("Saved Deck Edit!", newblue, 1400, 500)
        
    if(clearselectdeckchange) == True:
        message_to_screen2("Cleared Deck!", newblue, 1650, 500)
        
    

    #print(sizeofdeck)

    message_to_screen(sizeofdeck, red)
    #message_to_screen(currentdecktext, red)
    
    #message_to_screen(newdeck, red)

    


pass





























#########################
#   mainMenu function   #
#########################
def mainMenu():


    #print('mainMenu')

    global gameMenu

    #!event check
    for event in pygame.event.get():
                            
                        #print(event)

        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()
                            
                                  
                                   
        elif event.type == pygame.KEYDOWN:
                            
            if event.key == pygame.K_q:
                #are u sure prompt then quit
                print('QUIT: by quit key!')
                quitgame()
                                                 
                                        
            if event.key == pygame.K_ESCAPE:
                #are u sure prompt then quit
                print('QUIT: by escape!')
                quitgame()
                                



            if event.key == pygame.K_d:
                print('change deck selection!')
                
                gameMenu = 3



                
                                      
            if event.key == pygame.K_g:
                print('Enter game type selection!')
                
                gameMenu = 2





            if event.key == pygame.K_s:
                print('Enter setting selection!')
                
                gameMenu = 4



                

    #gameBackground fill
    gameDisplay.fill(black)


    #mainmenu background
    drawImage(mainMenuBackgroundImg, 0, 0)

    message_title("Untitled Card Game", red)

   

    #mainmenu bar // # 1060, 20
    drawImage(mainmenubarImg, 860, 280)
    drawImage(playgamebuttonImg, 910, 330)
    drawImage(changedeckbuttonImg, 910, 490)
    drawImage(settingsbuttonImg, 910, 650)



    #display commands to select menu
    message_to_screen2("G", newblue, 1300, 380)
    message_to_screen2("D", newblue, 1380, 550)
    message_to_screen2("S", newblue, 1100, 700)
    


    

pass          





























#########################################
#   game type selection menu function   #
#########################################
def gametypeMenu():

    global gameMenu

    #!event check
    for event in pygame.event.get():
                            
                        #print(event)

        if event.type == pygame.QUIT:
            print('QUIT: by execution!')
            quitgame()
                            
                                  
                                   
        elif event.type == pygame.KEYDOWN:
                                                 
                                        
            if event.key == pygame.K_ESCAPE:
                print('Return to mainmenu!')
                gameMenu = 1

            if event.key == pygame.K_1:
                print('Starting 1 round game')
                

            if event.key == pygame.K_2:
                print('Starting full game')
                
                                


    #gameBackground fill
    gameDisplay.fill(black)


    #mainmenu background
    drawImage(mainMenuBackgroundImg, 0, 0)

     #one round icon
    oneroundicon(100, 30)



pass





##############################################################################################################################################
##############################################################################################################################################

##                                              MAIN SYSTEM FUNCTIONS                                                                       ##

##############################################################################################################################################
##############################################################################################################################################



#####################
#   Quit function   #
#####################
def quitgame():
    
    isRunning = False
    pygame.display.quit()
    pygame.quit()


pass



#####################
#   Main function   #
#####################
def main():

   

    

    #boolean to run
    isRunning = True

    
    global gameMenu
    
    #gameMenu
    gameMenu = 1
    
    try:

        
        while isRunning:

            #print(gameMenu)
            
            # 1 = mainmenu, 2 = gametype selection, 3 = change deck, 4 = settings, 5 = game1, 6 = game2, 7 = result page
            #gameMenu check to switch gamemenu

            ##MAIN MENU##
            if gameMenu == 1:
                mainMenu()

            ##GAME TYPE##
            elif gameMenu == 2:
                gametypeMenu()

            ##CHANGE DECK##
            elif gameMenu == 3:
                changeDeckMenu()


            ##SETTINGS##
            elif gameMenu == 4:
                mainMenu()


            ##GAME 1##
            elif gameMenu == 5:
                break
    

            ##GAME 2##
            elif gameMenu == 6:
                gameLoop()

            ##CHECK FOR EXIT IF NOT RUNNING##
            if isRunning == False:
                break





            #display update function
            pygame.display.flip()

            #display tickrate
            clock.tick(30)


            
            
    except SystemExit:
        #quit message
        message_to_screen("Quit game!", red)
        pygame.display.update()
        pygame.display.quit()
        pygame.quit()
    finally:
        currentdeckData.close()
        newdeck.close()

    
pass



#intial code
if __name__ == '__main__':

    
    print('Ran successfully!')
    main()


