#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame
from constants import *
import SpriteSheet

class FlappyBird(pygame.sprite.Sprite):
    

    def __init__(self):
        # 부모 객체 초기화
        super(FlappyBird,self).__init__()
        
        # 애니메이션으로 만들 이미지를 불러옴
        sprite_sheet = SpriteSheet.SpriteSheet('./Assets/bird.png')
        
        self.animations = []

        # [ 이미지를 차례대로 부른 뒤, 리스트로 만듬 ]
        # 이미지에서 3,7 좌표에 해당하는 그림은 16 너비, 13 높이만큼 자름
        image = sprite_sheet.get_image(3, 7, 16, 13)
        # 자른 이미지를 게임 화면 크기에 맞게 조절
        image = pygame.transform.scale(image, (BIRD_WIDTH,BIRD_HEIGHT))
        # 애니메이션 리스트에 추가
        self.animations.append(image)
        # 이미지에서 31,7 좌표에 해당하는 그림은 16 너비, 13 높이만큼 자름
        image = sprite_sheet.get_image(31, 7, 16, 13)
        # 자른 이미지를 게임 화면 크기에 맞게 조절
        image = pygame.transform.scale(image, (BIRD_WIDTH,BIRD_HEIGHT))
        # 애니메이션 리스트에 추가
        self.animations.append(image)
        # 이미지에서 59,7 좌표에 해당하는 그림은 16 너비, 13 높이만큼 자름
        image = sprite_sheet.get_image(59, 7, 16, 13)
        # 자른 이미지를 게임 화면 크기에 맞게 조절
        image = pygame.transform.scale(image, (BIRD_WIDTH,BIRD_HEIGHT))
        # 애니메이션 리스트에 추가
        self.animations.append(image)

        # 애니메이션 프레임을 0으로 초기화
        self.animation_frame = 0

        # 애니메이션 초기 이미지를 지정
        self.image = self.animations[self.animation_frame]

        # 애니메이션의 위치를 지정
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 3
        self.rect.y = SCREEN_HEIGHT // 2        

        # 플래피버드의 동작에 대한 ON / OFF 스위치
        self.moveable = False       # 점프가 가능한가?
        self.actionable = False     # 날개를 움직일 수 있는가?
        self.isDead = False         # 플래피버드가 죽었나?
        self.isJump = True          # 클릭에 대해 반응하는가?
        # 
        self.height = 0.0
        self.canJump = False
        

    def update(self):
        if self.isJump:
            if self.moveable:
                # 클릭하지 않을 때 떨어지도록, 높이와 위치 조정
                self.height += .098*5 # 유사 중력가속도
                self.rect.y += self.height;
            if self.actionable:
                # 날개를 움직이도록 애니메이션 프레임 증가
                self.image = self.animations[self.animation_frame]
                self.animation_frame += 1
                self.animation_frame %= len(self.animations)
            if self.isDead:
                # 죽었을 때도 떨어지도록, 높이와 위치 조정
                self.height += .098*5 # 유사 중력가속도
                self.rect.y += self.height;

    def permitJump(self):
        # 플래피버드가 사용자가 클릭시, 점프할 수 있게 허용
        self.canJump = True

    def action(self):
        # 플래피버드가 날개를 움직이고 가만있으면 떨어지게 한다
        self.moveable = True
        self.actionable = True
        # 클릭 허용되지 않으면 점프하지 않음
        if self.canJump:
            self.height = -2.5*5

    def dead(self):
        # 날개짓을 멈추고, 클릭에도 반응 안함
        self.moveable = False
        self.actionable = False

        # 플래피버드의 사진을 가져옴
        sprite_sheet = SpriteSheet.SpriteSheet('./Assets/bird.png')
        # 플래피버드가 죽은 사진을 잘라옴
        image = sprite_sheet.get_image(87, 7, 16, 13)
        # 게임 화면에 맞게 크기 조정하고, 180도 뒤집어줌
        image = pygame.transform.scale(image, (BIRD_WIDTH,BIRD_HEIGHT))
        image = pygame.transform.rotate(image, 180)
        self.image = image
        self.isDead = True
    
    def get_rect(self):
        # 지금 플래피버드의 위치를 반환
        return pygame.Rect(self.rect.x,self.rect.y,BIRD_WIDTH,BIRD_HEIGHT)

    def stop(self):
        # 플래피버드가 떨어지는 것을 막음
        self.isJump= False

