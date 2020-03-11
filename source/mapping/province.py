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
        return self.selected

    def render(self, screen, bounds, time, player):
        if self.bounds.overlap(bounds):
            width, height = screen.get_size()
            vertexScreenCoords = []
            for vertex in self.vertices:
                screenX = int((vertex.x - bounds.v1.x) * width / bounds.getWidth())
                screenY = int((vertex.y - bounds.v1.y) * height / bounds.getHeight())
                vertexScreenCoords.append((screenX, screenY))
            
            color = pygame.Color(0, 0, 0)
            hue = (self.pid * 580) % 255
            sat = 50 * (self.pid in player.explored and player.explored[self.pid]) # if unexplored, set sat to 0
            for explorer in player.explorers:
                if explorer["provinceId"] == self.pid:
                    sat = 50 * math.e ** (-explorer["remainingTime"] / 10)
            val = 50 + 50 * (math.sin(time / 200.0) / 3.0 + 0.66) * (self.selected) # value varies if selected
            color.hsva = (hue, sat, val)

            pygame.draw.polygon(screen, color, vertexScreenCoords)
            pygame.draw.aalines(screen, (255, 255, 255), True, vertexScreenCoords, 2)

