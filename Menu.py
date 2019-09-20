from PPlay import gameimage as gi
import time

class Button():
    def __init__(self, image, name, pos):
        self.image_normal = gi.GameImage('assets/menu/1'+image)
        self.image_select = gi.GameImage('assets/menu/2'+image)
        self.image_normal.x = self.image_select.x = 1280/2 - self.image_normal.width/2
        self.image_normal.y = self.image_select.y = pos
        self.name = name

    def draw_normal(self):
        self.image_normal.draw()

    def draw_select(self):
        self.image_select.draw()

class Menu():
    def __init__(self, screen):
        self.mouse = screen.get_mouse()
        self.play_menu = [Button('play.png', 'PLAY', screen.height/10),
                          Button('dific.png', 'DIFICULDADE', (screen.height/10)*3),
                          Button('ranking.png', 'RANKING', (screen.height/10)*5),
                          Button('exit.png', 'EXIT', (screen.height/10)*7)]
        self.dificult_menu = [Button('easy.png', 'EASY',screen.height/10),
                              Button('medium.png', 'MEDIUM', (screen.height/10)*3),
                              Button('hard.png', 'HARD', (screen.height/10)*5),
                              Button('back.png', 'BACK', (screen.height/10)*7)]
    def loop_menu(self):
        for item in self.play_menu:
            if self.mouse.is_over_object(item.image_normal):
                item.draw_select()
                if self.mouse.is_button_pressed(1):
                    if item.name == 'PLAY':
                        return 1
                    elif item.name == 'DIFICULDADE':
                        time.sleep(0.1)
                        return 2
                    elif item.name == 'EXIT':
                        exit()
            else:
                item.draw_normal()
        return 0

class DificultyMenu():
    def __init__(self, screen):
        self.mouse = screen.get_mouse()
        self.play_menu = [Button('easy.png', 'EASY', screen.height / 10),
                              Button('medium.png', 'MEDIUM', (screen.height / 10) * 3),
                              Button('hard.png', 'HARD', (screen.height / 10) * 5),
                              Button('back.png', 'BACK', (screen.height / 10) * 7)]

    def loop_dif_menu(self):
        for item in self.play_menu:
            if self.mouse.is_over_object(item.image_normal):
                item.draw_select()
                if self.mouse.is_button_pressed(1):
                    if item.name == 'EASY':
                        return 1
                    elif item.name == 'MEDIUM':
                        return 1
                    elif item.name == 'HARD':
                        return 1
                    elif item.name == 'BACK':
                        return 0
            else:
                item.draw_normal()
        return 2