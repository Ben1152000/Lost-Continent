from .vertex import Vertex

class Rectangle():
    
    def __init__(self, x1, x2, y1, y2):
        self.lower = Vertex(x1, y1)
        self.upper = Vertex(x2, y2)

    def getMinX(self): return self.lower.x
    def getMinY(self): return self.lower.y
    def getMaxX(self): return self.upper.x
    def getMaxY(self): return self.upper.x
    def getWidth(self): return self.upper.x - self.lower.x
    def getHeight(self): return self.upper.y - self.lower.y

    def translate(self, dx, dy):
        self.lower.x += dx
        self.lower.y += dy
        self.upper.x += dx
        self.upper.y += dy
    
    def scale(self, sx, sy):
        width, height = self.getWidth(), self.getHeight()
        self.lower.x -= width * sx
        self.upper.x += width * sx
        self.lower.y -= height * sy
        self.upper.y += height * sy

    def overlap(self, other):
        return self.lower.x < other.upper.x and other.lower.x < self.upper.x \
            and self.lower.y < other.upper.y and other.lower.y < self.upper.y

    @staticmethod
    def fromVertices(vertices):
        x1 = x2 = vertices[0].x
        y1 = y2 = vertices[0].y
        for vertex in vertices:
            if vertex.x < x1: x1 = vertex.x
            if vertex.y < y1: y1 = vertex.y
            if vertex.x > x2: x2 = vertex.x
            if vertex.y > y2: y2 = vertex.y
        return Rectangle(x1, x2, y1, y2)