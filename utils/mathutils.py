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
    len1 = np.sqrt(np.sum(np.power(vec1, 2), 1))
    len2 = np.sqrt(np.sum(np.power(vec2, 2), 1))
    len3 = np.sqrt(np.sum(np.power(vec3, 2), 1))
    return (np.power(len1, 2) + np.power(len2, 2) - np.power(len3, 2)) / (2 * len1 * len2)


def radianof(vec1, vec2):
    '''
    find the angle between two vectors
    :param vec1:
    :param vec2:
    :return:
    '''
    cos_ang = cosof(vec1, vec2)
    return np.arccos(cos_ang)


def cordrectify(cord, strd):
    '''
    rectify coordinate
    :param cord: coordinate of the point to rectify
    :param strd: standard for rectifying
    :return:
    '''
    return np.array(cord) - np.array(strd)


def spherefit_center(datalist):
    '''

    :param datalist:
    :return:
    '''
    radius, x, y, z = sphere_fit(datalist)

    return [x, y, z]


def rot(vec, theta, axis):
    '''
    0, vec1,
    :param vec:
    :param theta:
    :param axis:
    :return:
    '''
    if np.shape(vec) == (1, 2):
        vec = np.hstack(vec, [[1]])
    elif np.shape(vec) == (2,):
        vec = np.hstack(np.array([vec]), [[1]])
    if np.shape(axis) == (1, 2):
        axis = np.hstack(axis, [[1]])
    elif np.shape(axis) == (2,):
        axis = np.hstack(np.array(axis), [[1]])

    mtx = rot_matrix3D(axis, theta)
    return np.dot(vec, mtx)


def rot_matrix3D(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / mt.sqrt(np.dot(axis, axis))
    a = mt.cos(theta / 2.0)
    b, c, d = -axis * mt.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def sphere_fit(data):
    #   Assemble the A matrix

    spX = np.array(data[:, 0])
    spY = np.array(data[:, 1])
    spZ = np.array(data[:, 2])
    A = np.zeros((len(spX), 4))
    A[:, 0] = spX * 2
    A[:, 1] = spY * 2
    A[:, 2] = spZ * 2
    A[:, 3] = 1
    #   Assemble the f matrix
    f = np.zeros((len(spX), 1))
    f[:, 0] = (spX * spX) + (spY * spY) + (spZ * spZ)
    C, residules, rank, singval = np.linalg.lstsq(A, f)
    #   solve for the radius
    t = (C[0] * C[0]) + (C[1] * C[1]) + (C[2] * C[2]) + C[3]
    radius = mt.sqrt(t)
    return radius, C[0], C[1], C[2]
