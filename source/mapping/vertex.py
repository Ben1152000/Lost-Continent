
class Vertex():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def fromDict(vectorDict):
        return Vertex(vectorDict["lon"], vectorDict["lat"])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __neg__(self):
        return Vertex(-self.x, -self.y)

    def __add__(self, other):
        return Vertex(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (-other)

    def __abs__(self):
        return (self.x * self.x + self.y * self.y) ** 0.5
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __mul__(self, other):
        return Vertex(self.x * other, self.y * other)

    def floor(self):
        self.x = int(self.x)
        self.y = int(self.y)

if __name__ == "__main__":
    v = Vertex(4, 8)
    u = Vertex(3, 2)
    print("v = " + str(v))
    print("u = " + str(u))
    print("v + u = " + str(v + u))
    print("v - u = " + str(v - u))