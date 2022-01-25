import pygame
import random
import time

pygame.init()
# шрифты
font1 = pygame.font.SysFont("Arial", 45, True)
font2 = pygame.font.SysFont("corbel", 90, True)
font3 = pygame.font.SysFont("Arial", 28, True)
font4 = pygame.font.SysFont("Arial", 20, True)
font5 = pygame.font.SysFont('Arial', 16, True)
# фоны
bg = pygame.image.load('floor1.jpg')
bg1 = pygame.image.load('floor.jpg')
bg3 = pygame.image.load('victory.jpg')

# создание таймера
def get_time(h, min, s):
    if len(str(h)) > 1:
        a = str(h)
    else:
        a = "0" + str(h)

    if len(str(min)) > 1:
        b = str(min)
    else:
        b = "0" + str(min)

    if len(str(s)) > 1:
        c = str(s)
    else:
        c = "0" + str(s)

    return a + ":" + b + ":" + c


# параметры таймера (часы, минуты, секунды)
def draw_time(st, p):
    hour = 0
    minute = 0
    second = 0
    curt = time.time() - p - st
    if curt > 3600:
        while True:
            if curt - 3600 > 0:
                hour += 1
                curt -= 3600
            else:
                while True:
                    if curt - 60 > 0:
                        minute += 1
                        curt -= 60
                    else:
                        second += int(curt)
                        break
                break

    else:
        while True:
            if curt - 60 > 0:
                minute += 1
                curt -= 60
            else:
                second += int(curt)
                break
    # настраиваем таймер и задний фон таймера
    return [font1.render(get_time(hour, minute, second), True, (0, 0, 0), (255, 255, 255)),
            get_time(hour, minute, second)]


class cell:
    def __init__(self, up, down, left, right):
        self.visited = False
        self.walls = [up, down, left, right]


class labyrinth:
    # создание лабиринта
    def __init__(self, id):
        self.id = id
        self.walls = []
        self.lab_walls = []
        self.cells = []

        q = 0
        t = 0

        for f in range(22):
            for s in range(28):
                if not (f in (0, 1, 2) and s > 20):
                    self.cells.append(
                        cell((q + 8, t, 25, 8), (q + 8, t + 33, 25, 8), (q, t + 8, 8, 25), (q + 33, t + 8, 8, 25)))
                q += 33
            q = 0
            t += 33

        for v in self.cells[0].walls:
            self.lab_walls.append(v)
            self.walls.append(v)

        self.cells[0].visited = True

        while len(self.walls) > 0:
            wall = random.choice(self.walls)
            divided_cells = []
            for u in self.cells:
                if wall in u.walls:
                    divided_cells.append(u)

            if len(divided_cells) > 1 and (not ((divided_cells[0].visited and divided_cells[1].visited) or (
                    (not divided_cells[0].visited) and (not divided_cells[1].visited)))):
                for k in divided_cells:
                    k.walls.remove(wall)
                    if k.visited == False:
                        k.visited = True

                    for q in k.walls:
                        if not q in self.walls:
                            self.walls.append(q)

                        if not q in self.lab_walls:
                            self.lab_walls.append(q)

                    if wall in self.lab_walls:
                        self.lab_walls.remove(wall)

            self.walls.remove(wall)

        for j in range(0, 736, 33):
            for i in range(0, 951, 33):
                self.lab_walls.append((i, j, 8, 8))

    def draw(self, finish):
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        for k in self.lab_walls:
            pygame.draw.rect(screen, color, pygame.Rect(k[0], k[1], k[2], k[3]))

        pygame.draw.rect(screen, color, pygame.Rect(695, 0, 400, 125))  # отдельное поле для таймера
        pygame.draw.rect(screen, (0, 255, 0), finish)  # выход


id = 0
running = True
while running:
    pygame.display.set_caption('Продвинутый лабиринт')
    screen = pygame.display.set_mode((930, 733))
    done = False
    star = False
    color = (255, 255, 0)
    x = 16
    y = 16
    clock = pygame.time.Clock()
    start = time.time()
    id += 1
    lab = labyrinth(id)
    fincoord = pygame.Rect(899, 701, 25, 25)
    victory = False
    start_window = False
    speed = 3
    pause = False
    volume = False
    pause_time = 0  # таймер ставится на пауз

    while not done:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True
                running = False
            # обработка паузы
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if pause:
                        pause = False
                        pause_time += time.time() - pause_time_start
                        pygame.mixer.music.unpause()
                    else:
                        pause = True
                        pause_time_start = time.time()
                        pygame.mixer.music.pause()

                if event.key == pygame.K_RETURN:
                    done = True
        # окно паузы
        if pause:
            screen.fill((0, 0, 0))
            screen.blit(bg1, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(318, 275, 300, 115))
            pause_text = font2.render("Пауза", True, (0, 255, 0))
            screen.blit(pause_text, (468 - (pause_text.get_width() // 2), 330 - (pause_text.get_height() // 2)))
        # если не победа и не пауза (Главное окно)
        if not victory and not pause:
            move_up = True
            move_down = True
            move_left = True
            move_right = True
            pressed = pygame.key.get_pressed()
            # обработка нажатий на кнопки
            if pressed[pygame.K_w] or pressed[pygame.K_UP]:
                for m in lab.lab_walls:
                    player = pygame.Rect(x, y - speed, 13, 13)
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_up = False
                        break
                if move_up:
                    y -= speed

            if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                player = pygame.Rect(x, y + speed, 13, 13)
                for m in lab.lab_walls:
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_down = False
                        break
                if move_down:
                    y += speed

            if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                player = pygame.Rect(x - speed, y, 13, 13)
                for m in lab.lab_walls:
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_left = False
                        break
                if move_left:
                    x -= speed

            if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                player = pygame.Rect(x + speed, y, 13, 13)
                for m in lab.lab_walls:
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_right = False
                        break
                if move_right:
                    x += speed

            # кнопка разработчика для проверки окна победы
            if pressed[pygame.K_LCTRL]:
                victory = True

            # проверяем дошёл ли игрок до финиша
            if fincoord.colliderect((x, y, 15, 15)):
                victory = True

            # рисуем окно
            lab.draw(fincoord)
            text = draw_time(start, pause_time)
            pygame.draw.rect(screen, (127, 0, 255), pygame.Rect(x, y, 13, 13))
            pause_button = font4.render("Нажмите ESC = пауза", True, (0, 0, 0))
            screen.blit(pause_button, (810 - (pause_button.get_width() // 2), 80 - (pause_button.get_height() // 2)))
            screen.blit(text[0], (730, 15))

        # если победа (окно победы)
        if victory:
            screen.fill((0, 0, 0))
            # устанавливаем фон
            screen.blit(bg3, (0, 0))
            time_text = font1.render("Время: " + text[1], True, (199, 21, 133))
            victory_text = font2.render("ПОБЕДА!", True, (255, 195, 0))
            reset = font3.render("(Нажмите Enter чтобы начать новую игру)", True, (0, 255, 0))
            # останавливаем музыку
            pygame.mixer.music.stop()

            # задний фон для текста, чтобы лучше было видно
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(167, 378, 600, 45))
            # расположение текста на экране
            screen.blit(victory_text, (468 - (victory_text.get_width() // 2), 228 - (victory_text.get_height() // 2)))
            screen.blit(time_text, (
                                    468 - (time_text.get_width() // 2), (225 - (time_text.get_height() // 2)) +
                                    victory_text.get_height()))
            screen.blit(reset, (468 - (reset.get_width() // 2),
                                (258 - (reset.get_height() // 2)) + victory_text.get_height() + time_text.get_height()))

        clock.tick(60)
        pygame.display.flip()
