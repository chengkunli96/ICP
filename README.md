# ICP

![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![GitHub stars](https://img.shields.io/github/stars/mremilien/ICP.svg?style=social)](https://github.com/mremilien/ICP/stargazers)

Iterative closest point (ICP) is an algorithm employed to minimize the difference between two clouds of points. 
This code is used to reconstrct 3d surfaces, and final result is shown by a trimesh-class-object.

The main steps for ICP is as list:
1. select a subject from source points (src-pts).
2. match each src-pts to closest destination points (dst-pts) by knn.
3. reject bad corresponding pairs.
4. solve optimization function to get homograph transformation matrix.
5. align src-pts to dst-pts, and then iterate.

For the rejection part, I reject all of corresponding paires which the angle residual of their normal vector is more than 20°.
If you want to change this, please use `ctrl+f` in core code to find key-words `threshold` to change it.

## Requirements 
The version of python is 3.6.12, and the libraries I used as following,
* open3d==0.12.0
* scikit-learn==0.24.1
* transformations==2020.1.1
* trimesh==3.9.1
* numpy==1.19.2
* matplotlib==3.3.2
* argparse==1.4.0

## File structure
* `data` this folder is used to place our resources files
* `docs` the report of my experiment.
* `src` includes all of the source code.
   * `part*.py` finishes different question.
   * `tools` floder is a package I build to implement core algorithm
        * `baseICP.py` - point to point ICP
        * `normalICP.py` - point to plane ICP
        * `tools.py` - some tool function, like show mesh in open3d gui
 
 ## How to run
 You should make sure all of dependencies have been build. And next,
```
cd src/
```
For experiment 1, see the ICP's performance:
```
# see the result by open3d
# remember to press ‘q’ in keyboard to see the next plot
python part1.py
	
# if you want to see the result by matplotlib
python part1.py -plt
```
For experiment 2, simulate the effect of increasing misalignment by adding a rotation.
```
python part2.py
```
For experiment 3, Evaluate how well ICP performs as you continue to add more noise.
```
python part3.py
```
For experiment 4, report accuracy with increasing subsampling rates.
```
python part4.py
```
For experiment 5, reconstruction from all of scan models.
```
python part5.py
```
For experiment 6, implement point to plane ICP.
```
python part6.py
```

## See a sample
If you run the `part5` code, you will the result as following.
![part5](https://github.com/mremilien/ICP/blob/main/docs/recon.png)
