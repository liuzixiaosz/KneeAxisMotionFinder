import random
import numpy as np
import utils.mathutils as mu
import os
import math
from analyzer import DEFAULT_SEG_DEG, DEFAULT_ROT_ANG, DEFAULT_PATH

PATH = '..' + os.sep + DEFAULT_PATH
MAX_RNG = DEFAULT_ROT_ANG
SEG_NUM = int(DEFAULT_ROT_ANG / DEFAULT_SEG_DEG)
SIZE = 1800
MARKS = 4
DIM = 3


def setbase(s):
    p1 = [0, 0, 0]
    p2 = [0, 1, 0]
    p3 = [0, 1, 0.1]
    p4 = [1, 1, 0]
    return np.repeat([p1 + p2 + p3 + p4], s, axis=0) * 100


def setnoise(s_turp, loc=0, scale=0.1):
    return np.random.normal(loc=loc, scale=scale, size=s_turp)


def setaxes(segs):
    d = random.random() / segs / 20
    axes = np.zeros([segs, DIM])
    axes[:, 2] = -1
    for i in range(0, segs):
        axes[i, 0] = d * i
    return axes


def write(data):
    print(str(data))
    np.savetxt(PATH, data, delimiter=',')


def frac():
    return random.random()


def main():
    base = setbase(SIZE)
    noise = setnoise(base.shape, scale=0.01)
    data = base + noise
    axes_raw = setaxes(DEFAULT_SEG_DEG)
    noise2 = setnoise(axes_raw.shape, scale=0.1)
    axes = axes_raw / mu.lengthvec(axes_raw)
    start_vec = np.array(data[0, DIM * (MARKS - 1):] - data[0, DIM: 2 * DIM])
    rad = math.radians(DEFAULT_SEG_DEG)
    for i in range(1, SIZE):
        index = i % SEG_NUM
        rotated = mu.rot(start_vec, index * rad + frac() * rad, [axes[index, :]])
        data[i, DIM * (MARKS - 1):] = data[i, DIM: 2 * DIM] + rotated
    np.savetxt('refaxis.txt', axes, delimiter=',')
    np.savetxt(PATH, data, delimiter=',')


if __name__ == '__main__':
    main()
