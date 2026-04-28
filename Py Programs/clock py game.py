import pygame as py
import numpy as np
from numpy import sin, cos, radians, pi
import datetime as dt
import pygame.gfxdraw
from pygame.draw_py import draw_lines

py.init()
py.font.init()
clock = py.time.Clock()

# Screen size and center of screen
screen = py.display.set_mode((1080, 720))
center = np.array([540,360])

# Font for numbers
font = py.font.SysFont('Impact', 40, bold=False)

def draw_styled_hand(surface, angle, length, width, color):

    x = center[0]
    y = center[1]

    # Angles declaration
    adjusted_angle = angle - pi/2
    perpendicular_angle = adjusted_angle + pi/2

    # Coordinate calculation
    tip = (x + length * cos(adjusted_angle),
           y + length * sin(adjusted_angle))

    base = (x - 20 * cos(adjusted_angle),
            y - 20 * sin(adjusted_angle))

    side1 = (x + width * cos(perpendicular_angle),
             y + width * sin(perpendicular_angle))

    side2 = (x - width * cos(perpendicular_angle),
             y - width * sin(perpendicular_angle))

    points = [tip, side1, base, side2]

    # Draw Polygon
    py.gfxdraw.filled_polygon(surface, points, color) # Filled jagged polygon
    py.gfxdraw.aapolygon(surface, points, color)  # Filled jagged polygon

def draw_numbers(surface, radius):
    for i in range(1, 13):
        angle = radians(i*30 - 90)
        x = center[0] + radius * cos(angle)
        y = center[1] + radius * sin(angle)

        text = font.render(str(i), True, (255,255,255))
        text_rect = text.get_rect(center=(x,y))
        surface.blit(text, text_rect)

def draw_realtime(surface, posn, Hour, Minute, Second):
    string = f"{Hour}-{Minute}-{Second}"
    text = font.render(str(string), True, (255, 255, 255))
    text_rect = text.get_rect(center=(posn[0], posn[1]))
    surface.blit(text, text_rect)

def draw_time_lines(surface, radius, thin, thick, length):

    for i in range(0, 60):
        angle = radians(i * 6 - 90)
        xStart = center[0] + radius * cos(angle)
        yStart = center[1] + radius * sin(angle)
        xEnd = center[0] + (radius - length) * cos(angle)
        yEnd = center[1] + (radius - length) * sin(angle)

        if i % 5 == 0:
            py.draw.line(surface, (255, 255, 255), (xStart, yStart), (xEnd, yEnd), thick)
        else:
            py.draw.line(surface, (255, 255, 255), (xStart, yStart), (xEnd, yEnd), thin)

running = True
while running:

    # Tick Speed
    clock.tick(60)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Background
    screen.fill((20, 20, 20))

    # Rim
    py.draw.circle(screen, (255, 255, 255), (540, 360), 360, 7)

    # Time Numbers
    draw_numbers(screen, 300)

    # Timelines
    draw_time_lines(screen, 350, 2, 5, 15)

    # Angle Calculation
    now = dt.datetime.now()
    sec_angle = radians(now.second * 6)
    min_angle = radians(now.minute * 6 + now.second * 0.1)
    hour_angle = radians((now.hour % 12) * 30 + now.minute * 0.5)

    # Draw Hands
    draw_styled_hand(screen, hour_angle, 180, 15, (255,255,255))
    draw_styled_hand(screen, min_angle, 260, 10, (180, 180, 180))
    draw_styled_hand(screen, sec_angle, 290, 4, (255, 10, 10))

    # Hub
    py.draw.circle(screen, (20, 20, 20), (540, 360), 10)
    py.draw.circle(screen, (255, 255, 255), (540, 360), 10, 2)

    # Time
    draw_realtime(screen, (100, 120), now.hour, now.minute, now.second)

    py.display.update()

py.quit()