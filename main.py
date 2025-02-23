import sys
import pygame
import requests
import os


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((650, 450))

    api_server = "https://static-maps.yandex.ru/v1"

    lon = "28.98513"
    lat = "41.036943"
    delta1 = "0.0029"
    delta2 = "0.0029"
    apikey = "81b63ec7-b5bf-4e94-97fd-5645a56b1305"
    scale_coefficient = 0.25

    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta1, delta2]),
        "size": '650,450',
        "scale": 1,
        "apikey": apikey,
    }
    response = requests.get(api_server, params=params)

    if response.status_code == 200:
        with open("map.png", "wb") as f:
            f.write(response.content)

    map_screen = pygame.image.load("map.png")
    screen.blit(map_screen, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove("map.png")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if params['scale'] + scale_coefficient < 4:
                        params['scale'] += scale_coefficient
                    response = requests.get(api_server, params=params)

                    if response.status_code == 200:
                        with open("map.png", "wb") as f:
                            f.write(response.content)

                if event.key == pygame.K_PAGEDOWN:
                    if params['scale'] - scale_coefficient > 1:
                        params['scale'] -= scale_coefficient
                    response = requests.get(api_server, params=params)

                    if response.status_code == 200:
                        with open("map.png", "wb") as f:
                            f.write(response.content)

        map_screen = pygame.image.load("map.png")
        screen.blit(map_screen, (0, 0))
        pygame.display.flip()
