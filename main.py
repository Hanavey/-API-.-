import sys
import pygame
import requests
import os
from interface import Button, FindLine


def create_responce(api, parampampam):
    response = requests.get(api, params=parampampam)
    if response.status_code == 200:
        with open("map.png", "wb") as f:
            f.write(response.content)


def find_place_cord(place):
    server = "http://geocode-maps.yandex.ru/1.x/?"
    API = "8013b162-6b42-4997-9691-77b7074026e0"
    geocoder = place
    request = f"{server}apikey={API}&geocode={geocoder}&format=json"
    response = requests.get(request)
    if response:
        pos = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        return pos
    else:
        return False


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((1000, 600))

    info = pygame.display.Info()
    center = [info.current_w / 2, info.current_h / 2]
    left_center = [0, info.current_h / 2]
    right_center = [info.current_w, info.current_h / 2]
    upper_center = [info.current_w / 2, 0]
    lower_center = [info.current_w / 2, info.current_h]

    theme_button = Button(screen, (right_center[0] - 90, 10), (70, 30))
    findline = FindLine(screen, (center[0] - 325, 20), (400, 35))
    find_button = Button(screen, (center[0] + 80, 15), (80, 45), text="Найти")
    delete_button = Button(screen, (10, 10), (70, 30), text="Delete")

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
        "theme": "light"
    }
    create_responce(api_server, params)

    map_screen = pygame.image.load("map.png")
    screen.blit(map_screen, (center[0] - 325, center[1] - 225))
    pygame.display.flip()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                os.remove("map.png")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if params['scale'] + scale_coefficient < 4:
                        params['scale'] += scale_coefficient
                    create_responce(api_server, params)

                if event.key == pygame.K_PAGEDOWN:
                    if params['scale'] - scale_coefficient > 1:
                        params['scale'] -= scale_coefficient
                    create_responce(api_server, params)

                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    d = 0.001
                    move_dkt = {pygame.K_UP: [lon, str(float(lat) + d)],
                                pygame.K_DOWN: [lon, str(float(lat) - d)],
                                pygame.K_LEFT: [str(float(lon) - d), lat],
                                pygame.K_RIGHT: [str(float(lon) + d), lat]}

                    lon, lat = move_dkt[event.key]
                    params["ll"] = ",".join([lon, lat])
                    create_responce(api_server, params)

        theme_button.update()
        findline.update(events)
        find_button.update()
        delete_button.update()

        if theme_button.result:
            params["theme"] = theme_button.theme
            create_responce(api_server, params)

        if delete_button.result:
            findline.delete()
            if 'pt' in params:
                del params["pt"]
            create_responce(api_server, params)

        if find_button.result:
            pos = find_place_cord(findline.text)
            if pos:
                lon, lat = pos.split()
                params["pt"] = f"{lon},{lat},pm2rdm"
                params["ll"] = f"{lon},{lat}"
                create_responce(api_server, params)
            else:
                print("Не удалось найти координаты для введенного адреса.")
        map_screen = pygame.image.load("map.png")
        screen.blit(map_screen, (center[0] - 325, center[1] - 225))
        pygame.display.flip()
