import pygame
import sys
import menu1

pygame.init()
RES = WIDTH, HEIGHT = 900, 700
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


def start_game():
    import menu1
    pygame.quit()


class Button:
    def __init__(self, width, height, inactive_color, active_color, text):
        self.width = width
        self.height = height
        self.inactive_color = pygame.Color(inactive_color)
        self.active_color = pygame.Color(active_color)
        self.text = text

    def draw(self, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(sc, self.active_color, (x, y, self.width,
                                                     self.height))
            if click[0] == 1 and action:
                pygame.time.delay(300)  # для предотвращения many clicks
                action()
        else:
            pygame.draw.rect(sc, self.inactive_color, (x, y, self.width,
                                                       self.height))

        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(self.text, True, pygame.Color("white"))
        text_rect = text_surface.get_rect(
            center=(x + self.width / 2, y + self.height / 2)
        )
        sc.blit(text_surface, text_rect)


# Отрисовка меню
def show_menu():
    sc.fill(pygame.Color("#293133"))
    title_font = pygame.font.SysFont("Utrom Press Kachat", 150)
    title_surface = title_font.render("THE MAZE", True, pygame.Color("orange"))
    title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    sc.blit(title_surface, title_rect)

    btn_width, btn_height = 200, 50
    start_btn = Button(btn_width, btn_height, "#49423D", "lightgreen",
                       "Начать игру")

    start_btn.draw(WIDTH / 2 - btn_width / 2, HEIGHT / 2, action=start_game)

    pygame.display.update()


def start_game():
    # Запуск
    menu1.main()


menu_active = True
while menu_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.set_caption("The Maze")
    show_menu()

    clock.tick(60)
