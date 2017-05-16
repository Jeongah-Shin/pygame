#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame
from constants import *

class SpriteSheet(object):
    
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        # 새로운 이미지 객체 생성
        image = pygame.Surface([width,height]).convert()
        image.blit(self.sprite_sheet, (0,0), (x,y,width,height))

        # 검은색 배경을 기본값으로 배경 삭제
        image.set_colorkey(BLACK)

        # 이미지 반환
        return image

    def get_image2(self, x, y, width, height):
        # 새로운 이미지 객체 생성
        image = pygame.Surface([width,height]).convert()
        image.blit(self.sprite_sheet, (0,0), (x,y,width,height))

        # 흰색 배경을 기본값으로 배경 삭제
        image.set_colorkey(WHITE)

        # 이미지 반환
        return image
    def get_image3(self, x, y, width, height):
        # 새로운 이미지 객체 생성
        image = pygame.Surface([width,height]).convert()
        image.blit(self.sprite_sheet, (0,0), (x,y,width,height))

        # 파란색 배경을 기본값으로 배경 삭제
        image.set_colorkey(BLUE)

        # 이미지 반환
        return image
