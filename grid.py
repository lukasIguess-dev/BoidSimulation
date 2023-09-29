import pygame
from boid import Boid
Vector2 = pygame.math.Vector2

class Cell():
    def __init__(self,root, min_x, min_y, max_x, max_y, grid_x, grid_y) -> None:
        self.content = []

        self.root = root

        self.min_x = min_x
        self.min_y = min_y
        self.max_y = max_y
        self.max_x = max_x

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.color = (255,255,255)
        self.color_active = (0,255,0)

    def empty(self) -> bool:
        if self.content == []:
            return True
        return False
    def get_content(self) -> Boid:
        if self.empty:
            return None
        return self.content
       
    def draw(self, surface):
        col = self.color
        if not self.empty():
            col = self.color_active
            pygame.draw.line(surface,col, (self.min_x, self.min_y), (self.max_x, self.min_y))
            pygame.draw.line(surface,col, (self.min_x, self.min_y), (self.min_x, self.max_y))
            pygame.draw.line(surface,col, (self.max_x-1, self.min_y), (self.max_x-1, self.max_y))
            pygame.draw.line(surface,col, (self.min_x, self.max_y-1), (self.max_x, self.max_y-1))

    def insert(self, entity:Boid):
        if entity != None:
            self.content.append(entity)


    def delete(self, content):
        self.content.remove(content)

    def __get_surounding_entities(self):
        near_enteties = []
        for y in range(self.grid_y-1,self.grid_y+1):
            for x in range(self.grid_x-1, self.grid_x+1):
                if x == -1: gx = self.root.count_x
                elif x == self.root.count_x +1: gx = 0
                else: gx = x
                if y == -1: gy = self.root.count_y
                elif y == self.root.count_y +1: gy = 0
                else: gy = y
                near_enteties.append(self.root.contents[gy][gx])

        return near_enteties

    def update(self, dt):
        if self.empty():
            return
        for entity in self.content:
            entity.update(dt, self.content)
            # check if content entities left the cell
            e_x = entity.get_pos().x
            e_y = entity.get_pos().y

            if e_x < self.min_x or e_y < self.min_y or e_x > self.min_x or e_y < self.min_y:
                # resort it
                self.root.insert(entity)

                # reomve entity from cell
                self.delete(entity)
    
class Grid():
    def __init__(self, screen_width, screen_height, cell_size) -> None:
        self.contents = []
        self.cell_size = cell_size
        self.count_x = int(screen_width/cell_size)
        self.count_y = int(screen_height/cell_size)
        # generate all cells and set their restrictions
        for y in range(self.count_y):
            new_row = []
            for x in range(self.count_x):
                new_cell = Cell(self, x*cell_size,y*cell_size, x*cell_size+cell_size, y*cell_size+cell_size, x,y)
                new_row.append(new_cell)
            self.contents.append(new_row)

            self.show_grid = True

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def draw(self,surface):
        if not self.show_grid:
            return
        for y in range(self.count_y):
            for x in range(self.count_x):
                self.contents[y][x].draw(surface)
    def update(self, dt):
        for y in range(self.count_y):
            for x in range(self.count_x):
                self.contents[y][x].update(dt)
    def insert(self, entity:Boid):
        entity_pos = entity.get_pos()
        g_x, g_y = int(entity_pos.x/self.cell_size), int(entity_pos.y/self.cell_size)
        self.contents[g_y][g_x].insert(entity)
