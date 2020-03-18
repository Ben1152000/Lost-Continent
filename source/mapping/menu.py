import pygame

class Menu():

    backgroundColor = (170, 145, 110)
    foregroundColor = (255, 250, 240)

    def __init__(self, mainmap):
        self.map = mainmap

    def click(self, screen, bounds, coords):
        pass

    def render(self, screen, bounds, font):

        pygame.draw.line(screen, self.foregroundColor,
            (bounds.getMinX(), bounds.getMinY()),
            (bounds.getMaxX(), bounds.getMinY()),
            5)
        pygame.draw.rect(screen, self.backgroundColor, 
            (
                bounds.getMinX(),
                bounds.getMinY(),
                bounds.getMaxX(),
                bounds.getMaxY()
            )
        )
        if self.map.selected > 0:
            fpsLabel = font.render(str(self.map.provinces[self.map.selected].backend.name), True, self.foregroundColor)
            screen.blit(fpsLabel, (bounds.getMinX() + 10, bounds.getMinY() + 10))
        
