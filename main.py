from random import randint

import pygame
pygame.init()
pygame.mixer.init()
import math
from pygame import mixer
from pygame import time

class Ball():
    def __init__(self):
        self.ball_x = 315
        self.ball_y = 95
        self.ball_radius = 25
        self.velocity_y = 0
        self.velocity_x = 0
        self.key = pygame.key.get_pressed()
        self.basketball = pygame.image.load('assets/images/Basketball.jpeg').convert_alpha()
        self.basketball = pygame.transform.scale(self.basketball, (30, 30))
        self.basketball.set_colorkey((255, 255, 255))
    def launched_7(self):
        self.shot_x = self.ball_x
        self.shot_y = self.ball_y
        self.ball_y += self.velocity_y
        self.ball_x += self.velocity_x
        self.velocity_y = -7
        return self.shot_x,self.shot_y
    def launched_10(self):
        self.shot_x = self.ball_x
        self.shot_y = self.ball_y
        self.ball_y += self.velocity_y
        self.ball_x += self.velocity_x
        self.velocity_y = -10
        return self.shot_x, self.shot_y
    def ball_movement(self,key,ball_in_air):
        if ball_in_air:
            self.velocity_y += 0.18
            self.velocity_x += 0.05
            self.ball_y += self.velocity_y
            self.ball_x += self.velocity_x
            if key[pygame.K_a]:
                self.ball_x += -4
            elif key[pygame.K_d]:
                self.ball_x += 4
            elif key[pygame.K_w]:
                self.ball_y += -4
            elif key[pygame.K_s]:
                self.ball_y += 4
    def reset(self):
        self.ball_x = 315
        self.ball_y = 95
        self.velocity_x = 0
        self.velocity_y = 0



class Player():
    def __init__(self):
        self.new_ball_y = None
        self.new_ball_x = None
        self.hali_shooting = pygame.image.load('assets/images/Hali Shooting.jpeg').convert_alpha()
        # this is where haliburton shoots from
        self.hali_x = 200
        self.hali_y = 100
        self.hali_radius = 25
    def haliReset(self):
        self.hali_x = 200
        self.hali_y = 100
        self.hali_radius = 25



class GameState():
    def __init__(self):
        self.score_surface = None
        self.score = 0
        self.streak = 0
        self.lives = 3
        self.reset = 7
        self.SCREEN_HEIGHT = 400
        self.SCREEN_WIDTH = 800
        self.shot_clock = self.reset
        self.ball_in_air = False
        self.made_basket = True
        self.three_pointer = True
        self.shot_x = None
        self.shot_y = None
        self.is_paused = False
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.my_font = pygame.font.SysFont('Arial', 20)
        self.MY_TIMER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MY_TIMER_EVENT, 1000)
        self.result = pygame.font.SysFont('Arial', 30)
        self.make_effect = pygame.mixer.Sound("assets/sounds/Basketball Swish - Sound Effect.mp3")
        self.brick_effect = pygame.mixer.Sound(
            "assets/sounds/Throwing a brick through a window sound effect glass shattering sound.mp3")
        self.sunk_it_three = self.result.render('Swish! Three pointer', True, (0, 255, 0))
        self.sunk_it_two = self.result.render('Swish! Two pointer', True, (0, 255, 0))
        self.missed_it = self.result.render('Brick!', True, (255, 0, 0))
        self.run = True
        pygame.display.set_caption("Magnet Ball")
        self.paused_screen = pygame.Rect(0,0,800,400)
        self.paused_text = self.result.render("PAUSED", True, (255, 0, 255))
        self.ball = Ball()
        self.player = Player()
        self.background = pygame.image.load("assets/images/background.jpeg").convert()
        self.background = pygame.transform.smoothscale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.text_surface = self.my_font.render('Press Space to release, move ball with ASDW!', True, (255, 255, 0))
        self.hoop = pygame.image.load('assets/images/hoop.jpeg').convert()
        self.hoop = pygame.transform.scale(self.hoop, (75, 75))
        self.hoop.set_colorkey((255, 255, 255))
        self.clock = pygame.time.Clock()
        self.end_game = pygame.image.load('assets/images/Hali Celebration.jpeg').convert()
        self.end_game = pygame.transform.scale(self.end_game, (800, 400))
        pygame.display.update()
    def setBackground(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.text_surface, (15, 25))
        self.screen.blit(self.hoop,(700,60))
        self.screen.blit(self.player.hali_shooting, (self.player.hali_x, self.player.hali_y))
        self.screen.blit(self.ball.basketball, (self.ball.ball_x, self.ball.ball_y))
        self.end_text = self.result.render(f'GAME OVER Score: {self.score}', True, (255, 0, 0))
        score_surface = self.my_font.render(f'Score: {self.score}', True, (255, 255, 0))
        self.screen.blit(score_surface, (15, 55))
        lives_message = self.my_font.render(f"Lives: {self.lives}", True, (255, 255, 0))
        streak_message = self.my_font.render(f"Streak: {self.streak}", True, (255, 255, 0))
        self.screen.blit(lives_message, (110, 55))
        self.screen.blit(streak_message, (15, 85))
        pygame.draw.line(self.screen, (255, 255, 255), start_pos=(500, 0), end_pos=(500, 400))
        # draw a half circle as the three point line
        pygame.draw.arc(
            self.screen, (255, 255, 255), (350, 0, 400, 400), math.pi / 2, -math.pi / 2, 3)

    def getKey(self):
        self.key = pygame.key.get_pressed()
    def shotClock(self):
        shot_clock_text = self.my_font.render(f"Shot Clock: {self.shot_clock}", True, (255, 0, 255))
        self.screen.blit(shot_clock_text,(15,170))
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.is_paused = not self.is_paused
                    self.screen.blit(self.paused_text, (300, 150))
            if event.type == self.MY_TIMER_EVENT:
                self.shot_clock -= 1
    def ballMovement(self):
        if self.key[pygame.K_SPACE] and not self.ball_in_air and self.ball.ball_y < 150:
            self.shot_x,self.shot_y = self.ball.launched_7()
            self.ball_in_air = True
        if self.key[pygame.K_SPACE] and not self.ball_in_air and self.ball.ball_y > 150:
            self.shot_x,self.shot_y = self.ball.launched_10()
            self.ball_in_air = True
        if self.ball_in_air:
            self.ball.ball_movement(self.key, self.ball_in_air)
    def countScore(self):
        if self.shot_clock == 0:
            self.lives -= 1
            self.streak = 0
            self.shot_clock = self.reset
        if self.ball.ball_x > 800 or self.ball.ball_x < -50 or self.ball.ball_y < -250 or self.ball.ball_y > 400:
            self.brick_effect.stop()
            self.brick_effect.play()
            self.ball.reset()
            self.player.haliReset()
            self.lives -= 1
            self.streak = 0
            self.shot_clock = self.reset
            self.made_basket = False
            self.ball_in_air = False
        ball_center_x = self.ball.ball_x + 15
        ball_center_y = self.ball.ball_y + 15
        if (725 < ball_center_x < 775) and (65 < ball_center_y < 95):
            if self.shot_x < 350 and self.shot_y > 0:
                self.score += 2
                self.make_effect.stop()
                self.make_effect.play()
                self.streak += 1
                if self.streak >= 2:
                    self.lives += 1
                self.shot_clock = self.reset
                self.ball_in_air = False
                self.made_basket = True
                self.three_pointer = True
            else:
                self.score += 1
                self.three_pointer = False
                self.make_effect.stop()
                self.make_effect.play()
                self.streak += 1
                if self.streak >= 2:
                    self.lives += 1
                self.shot_clock = self.reset
                self.ball_in_air = False
                self.made_basket = True

            self.ball.new_ball_x = randint(0, 450)
            self.ball.new_ball_y = randint(0, 300)
            self.ball.ball_x = self.ball.new_ball_x
            self.ball.ball_y = self.ball.new_ball_y
            self.player.hali_x = self.ball.new_ball_x - 115
            self.player.hali_y = self.ball.new_ball_y + 5
            self.ball_in_air = False
        if (self.made_basket == False) and self.score == 0:
            self.screen.blit(self.missed_it, (15, 130))
        if self.score != 0:
            if self.made_basket and self.three_pointer:
                self.screen.blit(self.sunk_it_three, (15, 130))
            elif self.made_basket:
                self.screen.blit(self.sunk_it_two,(15,130))
            else:
                self.screen.blit(self.missed_it, (15, 130))
    def end(self):
        if self.lives == 0:
            self.screen.blit(self.end_game, (0, 0))
            self.screen.blit(self.end_text,(300,300))
            pygame.display.update()
           # self.run = False

mixer.music.load("assets/sounds/Space Jam Theme Song.mp3")
mixer.music.play(-1)
game = GameState()
while game.run:
    game.setBackground()
    game.getKey()
    game.event()
    game.shotClock()
    game.ballMovement()
    game.countScore()
    game.end()
    pygame.display.update()
    game.clock.tick(75)

pygame.quit()
