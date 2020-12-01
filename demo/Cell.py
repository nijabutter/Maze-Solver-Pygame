import pygame
class Cell:
    color = (200, 200, 200)
    #       top    right bottom left
    def __init__(self, _window, _x, _y, _width, _height, _indexX, _indexY):
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        self.window = _window
        self.indexX = _indexX
        self.indexY = _indexY
        self.walls = [True, True]
        self.visited = False
        self.g = 0
        self.h = 0
        self.f = 0
        self.neighbours = []
        self.previous = None

    def draw(self):
        # right wall
        if self.walls[0] == True:
            pygame.draw.line(self.window, self.color, (self.x+self.width, self.y), (self.x+self.width, self.y+self.height))
        #bottom wall
        if self.walls[1] == True:
            pygame.draw.line(self.window, self.color, (self.x, self.y+self.height), (self.x+self.width, self.y+self.height))