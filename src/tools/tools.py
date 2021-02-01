import numpy as np
import argparse
import open3d as o3d
import matplotlib.pyplot as plt


def toO3d(tm, color):
    """put trimesh object into open3d object"""
    mesh_o3d = o3d.geometry.TriangleMesh()
    mesh_o3d.vertices = o3d.utility.Vector3dVector(tm.vertices)
    mesh_o3d.triangles = o3d.utility.Vector3iVector(tm.faces)
    mesh_o3d.compute_vertex_normals()
    vex_color_rgb = np.array(color)
    vex_color_rgb = np.tile(vex_color_rgb, (tm.vertices.shape[0], 1))
    mesh_o3d.vertex_colors = o3d.utility.Vector3dVector(vex_color_rgb)
    return mesh_o3d


def get_args():
    parser = argparse.ArgumentParser(description='Train the model.')
    parser.add_argument('-plt', '--matplot', dest='matplot', action='store_true',
                        help='use matplotlib to show the result')
    parser.add_argument('-o3d', '--open3d', dest='open3d', action='store_true',
                        help='use open3d to show the result')

    args = parser.parse_args()
    return args


def plot_trimesh(ax, tm, color='Reds'):
    ax.scatter3D(tm.vertices[:, 2], tm.vertices[:, 0], tm.vertices[:, 1],
                 c=(abs(tm.vertex_normals) @ np.array([0.299, 0.587, 0.114])),
                 cmap=color, alpha=0.2, marker='.')


def trans_trimesh(tm, angle, shift=None):
    # rotation
    rad = angle / 180 * np.pi
    R = np.array([[np.cos(rad), 0, np.sin(rad)],
                  [0, 1, 0],
                  [-np.sin(rad), 0, np.cos(rad)]])
    homo_R = np.eye(4)
    homo_R[:3, :3] = R

    # shift
    if shift is None:
        homo_T = np.eye(4)
    else:
        centroid = np.mean(np.array(tm.vertices), axis=0)
        homo_T = np.eye(4)
        homo_T[:3, 3] = -centroid + np.array(shift)

    tm.apply_transform(homo_R @ homo_T)


