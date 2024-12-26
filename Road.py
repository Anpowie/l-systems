import numpy as np

import Draw
import Easing
import Map
import colors
import util
from Vector import Vec
import random

intersectionPoints = []
mergePoints = []
specialPoints = []
streets = []


def getNewPos(pos, normal, segmentLength):
    return pos + normal * segmentLength


def constructRoad(map, mapsize, startPos, startNormal, segmentLength, rots, isHighWay, existingVecs=None):
    if existingVecs is None:
        existingVecs = []

    # first collision has to be ignored, otherwise the branch will stop instantly
    isFirstCollisionCheck = not isHighWay
    normal = startNormal
    pos = startPos

    roadVecs = [pos.tuple()]
    branches = []

    if 321 < startPos.x < 335 and 931 < startPos.y < 954:
        print(f"roading at {startPos}")

    while isPosInBounds(pos, mapsize):

        normals = []
        intensities = []

        # test all 3 degrees - how populated is the area there
        for rot in rots:
            normalRot = normal.rotate(rot)
            intensity = Map.getUpComingDensity(map, mapsize, pos, normalRot, segmentLength, isHighWay)
            normals.append(normalRot)
            intensities.append(intensity)

        # choose the degrees, that are most densely populated
        chosenDirection = intensities.index(max(intensities))
        chosenNormal = normals[chosenDirection]
        newPos = getNewPos(pos, chosenNormal, segmentLength)

        # connect vert with other if they are very close
        mergePoint = mergeWithOtherParts(pos, newPos, startNormal, existingVecs)
        merged = False

        if mergePoint is not None:
            merged = True
            newPos = mergePoint

        # end road if there is an intersection
        intersection = None
        if not isFirstCollisionCheck:  # Apparently useless
            intersection = checkForIntersections(pos, newPos, existingVecs, segmentLength)
        isFirstCollisionCheck = False

        if intersection is not None:
            roadVecs.append(intersection.tuple())
            streets.append((pos, intersection))
            intersectionPoints.append(intersection)


            if not isHighWay:
                for branch in branches:
                    intersectionPoints.remove(branch[0])
                return roadVecs, []

            # if 226 < newPos.x < 248 and 379 < newPos.y < 393:
            #    print(f"intersecting at {startPos}")

            return roadVecs, branches

        if merged:
            roadVecs.append(mergePoint.tuple())
            streets.append((pos, mergePoint))

            mergePoints.append(mergePoint)

            if not isHighWay:  # TODO: remove old points
                return roadVecs, []

            # streetLength = pos.distance(mergePoint)
            # if streetLength > segmentLength:
            #    roadVecs.append(Easing.lerpVec(pos, mergePoint, 0.5).tuple())

            return roadVecs, branches

        localIntensity = intensities[chosenDirection]

        # end branches if they are getting out of town
        if not isHighWay and doesBranchEnd(localIntensity, segmentLength, isHighWay):
            if len(roadVecs) < 2:  # this road is gonna get removed - no intersection needed
                intersectionPoints.remove(startPos)

            # if 226 < newPos.x < 248 and 379 < newPos.y < 393:
            #    print(f"ended at {startPos}")
            return roadVecs, branches

        roadVecs.append(newPos.tuple())
        streets.append((pos, newPos))

        # branch out
        if doesBranchStart(localIntensity, segmentLength, isHighWay):

            leftNormal = chosenNormal.rotate(-90)
            rightNormal = chosenNormal.rotate(90)

            leftIntensity = Map.getUpComingDensity(map, mapsize, newPos, leftNormal, segmentLength, isHighWay)
            rightIntensity = Map.getUpComingDensity(map, mapsize, newPos, rightNormal, segmentLength, isHighWay)

            branchThreashold = 10

            # branching can first start after all highways have been drawn

            if leftIntensity > branchThreashold:
                intersectionPoints.append(newPos)
                branches.append((newPos, leftNormal))


            if rightIntensity > branchThreashold:
                intersectionPoints.append(newPos)
                branches.append((newPos, rightNormal))


        normal = chosenNormal
        pos = newPos

    return roadVecs, branches


def mergeWithOtherParts(startPos, endPos, normal, existingVecs):
    mergeDistance = 20

    chosenVec = None
    chosenVecDistance = 999

    for vec in existingVecs:
        vec = Vec.of(vec)

        if endPos == vec:
            continue

        distance = endPos.distance(vec)

        if distance > mergeDistance:
            continue

        # if not isLookingAt(normal, pos, vec):
        #    continue


        for street in streets:
            pointA = street[0]
            pointB = street[1]


            if doLinesIntersect(startPos, vec, pointA, pointB):
                continue

        if chosenVec is None or distance < chosenVecDistance:



            chosenVec = vec
            chosenVecDistance = distance

    return chosenVec


def isLookingAt(normal, point, target):
    # Ensure the vectors are NumPy arrays for vector operations
    normal = np.array(normal.tuple())
    point = np.array(point.tuple())
    target = np.array(target.tuple())

    # Calculate the dot product
    dot_product = np.dot(normal, target - point)

    # Check the sign of the dot product
    """
    if dot_product > 0:
        return "The normal at point A is looking towards point B."
    elif dot_product < 0:
        return "The normal at point A is looking away from point B."
    else:
        return "The normal at point A is perpendicular to the line connecting points A and B."
    """

    return dot_product > 0


def weighted_random_choice(a, b):
    # Calculate the probabilities based on the magnitudes
    total_magnitude = abs(a) + abs(b)
    probability_a = abs(a) / total_magnitude

    # Generate a random number and check if it's less than the calculated probability
    return random.random() < probability_a


def doesBranchEnd(localIntensity, segmentLength, isHighway):
    maxIntensity = segmentLength
    if isHighway:
        maxIntensity *= 2

    p = 1 - localIntensity / segmentLength

    return Easing.easeInCubic(p) > random.random()


def doesBranchStart(localIntensity, segmentLength, isHighway):
    maxIntensity = segmentLength
    if isHighway:
        maxIntensity *= 2

    p = localIntensity / maxIntensity

    return p > random.random()


def checkForIntersections(oldPos, newPos, existingVecs, segmentLength):
    for i in range(len(existingVecs) - 1):
        pointA = Vec.of(existingVecs[i])
        pointB = Vec.of(existingVecs[i + 1])

        if not doLinesIntersect(oldPos, newPos, pointA, pointB):
            continue

        # the above sometimes produce a bug, with 2 lines intercepting, that are far away from another
        if not arePointsInProximity(oldPos, newPos, pointA, pointB, segmentLength):
            continue

        intersection = pointA if pointA.distance(newPos) < pointB.distance(newPos) else pointB

        return intersection

    return None


def arePointsInProximity(oldPos, newPos, pointA, pointB, segmentLength):
    # collisions aren't possible if they are this far away

    if pointA.distance(newPos) < segmentLength:
        return True
    if pointB.distance(newPos) < segmentLength:
        return True
    if pointA.distance(oldPos) < segmentLength:
        return True
    if pointB.distance(oldPos) < segmentLength:
        return True
    return False


def isPosInBounds(pos, screenSize) -> bool:
    if pos.x < 0:
        return False
    if pos.y < 0:
        return False
    if pos.x > screenSize:
        return False
    if pos.y > screenSize:
        return False
    return True


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


def doLinesIntersect(v1, v2, v3, v4):
    return ccw(v1, v3, v4) != ccw(v2, v3, v4) and ccw(v1, v2, v3) != ccw(v1, v2, v4)
