#!/usr/bin/env python3

import tkinter as tk
import analyzer
from analyzer import DEFAULT_IDX, DEFAULT_SEG_DEG, DEFAULT_PATH, DEFAULT_DIMEN, DEFAULT_ROT_ANG

# import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure

labels = {}
textentries = {}
buttons = {}
allele = []

DEFAULT_IDX_NAME = 'index'
DEFAULT_SEG_NAME = 'range of angle of each segment'
DEFAULT_DIMEN_NAME = 'dimensions'
DEFAULT_METHOD_NAME = 'method (1: cylinder; 2: plane + circle)'
DEFAULT_ROT_ANG_NAME = 'range of the rotation'
PATH_REMINDER = 'path to file'
INDEX_TXT = 'index of the start vector'
DEGREE_SEGMENT_TXT = 'degree range of a segment'
BUTTON_CALLBACK_TXT = 'launch'
DEFAULT_METHOD = '1'


def insertindict(dict_, ele, txt):
    if txt in dict_.keys():
        dict_[txt + '_'] = ele
    else:
        dict_[txt] = ele


def createlabel(root, txt, **kwargs):
    new_label = tk.Label(root, text=txt)
    insertindict(labels, new_label, txt)
    allele.append(new_label)
    return new_label


def createentry(root, defaultval, txt, **kwargs):
    new_textentry = tk.Entry(root)
    new_textentry.insert(0, defaultval)
    insertindict(textentries, new_textentry, txt)
    allele.append(new_textentry)
    return new_textentry


def createbutton(root, txt, callback, **kwargs):
    newbtn = tk.Button(root, text=txt, command=callback, fg='black')
    insertindict(buttons, newbtn, txt)
    allele.append(newbtn)
    return newbtn


def packall():
    for ele in allele:
        ele.pack()


def launch():
    index = textentries.get(DEFAULT_IDX_NAME).get()
    segment = textentries.get(DEFAULT_SEG_NAME).get()
    path = textentries.get(PATH_REMINDER).get()
    dim = textentries.get(DEFAULT_DIMEN_NAME).get()
    method = textentries.get(DEFAULT_METHOD_NAME).get()
    ang = textentries.get(DEFAULT_ROT_ANG_NAME).get()
    axes_syn = analyzer.main(
        [analyzer.__name__, '-p', path, '-i', index, '-s', segment, '-d', dim, '-r', ang, '-m', method])
    # plot on a figure
    return axes_syn


def main():
    root = tk.Tk()
    createlabel(root, INDEX_TXT)
    createentry(root, str(DEFAULT_IDX), DEFAULT_IDX_NAME)
    createlabel(root, DEGREE_SEGMENT_TXT)
    createentry(root, str(DEFAULT_SEG_DEG), DEFAULT_SEG_NAME)
    createlabel(root, PATH_REMINDER)
    createentry(root, DEFAULT_PATH, PATH_REMINDER)
    createlabel(root, DEFAULT_DIMEN_NAME)
    createentry(root, DEFAULT_DIMEN, DEFAULT_DIMEN_NAME)
    createlabel(root, DEFAULT_METHOD_NAME)
    createentry(root, DEFAULT_METHOD, DEFAULT_METHOD_NAME)
    createlabel(root, DEFAULT_ROT_ANG_NAME)
    createentry(root, DEFAULT_ROT_ANG, DEFAULT_ROT_ANG_NAME)
    createbutton(root, BUTTON_CALLBACK_TXT, launch)
    packall()
    root.mainloop()


if __name__ == '__main__':
    main()
