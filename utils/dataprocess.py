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


def sepdata(start_vec, org_data, seg_delta, **kwargs):
    '''
    seperate data

    ---o--------o------------> y
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


    new_data = []
    maxrot = mt.pi
    y_vec = np.zeros([1, np.size(org_data, 1)])
    y_vec[1] = 1
    if 'maxrot' in kwargs.keys():
        maxrot = kwargs.get('maxdeg')
    total_sep = mt.floor(maxrot / seg_delta)
    deg_to_y = mu.radianof(y_vec, start_vec)
    for i in range(0, total_sep):
        ceil_angle = (i + 1) * seg_delta
        floor_angle = i * seg_delta
        this_datalist = []
        for data in org_data:
            if (mu.radianof(data, y_vec) < deg_to_y or data[0] < 0) \
                    and floor_angle <= mu.radianof(start_vec, data) < ceil_angle:
                this_datalist.append(data)
        new_data.append(this_datalist)
    return new_data
