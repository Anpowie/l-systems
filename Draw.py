from pygame import draw
import pygame
import time

screen = None


def rect(color, x, y, u, v):
    global screen
    draw.rect(screen, color, (x, y, u, v))



def lines(color, vecs, pixles):
    global screen
    draw.lines(screen, color, False, vecs, pixles)

