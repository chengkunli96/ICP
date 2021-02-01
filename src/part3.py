#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""this is for the part 3 of CourseWork 1."""

__author__ = 'Chengkun Li'

import sys
import os

import open3d as o3d
import numpy as np
import trimesh

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

    # bounding box
    src_vertices_array = np.array(dst_tm.vertices)
    bounding_box = np.array([np.max(src_vertices_array[:, 0]) - np.min(src_vertices_array[:, 0]),
                             np.max(src_vertices_array[:, 1]) - np.min(src_vertices_array[:, 1]),
                             np.max(src_vertices_array[:, 2]) - np.min(src_vertices_array[:, 2]),])

    # noise scales
    noise_scales = np.array([0.01, 0.025, 0.05, 0.075, 0.1])

    # ME figure setting
    fig_ME = plt.figure(figsize=(16, 8))
    ax_ME = fig_ME.add_subplot(1, 1, 1)
    ax_ME.set_ylabel('distance ME')
    ax_ME.set_xlabel('iteration')
    # mesh figure
    fig_mesh = plt.figure(figsize=(16, 8 * noise_scales.size))

    for (i, k) in enumerate(noise_scales):
        # get src-trimesh by adding a random
        src_pts = np.array(src_tm.vertices)
        noisy = k * bounding_box * np.random.normal(loc=0.0, scale=1.0, size=src_pts.shape)
        noisy_src_pts = src_pts + noisy
        noisy_src_tm = trimesh.Trimesh(vertices=noisy_src_pts, faces=src_tm.faces)

        # ICP
        H, ME = tools.baseICP.icp(noisy_src_tm, dst_tm, max_iterations=30)
        res_tm = noisy_src_tm.copy()
        res_tm.apply_transform(H)

        # show mesh results
        # plot the original two meshes
        ax = fig_mesh.add_subplot(noise_scales.size, 2, 2 * i + 1, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, noisy_src_tm, color='Blues')
        ax.set_title('noise scale = {}'.format(k))
        ax.view_init(elev=30, azim=-40)
        # plot the result of ICP
        ax = fig_mesh.add_subplot(noise_scales.size, 2, 2 * i + 2, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, res_tm, color='Blues')
        ax.set_title('result of ICP')
        ax.view_init(elev=30, azim=-40)

        # show MES error
        ax_ME.plot(ME, label='noise scale = ' + str(k))

    fig_ME.legend()
    plt.show()