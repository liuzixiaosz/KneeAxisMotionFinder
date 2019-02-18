import sys
import os
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


def sepdata(start_vec, org_data, delta, **kwargs):
    '''
    seperate data
    :param start_vec:
    :param org_data:
    :param delta:
    :param kwargs: criterion --- to judge if two equals
            maxdeg --- maxdegree
    :return:
    '''
    new_data = []
    maxdeg = mt.pi
    cri = 0.05

    if 'criterion' in kwargs.keys():
        cri = kwargs.get('criterion')
    if 'maxdeg' in kwargs.keys():
        maxdeg = kwargs.get('maxdeg')
    total_sep = mt.floor(maxdeg / delta)

    for i in range(0, total_sep):
        ceil_angle = (i + 1) * delta
        this_datalist = []
        for data in org_data:
            if mt.fabs(mu.degreeof(start_vec, data) - ceil_angle) < cri:
                this_datalist.append(data)
        new_data.append(this_datalist)
    return new_data
