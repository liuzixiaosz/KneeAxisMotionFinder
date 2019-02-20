import numpy as np
import math as mt
import utils.mathutils as mu


def get_max_container(datalist, diff):
    '''

    :param datalist:
    :param diff:
    :return:
    '''
    container_dict = {}
    for data in datalist:
        floor, cell = checkcontainer(data, diff)
        if floor in container_dict.keys():
            container_dict[floor] = container_dict.get(floor) + 1
        else:
            container_dict[floor] = 1
    keys_list = list(container_dict.keys())
    keys_list.sort(key=lambda x: container_dict.get(x))
    floor_max = keys_list[-1]
    ceil_max = floor_max + diff
    return floor_max, ceil_max


def checkcontainer(data, diff):
    dimensions = np.size(data, 1)
    floor = np.zeros(np.shape(data))
    ceil = np.zeros(np.shape(data))
    for d in range(0, dimensions):
        floor_this = mt.floor(data[d] / diff) * diff
        ceil_this = floor_this + diff
        floor[d] = floor_this
        ceil[d] = ceil_this
    return floor, ceil


def readdata(path):
    rawdata = np.genfromtxt(path, delimiter=',')
    return rawdata


def sepdata(org_data, start_vec, seg_delta, **kwargs):
    '''
    seperate data

    X = z axis
    X---o--------o------------> y
    |          / \
    |         /   \
    |        /     o
    |       /       \
    |      /         \
    |     /           o
    |    v
    |    start_vec
    |
    v
    x
    :param start_vec:
    :param org_data:
    :param seg_delta:
    :param kwargs:
            maxdeg --- max range of rotation
    :return:
    '''
    markers = 4
    new_data = []
    maxrot = mt.pi
    dim = len(start_vec)
    y_vec = np.zeros([1, dim])
    y_vec[0, 1] = 1
    if 'maxrot' in kwargs.keys():
        maxrot = kwargs.get('maxrot')
    total_sep = mt.floor(maxrot / seg_delta)
    # rad2y = mu.radianof(y_vec, start_vec)[0, 0]
    vec = org_data[:, dim * (markers - 1):] - org_data[:, dim: dim * 2]
    rad2start = mu.radianof(vec, start_vec)

    for i in range(0, total_sep):
        new_data.append([])
    for i in range(0, len(vec)):
        this_vec = vec[i, :]
        this_ang = rad2start[i, :][0]
        for j in range(0, total_sep):
            ceil_angle = (j + 1) * seg_delta
            floor_angle = j * seg_delta
            if floor_angle <= this_ang < ceil_angle:
                new_data[j].append(this_vec)
                break
    return new_data
