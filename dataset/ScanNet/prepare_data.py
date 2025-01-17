# Copyright 2016-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import glob, plyfile, numpy as np, multiprocessing as mp, torch
import os
import os.path as osp

# Map relevant classes to {0,1,...,19}, and ignored classes to -100
remapper=np.ones(150)*(-100)
for i,x in enumerate([1,2,3,4,5,6,7,8,9,10,11,12,14,16,24,28,33,34,36,39]):
    remapper[x]=i

files=sorted(glob.glob('*/*_vh_clean_2.ply'))
files2=sorted(glob.glob('*/*_vh_clean_2.labels.ply'))
assert len(files) == len(files2)

def f(fn: str):
    split = fn.split('/')[0]
    file_name = fn[len(split) + 1:]
    fn2 = fn[:-3]+'labels.ply'
    scene_name = fn[:-15].split('/')[-1]
    fn3 = os.path.join('/share/datasets/ScanNetv2/scans', scene_name, scene_name + '.txt')

    pointcloud_file=plyfile.PlyData().read(fn)
    pointcloud=np.array([list(x) for x in pointcloud_file.elements[0]])
    center = pointcloud[:,:3].mean(0)
    coords=np.ascontiguousarray(pointcloud[:,:3] - center) # centering
    colors=np.ascontiguousarray(pointcloud[:,3:6])/127.5-1 # normalize

    labels_file=plyfile.PlyData().read(fn2)
    labels=remapper[np.array(labels_file.elements[0]['label'])]
    
    lines = open(fn3).readlines()
    for line in lines:
        if 'axisAlignment' in line:
            axis_align_matrix = [float(x) \
                for x in line.rstrip().strip('axisAlignment = ').split(' ')]
            break
    axis_align_matrix = np.ascontiguousarray(axis_align_matrix).reshape((4,4))

    if not osp.exists(split + '_processed'):
        os.makedirs(split + '_processed')
    torch.save(((coords, center), colors, labels, axis_align_matrix),osp.join(split + '_processed', file_name[:-4] + '.pth'))

    print(fn)

p = mp.Pool(processes=mp.cpu_count())
p.map(f,files)
p.close()
p.join()
