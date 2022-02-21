import sys,pygame,random

#Variables
class variables:
    screen_height,screen_width = 780,1000 #dimensions of viewport
    ball_speed_x,ball_speed_y = 7 * random.choice((-1,1)),7 * random.choice((-1,1)) #speed of ball in x and y dimensions
    player_speed = 0 #speed of player paddle
    opponent_speed = 7 #speed of computer paddle
    player_score,opponent_score = 0,0 #player and computer scores
    score_time = 0 #time since player or computer scores point

    intro,game,outro = True,True,True #booleans to run pages
v = variables()

#components
class components:
    play_button = pygame.Rect(v.screen_width/2-150,v.screen_height/2+30, 300,50) #play button on start page and main menu button on win page
    quit_button = pygame.Rect(v.screen_width/2-150,v.screen_height/2+180, 300,50) #quit button on both start and win pages
    quit_button_small = pygame.Rect(v.screen_width-85,5,80,20) #quit button on game page
    restart_button_small = pygame.Rect(v.screen_width-170,5,80,20) #restart button on game page

    ball = pygame.Rect(v.screen_width/2 - 10, v.screen_height/2 + 30 - 10, 20, 20) #Rectangle for ball
    player = pygame.Rect(10,v.screen_height/2 + 30 - 60,10,120) #Rectangle for player
    opponent = pygame.Rect(v.screen_width-20,v.screen_height/2 + 30 - 60,10,120) #Rectangle for opponent
    color = [ 
        pygame.Color(0,0,0), #black
        pygame.Color(255,255,255), #white
        pygame.Color(25,40,47), #dark_blue
        pygame.Color(179,48,48), #red
        pygame.Color(161,181,125), #dark_mint
        pygame.Color(211,236,167) #mint
    ] #colors
c = components()

#functions
class functions:
    def player_movement(self): #player movment logic
        c.player.y += v.player_speed 

        #stops player from moving off viewport
        if c.player.top <= 30:
            c.player.top = 30
        if c.player.bottom >= v.screen_height:
            c.player.bottom = v.screen_height
    
    def opponent_ai(self): #computer movement logic
        #if ball moves above upper edge of computer paddle then computer paddle moves up and vice-versa
        if c.opponent.top < c.ball.y:
            c.opponent.top += v.opponent_speed
        if c.opponent.bottom > c.ball.y:
            c.opponent.bottom -= v.opponent_speed
        
        #stops computer from moving off viewport
        if c.opponent.top <= 30:
            c.opponent.top = 30
        if c.opponent.bottom >= v.screen_height:
            c.opponent.bottom = v.screen_height
    
    def ball_movement(self): #ball movement logic
        c.ball.x += v.ball_speed_x
        c.ball.y += v.ball_speed_y

        #reversing y dimension of ball speed when ball hits top and bottom boundaries
        if c.ball.top <= 30 or c.ball.bottom >= v.screen_height:
            v.ball_speed_y *= -1

        #opponent gets point if ball touches left boundary and player gets point if ball touches right boundary
        if c.ball.left <= 0:
            v.opponent_score += 1
            v.score_time = pygame.time.get_ticks() #time of scoring
        if c.ball.right >= v.screen_width:
            v.player_score +=1
            v.score_time = pygame.time.get_ticks() #time of scoring
        
        #reversing y dimension of ball speed when ball touches paddles
        if c.ball.colliderect(c.player) or c.ball.colliderect(c.opponent):
            v.ball_speed_x *= -1
    
    def ball_start(self): #ball resetting logic
        current_time = pygame.time.get_ticks() #gets current time

        c.ball.center = (v.screen_width/2,v.screen_height/2 + 30) #resets ball position to center of screen

        #if the diffrence between current time and the time when point is scored is less than 1800ms ball doesn't move
        if current_time - v.score_time < 1800:
            v.ball_speed_x,v.ball_speed_y = 0,0
        else:
            v.ball_speed_x = 7 * random.choice((1,-1))
            v.ball_speed_y = 7 * random.choice((1,-1))
            v.score_time = 0 
    
    def gamescreen(self): #to go to the game screen
        v.intro = False
        v.game = True
        gameloop()

    def reset(self): #to reset the scores and ball position
        v.player_score,v.opponent_score = 0,0
        self.ball_start()
        startpage()
    
    def win_logic(self): #winning logic
        #when either player or computer scores 10 points game ends
        if v.player_score >= 10 or v.opponent_score >= 10:
            v.game = False
            v.outro = True
            winpage()
f = functions()

#pygame initialiser
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((v.screen_width,v.screen_height))
pygame.display.set_caption('Pong by HD')

#fonts
small_font = pygame.font.Font("assets\Montserrat-Regular.ttf",16) #small 16
medium_font = pygame.font.Font("assets\Montserrat-Regular.ttf",30) #medium 30
large_font = pygame.font.Font("assets\Montserrat-Regular.ttf",80) #large 80

#start page
def startpage():
    while v.intro:
        #loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #forward to gamescreen
                if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+30 <= mouse[1] <= v.screen_height/2+80:
                    f.gamescreen()
                
                #quit
                if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+180 <= mouse[1] <= v.screen_height/2+230:
                    pygame.quit()
                    sys.exit()
        
        mouse = pygame.mouse.get_pos() #stores mouse position

        # Screen Design
        screen.fill(c.color[3]) #background

        #title
        title = large_font.render("Pong!",True,c.color[2])
        screen.blit(title,(v.screen_width/2-110, v.screen_height/2-250))

        #subtitle
        subtitle = medium_font.render("by Hrishikesh Dubey",True,c.color[2])
        screen.blit(subtitle,(v.screen_width/2-150,v.screen_height/2-150))

        #responsive buttons
        #play button
        if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+30 <= mouse[1] <= v.screen_height/2+80:
            pygame.draw.rect(screen,c.color[5],c.play_button)
            play_text = medium_font.render("Play",True,c.color[2])
            screen.blit(play_text,(v.screen_width/2-30,v.screen_height/2+5+30))
        else:
            pygame.draw.rect(screen,c.color[2],c.play_button)
            play_text = medium_font.render("Play",True,c.color[4])
            screen.blit(play_text,(v.screen_width/2-30,v.screen_height/2+5+30)) 
        
        #quit button
        if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+180 <= mouse[1] <= v.screen_height/2+230:
            pygame.draw.rect(screen,c.color[5],c.quit_button)
            quit_text = medium_font.render("Quit",True,c.color[2])
            screen.blit(quit_text,(v.screen_width/2-30,v.screen_height/2+150+5+30)) 
        else:
            pygame.draw.rect(screen,c.color[2],c.quit_button)
            quit_text = medium_font.render("Quit",True,c.color[4])
            screen.blit(quit_text,(v.screen_width/2-30,v.screen_height/2+150+5+30))

        pygame.display.flip()
        clock.tick(15) #15 frames per second

def gameloop():
    while v.game:
        #loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #pressing a key
            if event.type == pygame.KEYDOWN:
                #pressing down arrow
                if event.key == pygame.K_DOWN:
                    v.player_speed += 7
                
                #pressing up arrow
                if event.key == pygame.K_UP:
                    v.player_speed -= 7
            
            #letting go of a key
            if event.type == pygame.KEYUP:
                #for down key
                if event.key == pygame.K_DOWN:
                    v.player_speed -= 7
                
                #for up key
                if event.key == pygame.K_UP:
                    v.player_speed += 7
            
            #on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #restart game
                if v.screen_width-170 <= mouse[0] <= v.screen_width-90 and 5 <= mouse[1] <= 25:
                    f.reset()
                
                #quit
                if v.screen_width-85 <= mouse[0] <= v.screen_width-5 and 5 <= mouse[1] <= 25:
                    pygame.quit()
                    sys.exit()
        
        #calling game logic functions
        f.player_movement()
        f.ball_movement()
        f.opponent_ai()

        mouse = pygame.mouse.get_pos() #stores mouse position


        #screen decoration
        screen.fill(c.color[2])
        pygame.draw.rect(screen,c.color[3],c.player)
        pygame.draw.rect(screen,c.color[3],c.opponent)
        pygame.draw.ellipse(screen,c.color[4],c.ball)
        pygame.draw.aaline(screen,c.color[4],(0,30),(v.screen_width,30))

        #responsive buttons
        #quit button
        if v.screen_width-85 <= mouse[0] <= v.screen_width-5 and 5 <= mouse[1] <= 25:
            pygame.draw.rect(screen,c.color[5],c.quit_button_small)
        else:
            pygame.draw.rect(screen,c.color[4],c.quit_button_small)
        quit_text = small_font.render("Quit",True,c.color[2])
        screen.blit(quit_text,(v.screen_width-65,4))

        #Restart button
        if v.screen_width-170 <= mouse[0] <= v.screen_width-90 and 5 <= mouse[1] <= 25:
            pygame.draw.rect(screen,c.color[5],c.restart_button_small)
        else:
            pygame.draw.rect(screen,c.color[4],c.restart_button_small)
        restart_text = small_font.render("Restart",True,c.color[2])
        screen.blit(restart_text,(v.screen_width-162,4))

        f.win_logic()

        #calls function only if ball_start>0
        if v.score_time:
            f.ball_start()
        
        #showing scores
        player_score = medium_font.render(f"{v.player_score}",True,c.color[4])
        screen.blit(player_score,(v.screen_width/2-50, v.screen_height/2+30))
        opponent_score = medium_font.render(f"{v.opponent_score}",True,c.color[4])
        screen.blit(opponent_score,(v.screen_width/2+35, v.screen_height/2+30))

        pygame.display.flip()
        clock.tick(60) #60 frames per second

def winpage():
    v.intro = True
    while v.outro:
        #loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #reset game
                if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+30 <= mouse[1] <= v.screen_height/2+80:
                    v.outro = False
                    f.reset()

                #quit game
                if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+180 <= mouse[1] <= v.screen_height/2 +230:
                    pygame.quit()
                    sys.exit()
        
        mouse = pygame.mouse.get_pos() #get mouse position

        #screen design
        screen.fill(c.color[3])
        #showing winner according to score
        if v.player_score>=10:
            win_text = large_font.render("Player Wins!",True,c.color[2])
            screen.blit(win_text,(v.screen_width/2-200,v.screen_height/2-250))
        else:
            win_text = large_font.render("Computer Wins!",True,c.color[2])
            screen.blit(win_text,(v.screen_width/2-300,v.screen_height/2-250))

        #responsive buttons
        #main menu button
        if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+30 <= mouse[1] <= v.screen_height/2+80:
            pygame.draw.rect(screen,c.color[5],c.play_button)
            menu_text = medium_font.render("Main Menu",True,c.color[2])
            screen.blit(menu_text,(v.screen_width/2-78,v.screen_height/2+5+30))
        else:
            pygame.draw.rect(screen,c.color[2],c.play_button)
            menu_text = medium_font.render("Main Menu",True,c.color[4])
            screen.blit(menu_text,(v.screen_width/2-78,v.screen_height/2+5+30)) 
        
        #quit button
        if v.screen_width/2-150 <= mouse[0] <= v.screen_width/2+150 and v.screen_height/2+180 <= mouse[1] <= v.screen_height/2+230:
            pygame.draw.rect(screen,c.color[5],c.quit_button)
            quit_text = medium_font.render("Quit",True,c.color[2])
            screen.blit(quit_text,(v.screen_width/2-30,v.screen_height/2+150+5+30)) 
        else:
            pygame.draw.rect(screen,c.color[2],c.quit_button)
            quit_text = medium_font.render("Quit",True,c.color[4])
            screen.blit(quit_text,(v.screen_width/2-30,v.screen_height/2+150+5+30))

        pygame.display.flip()
        clock.tick(15) #15 frames per second

startpage()