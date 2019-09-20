from PPlay import window as w
from PPlay import gameimage as gi
import Menu as menu
import playloop
class Jogo:
    def __init__(self):
        self.screen = w.Window(640, 480)
        self.screen.set_title("Space Invaders")
        self.bg1 = gi.GameImage("assets/bg1.jpg")
        self.bg2 = gi.GameImage("assets/bg1.jpg")
        self.bg2.y = -self.bg1.height
        self.menu = menu.Menu(self.screen)
        self.dific_menu = menu.DificultyMenu(self.screen)
        self.play = playloop.Play(self.screen)
        self.game_state = 0
        self.fps = 0
        self.difficult = 1
    def gameLoop(self):
        while True:
            self.bg_draw_scroll(1000)
            if self.game_state == 0:
                game_state_return = self.menu.loop_menu()
                if self.game_state != game_state_return:
                    self.menu = menu.Menu(self.screen)
                self.game_state = game_state_return

            elif self.game_state == 1:
                # game_state_return = self.play.loop_game()
                # if self.game_state != game_state_return:
                #     self.play = playloop.Play(self.screen)
                self.game_state = game_state_return

            elif self.game_state == 2:
                self.game_state = self.dific_menu.loop_dif_menu()

            self.change_fps()
            self.screen.draw_text('FPS: '+str(self.fps), self.screen.width - 60 , 5, size=10, color=(150, 250, 150))
            self.screen.update()

    def bg_draw_scroll(self, roll_speed):
        self.bg1.y += roll_speed * self.screen.delta_time()
        self.bg2.y += roll_speed * self.screen.delta_time()
        if self.bg2.y >= 0:
            self.bg1.y = 0
            self.bg2.y = - self.bg1.height
        self.bg1.draw()
        self.bg2.draw()

    def change_fps(self):
        if self.screen.total_time%100==0 and self.screen.total_time>1:
            self.fps = str(int(1/self.screen.delta_time()))