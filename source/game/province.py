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
    explored = False

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
        if count & 1:
            self.selected = True
        else:
            self.selected = False

    def render(self, screen, bounds, time):
        if self.bounds.overlap(bounds):
            width, height = screen.get_size()
            vertexScreenCoords = []
            for vertex in self.vertices:
                screenX = int((vertex.x - bounds.v1.x) * width / bounds.getWidth())
                screenY = int((vertex.y - bounds.v1.y) * height / bounds.getHeight())
                vertexScreenCoords.append((screenX, screenY))
            color = ((self.pid * 347) % 255, ((1 + self.pid) * 347) % 255, ((2 + self.pid) * 347) % 255)
            if self.selected:
                coef = math.sin(time / 200.0) / 3.0 + 0.66
                color = ((self.pid * 347) % 255 * (1 - coef) + 255 * coef, ((1 + self.pid) * 347) % 255 * (1 - coef) + 255 * coef, ((2 + self.pid) * 347) % 255 * (1 - coef) + 255 * coef)
            pygame.draw.polygon(screen, color, vertexScreenCoords)
            pygame.draw.lines(screen, (255, 255, 255), True, vertexScreenCoords, 2)

