import numpy as np
import matplotlib.pyplot as plt
import noise

import util

# Set up parameters for Perlin noise generation

threashold = 0.65

# Generate Perlin noise function
def generate_perlin_noise(width, height, seed, scale, octaves, persistence, lacunarity):
    world = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            value = 0.5 + noise.pnoise2(i/scale,
                                         j/scale,
                                         octaves=octaves,
                                         persistence=persistence,
                                         lacunarity=lacunarity,
                                         repeatx=1024,
                                         repeaty=1024,
                                         base=seed)
            if value <= threashold:
                world[i][j] = 0
            else:
                # for what ever reason, the function can release values bigger than 1
                world[i][j] = (min(1, value) - threashold) / (1 - threashold)

    return world


def getUpComingDensity(map, mapsize, pos, normal, length, ishighway):

    intensity = 0

    searchDept = length
    if ishighway:
        searchDept *= 2

    for step in range(searchDept):
        testPos = pos + normal * step

        x = util.clamp(int(testPos.x), 0, mapsize-1)
        y = util.clamp(int(testPos.y), 0, mapsize-1)

        intensity += map[x, y]

    return intensity


""""


# Example usage and visualization
width, height = 100, 100
perlin_noise = generate_perlin_noise(width, height)

plt.imshow(perlin_noise, cmap='viridis', origin='upper')
plt.colorbar()
plt.title('2D Perlin Noise')
plt.show()
"""