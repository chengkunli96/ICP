#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""this is for the part 1 of CourseWork 1."""

__author__ = 'Chengkun Li'

import os
import open3d as o3d
import numpy as np
import trimesh

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

    args = tools.tools.get_args()

    # Load data file into trimesh-object
    dst_DataFile = 'bun000_v2.ply'
    src_DataFile = 'bun045_v2.ply'

    mesh_fp = os.path.join(RES_PATH, dst_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    dst_tm = trimesh.load(mesh_fp)

    mesh_fp = os.path.join(RES_PATH, src_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    src_tm = trimesh.load(mesh_fp)

    # ICP
    H, ME = tools.baseICP.icp(src_tm, dst_tm, max_iterations=30)
    res_tm = src_tm.copy()
    res_tm.apply_transform(H)

    # plt.plot(ME)
    # plt.show()

    # show the result
    if not args.matplot:
        # show the result by open3d
        dst_mesh_o3d = tools.tools.toO3d(dst_tm, color=(0.5, 0, 0))
        src_mesh_o3d = tools.tools.toO3d(src_tm, color=(0, 0, 0.5))
        res_mesh_o3d = tools.tools.toO3d(res_tm, color=(0, 0, 0.5))
        o3d.visualization.draw_geometries([dst_mesh_o3d, src_mesh_o3d])
        o3d.visualization.draw_geometries([dst_mesh_o3d, res_mesh_o3d])
    else:
        fig = plt.figure()
        # plot the original two meshes
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, src_tm, color='Blues')
        ax.view_init(elev=30, azim=-40)
        ax.axis('off')
        # plot the result of ICP
        ax = fig.add_subplot(1, 2, 2, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, res_tm, color='Blues')
        ax.view_init(elev=30, azim=-40)
        ax.axis('off')
        plt.show()







