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

    def render(self, screen, bounds):
        for province in self.provinces:
            province.render(screen, bounds)

    def click(self, bounds):
        pass

if __name__ == "__main__":
    pass
    #gamemap = Map("map.json")