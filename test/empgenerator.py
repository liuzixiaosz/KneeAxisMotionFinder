import random
import numpy as np
import utils.mathutils as mu
import os
import math

PATH = "../data.txt"
MAX_RNG = math.pi / 2
DELTA_SEG = MAX_RNG / 18
SEGS = int(MAX_RNG / DELTA_SEG)
SIZE = 1000
MARKS = 4
DIM = 3


def setbase(s):
    p1 = [0, 0, 0]
    p2 = [0.3, 1, -0.02]
    p3 = [0.4, 1, 0.02]
    p4 = [1.4, 1, 0]
    return np.repeat([p1 + p2 + p3 + p4], s, axis=0) * 100


def setnoise(s_turp, loc=0, scale=0.1):
    return np.random.normal(loc=loc, scale=scale, size=s_turp)


def setaxes(segs):
    d = random.random() / 10 / segs
    axes = np.zeros([segs, DIM])
    axes[:, 2] = 1
    for i in range(0, segs):
        axes[i, 0] = d * i
    return axes


def write(data):
    # org = str(data)[1: -1].split('\n ')
    # f = open(PATH, 'w')
    # for line in org:
    #     line = line[1: -1].replace(' ', ',').replace(',,', ',')
    #     if len(line) > 0 and line[0] == ',':
    #         line = line[1:]
    print(str(data))
    np.savetxt(PATH, data, delimiter=',')


def main():
    base = setbase(SIZE)
    noise = setnoise(base.shape, scale=0.1)
    data = base #+ noise
    axes_raw = setaxes(SEGS)
    noise2 = setnoise(axes_raw.shape, scale=0.1)
    axes = axes_raw / mu.lengthvec(axes_raw)
    start_vec = np.array(data[0, DIM * (MARKS - 1):] - data[0, DIM: 2 * DIM])
    for i in range(1, SIZE):
        # thisvec = np.array(data[i, DIM * (MARKS - 1):] - data[i, DIM: 2 * DIM])
        index = random.randint(0, SEGS - 1)
        rotated = mu.rot(start_vec, index * DELTA_SEG + random.random() * DELTA_SEG, [-axes[index, :]])
        data[i, DIM * (MARKS - 1):] = data[i, DIM: 2 * DIM] + rotated
    np.savetxt('refaxis.txt', axes, delimiter=',')
    np.savetxt(PATH, data, delimiter=',')


if __name__ == '__main__':
    main()
