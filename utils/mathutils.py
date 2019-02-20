import numpy as np
import math as mt
import scipy.optimize as opt
from cylinder_fitting import fitting as cf
import scipy.optimize as opt


def normal_vec_plane(a, b, c=-1):
    '''
    ax + by + d = cz
    ax - by - cz = d
    :param a:
    :param b:
    :param c:
    :return:
    '''
    vec = np.array([a, b, c])
    return vec / lengthvec(np.array([vec]))


def plane_fitting(x, y, z):
    '''
    z = ax + by + c
    :param x:
    :param y:
    :param z:
    :return: r with [[a, b, c], 1]
    '''
    def f(param):
        a, b, c = param
        return a * x + b * y + c - z
    r = opt.leastsq(f, np.array([0, 0, 1]))
    return r


def lengthvec(vec):
    '''
    find length of a vector
    :param vec:
    :return:
    '''
    return np.sqrt(np.sum(np.power(vec, 2), 1, keepdims=True))


def cosof(vec1, vec2):
    '''

    :param vec1:
    :param vec2:
    :return:
    '''
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if len(vec1.shape) == 1:
        vec1 = np.array([vec1])
    if len(vec2.shape) == 1:
        vec2 = np.array([vec2])
    vec3 = vec1 - vec2
    len1 = np.sqrt(np.sum(np.power(vec1, 2), 1, keepdims=True))
    len2 = np.sqrt(np.sum(np.power(vec2, 2), 1, keepdims=True))
    len3 = np.sqrt(np.sum(np.power(vec3, 2), 1, keepdims=True))
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
    if np.all(vec == axis):
        return vec
    is2D = False
    if np.shape(vec) == (1, 2):
        vec = np.hstack(vec, [[1]])
        is2D = True
    elif np.shape(vec) == (2,):
        vec = np.hstack(np.array([vec]), [[1]])
        is2D = True
    if np.shape(axis) == (1, 2):
        axis = np.hstack(axis, [[1]])
    elif np.shape(axis) == (2,):
        axis = np.hstack(np.array(axis), [[1]])
    if len(vec.shape) == 1:
        vec = np.array([vec])
    if type(theta) is float or type(theta) is int:
        theta = np.array([theta])
    mtx = rot_matrix3D(axis, theta)
    vec_new = np.zeros(vec.shape)
    for i in range(0, mtx.shape[-1]):
        vec_new[i, :] = np.dot(vec[i, :], mtx[:, :, i])
    if is2D:
        vec_new[:, 3] = 0
    return vec_new


def rot_matrix3D(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    if type(theta) is float or type(theta) is int:
        theta = np.array([theta])
    if len(np.array(theta).shape) == 1:
        theta = np.array([theta])
    axis = np.array(axis) / lengthvec(axis)
    if axis.shape[1] == 1:
        axis = np.repeat(axis, np.size(theta), axis=0)
    a = np.array(np.cos(theta / 2.0))[:, 0]
    var = -axis * np.repeat(np.array(np.sin(theta / 2.0)), axis.shape[1], axis=1)
    b = np.array(var[:, 0])
    c = np.array(var[:, 1])
    d = np.array(var[:, 2])
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


def cylinderfitting(xyz, p, th):
    """
    This is a fitting for a vertical cylinder fitting
    Reference:
    http://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XXXIX-B5/169/2012/isprsarchives-XXXIX-B5-169-2012.pdf

    xyz is a matrix contain at least 5 rows, and each row stores x y z of a cylindrical surface
    p is initial values of the parameter;
    p[0] = Xc, x coordinate of the cylinder centre
    P[1] = Yc, y coordinate of the cylinder centre
    P[2] = alpha, rotation angle (radian) about the x-axis
    P[3] = beta, rotation angle (radian) about the y-axis
    P[4] = r, radius of the cylinder

    th, threshold for the convergence of the least squares

    """
    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]

    fitfunc = lambda p, x, y, z: (- np.cos(p[3]) * (p[0] - x) - z * np.cos(p[2]) * np.sin(p[3]) - np.sin(
        p[2]) * np.sin(p[3]) * (p[1] - y)) ** 2 + (
                                         z * np.sin(p[2]) - np.cos(p[2]) * (p[1] - y)) ** 2  # fit function
    errfunc = lambda p, x, y, z: fitfunc(p, x, y, z) - p[4] ** 2  # error function

    est_p, success = opt.leastsq(errfunc, p, args=(x, y, z), maxfev=1000)

    return est_p
