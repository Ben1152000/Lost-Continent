from .vertex import Vertex
from .rectangle import Rectangle
import pygame
import pygame.gfxdraw

from random import randint

class Province():
    
    name = ""
    pid = 0
    vertices = []
    bounds = []

    def __init__(self, provinceDict):
        self.name = str(provinceDict["name"])
        self.pid = int(provinceDict["id"])
        vertices = provinceDict["vertices"]
        self.vertices = [Vertex.fromDict(vertex) for vertex in vertices]
        self.bounds = Rectangle.fromVertices(self.vertices)

    def __str__(self):
        return str(self.pid) + ": " + self.name

    def render(self, screen, bounds):
        width, height = screen.get_size()
        vertexScreenCoords = []
        for vertex in self.vertices:
            screenX = int((vertex.x - bounds.getMinX()) * width / bounds.getWidth())
            screenY = int((vertex.y - bounds.getMinY()) * height / bounds.getHeight())
            vertexScreenCoords.append((screenX, screenY))
        color = ((self.pid * 347) % 255, ((1 + self.pid) * 347) % 255, ((2 + self.pid) * 347) % 255)
        pygame.draw.polygon(screen, color, vertexScreenCoords)
        pygame.draw.lines(screen, (255, 255, 255), True, vertexScreenCoords, 1)
        pygame.draw.aalines(screen, (255, 255, 255), True, vertexScreenCoords, 1)
        """
        for i in range(len(self.vertices)):
            pygame.draw.aaline(
                screen, 
                (255, 255, 255), 
                vertexScreenCoords[i], 
                vertexScreenCoords[(i + 1) % len(self.vertices)],
                2
            )
            #pygame.gfxdraw.line(
            #    screen, 
            #    vertexScreenCoords[i][0], 
            #    vertexScreenCoords[i][1], 
            #    vertexScreenCoords[(i + 1) % len(self.vertices)][0], 
            #    vertexScreenCoords[(i + 1) % len(self.vertices)][1], 
            #    (200, 200, 200),
            #)
        """