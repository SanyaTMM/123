import pygame
import sys

import new_db

pygame.init()


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((820, 400))

        self.score = 0
        self.hp = 3

        self.f_left = True
        self.f_right = True
        self.f_down = True
        self.f_up = True

        self.krug_rect = pygame.Rect(0, 0, 40, 40)
        self.krug_rect.center = (410, 200)

        self.vrag_rect = pygame.Rect(0, 0, 40, 40)
        self.vrag_rect.center = (50, 110)

        self.coin = pygame.transform.scale(pygame.image.load("png/coin1.png").convert_alpha(), (25, 25))
        self.krug_hp = pygame.transform.scale(pygame.image.load("png/hp.png").convert_alpha(), (60, 40))
        self.galka = pygame.transform.scale(pygame.image.load("png/hp.png").convert_alpha(), (40, 20))

        self.coin1 = self.coin.get_rect(topleft=(120, 45))
        self.coin2 = self.coin.get_rect(topleft=(770, 50))
        self.coin3 = self.coin.get_rect(topleft=(70, 255))
        self.coin4 = self.coin.get_rect(topleft=(610, 255))
        self.coins2 = [self.coin1, self.coin2, self.coin3, self.coin4]

        width = 4
        self.line1 = pygame.Rect(0, 40, 820, width)
        self.line2 = pygame.Rect(115, 40, width, 50)
        self.line3 = pygame.Rect(0, 140, 200, width)
        self.line4 = pygame.Rect(120, 210, width, 100)
        self.line5 = pygame.Rect(350, 110, width, 120)
        self.line6 = pygame.Rect(350, 350, width, 50)
        self.line7 = pygame.Rect(200, 270, 90, width)
        self.line8 = pygame.Rect(500, 180, width, 80)
        self.line9 = pygame.Rect(580, 100, width, 60)
        self.line10 = pygame.Rect(600, 320, width, 30)
        self.line11 = pygame.Rect(750, 100, width, 60)
        self.line12 = pygame.Rect(600, 250, 90, width)
        self.line13 = pygame.Rect(650, 100, 100, width)

        self.redlines = [self.line1, self.line2, self.line3, self.line7, self.line11, self.line12, self.line13]
        self.bluelines = [self.line4, self.line5, self.line6, self.line8, self.line9, self.line10]

        self.krug_speed = 3

        self.all_coins = [self.coin1, self.coin2, self.coin3, self.coin4]

        self.coins_sound = pygame.mixer.Sound("songs/Coin.wav")
        self.line_sound = pygame.mixer.Sound("songs/Hit.wav")

        self.name = "user1"

        self.skin = 1

    def vrag_move(self):
        x = self.vrag_rect.center[0]
        y = self.vrag_rect.center[1]

        vrag_speed = 2

        def left():
            self.vrag_rect.x -= vrag_speed

        def right():
            self.vrag_rect.x += vrag_speed

        def up():
            self.vrag_rect.y -= vrag_speed

        def down():
            self.vrag_rect.y += vrag_speed

        if x < 250 and y == 110:
            right()
        elif y > 70 and x == 250:
            up()
        elif x < 790 and y == 70:
            right()
        elif y < 350 and x == 790:
            down()
        elif x > 630 and y == 350:
            left()
        elif y > 280 and x == 630:
            up()
        elif x > 530 and y == 280:
            left()
        elif y > 130 and x == 530:
            up()
        elif x > 430 and y == 130:
            left()
        elif y < 260 and x == 430:
            down()
        elif x > 310 and y == 260:
            left()
        elif y < 340 and x == 310:
            down()
        elif x > 80 and y == 340:
            if x == 250 + vrag_speed:
                self.vrag_rect.x -= (vrag_speed * 2)
            left()
        elif y > 170 and x == 80:
            up()
        elif x < 250 and y == 170:
            right()
        elif y < 70 and x == 250:
            up()

    def make_true_move(self):
        self.f_right = True
        self.f_left = True
        self.f_up = True
        self.f_down = True

    def draw_intro(self):
        end = True

        while end:
            self.screen.fill("#E3E3E3")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        end = False
            self.screen.fill("black")
            pygame.display.update()

    def leaderbord(self, nem_db=None):
        def draw_skin(i):
            user_id = new_db.user_info(self.name)[0][0]
            skin_list = new_db.user_skins(user_id)

            s = new_db.get_skin_info(i)

            r = pygame.Rect(40, 40, 40, 40)

            if i < 5:
                r.center = (60, 120 + (i - 1) * 60)

            else:
                r.center = (270, 120 + (i - 5) * 60)

            pygame.draw.circle(self.screen, s["color1"], r.center, 20, width=s["width"], )
            pygame.draw.circle(self.screen, s["color2"], r.center, 20 - s["width"], )

            # i = skin_id
            if i in skin_list:
                self.screen.blit(self.galka, (r.topright[0] + 20, r.topright[1] - 3))
            else:
                self.screen.blit(font_40.render(f"{s['cost']}", True, "#E81931"),
                                 (r.topright[0] + 20, r.topright[1] - 3)),

            if self.skin == i:
                pygame.draw.rect(self.screen, "#f25757", rect=(r.x -5, r.y - 5, 50, 50), width=2, border_radius=5)

            #draw skin
            if pygame.mouse.get_pressed()[0]:
                if r.collidepoint(pygame.mouse.get_pos()):
                    if i in skin_list:
                        self.skin = i
                    else:
                        new_db.buy_skin(i, self.name, s['cost'])

        restart = False
        font_40 = pygame.font.SysFont("arial", 40)
        font_30 = pygame.font.SysFont("arial", 30)
        font_25 = pygame.font.SysFont("arial", 25)

        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.vrag_rect.center = (50, 110)
                        self.hp = 3
                        self.score = 0
                        restart = True

            self.screen.fill("#E3E3E3")
            pygame.draw.line(self.screen, "#3EBDF8", (500, 0), (500, 400), 4)
            pygame.draw.line(self.screen, "#3EBDF8", (500, 270), (820, 270), 4)

            #skin store
            balance = new_db.user_info(self.name)[0][2]
            self.screen.blit(font_40.render("Магазин скинов", True, "#E81931"), (40, 10))
            self.screen.blit(font_25.render(f"{balance}", True, "#E81931"), (350, 23))

            #leaderboard
            leaders = new_db.lb()
            self.screen.blit(font_40.render("Лучшие игроки", True, "#E81931"), (540, 10))
            self.screen.blit(font_30.render(f"{leaders[0][1]}", True, "#3EBDF8"), (540, 100))
            self.screen.blit(font_30.render(f"{leaders[0][3]}", True, "#3EBDF8"), (700, 100))

            self.screen.blit(font_30.render(f"{leaders[1][1]}", True, "#3EBDF8"), (540, 150))
            self.screen.blit(font_30.render(f"{leaders[1][3]}", True, "#3EBDF8"), (700, 150))

            self.screen.blit(font_30.render(f"{leaders[2][1]}", True, "#3EBDF8"), (540, 200))
            self.screen.blit(font_30.render(f"{leaders[2][3]}", True, "#3EBDF8"), (700, 200))

            #resultat
            self.screen.blit(font_25.render("Результат", True, "#E81931"), (540, 280))
            self.screen.blit(font_40.render(f"{self.score}", True, "#3EBDF8"), (540, 317))

            best_score = new_db.user_info(self.name)
            self.screen.blit(font_25.render("Рекорд", True, "#E81931"), (700, 280))
            self.screen.blit(font_40.render(f"{best_score[0][3]}", True, "#3EBDF8"), (700, 317))

            # skins
            for i in range(1, 9):
                draw_skin(i)

            pygame.display.update()

    def run(self):
        """Main game method"""
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("arial", 50)

        while True:
            clock.tick(60)
            self.screen.fill("#E3E3E3")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            keys = pygame.key.get_pressed()

            # Right
            if keys[pygame.K_d] and self.f_right:
                self.krug_rect.x += self.krug_speed
                self.make_true_move()

            # Left
            if keys[pygame.K_a] and self.f_left:
                self.krug_rect.x -= self.krug_speed
                self.make_true_move()

            # up
            if keys[pygame.K_w] and self.f_up:
                self.krug_rect.y -= self.krug_speed
                self.make_true_move()

            # down
            if keys[pygame.K_s] and self.f_down:
                self.krug_rect.y += self.krug_speed
                self.make_true_move()

            # left - right
            if self.krug_rect.left > 820:
                self.krug_rect.right = 0
            if self.krug_rect.right < 0:
                self.krug_rect.left = 820

            # redline collision
            for line in self.redlines:
                if line.colliderect(self.krug_rect):
                    self.krug_rect.center = (410, 200)
                    self.hp -= 1
                    self.line_sound.play()

            # blueline collision
            for line in self.bluelines:
                c = self.krug_rect.clipline(line.bottomleft, line.topleft)
                f = self.krug_rect.clipline(line.bottomright, line.topright)

                if c:
                    r = self.krug_rect.right
                    for i in range(r - 3, r + 3):
                        if i == c[0][0]:
                            self.f_right = False
                if f:
                    l = self.krug_rect.left
                    for i in range(l - 3, l + 3):
                        if i == f[0][0]:
                            self.f_left = False

                    b = self.krug_rect.bottom
                    for i in range(b - 3, b + 3):
                        if i == f[0][1]:
                            self.f_down = False

                    d = self.krug_rect.top
                    for i in range(d - 3, d + 3):
                        if i == f[0][1]:
                            self.f_up = False

            # draw krug
            pygame.draw.circle(self.screen, "#4EAA5C", self.krug_rect.center, 20.0)

            # draw vrag
            pygame.draw.circle(self.screen, "#74121D", self.vrag_rect.center, 20.0)

            # score
            self.screen.blit(font.render(str(self.score), True, (255, 50, 50)), (760, -10))

            # blit coin
            for c in self.coins2:
                self.screen.blit(self.coin, c)
                if c.colliderect(self.krug_rect):
                    self.score += 1
                    ind = self.coins2.index(c)
                    self.coins2.pop(ind)
                    self.coins_sound.play()
                if self.vrag_rect.colliderect(c):
                    ind = self.coins2.index(c)
                    self.coins2.pop(ind)
                    self.coins_sound.play()

            if len(self.coins2) <= 2:
                for s in self.all_coins:
                    if s not in self.coins2:
                        self.coins2.append(s)

            if self.vrag_rect.colliderect(self.krug_rect):
                self.krug_rect.center = (410, 200)
                self.hp -= 1
                self.line_sound.play()
                self.vrag_rect.center = (50, 110)

            # blit lines
            for line in self.redlines:
                pygame.draw.rect(self.screen, "#E81931", line)
            for line in self.bluelines:
                pygame.draw.rect(self.screen, "#3EBDF8", line)

            # blit hp
            for i in range(self.hp):
                self.screen.blit(self.krug_hp, (2 + 47 * i, 2))

            self.vrag_move()

            if self.hp == 0:
                new_db.add_score(self.name, self.score)
                self.leaderbord()

            pygame.display.update()



if __name__ == "__main__":
    Game().run()

