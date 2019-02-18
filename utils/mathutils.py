import sys
import os
import numpy as np
import math as mt


def lengthvec(vec):
    '''
    find length of a vector
    :param vec:
    :return:
    '''
    return np.sqrt(np.sum(np.power(vec, 2)))


def cosof(vec1, vec2):
    '''

    :param vec1:
    :param vec2:
    :return:
    '''
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    vec3 = vec1 - vec2
    len1 = np.sqrt(np.sum(np.power(vec1, 2)))
    len2 = np.sqrt(np.sum(np.power(vec2, 2)))
    len3 = np.sqrt(np.sum(np.power(vec3, 2)))
    return (mt.pow(len1, 2) + mt.pow(len2, 2) - mt.pow(len3, 2)) / (2 * len1 * len2)


def degreeof(vec1, vec2):
    '''
    find the angle between two vectors
    :param vec1:
    :param vec2:
    :return:
    '''
    cos_ang = cosof(vec1, vec2)
    return mt.acos(cos_ang)


def cordrectify(cord, strd):
    '''
    rectify coordinate
    :param cord: coordinate of the point to rectify
    :param strd: standard for rectifying
    :return:
    '''
    return np.array(cord) - np.array(strd)


def getaxis(datalist):
    '''

    :param datalist:
    :return:
    '''
    # 拟合轴 TODO
    ax = None

    return ax
