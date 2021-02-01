# COMP119-Assignment1
This part is to introduce the file structure 
and the instruction for running code.

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
For question 1, see the ICP's performance:
```
# see the result by open3d
# remember to press ‘q’ in keyboard to see the next plot
python part1.py
	
# if you want to see the result by matplotlib
python part1.py -plt
```
For quetion 2, simulate the effect of increasing misalignment by adding a rotation.
```
python part2.py
```
For question 3, Evaluate how well ICP performs as you continue to add more noise.
```
python part3.py
```
For question 4, report accuracy with increasing subsampling rates.
```
python part4.py
```
For question 5, reconstruction from all of scan models.
```
python part5.py
```
For question 6, implement point to plane ICP.
```
python part6.py
```