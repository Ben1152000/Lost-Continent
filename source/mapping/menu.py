import pygame

class Box():

    def __init__(self, parent, x, y, w, h, color, border, borderColor):
        self.parent = parent
        if self.parent == None: self.rect = pygame.Rect((x, y, w, h))
        else: self.rect = pygame.Rect((x + parent.rect.x, y + parent.rect.y, w, h))
        self.color = color
        self.border = border
        self.borderColor = borderColor
    
    def setColor(self, color):
        self.color = color

    def render(self, screen):
        borderRect = pygame.Rect((self.rect.x + self.border, self.rect.y + self.border, self.rect.w - 2 * self.border, self.rect.h - 2 * self.border))
        pygame.draw.rect(screen, self.borderColor, self.rect)
        pygame.draw.rect(screen, self.color, borderRect)

class Button(Box):

    def __init__(self, parent, x, y, w, h, color, border, borderColor):
        super().__init__(parent, x, y, w, h, color, border, borderColor)
        self.toggled = False
        self.active = False
    
    def click(self, location):
        if self.rect.collidepoint(location):
            self.active = True
            self.doWhenClicked()

    def doWhenClicked(self):
        pass

    def release(self, location=None):
        if location == None or (self.rect.collidepoint(location) and self.active):
            self.active = False
            self.toggled = not self.toggled
            self.doWhenReleased()
        else:
            self.active = False
            self.doWhenCancelled()
        
    def doWhenReleased(self):
        pass

    def doWhenCancelled(self):
        pass

class ExploreButton(Button):

    def __init__(self, parent, game, province, x, y, w, h, color, border, borderColor):
        self.game = game
        self.province = province
        super().__init__(parent, x, y, w, h, color, border, borderColor)
    
    def doWhenClicked(self):
        self.game.factions["FRA"].assignExplorer(self.province.pid)
    

class Menu():

    backgroundColor = (170, 145, 110)
    foregroundColor = (255, 250, 240)
    enabledColor = (200, 160, 130)
    disabledColor = (180, 180, 180)

    def __init__(self, mainmap, gamestate):
        self.map = mainmap
        self.state = gamestate

    def reset(self):
        self.fpsLabel = None
        self.infrastructureLabel = None
        self.civilianLabel = None
        self.transportLabel = None
        self.extractionLabel = None
        self.exploreLabel = None
        self.exploreButton = None

    def update(self, screen, bounds, font):
        
        self.reset()

        if self.map.selected > 0:

            selectedProvince = self.map.provinces[self.map.selected - 1]
            self.fpsLabel = font.render(str(selectedProvince.backend.name), True, self.foregroundColor)
            
            if self.map.selected in self.state.factions["FRA"].explored and self.state.factions["FRA"].explored[self.map.selected]:
                self.infrastructureLabel = font.render("Infrastructure: ", True, self.foregroundColor)
                self.civilianLabel = font.render("Civilian: " + str(selectedProvince.backend.civilianInf), True, self.foregroundColor)
                self.transportLabel = font.render("Transport: " + str(selectedProvince.backend.transportInf), True, self.foregroundColor)
                self.extractionLabel = font.render("Extraction: " + str(selectedProvince.backend.extractionInf), True, self.foregroundColor)
            else:
                self.exploreLabel = font.render("Explore", True, self.foregroundColor)

                color = self.enabledColor
                if self.map.selected in self.state.factions["FRA"].explored:
                    color = self.disabledColor
                self.exploreButton = ExploreButton(None, self.state, selectedProvince, bounds.getMinX() + 50, bounds.getMinY() + 50, 100, 40, color, 2, self.foregroundColor)
    
    def click(self, screen, bounds, coords):
        
        self.exploreButton.click(coords)

    def release(self, screen, bounds, coords):

        self.exploreButton.release(coords)

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

            if self.fpsLabel != None:
                screen.blit(self.fpsLabel, (bounds.getMinX() + 10, bounds.getMinY() + 10))
            if self.infrastructureLabel != None:
                screen.blit(self.infrastructureLabel, (bounds.getMinX() + 15, bounds.getMinY() + 40))
            if self.civilianLabel != None:
                screen.blit(self.civilianLabel, (bounds.getMinX() + 15, bounds.getMinY() + 60))
            if self.transportLabel != None:
                screen.blit(self.transportLabel, (bounds.getMinX() + 15, bounds.getMinY() + 80))
            if self.extractionLabel != None:
                screen.blit(self.extractionLabel, (bounds.getMinX() + 15, bounds.getMinY() + 100))
            if self.exploreButton != None:
                self.exploreButton.render(screen)
            if self.exploreLabel != None:
                screen.blit(self.exploreLabel, (bounds.getMinX() + 60, bounds.getMinY() + 60))

