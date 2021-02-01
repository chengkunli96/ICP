#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""this is for the part 2 of CourseWork 1."""

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

    # Load data file into trimesh-object
    dst_DataFile = 'bun000_v2.ply'

    mesh_fp = os.path.join(RES_PATH, dst_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    dst_tm = trimesh.load(mesh_fp)

    # rotation angle
    rotate_angles = np.array([-15, -10, -5, 5, 10, 15])
    rotate_rads = np.pi / 180 * rotate_angles
    # rotation center and shift matrix (shift this mesh's center to origin)
    centroid = np.mean(np.array(dst_tm.vertices), axis=0)
    homo_T = np.eye(4)
    homo_T[:3, 3] = -centroid

    # ME figure setting
    fig_ME = plt.figure(figsize=(16, 8))
    ax_ME = fig_ME.add_subplot(1, 1, 1)
    ax_ME.set_ylabel('distance ME')
    ax_ME.set_xlabel('iteration')
    # mesh figure
    fig_mesh = plt.figure(figsize=(16, 8 * rotate_angles.size))

    for (i, rad) in enumerate(rotate_rads):
        # assume rotation axe is z-axe
        # get Rotation Matrix
        R = np.array([[np.cos(rad), -np.sin(rad), 0],
                      [np.sin(rad), np.cos(rad), 0],
                      [0, 0, 1]])
        homo_R = np.eye(4)
        homo_R[:3, :3] = R

        # rotate destination trimesh as src-trimesh
        src_tm = dst_tm.copy()
        src_tm.apply_transform(np.linalg.inv(homo_T) @ homo_R @ homo_T)

        # ICP
        H, ME = tools.baseICP.icp(src_tm, dst_tm, max_iterations=30)
        res_tm = src_tm.copy()
        res_tm.apply_transform(H)

        # show mesh results
        # plot the original two meshes
        ax = fig_mesh.add_subplot(rotate_angles.size, 2, 2 * i + 1, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, src_tm, color='Blues')
        ax.set_title('{}° rotation'.format(rotate_angles[i]))
        ax.view_init(elev=30, azim=-40)
        # plot the result of ICP
        ax = fig_mesh.add_subplot(rotate_angles.size, 2, 2 * i + 2, projection='3d')
        tools.tools.plot_trimesh(ax, dst_tm, color='Reds')
        tools.tools.plot_trimesh(ax, res_tm, color='Blues')
        ax.set_title('result of ICP')
        ax.view_init(elev=30, azim=-40)

        # show MES error
        ax_ME.plot(ME, label=str(rotate_angles[i]))

    fig_ME.legend()
    plt.show()








