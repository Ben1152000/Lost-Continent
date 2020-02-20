import pygame, math
import game

FPS = GAMECLOCK = DISPLAYSCREEN = None

def main():
    global FPS, GAMECLOCK, DISPLAYSCREEN

    pygame.init()

    FPS = 45
    WINDOWWIDTH = 680
    WINDOWHEIGHT = 480
    if False:
        WINDOWWIDTH = pygame.display.Info().current_w # Set the screen width and height to cover screen
        WINDOWHEIGHT = pygame.display.Info().current_h - 92 # 92 for bottom bar

    GAMECLOCK = pygame.time.Clock()
    flags = pygame.DOUBLEBUF
    DISPLAYSCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), flags)
    pygame.display.set_caption("Hyperagressive Birds")
    showMapScene()

def showMapScene():
    mainmap = game.mapping.Map("../resources/parsedMap.json")
    viewport = game.rectangle.Rectangle(-15, -0, 35, 25)
    font = pygame.font.Font(None, 30)

    ZOOMSPEED = 1
    MOVESPEED = 0.5
    MINZOOM = 5
    MAXZOOM = 100
    done = False
    while not done: # Game loop
        dt = GAMECLOCK.get_time() / 1000.0 # prev tick in seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if viewport.getWidth() > MINZOOM:
                        viewport.scale(-ZOOMSPEED * dt, -ZOOMSPEED * dt)
                if event.button == 5:
                    if viewport.getWidth() < MAXZOOM:
                        viewport.scale(ZOOMSPEED * dt, ZOOMSPEED * dt)
        
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_a]: viewport.translate(-MOVESPEED * viewport.getWidth() * dt, 0)
        if pressed[pygame.K_w]: viewport.translate(0, MOVESPEED * viewport.getWidth() * dt)
        if pressed[pygame.K_d]: viewport.translate(MOVESPEED * viewport.getWidth() * dt, 0)
        if pressed[pygame.K_s]: viewport.translate(0, -MOVESPEED * viewport.getWidth() * dt)

        DISPLAYSCREEN.fill((0, 0, 0))
        
        fpsLabel = font.render("fps: " + str(int(GAMECLOCK.get_fps())), True, (255, 255, 255))
        DISPLAYSCREEN.blit(fpsLabel, (0, 0))

        mainmap.render(DISPLAYSCREEN, viewport)
        pygame.display.flip()
        GAMECLOCK.tick(FPS)



def draw(surface):
    color = (255, 0, 0) # red
    
    # draw a rectangle
    pygame.draw.rect(surface, color, pygame.Rect(10, 10, 100, 100), 10)

    # draw a circle
    pygame.draw.circle(surface, color, (300, 60), 50, 10)

if __name__ == "__main__":
    main()
