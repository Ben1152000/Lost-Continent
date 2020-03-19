import pygame, math
import mapping
from backend import game

FPS = GAMECLOCK = DISPLAYSCREEN = None

def main():
    global FPS, GAMECLOCK, DISPLAYSCREEN

    pygame.init()

    FPS = 30
    WINDOWWIDTH = 800
    WINDOWHEIGHT = 600
    if False:
        WINDOWWIDTH = pygame.display.Info().current_w # Set the screen width and height to cover screen
        WINDOWHEIGHT = pygame.display.Info().current_h - 92 # 92 for bottom bar

    GAMECLOCK = pygame.time.Clock()
    flags = pygame.DOUBLEBUF
    DISPLAYSCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), flags)
    pygame.display.set_caption("The Lost Continent")
    showMapScene()

def showMapScene():
    mainmap = mapping.mapping.Map("../resources/map.json")
    viewport = mapping.rectangle.Rectangle(-18, -0, 35, 25)
    font = pygame.font.Font(None, 30)
    gameState = game.Game()
    gameState.load("backend/data.json")
    for province in mainmap.provinces:
        province.backend = gameState.provinces[province.pid]

    provenceMenu = mapping.menu.Menu(mainmap, gameState)

    menuHeight = 150
    mainmapRect = mapping.rectangle.Rectangle(0, DISPLAYSCREEN.get_width(), 0, DISPLAYSCREEN.get_height() - menuHeight)
    menuRect = mapping.rectangle.Rectangle(0, DISPLAYSCREEN.get_width(), DISPLAYSCREEN.get_height() - menuHeight, DISPLAYSCREEN.get_height())

    ZOOMSPEED = 1
    MOVESPEED = 0.5
    MINZOOM = 5
    MAXZOOM = 130
    TICKTIME = 0.05

    timeSinceLastTick = 0

    done = False
    while not done: # Game loop
        
        dt = GAMECLOCK.get_time() / 1000.0 # prev tick in seconds
        timeSinceLastTick += dt

        if timeSinceLastTick > TICKTIME:
            timeSinceLastTick = 0
            gameState.tick()
            provenceMenu.update(DISPLAYSCREEN, menuRect, font)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    done = True

                if event.key == pygame.K_RETURN:
                    gameState.execute("explore FRA " + str(mainmap.selected))

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    clickPos = mapping.vertex.Vertex(event.pos[0], event.pos[1])
                    if clickPos in mainmapRect:
                        mainmap.click(DISPLAYSCREEN, mainmapRect, event.pos, viewport)
                    elif clickPos in menuRect:
                        provenceMenu.click(DISPLAYSCREEN, menuRect, event.pos)
                    provenceMenu.update(DISPLAYSCREEN, menuRect, font)

                if event.button == 4:
                    if viewport.getWidth() > MINZOOM:
                        viewport.scale(-ZOOMSPEED * dt, -ZOOMSPEED * dt)

                if event.button == 5:
                    if viewport.getWidth() < MAXZOOM:
                        viewport.scale(ZOOMSPEED * dt, ZOOMSPEED * dt)

            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    clickPos = mapping.vertex.Vertex(event.pos[0], event.pos[1])
                    if clickPos in menuRect:
                        provenceMenu.release(DISPLAYSCREEN, menuRect, event.pos)
                    provenceMenu.update(DISPLAYSCREEN, menuRect, font)
        
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_a]: viewport.translate(-MOVESPEED * viewport.getWidth() * dt, 0)
        if pressed[pygame.K_w]: viewport.translate(0, MOVESPEED * viewport.getWidth() * dt)
        if pressed[pygame.K_d]: viewport.translate(MOVESPEED * viewport.getWidth() * dt, 0)
        if pressed[pygame.K_s]: viewport.translate(0, -MOVESPEED * viewport.getWidth() * dt)

        DISPLAYSCREEN.fill((20, 40, 90))

        mainmap.render(DISPLAYSCREEN, mainmapRect, viewport, pygame.time.get_ticks(), gameState.factions["FRA"], font)
        provenceMenu.render(DISPLAYSCREEN, menuRect, font)

        fpsLabel = font.render("fps: " + str(int(GAMECLOCK.get_fps())), True, (255, 255, 255))
        DISPLAYSCREEN.blit(fpsLabel, (5, 5))

        dateLabel = font.render(str(gameState.date), True, (255, 255, 255))
        DISPLAYSCREEN.blit(dateLabel, (5, 30))

        pygame.display.flip()
        GAMECLOCK.tick(FPS)

if __name__ == "__main__":
    main()
