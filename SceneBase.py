#!/usr/local/bin/python
# -*- coding: utf-8 -*-

class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        pass # 사용자의 입력(마우스, 키보드)

    def Render(self, screen):
        pass # 그림 그리기

    def SwitchToScene(self, next_scene): # 장면을 전환
        self.next = next_scene
    
    def Terminate(self): # 장면 전환
        self.SwitchToScene(None)