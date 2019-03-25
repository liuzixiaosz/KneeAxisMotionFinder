#!/usr/bin/env python3
import matplotlib

matplotlib.use('TkAgg')
import sys
import getopt
import os
import numpy as np
import math as mt
import utils.dataprocess as dp
import utils.mathutils as mu
from cylinder_fitting import show_fit

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

DEFAULT_IDX = 0
DEFAULT_SEG_DEG = 10
DEFAULT_PATH = 'data.txt'
DEFAULT_DIMEN = 3
# DEFAULT_DIFF = 0.5
DEFAULT_ROT_ANG = 90
MARKERS = 4
FIG1 = plt.figure()


def set_start_vec(index, alldata, refvec):
    dim = refvec.size
    if index < 0:
        maxang = 0
        index = 0
        for i in range(0, len(alldata)):
            this_vec = alldata[i, dim * (MARKERS - 1):] - alldata[i, dim * (MARKERS - 3): dim * (MARKERS - 2)]
            this_ang = mu.radianof(this_vec, refvec)
            if this_ang > maxang:
                maxang = this_ang
                index = i
    return alldata[index, dim * (MARKERS - 1):] - alldata[index, dim * (MARKERS - 3): dim * (MARKERS - 2)]


def parseargv(argv):
    try:
        opts, args = getopt.getopt(args=argv, shortopts='p:i:D:s:',
                                   longopts=['path=', 'dimension=', 'segment=', 'index='])
    except getopt.GetoptError:
        print('args error')
        sys.exit(0)
    path = DEFAULT_PATH
    index = DEFAULT_IDX
    delta_seg = DEFAULT_SEG_DEG
    dimension = DEFAULT_DIMEN
    # diff = DEFAULT_DIFF
    ang_rng = DEFAULT_ROT_ANG
    for o in opts:
        if o[0] == '-p' or o[0] == '--path':
            path = o[1]
        if o[0] == '-i' or o[0] == '--index':
            index = int(o[1])
        if o[0] == '-s' or o[0] == '--segment':
            delta_seg = float(o[1])
        if o[0] == '-D' or o[0] == '--dimension':
            dimension = int(o[1])
        # if o[0] == '-d' or o[0] == '--diff':
        #     diff = float(o[1])
        if o[0] == '-r' or o[0] == '--range':
            ang_rng = float(o[1])
    # return path, index, delta_seg, dimension, diff, ang_rng
    return path, index, delta_seg, dimension, ang_rng


def rot_step1(alldata, dim):
    z_vec = np.zeros([1, dim])
    if dim > 2:
        z_vec[0, 2] = 1
    y_vec = np.zeros([1, dim])
    y_vec[0, 1] = 1
    x_vec = np.zeros([1, dim])
    x_vec[0, 0] = 1
    vec1 = alldata[:, dim: 2 * dim]
    rad2z = mu.radianof(z_vec, vec1) * (1 / 2 - np.array([vec1[:, 1] < 0]).T) * 2
    rotated_vec1 = mu.lengthvec(vec1) * mu.rot(z_vec.repeat(len(rad2z), axis=0), rad2z, x_vec)
    proj1 = np.copy(rotated_vec1)
    proj1[:, 1] = 0
    vec1_rad2rot = mu.radianof(rotated_vec1 - proj1, vec1 - proj1) * (1 / 2 - np.array([vec1[:, 0] > 0]).T) * 2
    # TODO: +- value, rotation varification
    for i in range(0, MARKERS):
        alldata[:, i * dim: i * dim + dim] = mu.rot(alldata[:, i * dim: i * dim + dim], vec1_rad2rot, z_vec)
    vec2 = alldata[:, 2 * dim: 3 * dim]
    rad2vec1 = mu.radianof(vec1, vec2) * (1 / 2 - np.array([vec2[:, 2] > 0]).T) * 2

    # TODO: PROBLEMS HERE ABOUT ROTATION
    rotated_vec2 = mu.lengthvec(vec2) * mu.rot(vec1, rad2vec1, x_vec) / mu.lengthvec(vec1)

    # proj2 = np.copy(rotated_vec2)
    # proj2[:, 2] = 0
    proj2 = vec1 * mu.lengthvec(vec2) * mu.cosof(vec1, vec2) / mu.lengthvec(vec1)
    vec2_rad2rot = mu.radianof(rotated_vec2 - proj2, vec2 - proj2) * (1 / 2 - np.array([vec2[:, 0] < 0]).T) * 2
    for i in range(0, MARKERS):
        alldata[:, i * dim: i * dim + dim] = mu.rot(alldata[:, i * dim: i * dim + dim], vec2_rad2rot, vec1)
    return alldata


def plot_data(data, ax):
    for d in data:
        d = np.array(d)
        if d.size != 0:
            ax.scatter(xs=d[:, 0], ys=d[:, 1], zs=d[:, 2])
    return ax


def plot_axes(center_dict, ax_dict, ax, scale=100):
    for k in ax_dict.keys():
        d = np.vstack((center_dict.get(k), ax_dict.get(k) + center_dict.get(k))) * scale
        ax.plot(xs=d[:, 0], ys=d[:, 1], zs=d[:, 2])
    return ax


def main(argv):
    '''

    :param argv: path to file
    :return:
    '''
    path, index_org_vec, delta_seg, dimensions, ang_rng = parseargv(argv)
    print('start analyzing ...')
    delta_seg = mt.radians(delta_seg)
    rawdata = np.array(dp.readdata(path))
    rec_data = np.zeros(rawdata.shape)
    y_vec = np.zeros([1, dimensions])
    y_vec[0, 1] = 1
    x_vec = np.zeros([1, dimensions])
    x_vec[0, 0] = 1
    z_vec = np.zeros([1, dimensions])
    ang_rng = mt.radians(ang_rng)
    if dimensions > 2:
        z_vec[0, 2] = 1
    for mk in range(0, MARKERS):
        this_start = mk * dimensions
        this_end = this_start + dimensions

        # rectify coordinate: all minus the first marked.
        rectified = mu.cordrectify(rawdata[:, this_start: this_end], rawdata[:, 0: dimensions])
        rec_data[:, this_start: this_end] = rectified

    rec_data = rot_step1(rec_data, dimensions)
    start_vec = set_start_vec(index_org_vec, rec_data, y_vec)
    seped_datalists, seped_marker4 = dp.sepdata(rec_data, start_vec, delta_seg, maxrot=ang_rng)
    ax = Axes3D(FIG1)
    plot_data(seped_marker4, ax)

    axes_syn = {}
    center_syn = {}
    for l_idx in range(0, len(seped_marker4)):
        if len(seped_marker4[l_idx]) < 3:
            continue

        # plt.figure(l_idx)
        # w_fit, C_fit, r_fit, fit_err = mu.cf.fit(seped_marker4[l_idx])
        # axes = w_fit
        #
        # show_fit(w_fit, C_fit, r_fit, seped_marker4[l_idx])

        data_this = np.array(seped_marker4[l_idx])
        r = mu.plane_fitting(data_this[:, 0], data_this[:, 1], data_this[:, 2])
        xyz = mu.spherefit_center(data_this)
        tmp_line = mu.normal_vec_plane(r[0][0], r[0][1])
        axes_syn[l_idx] = tmp_line
        center_syn[l_idx] = np.array([xyz[0][0], xyz[1][0], xyz[2][0]])

    plot_axes(center_syn, axes_syn, ax, scale=1)
    print('end fitting')
    print(str(axes_syn))
    plt.show()
    return axes_syn


if __name__ == '__main__':
    axes_syn_dict = main(sys.argv)
