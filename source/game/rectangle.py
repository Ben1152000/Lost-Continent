from .vertex import Vertex

class Rectangle():
    
    def __init__(self, x1, x2, y1, y2):
        self.v1 = Vertex(x1, y1)
        self.v2 = Vertex(x2, y2)

    def getMinX(self): return min(self.v1.x, self.v2.x)
    def getMinY(self): return min(self.v1.y, self.v2.y)
    def getMaxX(self): return max(self.v1.x, self.v2.x)
    def getMaxY(self): return max(self.v1.y, self.v2.y)
    def getWidth(self): return self.v2.x - self.v1.x
    def getHeight(self): return self.v2.y - self.v1.y

    def translate(self, dx, dy):
        self.v1.x += dx
        self.v1.y += dy
        self.v2.x += dx
        self.v2.y += dy
    
    def scale(self, sx, sy):
        width, height = self.getWidth(), self.getHeight()
        self.v1.x -= width * sx
        self.v1.y -= height * sy
        self.v2.x += width * sx
        self.v2.y += height * sy

    def __contains__(self, vertex):
        return vertex.x >= self.getMinX() and vertex.x <= self.getMaxX() \
            and vertex.y >= self.getMinY() and vertex.y <= self.getMaxY()

    def overlap(self, other):
        return self.getMinX() < other.getMaxX() and other.getMinX() < self.getMaxX() \
            and self.getMinY() < other.getMaxY() and other.getMinY() < self.getMaxY()

    def __repr__(self):
        return "(" + str(self.v1.x) + ":" + str(self.v1.x) + ", " + str(self.v2.y) + ":" + str(self.v2.y) + ")"

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