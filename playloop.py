from PPlay import gameimage as gi
from PPlay import keyboard as kb
from PPlay import sprite as sp
import random
class Play():
    def __init__(self, screen):
        self.kb = screen.get_keyboard()
        self.player = Player(self.kb)
        self.aliens = Enemies()
        self.aliens.spawn_enemies()
        self.screen = screen
        self.bullets = []
        self.lost = False

    def loop_game(self):
        self.player.player_movement(self.screen.delta_time())
        self.player_shoot()
        self.draw_game()
        self.aliens.enemies_move(self.screen.delta_time())
        self.bullet_movement()
        self.update_counters()
        self.bullet_collision()
        self.bullet_bullet_collision()
        if self.lost or self.won():
            return 0
        else:
            return 1
    def draw_game(self):
        self.player.draw()
        self.aliens.draw_enemies()
        self.draw_bullets()

    def won(self):
        win = True
        for row in range(self.aliens.matrix_x):
            if win:
                for collumn in range(self.aliens.matrix_y):
                    if self.aliens.enemies_mat[row][collumn]!=0:
                        win = False
                        return win
        if win:
            return True
    def shoot(self, shooter):
        shooter.shoot_tick = 0
        bullet = sp.Sprite('assets/game/shot.png')
        self.adjust_bullet(shooter, bullet)
        self.bullets.append(bullet)
    def adjust_bullet(self, actor, bullet):
        x_fire = actor.x + (actor.width / 2) - (bullet.width / 2)
        if actor.direction == -1:
            y_fire = actor.y
        elif actor.direction == 1:
            y_fire = actor.y + actor.height - bullet.height
        bullet.x = x_fire
        bullet.y = y_fire
        bullet.direction = actor.direction
    def player_shoot(self):
        if self.kb.key_pressed("space"):
            if self.player.shoot_tick > self.player.shoot_delay:
                self.shoot(self.player)

    def bullet_movement(self):
        for b in self.bullets:

            b.move_y(300 * b.direction * self.screen.delta_time())

            if b.y < -b.height or b.y > self.screen.height + b.height:
                self.bullets.remove(b)
    def draw_bullets(self):
        for b in self.bullets:
            b.draw()

    def update_counters(self):
        self.player.shoot_tick+=self.screen.delta_time()
        for row in range(self.aliens.matrix_x):
            for collumn in range(self.aliens.matrix_y):
                if self.aliens.enemies_mat[row][collumn] != 0:
                    self.aliens.enemies_mat[row][collumn].shoot_tick+=self.screen.delta_time()
                    if self.aliens.enemies_mat[row][collumn].shoot_delay < self.aliens.enemies_mat[row][collumn].shoot_tick:
                        self.shoot(self.aliens.enemies_mat[row][collumn])
                        self.aliens.enemies_mat[row][collumn].shoot_tick = 0
                        self.aliens.enemies_mat[row][collumn].shoot_delay = random.uniform(0, 15)

    def bullet_collision(self):
        for b in self.bullets:
            if b.direction == 1 and b.collided(self.player):
                self.lost = True
                return
            elif b.direction == -1:
                self.check_enemy_collided(b)
    def check_enemy_collided(self, b):
        for row in range(self.aliens.matrix_x):
            for collumn in range(self.aliens.matrix_y):
                if self.aliens.enemies_mat[row][collumn] != 0:
                    if b.collided(self.aliens.enemies_mat[row][collumn]):
                        self.bullets.remove(b)
                        self.aliens.enemies_mat[row][collumn] = 0
                        self.player.score+=50
                        return

    def bullet_bullet_collision(self):
        for b1 in self.bullets:
            if b1.direction == -1:
                for b2 in self.bullets:
                    if b2.direction == 1:
                        if b1.collided(b2):
                            self.bullets.remove(b1)
                            self.bullets.remove(b2)

                            break



class Player(gi.GameImage):
    def __init__(self, keyb):
        gi.GameImage.__init__(self, "assets/game/spaceship.png")
        self.y = 720 - self.height
        self.x = 1280 / 2 - self.width
        self.direction = -1
        self.score = 0
        self.shoot_delay = 0.5
        self.shoot_tick = self.shoot_delay
        self.keyb = keyb
    def player_movement(self, delta_time):
        if self.keyb.key_pressed('left'):
            self.x-=400*delta_time
        elif self.keyb.key_pressed('right'):
            self.x += 400 * delta_time




class Enemies():
    def __init__(self):
        self.matrix_x = int(random.uniform(5, 10))
        self.matrix_y = int(random.uniform(3, 7))
        self.enemies_mat = [[0 for x in range(10)] for x in range(10)]
        self.enemy_shoot_delay = 1
        self.enemies_direction = 1
        self.enemy_speed = 200
        self.enemy_add = 'assets/game/enemy'
    def spawn_enemies(self):
        for x in range(self.matrix_x):
            for y in range(self.matrix_y):
                enemy = sp.Sprite(self.enemy_add +str(random.randint(0,6))+'.png')
                enemy.set_position(x * enemy.width * 3 + 5, y * enemy.height * 3 + 5)
                enemy.direction = 1
                enemy.shoot_delay = random.uniform(0, 15)
                enemy.shoot_tick = 0
                self.enemies_mat[x][y] = enemy
    def enemies_move(self,delta_time):
        self.inverted = False
        new_position = self.enemy_speed * self.enemies_direction * delta_time
        for row in range(self.matrix_x):
            for collumn in range(self.matrix_y):
                if self.enemies_mat[row][collumn] != 0:
                    self.enemies_mat[row][collumn].move_x(new_position)

                    if not self.inverted:
                        if self.enemies_mat[row][collumn].x >= 1254:
                            self.enemies_direction= -1
                            self.inverted = True
                        elif self.enemies_mat[row][collumn].x + self.enemies_mat[row][collumn].width <=26:
                            self.enemies_direction = 1
                            self.inverted = True




    def draw_enemies(self):
        for i in range(self.matrix_x):
            for j in range(self.matrix_y):
                if self.enemies_mat[i][j]!=0:
                    self.enemies_mat[i][j].draw()
