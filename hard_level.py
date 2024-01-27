import pygame
from random import choice
from random import choice, randint
import sys
import sqlite3
import menu1
import random


def main():
    RES = WIDTH, HEIGHT = 1200, 795
    TILE = 50
    cols, rows = WIDTH // TILE, HEIGHT // TILE

    pygame.init()
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    coin_images = [
        pygame.image.load("images/flag_1.png"),
        pygame.image.load("images/flag_2.png"),
        pygame.image.load("images/flag_3.png"),
        pygame.image.load("images/flag_4.png"),
        pygame.image.load("images/flag_5.png"),
        pygame.image.load("images/flag_6.png"),
        pygame.image.load("images/flag_7.png"),
        pygame.image.load("images/flag_8.png"),
        pygame.image.load("images/flag_9.png"),
    ]
    current_frame = 0
    animation_time = 0
    frame_duration = 100

    class Button:
        def __init__(self, width, height, color, hover_color, text,
                     font_size=30):
            self.width = width
            self.height = height
            self.color = color
            self.hover_color = hover_color
            self.font_size = font_size
            self.text = text

            self.font = pygame.font.Font(None, font_size)

            self.rect = pygame.Rect(0, 0, width, height)

        def draw(self, x, y):
            # Получаем текущую позицию курсора
            mouse_pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_pos):
                color = self.hover_color
            else:
                color = self.color

            pygame.draw.rect(sc, color, self.rect)

            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)

            sc.blit(text_surface, text_rect)

            return self.rect  # Возвращаем rect для кнопки

        def set_position(self, x, y):
            self.rect.x = x
            self.rect.y = y

    class Cell:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {"top": True, "right": True,
                          "bottom": True, "left": True}
            self.visited = False

        def draw_background(self, color):
            x, y = self.x * TILE, self.y * TILE
            pygame.draw.rect(sc, color, (x, y, TILE, TILE))

        def draw_current_cell(self):
            x, y = self.x * TILE, self.y * TILE
            pygame.draw.rect(
                sc, pygame.Color("saddlebrown"),
                (x + 2, y + 2, TILE - 2, TILE - 2)
            )

        def draw(self):
            x, y = self.x * TILE, self.y * TILE
            if self.visited:
                pygame.draw.rect(sc, pygame.Color("black"), (x, y, TILE, TILE))

            if self.walls["top"]:
                pygame.draw.line(
                    sc, pygame.Color("darkorange"), (x, y), (x + TILE, y), 3
                )
            if self.walls["right"]:
                pygame.draw.line(
                    sc,
                    pygame.Color("darkorange"),
                    (x + TILE, y),
                    (x + TILE, y + TILE),
                    3,
                )
            if self.walls["bottom"]:
                pygame.draw.line(
                    sc,
                    pygame.Color("darkorange"),
                    (x + TILE, y + TILE),
                    (x, y + TILE),
                    3,
                )
            if self.walls["left"]:
                pygame.draw.line(
                    sc, pygame.Color("darkorange"), (x, y + TILE), (x, y), 3
                )

        def check_cell(self, x, y):
            find_index = lambda x, y: x + y * cols
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return grid_cells[find_index(x, y)]

        def check_neighbors(self):
            neighbors = []
            top = self.check_cell(self.x, self.y - 1)
            right = self.check_cell(self.x + 1, self.y)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)
            if top and not top.visited:
                neighbors.append(top)
            if right and not right.visited:
                neighbors.append(right)
            if bottom and not bottom.visited:
                neighbors.append(bottom)
            if left and not left.visited:
                neighbors.append(left)
            return choice(neighbors) if neighbors else False

    pygame.font.init()
    font = pygame.font.Font(None, 60)

    conn = sqlite3.connect("score.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS eda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER
    )
    """
    )
    conn.commit()

    def back_to_menu():
        import menu1

        menu1.main_menu()

    def spawn_enemy():
        global enemy
        start_x, start_y = 0, 0
        # Создание экземпляра Enemy
        enemy = Enemy("ghost_2(2).png", start_x, start_y)
        enemy.draw()

    enemy_spawn_time = 5000
    enemy_timer = pygame.time.get_ticks()
    enemy = None

    enemy_move_timer = pygame.time.get_ticks()
    enemy_move_time = 1000  # Враг двигается каждую секунду

    def show_victory_message():
        high_score = get_high_score()
        scoreitog = score * 1000 / (elapsed_seconds / 4)
        poland = int(scoreitog)
        text = font.render(
            f"Вы выиграли! Время:"
            f" {elapsed_seconds} сек. Собрано монет: {score}",
            True,
            pygame.Color("orange"),
        )
        score_text = font.render(f"Ваш счёт: {poland}",
                                 True, pygame.Color("orange"))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        score_text_rect = score_text.get_rect(
            center=(WIDTH // 2, text_rect.bottom + 40)
        )

        high_score_text = font.render(
            f"Лучший счёт: {high_score}", True, pygame.Color("orange")
        )
        high_score_rect = high_score_text.get_rect(
            center=(WIDTH // 2, score_text_rect.bottom + 40)
        )

        cursor.execute("INSERT INTO eda (score) VALUES (?)", (scoreitog,))
        conn.commit()

        back_button = Button(
            200, 50, "skyblue", "lightskyblue",
            "Вернуться в меню", font_size=30
        )
        back_button_rect = back_button.draw(
            WIDTH // 2 - 100, high_score_rect.bottom + 60
        )

        pygame.display.flip()

        in_victory = True
        while in_victory:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_victory = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if back_button_rect.collidepoint(mouse_pos):
                        import menu1

                        menu1.main()

            sc.blit(text, text_rect)
            sc.blit(score_text, score_text_rect)
            sc.blit(high_score_text, high_score_rect)
            back_button_rect = back_button.draw(
                WIDTH // 2 - 100, high_score_rect.bottom + 60
            )
            pygame.display.flip()

            clock.tick(30)

    def show_lose_message():
        sc.fill(pygame.Color("black"))
        text = font.render(
            f"Вы проиграли! Время:"
            f" {elapsed_seconds} сек. Собрано монет: {score}",
            True,
            pygame.Color("orange"),
        )
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        score_text_rect = score_text.get_rect(
            center=(WIDTH // 2, text_rect.bottom + 40)
        )

        back_button = Button(
            200, 50, "skyblue",
            "lightskyblue", "Вернуться в меню",
            font_size=30
        )

        pygame.display.flip()

        in_victory = True
        while in_victory:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_victory = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if back_button_rect.collidepoint(mouse_pos):
                        import menu1

                        menu1.main()

            sc.blit(text, text_rect)
            sc.blit(score_text, score_text_rect)
            back_button_rect = back_button.draw(WIDTH // 2 - 100, 60)
            pygame.display.flip()

            clock.tick(30)

    def remove_walls(current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls["left"] = False
            next.walls["right"] = False
        elif dx == -1:
            current.walls["right"] = False
            next.walls["left"] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls["top"] = False
            next.walls["bottom"] = False
        elif dy == -1:
            current.walls["bottom"] = False
            next.walls["top"] = False

    class Player:
        def __init__(self, pic, x, y):
            self.x, self.y = x, y
            self.color = pygame.Color("red")
            self.image = pygame.image.load(f"images/{pic}")
            self.images = {
                "up": pygame.image.load("images/up_1(2).png"),
                "down": pygame.image.load("images/run_down_2(2).png"),
                "left": pygame.image.load("images/left_1(2).png"),
                "right": pygame.image.load("images/right_1(2).png"),
            }

            self.direction = "down"

        def draw(self):
            delta = (self.image.get_width() - TILE) + 2
            sc.blit(
                self.images[self.direction],
                (self.x * TILE - delta, self.y * TILE - delta),
            )

        def move(self, dx, dy):
            new_x = self.x + dx
            new_y = self.y + dy
            # Проверка на наличие стен в заданном направлении
            if (dx == -1 and
                    not grid_cells[self.y * cols + new_x].walls["right"]):
                self.direction = "left"
                self.x = new_x
            elif (dx == 1 and
                  not grid_cells[self.y * cols + self.x].walls["right"]):
                self.direction = "right"
                self.x = new_x
            elif (dy == -1 and
                  not grid_cells[new_y * cols + self.x].walls["bottom"]):
                self.direction = "up"
                self.y = new_y
            elif (dy == 1 and
                  not grid_cells[self.y * cols + self.x].walls["bottom"]):
                self.direction = "down"
                self.y = new_y

    class Coin:
        def __init__(self, pics, x, y):

            self.x = x
            self.y = y
            self.frame_count = 0
            self.image_index = 0
            self.animation_speed = 17

            self.color = pygame.Color("#FFCF48")
            self.rect = pygame.Rect(
                x * TILE + TILE // 4,
                y * TILE + TILE // 4, TILE // 2, TILE // 2
            )
            self.images = [pygame.image.load(f"images/{pic}") for pic in pics]

        def draw(self):
            if self.frame_count % self.animation_speed == 0:
                self.image_index = (self.image_index + 1) % len(self.images)
            sc.blit(self.images[self.image_index],
                    (self.rect.x + 7, self.rect.y + 10))

            self.frame_count += 1

    class Enemy:
        def __init__(self, pic, x, y):
            self.x = x
            self.y = y
            self.path = []  # Путь, по которому будет двигаться враг
            self.color = pygame.Color("blue")
            self.walls = {"top": True, "right": True,
                          "bottom": True, "left": True}
            self.image = pygame.image.load(f"images/{pic}")

        def draw(self):
            delta = (self.image.get_width() - TILE) + 2
            sc.blit(self.image, (self.x * TILE - delta, self.y * TILE - delta))

        def move_towards_player(self, grid_cells, cols, rows):

            # Вычисляем разницу по координатам между врагом и игроком
            delta_x = player.x - self.x
            delta_y = player.y - self.y

            moved = False
        # Пытаемся двигаться по горизонтали в сторону игрока, если это возможно
            if delta_x > 0:  # Игрок находится справа от врага
                self.x += 1
                moved = True
            elif delta_x < 0:  # Игрок находится слева от врага

                self.x -= 1
                moved = True

            # если ничерта не получилось ходим как карты лягут
            if not moved:
                if delta_y > 0:
                    self.y += 1
                elif delta_y < 0:
                    self.y -= 1

    def get_high_score():
        cursor.execute("SELECT MAX(score) FROM eda")
        return cursor.fetchone()[0]

    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    colors, color = [], 40
    player = Player("stand (1).png", 0, 0)
    start_cell = grid_cells[0]
    end_cell = grid_cells[-1]
    coin_images_2 = [
        "moneta_1.png",
        "moneta_2.png",
        "moneta_3.png",
        "moneta_4.png",
        "moneta_5.png",
        "moneta_6.png",
        "moneta_7.png",
        "moneta_8.png",
    ]
    coins = [
        Coin(coin_images_2, randint(1, cols - 2), randint(1, rows - 2))
        for _ in range(40)
    ]

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    width, height = 1200, 900
    screen = pygame.display.set_mode((width, height))

    font = pygame.font.Font(None, 36)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    score = 0

    while True:

        sc.fill(pygame.Color("black"))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)
        current_time = pygame.time.get_ticks()

        # таймер (по сути можно это удалить, но мне страшно)
        elapsed_time = pygame.time.get_ticks() - start_time
        elapsed_seconds = elapsed_time // 1000
        timer_text = font.render(f"Время: {elapsed_seconds} сек", True, BLACK)
        timer_rect = timer_text.get_rect(topright=(width - 10, 10))

        # до сюда

        # cчётчик (по сути можно это удалить, но мне страшно)

        score_text = font.render(f"Монеты: {score}", True, BLACK)
        score_rect = score_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, score_rect)

        # до сюда
        if player.x == end_cell.x and player.y == end_cell.y:
            show_victory_message()

        [cell.draw() for cell in grid_cells]
        current_cell.visited = True
        current_cell.draw_current_cell()
        [
            pygame.draw.rect(
                sc,
                colors[i],
                (cell.x * TILE + 2, cell.y * TILE + 2, TILE - 4, TILE - 4),
            )
            for i, cell in enumerate(stack)
        ]

        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            colors.append((min(color, 255), 10, 100))
            color += 1
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        for cell in grid_cells:
            cell.draw()
        start_cell.draw_background(pygame.Color("#EE204D"))

        for coin in coins:
            coin.draw()
        player_cell_index = player.y * cols + player.x
        for coin in coins[:]:
            if coin.rect.colliderect(player.x * TILE,
                                     player.y * TILE, TILE, TILE):
                coins.remove(coin)
                score += 1
        player.draw()
        player_cell_index = player.y * cols + player.x
        current_time = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        if enemy is None and current_time - enemy_timer > enemy_spawn_time:
            spawn_enemy()
            enemy = Enemy("ghost_2(2).png", 0, 0)

        if enemy:
            enemy.draw()

        if enemy is not None:
            current_time = pygame.time.get_ticks()
            if current_time - enemy_move_timer > 600:
                enemy_move_timer = pygame.time.get_ticks()

                enemy.move_towards_player(grid_cells, cols, rows)

        if player is not None and enemy is not None:
            if player.x == enemy.x and player.y == enemy.y:
                show_lose_message()
                running = False

        animation_time += clock.get_time()
        if animation_time >= frame_duration:
            current_frame = (current_frame + 1) % len(
                coin_images
            )  # Переключение кадров
            animation_time = 0

        screen.blit(coin_images[current_frame], (1165, 710))

        pygame.display.flip()

        clock.tick(3000)
