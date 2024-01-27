import pygame
import sys
import game
import hard_level
import normal_level

pygame.init()
RES = WIDTH, HEIGHT = 900, 700
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


def start_easy():
    game.main()


def start_normal():
    normal_level.main()


def start_hard():
    hard_level.main()


def main():
    class Button:
        def __init__(
            self, width, height, inactive_color, active_color, text,
                font_size=30
        ):
            self.width = width
            self.height = height
            self.inactive_color = pygame.Color(inactive_color)
            self.active_color = pygame.Color(active_color)
            self.text = text
            self.font_size = font_size

        def draw(self, x, y, action=None):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            button_rect = pygame.Rect(x, y, self.width, self.height)

            if button_rect.collidepoint(mouse):
                pygame.draw.rect(sc, self.active_color, button_rect)
                if click[0] == 1 and action is not None:
                    pygame.time.delay(100)
                    # Задержка, чтобы избежать двойного клика
                    action()
            else:
                pygame.draw.rect(sc, self.inactive_color, button_rect)

            font = pygame.font.SysFont("Arial", self.font_size)
            text_surface = font.render(self.text, True, pygame.Color("white"))
            text_rect = text_surface.get_rect(center=button_rect.center)
            sc.blit(text_surface, text_rect)

    # отображения меню
    def show_menu():
        sc.fill(pygame.Color("#293133"))
        title_font = pygame.font.SysFont("Utrom Press Kachat", 150)
        title_surface = title_font.render("THE MAZE", True,
                                          pygame.Color("orange"))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        sc.blit(title_surface, title_rect)

        subtitle_font = pygame.font.SysFont("Arial", 50)
        subtitle_surface = subtitle_font.render(
            "Выбор уровня сложности", True, pygame.Color("orange")
        )
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2,
                                                          HEIGHT // 4))
        sc.blit(subtitle_surface, subtitle_rect)

        button_font_size = 30
        button_width, button_height = 200, 70
        interval = 10  # Расстояние между кнопками
        easy_btn = Button(
            button_width, button_height, "#293133",
            "#387F09", "Легко", button_font_size
        )
        normal_btn = Button(
            button_width,
            button_height,
            "#293133",
            "#230C63",
            "Нормально",
            button_font_size,
        )
        hard_btn = Button(
            button_width,
            button_height,
            "#293133",
            "#91520A",
            "Тяжело",
            button_font_size,
        )

        button_y = HEIGHT // 2
        easy_btn.draw(WIDTH // 2 - button_width // 2,
                      button_y, action=start_easy)
        normal_btn.draw(
            WIDTH // 2 - button_width // 2,
            button_y + button_height + interval,
            action=start_normal,
        )
        hard_btn.draw(
            WIDTH // 2 - button_width // 2,
            button_y + 2 * (button_height + interval),
            action=start_hard,
        )

        pygame.display.update()

    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        show_menu()

        clock.tick(60)
