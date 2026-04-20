import pygame as py

py.init()
screen = py.display.set_mode((1080, 720))
clock = py.time.Clock()

class heavenly_body:
    def __init__(self,coord,vel,acc,mass,color,size):
        self.coord = coord
        self.vel = vel
        self.acc = acc
        self.mass = mass
        self.color = color
        self.size = size

sun = heavenly_body([540, 360],[0,0],[0, 0], 1000, (220,230,50),50)
planet = heavenly_body([300, 360], [0, 5], [0, 0], 10, (180,180,180), 20)
planet1 = heavenly_body([800, 360], [0, -4], [0, 0], 10, (100,100,100), 15)

bodies = [sun, planet, planet1]

G = 6

def zeroAll():
    for i in bodies:
        i.acc[0] = 0
        i.acc[1] = 0

def find_acc():
    zeroAll()
    for i in bodies:
        for j in bodies:
            if i == j:
                continue
            dx = j.coord[0] - i.coord[0]
            dy = j.coord[1] - i.coord[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            f = G * j.mass * i.mass / dist ** 2
            a = f / i.mass
            i.acc[0] += a * dx / dist
            i.acc[1] += a * dy / dist

def VelPos():
    for i in bodies:
        i.vel[0] += i.acc[0]
        i.vel[1] += i.acc[1]
        i.coord[0] += i.vel[0]
        i.coord[1] += i.vel[1]

def Draw():
    for i in bodies:
        py.draw.circle(screen,i.color,i.coord,i.size)

running = True
while running:
    clock.tick(60)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.fill((0, 0, 0))

    find_acc()
    VelPos()
    Draw()

    py.display.update()

py.quit()