import json
from .vertex import Vertex
from .province import Province

class Map():

    provinces = []

    def __init__(self, mapfile):
        mapDict = {}
        with open(mapfile) as readFile:
            mapDict = json.loads(readFile.read())
        for pid in mapDict["provinces"]:
            provinceDict = mapDict["provinces"][pid]
            provinceDict["id"] = pid
            provinceDict["vertices"] = [mapDict["vertices"][str(v)] for v in provinceDict["vertices"]]
            self.provinces.append(Province(provinceDict))

    def render(self, screen, bounds, time):
        for province in self.provinces:
            province.render(screen, bounds, time)

    def click(self, screen, coords, viewport):
        width, height = screen.get_size()
        coords = Vertex(coords[0] / width * viewport.getWidth() + viewport.v1.x, 
                coords[1] / height * viewport.getHeight() + viewport.v1.y)
        for province in self.provinces:
            province.click(coords)

if __name__ == "__main__":
    pass
    #gamemap = Map("map.json")