import sys
import getopt
import os
import numpy as np
import math as mt
import utils.dataprocess as dp
import utils.mathutils as mu

DEFAULT_IDX = 0
DEFAULT_SEG = 15
DEFAULT_PATH = 'data.txt'
DEFAULT_DIMEN = 3
DEFAULT_DIFF = 0.5


def set_start_vec(index, rawdata):
    return rawdata[index][:]


def parseargv(argv):
    try:
        opts, args = getopt.getopt(args=argv, shortopts='p:i:d:D:s:',
                                   longopts=['path=', 'dimension=', 'segment=', 'index=', 'diff='])
    except getopt.GetoptError:
        print('args error')
        sys.exit(0)
    path = DEFAULT_PATH
    index = DEFAULT_IDX
    delta_seg = DEFAULT_SEG
    dimension = DEFAULT_DIMEN
    diff = DEFAULT_DIFF
    for o in opts:
        if o[0] == '-p' or o[0] == '--path':
            path = o[1]
        if o[0] == '-i' or o[0] == '--index':
            index = int(o[1])
        if o[0] == '-s' or o[0] == '--segment':
            delta_seg = float(o[1])
        if o[0] == '-D' or o[0] == '--dimension':
            dimension = int(o[1])
        if o[0] == '-d' or o[0] == '--diff':
            diff = float(o[1])
    return path, index, delta_seg, dimension, diff


def main(argv):
    '''

    :param argv: path to file
    :return:
    '''

    path, index_org_vec, delta_seg, dimensions, diff = parseargv(argv)
    print('start analyzing ...')
    rawdata = np.array(dp.readdata(path))
    rec_data = np.zeros(rawdata.shape)
    for dim in range(0, int(np.size(rawdata, 1) / dimensions)):
        this_start = dim * dimensions
        this_end = this_start + dimensions - 1
        rec_data[:, this_start: this_end] = mu.cordrectify(rawdata[:, this_start: this_end],
                                                           rawdata[:, 0: dimensions - 1])
    start_vec = set_start_vec(index_org_vec, rec_data)
    seped_datalists = dp.sepdata(rec_data, start_vec, delta_seg)
    axes_syn = {}
    for listidx in range(0, len(seped_datalists)):
        axes = mu.getaxis(seped_datalists[listidx])
        floor, ceil = dp.get_max_container(axes, diff)
        center = floor + ceil / 2
        axes_syn[listidx] = center
    print(str(axes_syn_dict))
    return axes_syn


if __name__ == '__main__':
    axes_syn_dict = main(sys.argv)

