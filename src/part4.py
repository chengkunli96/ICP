#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""this is for the part 4 of CourseWork 1."""

__author__ = 'Chengkun Li'

import sys
import os

import open3d as o3d
import numpy as np
import trimesh
import time

import matplotlib
import matplotlib.pyplot as plt
import tools.baseICP
import tools.tools


# check whether the data folder exists
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
RES_PATH = os.path.join(FILE_PATH, '../data/bunny_v2')
if not os.path.exists(RES_PATH):
    print('cannot find resources folder, please update RES_PATH')
    exit(1)


if __name__ == '__main__':
    # Load data file into trimesh-object
    dst_DataFile = 'bun000_v2.ply'
    src_DataFile = 'bun045_v2.ply'

    mesh_fp = os.path.join(RES_PATH, dst_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    dst_tm = trimesh.load(mesh_fp)

    mesh_fp = os.path.join(RES_PATH, src_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    src_tm = trimesh.load(mesh_fp)

    # rate list
    rates = np.array([0.01, 0.1, 0.25, 0.5, 0.75, 1])

    # ME figure setting
    fig_ME = plt.figure(figsize=(16, 8))
    ax_ME = fig_ME.add_subplot(1, 2, 1)
    ax_time = fig_ME.add_subplot(1, 2, 2)
    ax_ME.set_ylabel('distance ME')
    ax_ME.set_xlabel('iteration')
    # mesh figure
    fig_mesh = plt.figure(figsize=(16, 8 * rates.size))

    print(src_tm.vertices.shape)

    run_times = []
    for (i, rate) in enumerate(rates):

        start = time.time()

        # ICP
        H, ME = tools.baseICP.icp(src_tm, dst_tm, max_iterations=30, samplerate=rate)
        res_tm = src_tm.copy()
        res_tm.apply_transform(H)

        end = time.time()
        run_times.append(end - start)

        # show mesh results
        # plot the original two meshes
        ax = fig_mesh.add_subplot(rates.size, 2, 2 * i + 1, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, src_tm, color='Blues')
        ax.set_title('sub sample rate={}%'.format(rates[i] * 100))
        ax.view_init(elev=30, azim=-40)
        # plot the result of ICP
        ax = fig_mesh.add_subplot(rates.size, 2, 2 * i + 2, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, res_tm, color='Blues')
        ax.set_title('result of ICP')
        ax.view_init(elev=30, azim=-40)

        # show MES error
        ax_ME.plot(ME, label='rate='+str(100 * rate)+'%')

    ax_ME.legend()

    ax_time.plot(rates, run_times, marker='*')
    ax_time.set_title('running time for 30 iteration')
    ax_time.set_xlabel('subsample rate')
    ax_time.set_ylabel('time/s')

    plt.show()


