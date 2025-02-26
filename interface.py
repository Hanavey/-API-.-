import pygame


class Button:
    def __init__(self, screen, button_cor, button_size, text=""):
        self.screen = screen
        self.button_x = button_cor[0]
        self.button_y = button_cor[1]
        self.button_width = button_size[0]
        self.button_height = button_size[1]
        self.font = pygame.font.Font(None, 30)
        self.theme = "light"
        self.count = 0
        self.lmb = False
        self.result = False
        self.text = text

    def update(self):
        self.result = False
        mx, my = pygame.mouse.get_pos()
        theme_button = pygame.Surface((self.button_width, self.button_height))
        theme_button.fill((200, 200, 200))
        if (self.button_x <= mx <= self.button_x + self.button_width and
                self.button_y <= my <= self.button_y + self.button_height):
            theme_button.fill((150, 150, 150))
            if pygame.mouse.get_pressed()[0] and not self.lmb:
                self.count = (self.count + 1) % 2
                self.theme = ["light", "dark"][self.count]
                self.result = True
                self.lmb = True

        if not pygame.mouse.get_pressed()[0]:
            self.lmb = False
        if self.text:
            theme_text = self.font.render(self.text, True, "black")
        else:
            theme_text = self.font.render(self.theme, True, "black")
        theme_button.blit(theme_text, (7, (self.button_height // 2) - 10))
        self.screen.blit(theme_button, (self.button_x, self.button_y))


class FindLine:
    def __init__(self, screen, line_cor, line_size):
        self.screen = screen
        self.line_x = line_cor[0]
        self.line_y = line_cor[1]
        self.line_width = line_size[0]
        self.line_height = line_size[1]
        self.lmb = False
        self.input_active = False
        self.text = ""
        self.font = pygame.font.Font(None, 30)

    def update(self, events):
        mx, my = pygame.mouse.get_pos()
        find_line = pygame.Surface((self.line_width, self.line_height))
        find_line.fill((255, 255, 255))

        if pygame.mouse.get_pressed()[0] and not self.lmb:
            self.lmb = True
            if (self.line_x <= mx <= self.line_x + self.line_width and
                    self.line_y <= my <= self.line_y + self.line_height):
                self.input_active = True
            else:
                self.input_active = False

        if not pygame.mouse.get_pressed()[0]:
            self.lmb = False

        self.input_text(events)
        line_text = self.font.render(self.text, True, "black")
        find_line.blit(line_text, (7, 6))
        self.screen.blit(find_line, (self.line_x, self.line_y))

    def input_text(self, events):
        if self.input_active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and self.text:
                        self.text = self.text[:-1]
                    elif event.unicode.isprintable():
                        self.text += event.unicode

    def delete(self):
        self.text = ""

class Label:
    def __init__(self, screen, label_cor, label_size):
        self.screen = screen
        self.label_cor = label_cor
        self.label_size = label_size
        self.text = ''
        self.font = pygame.font.Font(None, 30)

    def update(self):
        label_line = pygame.Surface((self.label_size[0], self.label_size[1]))
        label_line.fill((255, 255, 255))
        label_text = self.font.render(self.text, True, "black")
        label_line.blit(label_text, (7, 6))
        self.screen.blit(label_line, (self.label_cor[0], self.label_cor[1]))

    def set_text(self, text):
        self.text = text
