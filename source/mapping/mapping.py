import json
from .vertex import Vertex
from .province import Province

class Map():

    provinces = []
    selected = -1

    def __init__(self, mapfile):
        mapDict = {}
        with open(mapfile) as readFile:
            mapDict = json.loads(readFile.read())
        for pid in mapDict["provinces"]:
            provinceDict = mapDict["provinces"][pid]
            provinceDict["id"] = pid
            provinceDict["vertices"] = [mapDict["vertices"][str(v)] for v in provinceDict["vertices"]]
            self.provinces.append(Province(provinceDict))

    def render(self, screen, bounds, viewport, time, player, font):
        for province in self.provinces:
            province.render(screen, bounds, viewport, time, player, font)

    def click(self, screen, bounds, coords, viewport):
        width, height = bounds.getWidth(), bounds.getHeight()
        coords = Vertex(coords[0] / width * viewport.getWidth() + viewport.v1.x, 
                coords[1] / height * viewport.getHeight() + viewport.v1.y)
        if self.selected > 0:
            self.provinces[self.selected - 1].selected = False
        self.selected = -1
        for province in self.provinces:
            self.selected = province.pid if province.click(coords) else self.selected
        if self.selected > 0:
            self.provinces[self.selected - 1].selected = True
        
        

if __name__ == "__main__":
    pass
    #gamemap = Map("map.json")