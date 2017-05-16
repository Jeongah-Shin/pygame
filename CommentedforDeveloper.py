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
    # pygame 시작과 함께 초기화
    pygame.init()
    # 게임 초기 화면 크기를 지정
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # 시간이 흘러가도록 지정
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        # 키 입력을 저장
        pressed_keys = pygame.key.get_pressed()
        
        filtered_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 게임 종료 키 들어오면 종료
                active_scene.Terminate()
            else:
                # 이외의 모든 입력을 추가
                filtered_events.append(event)
        
        # 해당하는 모든 입력을 현재 장면에 넘겨줌
        active_scene.ProcessInput(filtered_events, pressed_keys)
        # 입력에 대한 상태값 변화 처리 후 그려줌
        active_scene.Render(screen)
        # 장면 전환 입력 시 전환
        active_scene = active_scene.next 
        
        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)

class LoginScene(SceneBase,pygame.sprite.Sprite):
    def __init__(self):
        SceneBase.__init__(self)
        pygame.init()
        # 현재 사용자가 이름을 입력했는지 ON / OFF 스위치
        self.isName = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        
        # 폰트 크기와 스타일 지정
        self.input_font = pygame.font.Font("./Assets/BRLNSB.ttf", 50)
        # 초기 name을 지정
        self.name = ""
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_loop = False
                
            elif event.type == pygame.KEYDOWN:
                #사용자가 값 입력 후 엔터 입력 시 이동
                if not self.isName:
                    # 입력한 값이 알파벳일때 이름에 추가
                    if event.unicode.isalpha():
                        self.name += event.unicode
                    # 백스페이스 입력 시 끝자리 글자 하나만 지움
                    elif event.key == K_BACKSPACE:
                        self.name = self.name[:-1]
                    # 엔터 입력 시 지금까지 입력한 이름 저장하고 Title 장면으로 전환
                    elif event.key == K_RETURN:
                        global UserName
                        print(self.name)
                        UserName = self.name
                        self.SwitchToScene(TitleScene())
    def Render(self, screen):
        # 검은색 화면으로 초기화
        self.screen.fill((0, 0, 0))
        # 이름을 묻는 안내 문구와 문구의 색깔(RGB: 252/159/73) 지정
        self.whoareyou = self.input_font.render("What's your name?", True, (252, 159, 73))
        # 안내 문구를 그릴 좌표 그려줌
        self.screen.blit(self.whoareyou,(10,SCREEN_WIDTH//3))

        # 입력한 이름의 내용과 색깔(흰색, RGB: 255/255/255) 지정
        self.block = self.input_font.render(self.name, True, (255, 255, 255))
        # 입력한 이름의 위치 지정
        self.rect = self.block.get_rect()
        self.rect.center = self.screen.get_rect().center
        # 입력한 이름과 위치 그려줌
        self.screen.blit(self.block, self.rect)

class TitleScene(SceneBase,pygame.sprite.Sprite):
    def __init__(self):
        SceneBase.__init__(self)
        # 타이틀 배경 그림 불러와서 게임화면에 맞게 조정
        self.background = pygame.image.load('./Assets/loading_background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH,SCREEN_HEIGHT))
        # 타이틀 화면의 제목(FlappyBird) 그림 불러와서  게임화면에 맞게 조정
        self.title = pygame.image.load('./Assets/represet_title.png')
        self.title = pygame.transform.scale(self.title, (TITLE_WIDTH,TITLE_HEIGHT))
        # 타이틀 배경 그림과 제목의 크기와 위치 지정
        self.background_size = self.background.get_size()
        self.background_rect = self.background.get_rect()
        self.title_size = self.title.get_size()
        self.title_rect = self.title.get_rect()
        # 게임 화면 크기 지정
        self.screen = pygame.display.set_mode(self.background_size)
        self.w,h = self.background_size

        # 첫번째 배경과 두번째 배경의 x 좌표 지정
        self.first_bg_x = 0
        self.second_bg_x = self.w
        
        # 첫 배경 그려줌
        self.screen.blit(self.background,self.background_rect)
        # 클릭유도 그림 생성(초기화)
        self.showClick = ShowClick()
        # 클릭유도 그림 움직이도록
        self.showClick.action()
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 클릭하면 게임 화면으로 !!
                self.SwitchToScene(GameScene())

    
        
    
    def Render(self, screen):
        # 첫번째와 두번째 배경화면 왼쪽으로 5포인트씩 이동
        self.second_bg_x -= 5
        self.first_bg_x -= 5

        # 왼쪽으로 첫번째 배경화면이 넘어가면 다시 오른쪽으로 넘겨줌
        if self.first_bg_x < -self.w:
           self.first_bg_x = self.w
        # 왼쪽으로 두번째 배경화면이 넘어가면 다시 오른쪽으로 넘겨줌
        if self.second_bg_x < -self.w:
           self.second_bg_x = self.w

        # 클릭유도 애니메이션 갱신
        self.showClick.update()

        # 첫번째와 두번째 배경화면 그리기
        self.screen.blit(self.background,(self.first_bg_x,0))
        self.screen.blit(self.background,(self.second_bg_x,0))

        # 타이틀 제목과 클릭유도 그림 그리기
        self.screen.blit(self.title,(25,SCREEN_HEIGHT//4))
        self.screen.blit(self.showClick.image, (self.showClick.rect.x,self.showClick.rect.y))
        
class GameScene(SceneBase,pygame.sprite.Sprite):
    
    def __init__(self):
        SceneBase.__init__(self)
        # 죽었을때, 점프할때, 시작할때 음악파일 불러옴
        self.dead_bgm = pygame.mixer.Sound('./Assets/You_Are_My_Girl_cut.wav')
        self.jump_bgm = pygame.mixer.Sound('./Assets/jump.wav')
        self.start_bgm = pygame.mixer.Sound('./Assets/start.wav')

        # 배경화면 불러와서 게임화면에 맞게 조정
        self.background = pygame.image.load('./Assets/ingame_background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH,SCREEN_HEIGHT))

        # 배경화면 크기와 위치 저장
        self.background_size = self.background.get_size()
        self.background_rect = self.background.get_rect()

        # 게임화면에 맞게 크기 지정
        self.screen = pygame.display.set_mode(self.background_size)
        self.w,h = self.background_size
        
        # 첫번째 배경과 두번째 배경의 x 좌표 지정
        self.first_bg_x = 0
        self.second_bg_x = self.w

        # 게임 화면 시작 전, 후 커버 불러와서 화면에 맞게 조정
        self.cover = pygame.image.load('./Assets/cafebene_bg.png')
        self.cover = pygame.transform.scale(self.cover, (SCREEN_WIDTH,SCREEN_HEIGHT))

        # 시작 전 대기 타이틀 불러와서 화면에 맞게 조정
        self.tit_ready = pygame.image.load('./Assets/ready.png')
        self.tit_ready = pygame.transform.scale(self.tit_ready, (TITLE_WIDTH,TITLE_HEIGHT))
        # 죽은 후 게임오버 타이틀 불러와서 화면에 맞게 조정
        self.tit_gameover = pygame.image.load('./Assets/gameover.png')
        self.tit_gameover = pygame.transform.scale(self.tit_gameover, (TITLE_WIDTH,TITLE_HEIGHT))
        # 죽은 후 카페베네 타이틀 불러와서 화면에 맞게 조정
        self.tit_cafebene = pygame.image.load('./Assets/cafebene.png')
        self.tit_cafebene = pygame.transform.scale(self.tit_cafebene, (TITLE_WIDTH,TITLE_HEIGHT))

        # 파이프 이미지 불러옴
        self.sprite_sheet = SpriteSheet.SpriteSheet('./Assets/pipe.png')
        # 28, 0 좌표에서 너비 26, 높이 160만큼 잘라서 위쪽 파이프로 지정
        self.top_pipe = self.sprite_sheet.get_image2(28,0,26,160)
        self.top_pipe = pygame.transform.scale(self.top_pipe, (PIPE_WIDTH,PIPE_HEIGHT))
        # 0,0 좌표에서 너비 26, 높이 160만큼 잘라서 아래쪽 파이프로 지정
        self.bot_pipe = self.sprite_sheet.get_image2(0,0,26,160)
        self.bot_pipe = pygame.transform.scale(self.bot_pipe, (PIPE_WIDTH,PIPE_HEIGHT))
        # 각 파이프의 크기와 위치 지정
        self.top_pipe_size = self.top_pipe.get_size()
        self.top_pipe_rect = self.top_pipe.get_rect()
        self.bot_pipe_size = self.bot_pipe.get_size()
        self.bot_pipe_rect = self.bot_pipe.get_rect()

        # 플래피버드 생성(초기화)
        self.flappybird = FlappyBird()

        # 랭킹 보여줄 때, 작은 점수, 큰 점수 폰트 스타일과 크기 지정
        self.ranking_font = pygame.font.Font("./Assets/BRLNSB.ttf", 50)
        self.mini_score_font = pygame.font.Font("./Assets/BRLNSB.ttf", 50)
        self.big_score_font = pygame.font.Font("./Assets/BRLNSB.ttf", 150)
        
        # 게임 진행에 필요한 ON / OFF 스위치 지정
        self.game_loop = True         # 메인 게임루프 스위치
        self.in_game_loop = False     # 작은 게임루프 스위치
        self.isStart = False          # 시작 전 스위치
        self.isMusic = False          # 음악 스위치 (중복 실행 방지)
        self.isAlive = True           # 플래피버드 생존여부 스위치
        self.is_next_stage = False    # 다음 스테이지 이동 스위치
        self.is_response_ranking = False # 랭킹 점수 스위치
        self.response_ranking = [];   # 랭킹 점수 리스트

        # 초기에 파이프 높이 랜덤 지정
        self.pipe_y = random.randint(0, BETWEEN_PIPE_MIN_HEIGHT) * (-1)

        # 움직이는 카운트와 점수 초기화
        self.movement_cnt = 0
        self.movement_score = 0
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.isAlive:
                    # 게임 시작 후에 클릭 시 점프 음악 재생
                    if self.in_game_loop: 
                        self.jump_bgm.play()
                    
                    if not self.in_game_loop:
                        # 게임 시작 전에 클릭 시 출발 음악 재생
                        self.start_bgm.play()
                        # 작은 게임 시작 루프 재생
                        self.in_game_loop = True
                        self.isStart = True
                        # 클릭 시 플래피버드가 점프하도록 허용
                        self.flappybird.permitJump()
                    
                    # 플래피버드가 날개짓을 시작하고 가만있으면 떨어지도록
                    self.flappybird.action()
                        
                    

                elif not self.isAlive:
                    if not self.is_next_stage:
                        # 글로벌 변수 사용 선언
                        global UserName
                        # gameover 시 서버에 유저가 LoginScene에서 입력한 이름과 현재 점수를 보냄
                        url = "http://donzurewebtesting0530.azurewebsites.net/gameover"
                        params = { 'ID': UserName,
                                    'Score': self.movement_score        
                        }
                        r = requests.post(url, params=params)
                        # 제대로 정상 처리되었는지 반환 코드와 결과 출력(200코드는 정상)
                        print(r.status_code, r.reason)
                        # 현재 TOP 5 랭커의 점수들을 요청
                        url = "http://donzurewebtesting0530.azurewebsites.net/ranking"
                        r = requests.get(url)
                        # 제대로 정상 처리되었는지 반환 코드와 결과 출력(200코드는 정상)
                        print(r.status_code, r.reason)
                        # 반환 결과 값을 저장
                        self.response_ranking = json.loads(r.text)
                        # 다음 장면으로 넘어갈 수있도록 허용
                        self.is_next_stage = True
                        # 랭킹 점수 보여주도록 허용
                        self.is_response_ranking = True
                    else:
                        # 죽은 뒤 재생되던 음악 정지
                        self.dead_bgm.stop()
                        # 다음화면으로 이동
                        self.SwitchToScene(TitleScene())

    
    def Render(self, screen):
        if self.game_loop:
            if self.in_game_loop:
                # 너무 빠르게 점수가 올라가지 않도록 연기(Delay) 시킴
                self.movement_cnt += 1
                # movement_cnt가 10을 채울때마다 점수를 2점 올리고 movement_cnt를 0으로 초기화
                if self.movement_cnt > 10:
                    self.movement_score += 2
                    self.movement_cnt=0

                # 첫번째와 두번째 배경화면 왼쪽으로 5포인트씩 이동
                self.second_bg_x -= 5
                self.first_bg_x -= 5

                # 왼쪽으로 첫번째 배경화면이 넘어가면 다시 오른쪽으로 넘겨줌
                if self.first_bg_x < -self.w:
                    self.first_bg_x = self.w
                    # 파이프 간격 위치를 랜덤으로 조정
                    self.pipe_y = random.randint(0, BETWEEN_PIPE_MIN_HEIGHT) * (-1)
                # 왼쪽으로 두번째 배경화면이 넘어가면 다시 오른쪽으로 넘겨줌
                if self.second_bg_x < -self.w:
                    self.second_bg_x = self.w

            # 현재 점수를 스트링으로 만듬
            self.str_score = str(self.movement_score)
            # 작은 점수(게임 중)와 큰 점수(게임 오버)의 값을 입력하고 색깔(흰색, RGB: 255/255/255) 입력
            self.mini_score_rend = self.mini_score_font.render(self.str_score, True, (255,255,255))       
            self.big_score_rend = self.big_score_font.render(self.str_score, True, (255,255,255))   

            # 플래피버드의 애니메이션 갱신
            self.flappybird.update()

            # 위 파이프에 플래피버드가 부딪히면 죽음 처리
            if pygame.Rect(self.first_bg_x,self.pipe_y,PIPE_WIDTH,PIPE_HEIGHT).colliderect(self.flappybird.get_rect()):
                self.FlappyBirdDie()

            # 아래 파이프에 플래피버드가 부딪히면 죽음 처리
            if pygame.Rect(self.first_bg_x,self.pipe_y+BETWEEN_PIPE+PIPE_HEIGHT,PIPE_WIDTH,PIPE_HEIGHT).colliderect(self.flappybird.get_rect()):
                self.FlappyBirdDie()

            # 게임 화면 아래로 내려가면 죽음 처리
            if self.flappybird.get_rect().y > SCREEN_HEIGHT+10:
                self.FlappyBirdDie()
                self.flappybird.stop()
            # 게임 화면 위로 올라가면 죽음 처리
            if self.flappybird.get_rect().y < -50:
                self.FlappyBirdDie()

        if self.in_game_loop:
            # 첫번째와 두번째 배경화면 다시 그리기
            self.screen.blit(self.background,(self.first_bg_x,0))
            self.screen.blit(self.background,(self.second_bg_x,0))
            # 위 파이프와 아래 파이프 다시 그리기
            self.screen.blit(self.top_pipe,(self.first_bg_x,self.pipe_y+BETWEEN_PIPE+PIPE_HEIGHT))
            self.screen.blit(self.bot_pipe,(self.first_bg_x,self.pipe_y))

        # 플래피버드를 다시 그리기
        self.screen.blit(self.flappybird.image, (self.flappybird.rect.x,self.flappybird.rect.y))

        # 게임 중이고 플래피버드가 살아있을 때, 작은 점수 그리기
        if self.isStart and self.isAlive:
            self.screen.blit(self.mini_score_rend, (10, 10))
       
        # 게임 시작 전에 커버와 게임 대기 타이틀 표시
        if not self.isStart:
            self.screen.blit(self.cover,(0,0))
            self.screen.blit(self.tit_ready,(25,SCREEN_HEIGHT//4))

        
        #[3] 2-3 죽은 뒤 화면
        if not self.isAlive:
            # 죽었을 때 커버 그리기
            self.screen.blit(self.cover,(0,0))
            if not self.is_response_ranking:
                # 게임오버 타이틀과 카페베네 배너 다시 그리기
                self.screen.blit(self.tit_gameover,(25,SCREEN_HEIGHT//4))
                self.screen.blit(self.tit_cafebene,(25,SCREEN_HEIGHT//4*3))
                # 큰 점수 표시
                self.screen.blit(self.big_score_rend, (SCREEN_WIDTH //3, (SCREEN_HEIGHT//2)-20))
            else:
                i = 0
                for id, score in self.response_ranking:
                    # Top 5 타이틀 내용과 색깔(흰색, RGB: 252/159/73) 지정
                    font_title = self.ranking_font.render("Top 5", True, (252, 159, 73))
                    # 사용자의 아이디(이름) 내용과 색깔(흰색, RGB: 255/255/255) 지정
                    font_id = self.ranking_font.render(id, True, (255, 255, 255))
                    # 사용자의 점수 내용과 색깔(흰색, RGB: 255/255/255) 지정
                    font_score = self.ranking_font.render(str(score), True, (255, 255, 255))
                    
                    # Top 5 타이틀 내용과 좌표(50,100)으로 그리기
                    self.screen.blit(font_title,(50,100))
                    # 사용자의 이름 내용과 좌표(40,180+60*i)으로 그리기
                    self.screen.blit(font_id,(40,180+60*i))
                    # 사용자의 점수 내용과 좌표(SCREEN_WIDTH //2+70,180+60*i)으로 그리기
                    self.screen.blit(font_score,(SCREEN_WIDTH //2+70,180+60*i))
                    # 다음 랭커의 정보 받아오도록
                    i += 1

    def FlappyBirdDie(self):
        # 현재 음악 재생중이 아닐때
        if not self.isMusic:
            # 죽은 음악 실행
            self.dead_bgm.play()
            # 현재 음악 재생 중 스위치 ON
            self.isMusic = True
        # 작은 게임 루프 스위치 OFF
        self.in_game_loop = False

        # 플래피버드가 죽었으므로 스위치 OFF
        self.isAlive = False
        self.flappybird.dead()

# 게임을 LoginScene이면서 50의 시간속도로 시작
run_game(50, LoginScene())