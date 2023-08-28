import pygame
import sys


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((820, 400))

        self.coins = 0
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

        self.coin1 = self.coin.get_rect(topleft=(120, 45))
        self.coin2 = self.coin.get_rect(topleft=(770, 50))
        self.coin3 = self.coin.get_rect(topleft=(70, 255))
        self.coin4 = self.coin.get_rect(topleft=(610, 255))
        self.coins = [self.coin1, self.coin2, self.coin3, self.coin4]

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

        self.score = 0

        self.all_coins = [self.coin1, self.coin2, self.coin3, self.coin4]

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
            for c in self.coins:
                self.screen.blit(self.coin, c)
                if c.colliderect(self.krug_rect):
                    self.score += 1
                    ind = self.coins.index(c)
                    self.coins.pop(ind)

            if len(self.coins) <= 2:
                for s in self.all_coins:
                    if s not in self.coins:
                        self.coins.append(s)

            # blit lines
            for line in self.redlines:
                pygame.draw.rect(self.screen, "#E81931", line)
            for line in self.bluelines:
                pygame.draw.rect(self.screen, "#3EBDF8", line)

            # blit hp
            self.screen.blit(self.krug_hp, (-10, 0))
            self.screen.blit(self.krug_hp, (30, 0))
            self.screen.blit(self.krug_hp, (70, 0))

            self.vrag_move()

            pygame.display.update()


if __name__ == "__main__":
    Game().run()
