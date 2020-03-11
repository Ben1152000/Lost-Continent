import datetime, time, json

class Game():

    days = 0
    date = datetime.date(1869, 11, 17)
    provinces = {}
    factions = {}

    def load(self, dataFile):
        with open(dataFile) as data:
            dataDict = json.loads(data.read())
            for provinceId in dataDict["provinces"]:
                if int(provinceId) not in self.provinces:
                    self.provinces[int(provinceId)] = Province(self, int(provinceId))
                self.provinces[int(provinceId)].update(dataDict["provinces"][provinceId])
            for factionId in dataDict["factions"]:
                if factionId not in self.factions:
                    self.factions[factionId] = Faction(self, factionId)
                self.factions[factionId].update(dataDict["factions"][factionId])

    def __init__(self, provinces={}, factions={}):
        self.provinces = provinces
        self.factions = factions

    def tick(self):
        self.days += 1
        self.date += datetime.timedelta(1)
        if self.date.weekday() == 6:
            self.week()
        for faction in self.factions:
            self.factions[faction].tick()

    def week(self):
        for faction in self.factions:
            self.factions[faction].week()

    def execute(self, command):
        # Command structure is <operation> <param1> <param2>...
        params = command.split()
        if params[0] == "tick":
            self.tick()
            return True
        if params[0] == "explore":
            factionId = params[1]
            provinceId = int(params[2])
            if factionId not in self.factions:
                return False
            if provinceId not in self.provinces:
                return False
            self.factions[factionId].assignExplorer(provinceId)
            return True


class Province():

    game = None

    name = ""
    id = 0
    neighbors = []

    def __init__(self, game, provinceId):
        self.game = game
        self.provinceId = provinceId

    def update(self, dataDict):
        for key in dataDict:
            setattr(self, key, dataDict[key])

class Faction():

    game = None

    id = "XXX"

    explorerLimit = 2 # number of available explorers
    explorerDuration = 120

    actions = 0 # action points, tick up at the end of week

    prestige = 0

    wealth = 0

    mercantilism = 0

    def __init__(self, game, factionId):
        self.game = game
        self.id = factionId
        self.explorers = [] # current explorers
        self.explored = {} # list of explored provinces

    def update(self, dataDict):
        for key in dataDict:
            setattr(self, key, dataDict[key])

    def tick(self):
        # update explorers
        e = 0
        while e < len(self.explorers):
            if self.explorers[e]["remainingTime"] > 0:
                self.explorers[e]["remainingTime"] -= 1
                e += 1
            else:
                self.explored[self.explorers[e]["provinceId"]] = True
                del self.explorers[e]

    def week(self):
        self.actions += 1

    def assignExplorer(self, provinceId):
        if len(self.explorers) < self.explorerLimit and provinceId not in self.explored:
            accessible = self.game.provinces[provinceId].coastal
            for neighborId in self.game.provinces[provinceId].neighbors:
                accessible = accessible or (neighborId in self.explored and self.explored[neighborId])
            if accessible:
                self.explorers.append({
                    "provinceId": provinceId,
                    "remainingTime": self.explorerDuration 
                })
                self.explored[provinceId] = False
    
        
if __name__ == "__main__":

    game = Game()
    game.load("data.json")

    game.execute("explore FRA 2")
    game.execute("explore FRA 3")
    game.execute("explore FRA 4")

    while True:
        game.tick()
        print(game.date)
        print(game.factions["FRA"].explorers)
        print(game.factions["FRA"].explored)
        time.sleep(0.1)
    