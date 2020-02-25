import datetime, time

class Game():

    days = 0
    date = datetime.date(1869, 11, 17)
    provinces = {}
    factions = {}

    def __init__(self, provinces, factions):
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

class Province():

    provinceId = 0

    def __init__(self, pid):
        self.provinceId = provinceId


class Faction():

    explorerLimit = 1 # number of available explorers
    explorerDuration = 120
    explorers = [] # current explorers
    explored = {} # list of explored provinces

    actions = 0 # action points, tick up at the end of week

    prestige = 0

    wealth = 0

    mercantilism = 0

    def tick(self):

        # update explorers
        for e in range(len(self.explorers)):
            if self.explorers[e]["remainingTime"] > 0:
                self.explorers[e]["remainingTime"] -= 1
            else:
                self.explored[self.explorers[e]["provinceId"]] = True
                del self.explorers[e]

    def week(self):
        self.actions += 1

    def assignExplorer(self, provinceId):
        if len(self.explorers) < self.explorerLimit and provinceId not in self.explored:
            self.explorers.append({
                "provinceId": provinceId,
                "remainingTime": self.explorerDuration
            })
    
        
if __name__ == "__main__":

    provinces = {0: Province(0), 1: Province(1), 2: Province(2)}
    faction = Faction()
    game = Game(provinces, {0: faction})
    while True:
        game.tick()
        print(game.date)
        game.factions[0].assignExplorer(0)
        game.factions[0].assignExplorer(1)
        print(game.factions[0].explorers, game.factions[0].explored)
        time.sleep(0.2)