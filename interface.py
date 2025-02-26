import pygame


class Button:
    def __init__(self, screen, button_cor, button_size):
        self.screen = screen
        self.button_x = button_cor[0]
        self.button_y = button_cor[1]
        self.button_width = button_size[0]
        self.button_height = button_size[1]
        self.color = None
        self.font = pygame.font.Font(None, 30)
        self.theme = "light"
        self.count = 0
        self.lmb = False

    def update(self):
        result = False
        mx, my = pygame.mouse.get_pos()
        theme_button = pygame.Surface((self.button_width, self.button_height))
        theme_button.fill((200, 200, 200))
        if (self.button_x <= mx <= self.button_x + self.button_width and
                self.button_y <= my <= self.button_y + self.button_height):
            theme_button.fill((150, 150, 150))
            if pygame.mouse.get_pressed()[0] and not self.lmb:
                self.count = (self.count + 1) % 2
                self.theme = ["light", "dark"][self.count]
                result = True
                self.lmb = True

        if not pygame.mouse.get_pressed()[0]:
            self.lmb = False
        theme_text = self.font.render(self.theme, True, "black")
        theme_button.blit(theme_text, (7, 6))
        self.screen.blit(theme_button, (self.button_x, self.button_y))

        return result
