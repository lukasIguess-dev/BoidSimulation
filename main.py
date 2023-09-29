import sys
import pygame

from boid import Boid
from grid import Grid

def update(dt):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit() 
                sys.exit() 
            if event.key == pygame.K_g:
                grid.toggle_grid()             


width, height = 1000, 700
grid = Grid(width, height, 50)


def draw(screen,drawList):
    screen.fill((40,40,40))

    # draw grid
    grid.draw(screen)

    for this in drawList:
        this.draw(screen)

    # display statistics
    display_stats(surface=screen, fps=clock.get_fps(), boidCount=len(boidList))

    #update display
    pygame.display.flip()
 
def runPyGame():
    # Initialise PyGame.
    pygame.init()
  
    fps = 60.0
    global clock 
    clock = pygame.time.Clock()
  
    width, height = 1000, 700
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.Font('freesansbold.ttf', 32) # create font object

    drawList = []

    # create boids
    global boidList
    boidList = []
    for i in range(1000):
        newBoid = Boid()
        grid.insert(newBoid)
        boidList.append(newBoid)
        drawList.append(newBoid)
    
    # Main game loop.
    dt = 1/fps 
    while True:
        update(dt) 
        draw(screen, drawList)
        """
        for boid in boidList:
            boid.update(dt, boidList)
        """
        grid.update(dt)
        dt = clock.tick(fps)

def display_stats(surface: pygame.Surface, fps, boidCount):
    # display FPS
    render_Text(surface, f"FPS: {round(fps, 2)}", (0,0,0), (10,10), 15)
    render_Text(surface, f"Boids: {'{:,}'.format(boidCount)}", (0,0,0), (10,30), 10)

def render_Text(surface: pygame.Surface,what:str, color, where, size:int):
    font = pygame.font.SysFont("Consolas", size)
    text = font.render(what, 1, color, (255,255,255))
    surface.blit(text, where)

if __name__ == "__main__":
    runPyGame()