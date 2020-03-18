from .vertex import Vertex
from .rectangle import Rectangle
import pygame
import pygame.gfxdraw
import math


from random import randint

class Province():
    
    name = ""
    pid = 0
    vertices = []
    bounds = []

    selected = False

    backend = None

    biomeColors = {"jungle": (150, 80, 50), "marshlands": (170, 50, 60), "desert": (50, 50, 80), "drylands": (25, 50, 80), 
        "mountains": (30, 50, 40), "savanna": (75, 50, 70), "steppe": (60, 50, 75), "grasslands": (100, 50, 75), "highlands": (40, 55, 60)}

    def __init__(self, provinceDict):
        self.name = str(provinceDict["name"])
        self.pid = int(provinceDict["id"])
        vertices = provinceDict["vertices"]
        self.vertices = [Vertex.fromDict(vertex) for vertex in vertices]
        self.bounds = Rectangle.fromVertices(self.vertices)

    def __str__(self):
        return str(self.pid) + ": " + self.name

    def click(self, coords):
        count = 0
        if coords in self.bounds:
            for v in range(len(self.vertices)):
                if (coords.y <= self.vertices[v].y and coords.y >= self.vertices[v - 1].y
                    or coords.y >= self.vertices[v].y and coords.y <= self.vertices[v - 1].y):
                    slope = (self.vertices[v].x - self.vertices[v - 1].x) / (self.vertices[v].y - self.vertices[v - 1].y)
                    if (coords.y - self.vertices[v].y) * slope + self.vertices[v].x >= coords.x:
                        count += 1
        return count & 1

    def render(self, screen, bounds, viewport, time, player, font):
        
        if self.bounds.overlap(viewport):
            width, height = bounds.getWidth(), bounds.getHeight()
            vertexScreenCoords = []
            averageScreenCoord = Vertex(0, 0)
            for vertex in self.vertices:
                screenX = int((vertex.x - viewport.v1.x) * width / viewport.getWidth())
                screenY = int((vertex.y - viewport.v1.y) * height / viewport.getHeight())
                averageScreenCoord += Vertex(screenX, screenY)
                vertexScreenCoords.append((screenX, screenY))
            averageScreenCoord *= 1.0 / len(vertexScreenCoords)
            averageScreenCoord.floor()
            
            color = pygame.Color(0, 0, 0)
            hue, sat, val = (0, 50, 50)
            if self.backend.biome in self.biomeColors:
                hue, sat, val = self.biomeColors[self.backend.biome]
            """
            sat = sat * (self.pid in player.explored and player.explored[self.pid]) # if unexplored, set sat to 0
            for explorer in player.explorers:
                if explorer["provinceId"] == self.pid:
                    sat = 40 * math.e ** (-explorer["remainingTime"] / 20) + 10
            """
            if self.selected:
                val = min(val + 0.6 * (100.0 - val) * (math.sin(time / 200.0) / 2.0 + 0.5), 100)
            color.hsva = (hue, sat, val)

            pygame.draw.polygon(screen, color, vertexScreenCoords)
            pygame.draw.aalines(screen, (255, 255, 255), True, vertexScreenCoords, 2)

            """if abs(self.bounds.getWidth() * self.bounds.getHeight() / viewport.getWidth() / viewport.getHeight()) > 0.1:
                fpsLabel = font.render(self.backend.name, True, (255, 255, 255))
                screen.blit(fpsLabel, (averageScreenCoord.x, averageScreenCoord.y))
            """

