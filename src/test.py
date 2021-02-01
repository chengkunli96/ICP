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
    dst_DataFile = 'bun045_v2.ply'
    src_DataFile = 'bun090_v2.ply'

    mesh_fp = os.path.join(RES_PATH, dst_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    dst_tm = trimesh.load(mesh_fp)

    mesh_fp = os.path.join(RES_PATH, src_DataFile)
    assert os.path.exists(mesh_fp), 'cannot found:' + mesh_fp
    src_tm = trimesh.load(mesh_fp)

    # R
    rad = 45/180 * np.pi
    R = np.array([[np.cos(rad), 0, np.sin(rad)],
                  [0, 1, 0],
                  [-np.sin(rad), 0, np.cos(rad)]])
    homo_R = np.eye(4)
    homo_R[:3, :3] = R

    # T
    centroid = np.mean(np.array(src_tm.vertices), axis=0)
    homo_T = np.eye(4)
    homo_T[:3, 3] = -centroid

    src_tm.apply_transform(homo_R @ homo_T)

    # T
    centroid = np.mean(np.array(dst_tm.vertices), axis=0)
    homo_T = np.eye(4)
    homo_T[:3, 3] = -centroid
    dst_tm.apply_transform(homo_T)


    # ICP
    H, MSE = tools.baseICP.icp(src_tm, dst_tm, max_iterations=100)
    res_tm = src_tm.copy()
    res_tm.apply_transform(H)
    print(H)

    plt.plot(MSE)
    plt.show()

    # show the result by open3d
    dst_mesh_o3d1 = tools.tools.toO3d(dst_tm, color=(0.5, 0, 0))
    src_mesh_o3d2 = tools.tools.toO3d(src_tm, color=(0, 0, 0.5))
    res_mesh_o3d2 = tools.tools.toO3d(res_tm, color=(0, 0, 0.5))
    o3d.visualization.draw_geometries([dst_mesh_o3d1, src_mesh_o3d2])
    o3d.visualization.draw_geometries([dst_mesh_o3d1, res_mesh_o3d2])







