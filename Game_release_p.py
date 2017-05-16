#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame, sys, random
from constants import *
import SpriteSheet
from ShowClick import ShowClick
from FlappyBird import FlappyBird
from pygame.locals import *
from SceneBase import *

import requests
import json

UserName = None

def run_game(fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        
        filtered_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Render(screen)
        
        active_scene = active_scene.next 
        
        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)

class LoginScene(SceneBase,pygame.sprite.Sprite):
    def __init__(self):
        SceneBase.__init__(self)
        pygame.init()
        self.isName = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        
        self.input_font = pygame.font.Font("./Assets/BRLNSB.ttf", 50)
        self.name = ""
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_loop = False
                
            elif event.type == pygame.KEYDOWN:
                #[1] 2 사용자가 입력 & 편집, 엔터 입력 시 이동
                if not self.isName:
                    if event.unicode.isalpha():
                        self.name += event.unicode
                    elif event.key == K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key == K_RETURN:
                        global UserName
                        print(self.name)
                        UserName = self.name
                        self.SwitchToScene(TitleScene())
    def Render(self, screen):
        self.screen.fill((0, 0, 0))
        #[1] 1 이름 묻는 문장이 표시된다
        self.whoareyou = self.input_font.render("What's your name?", True, (252, 159, 73))
        self.screen.blit(self.whoareyou,(10,SCREEN_WIDTH//3))

        self.block = self.input_font.render(self.name, True, (255, 255, 255))
        self.rect = self.block.get_rect()
        self.rect.center = self.screen.get_rect().center
        
        self.screen.blit(self.block, self.rect)

class TitleScene(SceneBase,pygame.sprite.Sprite):
    def __init__(self):
        SceneBase.__init__(self)
        self.background = pygame.image.load('./Assets/loading_background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH,SCREEN_HEIGHT))
        self.title = pygame.image.load('./Assets/represet_title.png')
        self.title = pygame.transform.scale(self.title, (TITLE_WIDTH,TITLE_HEIGHT))
        self.background_size = self.background.get_size()
        self.background_rect = self.background.get_rect()
        self.title_size = self.title.get_size()
        self.title_rect = self.title.get_rect()

        self.screen = pygame.display.set_mode(self.background_size)
        self.w,h = self.background_size

        self.first_bg_x = 0
        self.second_bg_x = self.w
        
        
        self.screen.blit(self.background,self.background_rect)
        #[2] 2-1 타이틀과 클릭 버튼이 표시된다.
        self.showClick = ShowClick()
        #[2] 3-1 손가락이 움직인다.
        self.showClick.action()
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                #[2] 4 클릭하면 게임 화면으로 !!
                self.SwitchToScene(GameScene())

    
        
    
    def Render(self, screen):
        #[2] 1 배경화면 왼쪽으로 이동한다
        self.second_bg_x -= 5
        self.first_bg_x -= 5

        if self.first_bg_x < -self.w:
           self.first_bg_x = self.w
        if self.second_bg_x < -self.w:
           self.second_bg_x = self.w

        #[2] 3-2 손가락이 움직인다 
        self.showClick.update()


        self.screen.blit(self.background,(self.first_bg_x,0))
        self.screen.blit(self.background,(self.second_bg_x,0))

        #[2] 2-2 타이틀과 클릭 버튼이 표시된다.
        self.screen.blit(self.title,(25,SCREEN_HEIGHT//4))
        self.screen.blit(self.showClick.image, (self.showClick.rect.x,self.showClick.rect.y))
        
class GameScene(SceneBase,pygame.sprite.Sprite):
    
    def __init__(self):
        SceneBase.__init__(self)

        self.dead_bgm = pygame.mixer.Sound('./Assets/You_Are_My_Girl_cut.wav')
        self.jump_bgm = pygame.mixer.Sound('./Assets/jump.wav')
        self.start_bgm = pygame.mixer.Sound('./Assets/start.wav')

        self.background = pygame.image.load('./Assets/ingame_background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH,SCREEN_HEIGHT))
        self.background_size = self.background.get_size()
        self.background_rect = self.background.get_rect()
        self.screen = pygame.display.set_mode(self.background_size)
        self.w,h = self.background_size
        
        self.first_bg_x = 0
        self.second_bg_x = self.w

        self.cover = pygame.image.load('./Assets/cafebene_bg.png')
        self.cover = pygame.transform.scale(self.cover, (SCREEN_WIDTH,SCREEN_HEIGHT))
        self.tit_ready = pygame.image.load('./Assets/ready.png')
        self.tit_ready = pygame.transform.scale(self.tit_ready, (TITLE_WIDTH,TITLE_HEIGHT))
        self.tit_gameover = pygame.image.load('./Assets/gameover.png')
        self.tit_gameover = pygame.transform.scale(self.tit_gameover, (TITLE_WIDTH,TITLE_HEIGHT))
        self.tit_cafebene = pygame.image.load('./Assets/cafebene.png')
        self.tit_cafebene = pygame.transform.scale(self.tit_cafebene, (TITLE_WIDTH,TITLE_HEIGHT))

        self.sprite_sheet = SpriteSheet.SpriteSheet('./Assets/pipe.png')
        self.top_pipe = self.sprite_sheet.get_image2(28,0,26,160)
        self.top_pipe = pygame.transform.scale(self.top_pipe, (PIPE_WIDTH,PIPE_HEIGHT))
        self.bot_pipe = self.sprite_sheet.get_image2(0,0,26,160)
        self.bot_pipe = pygame.transform.scale(self.bot_pipe, (PIPE_WIDTH,PIPE_HEIGHT))
        self.top_pipe_size = self.top_pipe.get_size()
        self.top_pipe_rect = self.top_pipe.get_rect()
        self.bot_pipe_size = self.bot_pipe.get_size()
        self.bot_pipe_rect = self.bot_pipe.get_rect()

        self.flappybird = FlappyBird()

        self.ranking_font = pygame.font.Font("./Assets/BRLNSB.ttf", 50)
        self.mini_score_font = pygame.font.Font("./Assets/BRLNSB.ttf", 50)
        self.big_score_font = pygame.font.Font("./Assets/BRLNSB.ttf", 150)
        
        self.game_loop = True       
        self.in_game_loop = False   
        self.isStart = False       
        self.isMusic = False        
        self.isAlive = True

        self.pipe_y = random.randint(0, BETWEEN_PIPE_MIN_HEIGHT) * (-1)
        self.movement_cnt = 0
        self.movement_score = 0

        self.is_next_stage = False
        self.is_response_ranking = False
        self.response_ranking = [];

    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.isAlive:
                    if self.in_game_loop: 
                        self.jump_bgm.play()
                    if not self.in_game_loop:
                        self.start_bgm.play()
                        self.in_game_loop = True
                        self.isStart = True
                        #[3] 2-4 클릭하면 점프한다
                        self.flappybird.permitJump()
                    
                    #[3] 2-2 가만있으면 떨어진다
                    self.flappybird.action()
                        
                    

                elif not self.isAlive:
                    """
                    if not self.is_next_stage:
                        global UserName
                        url = "/gameover"
                        params = { 'ID': UserName,
                                    'Score': self.movement_score        
                        }
                        r = requests.post(url, params=params)
                        print(r.status_code, r.reason)
                        url = "/ranking"
                        r = requests.get(url)
                        print(r.status_code, r.reason)
                        self.response_ranking = json.loads(r.text)
                        self.is_next_stage = True
                        self.is_response_ranking = True
                    else:
                    """
                    #[3] 4-1 죽은 뒤, 클릭하면 타이틀 화면으로 !!
                    self.dead_bgm.stop()
                    self.SwitchToScene(TitleScene())

    
    def Render(self, screen):
        if self.game_loop:
            if self.in_game_loop:
                #[3] 3-2 점수판 점수가 증가한다
                self.movement_cnt += 1
                if self.movement_cnt > 10:
                    self.movement_score += 2
                    self.movement_cnt=0

                #[3] 1-1 왼쪽으로 이동한다
                self.second_bg_x -= 5
                self.first_bg_x -= 5
                if self.first_bg_x < -self.w:
                    self.first_bg_x = self.w
                    #[3] 4-2 파이프 위치가 바뀐다
                    self.pipe_y = random.randint(0, BETWEEN_PIPE_MIN_HEIGHT) * (-1)
                if self.second_bg_x < -self.w:
                    self.second_bg_x = self.w

            self.str_score = str(self.movement_score)
            self.mini_score_rend = self.mini_score_font.render(self.str_score, True, (255,255,255))       
            self.big_score_rend = self.big_score_font.render(self.str_score, True, (255,255,255))   

            #[3] 2-1 새가 보인다
            self.flappybird.update()

            #[3] 2-5 파이프에 부딪히면 새가 죽는다 
            if pygame.Rect(self.first_bg_x,self.pipe_y,PIPE_WIDTH,PIPE_HEIGHT).colliderect(self.flappybird.get_rect()):
                self.FlappyBirdDie()

            #[3] 2-5 파이프에 부딪히면 새가 죽는다
            if pygame.Rect(self.first_bg_x,self.pipe_y+BETWEEN_PIPE+PIPE_HEIGHT,PIPE_WIDTH,PIPE_HEIGHT).colliderect(self.flappybird.get_rect()):
                self.FlappyBirdDie()

            if self.flappybird.get_rect().y > SCREEN_HEIGHT+10:
                self.FlappyBirdDie()
                self.flappybird.stop()

        if self.in_game_loop:
            self.screen.blit(self.background,(self.first_bg_x,0))
            self.screen.blit(self.background,(self.second_bg_x,0))
            self.screen.blit(self.top_pipe,(self.first_bg_x,self.pipe_y+BETWEEN_PIPE+PIPE_HEIGHT))
            self.screen.blit(self.bot_pipe,(self.first_bg_x,self.pipe_y))

        #[3] 2-1 새가 보인다
        self.screen.blit(self.flappybird.image, (self.flappybird.rect.x,self.flappybird.rect.y))

        #[3] 3-1 점수판이 보인다
        if self.isStart and self.isAlive:
            self.screen.blit(self.mini_score_rend, (10, 10))
       
        #[3] 2-3 시작 전 화면
        if not self.isStart:
            self.screen.blit(self.cover,(0,0))
            self.screen.blit(self.tit_ready,(25,SCREEN_HEIGHT//4))

        #[3] 2-3 죽은 뒤 화면
        if not self.isAlive:
            self.screen.blit(self.cover,(0,0))
            self.screen.blit(self.tit_gameover,(25,SCREEN_HEIGHT//4))
            self.screen.blit(self.tit_cafebene,(25,SCREEN_HEIGHT//4*3))
            #[3] 3-3 점수판이 보인다
            self.screen.blit(self.big_score_rend, (SCREEN_WIDTH //3, (SCREEN_HEIGHT//2)-20))
        
        """
        #[3] 2-3 죽은 뒤 화면
        if not self.isAlive:
            self.screen.blit(self.cover,(0,0))
            if not self.is_response_ranking:
                self.screen.blit(self.tit_gameover,(25,SCREEN_HEIGHT//4))
                self.screen.blit(self.tit_cafebene,(25,SCREEN_HEIGHT//4*3))
                ##3-2 점수판이 보인다
                self.screen.blit(self.big_score_rend, (SCREEN_WIDTH //3, (SCREEN_HEIGHT//2)-20))
            else:
                i = 0
                for id, score in self.response_ranking:
                    font_id = self.ranking_font.render(id, True, (255, 255, 255))
                    font_score = self.ranking_font.render(str(score), True, (255, 255, 255))
                    font_title = self.ranking_font.render("Top 5", True, (252, 159, 73))
                    self.screen.blit(font_title,(50,100))
                    self.screen.blit(font_id,(40,180+60*i))
                    self.screen.blit(font_score,(SCREEN_WIDTH //2+70,180+60*i))
                    i += 1
        """




    def FlappyBirdDie(self):
        if not self.isMusic:
            self.dead_bgm.play()
            self.isMusic = True
        self.in_game_loop = False
        self.isAlive = False
        self.flappybird.dead()


run_game(50, LoginScene())