# -*- coding: utf-8 -*-

"""this is for the part 5 of CourseWork 1."""

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
    # Load data file
    files = os.listdir(RES_PATH)
    files.sort()

    # start scan plane
    start_index = 4
    dst_DataFile = files[start_index]
    scan_angle = int(dst_DataFile[3:6])

    mesh_fp = os.path.join(RES_PATH, dst_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    dst_tm = trimesh.load(mesh_fp)
    tools.tools.trans_trimesh(dst_tm, scan_angle)

    for i in range(len(files) - 1):
        next_index = i + 1 + start_index
        next_index = (next_index - len(files) if next_index >= len(files) else next_index)
        src_DataFile = files[next_index]
        scan_angle = int(src_DataFile[3:6])

        mesh_fp = os.path.join(RES_PATH, src_DataFile)
        assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
        src_tm = trimesh.load(mesh_fp)
        tools.tools.trans_trimesh(src_tm, scan_angle)

        # ICP
        H, _ = tools.baseICP.icp(src_tm, dst_tm, max_iterations=30)
        res_tm = src_tm.copy()
        res_tm.apply_transform(H)

        # get new dst_tm
        dst_vertices_array = np.array(dst_tm.vertices)
        res_vertices_array = np.array(res_tm.vertices)
        dst_faces_array = np.array(dst_tm.faces)
        res_faces_array = np.array(res_tm.faces)
        new_vertices = np.vstack((dst_vertices_array, res_vertices_array))
        new_faces = np.vstack((dst_faces_array, res_faces_array + dst_vertices_array.shape[0]))
        syn_dst_tm = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)

        # update
        dst_tm = syn_dst_tm

    # show
    fig_mesh = plt.figure(figsize=(16, 8))
    for i in range(6):
        ax = fig_mesh.add_subplot(2, 3, i + 1, projection='3d')
        ax.scatter3D(syn_dst_tm.vertices[:, 2], syn_dst_tm.vertices[:, 0], syn_dst_tm.vertices[:, 1],
                     c=(abs(syn_dst_tm.vertex_normals)), marker='.')
        ax.view_init(elev=30, azim=-40 + 60 * i)
        ax.axis('off')
    plt.show()



