import random

import pygame
from pygame.locals import QUIT

import Map
import Vector
import colors
import util
import Road
import Draw
from Vector import Vec
import time

SCREEN_SIZE = 1000
INTERSECTION_POINT_WIDTH = 5

seed = 308#30#8  # 123#13 #123 # 55 # You can change the seed for different patterns
scale = 500.0
octaves = 1
persistence = 0.5
lacunarity = 4.0

rots = [2.5, 0, -2.5]
segmentsAmount = 60
highwayLength = 40
branchLength = 30

random.seed(seed)


def branchOut(branch):
    branchVecs = Road.constructRoad(map, SCREEN_SIZE, branch[0], branch[1], branchLength, rots, False, allVecs)

    if len(branchVecs[0]) < 2:  # roads cannot be this small
        return

    allVecs.extend(branchVecs[0])
    Draw.lines(colors.BLUE, branchVecs[0], 1)

    #pygame.display.flip()
    #time.sleep(0.05)

    for innerBranch in branchVecs[1]:
        branchOut(innerBranch)


pygame.init()
Draw.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

map = Map.generate_perlin_noise(SCREEN_SIZE, SCREEN_SIZE, seed=seed, scale=scale, octaves=octaves,
                                persistence=persistence, lacunarity=lacunarity)

# debug view -> draw noise

for x in range(SCREEN_SIZE):
    for y in range(SCREEN_SIZE):
        value = map[x][y]
        value = util.clamp(value * 255, 0, 255)

        Draw.rect((value, value, value), x, y, 1, 1)


startTime = time.time()
allVecs = []
highways = []

highway1 = Road.constructRoad(map, SCREEN_SIZE, Vec(0, 0), Vector.UP.rotate(-45), highwayLength, rots, True, allVecs)
allVecs.extend(highway1[0])

highway2 = Road.constructRoad(map, SCREEN_SIZE, Vec(0, SCREEN_SIZE), Vector.UP.rotate(-135), highwayLength, rots, True, allVecs)
allVecs.extend(highway2[0])

highway3 = Road.constructRoad(map, SCREEN_SIZE, Vec(SCREEN_SIZE, 250), Vector.UP.rotate(90), highwayLength, rots, True, allVecs)
allVecs.extend(highway3[0])

highways.append(highway1)
#highways.append(highway2)
highways.append(highway3)

Draw.lines(colors.RED, highway1[0], 3)
Draw.lines(colors.RED, highway2[0], 3)
Draw.lines(colors.RED, highway3[0], 3)
# Update the display
pygame.display.flip()
colorint = 0


for highway in highways:
    for branch in highway[1]:
        branchOut(branch)

pygame.display.flip()

"""
for intersection in Road.intersectionPoints:
    Draw.rect(colors.YELLOW, intersection.x - INTERSECTION_POINT_WIDTH / 2,
              intersection.y - INTERSECTION_POINT_WIDTH / 2, INTERSECTION_POINT_WIDTH, INTERSECTION_POINT_WIDTH)

for mergePoint in Road.mergePoints:
    Draw.rect(colors.TURKEY, mergePoint.x - INTERSECTION_POINT_WIDTH / 2, mergePoint.y - INTERSECTION_POINT_WIDTH / 2,
              INTERSECTION_POINT_WIDTH, INTERSECTION_POINT_WIDTH)


for vec in allVecs:
    vec = Vec.of(vec)
    if 275 < vec.x < 341 and 923 < vec.y < 983:
        Road.specialPoints.append(vec)


for mergePoint in Road.specialPoints:
    Draw.rect(colors.GREEN, mergePoint.x - INTERSECTION_POINT_WIDTH / 2, mergePoint.y - INTERSECTION_POINT_WIDTH / 2,
              INTERSECTION_POINT_WIDTH, INTERSECTION_POINT_WIDTH)
    
"""

print(Road.doLinesIntersect(Vec.of((326 , 947)), Vec.of((287 , 931)), Vec.of((303 , 949)), Vec.of((308 , 918))))

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check for left mouse button click (button index 0)
            if pygame.mouse.get_pressed()[0]:
                print(mouse_x, ",", mouse_y)

pygame.quit()
