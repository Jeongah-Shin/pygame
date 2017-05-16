#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame
from constants import *
import SpriteSheet

class ShowClick(pygame.sprite.Sprite):
    
    def __init__(self):
        # 부모 객체 초기화
        super(ShowClick,self).__init__()
        
        # 애니메이션으로 만들 이미지를 불러옴
        sprite_sheet = SpriteSheet.SpriteSheet('./Assets/click.png')
        
        self.animations = []

        # [ 이미지를 차례대로 부른 뒤, 리스트로 만듬 ]
        # 이미지에서 0,0 좌표에 해당하는 그림은 57 너비, 24 높이만큼 자름
        image = sprite_sheet.get_image3(0, 0, 57, 24)
        # 자른 이미지를 게임 화면 크기에 맞게 조절
        image = pygame.transform.scale(image, (CLICK_WIDTH,CLICK_HEIGHT))
        # 애니메이션 리스트에 추가
        self.animations.append(image)
        # 이미지에서 0,24 좌표에 해당하는 그림은 57 너비, 24 높이만큼 자름
        image = sprite_sheet.get_image3(0, 24, 57, 24)
        # 자른 이미지를 게임 화면 크기에 맞게 조절
        image = pygame.transform.scale(image, (CLICK_WIDTH,CLICK_HEIGHT))
        # 애니메이션 리스트에 추가
        self.animations.append(image)
        # 이미지에서 0,48 좌표에 해당하는 그림은 57 너비, 24 높이만큼 자름
        image = sprite_sheet.get_image3(0, 48, 57, 24)
        # 자른 이미지를 게임 화면 크기에 맞게 조절
        image = pygame.transform.scale(image, (CLICK_WIDTH,CLICK_HEIGHT))
        # 애니메이션 리스트에 추가
        self.animations.append(image)

        # 애니메이션 프레임을 0으로 초기화
        self.animation_frame = 0

        # 애니메이션 초기 이미지를 지정
        self.image = self.animations[self.animation_frame]

        # 애니메이션의 위치를 지정
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 3
        self.rect.y = (SCREEN_HEIGHT*2 // 3  ) - 20
        self.count = 0

        self.isAction = False

        

    def update(self):
        if self.isAction:
            # 조금 더 천천히(자연스럽게) 애니메이션이 동작하도록, 5개 카운트마다 애니메이션 변화
            self.count += 1
            if self.count > 5:
                self.image = self.animations[self.animation_frame]
                self.animation_frame += 1
                self.animation_frame %= len(self.animations)
                self.count = 0

    def action(self):
        # 손가락이 움직이도록 허용
        self.isAction= True
