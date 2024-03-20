'''
    Specific to sphere placental segmentations...
'''

import pandas as pd
import glob
import os 
import shutil

dat_dir = "/Volumes/PIRG_Research/Wellcome Leap/Sphere placenta segmentations/"
out_dir = "/Volumes/PIRG_Research/Wellcome Leap/Sphere Placental Segementations Renamed/"

files = glob.glob(dat_dir+"/*")

c = 0
for i in range(len(files)):
    file_i = files[i]
    base = os.path.basename(file_i)
    splt = os.path.splitext(base)
    base_noext = splt[0].split(".")[0] # extra split just in case
    base_ext = splt[1]

    tmp = base_noext.split("_")
    casename = tmp[0]+"_"+tmp[1][0:2]
    casename.replace(' ', '')


    # if base_ext[-1]
    addon = ''
    cancopy = False

    out_ext = base_ext

    if out_ext == '.gz': # replace .gz
        out_ext = '.nii.gz'

    if out_ext == '.vol':
        # kretz
        addon = ''
        cancopy = True

    if not cancopy and out_ext == '.nii.gz' and "seg" in splt[0]:
        # segmentation
        addon = '_seg'
        cancopy = True
    
    if not cancopy and out_ext == '.nii.gz' and "dp" in splt[0] and "(1)" in splt[0]:
        # power doppler
        addon = '_dp'
        cancopy = True

    if not cancopy and out_ext == '.nii.gz' and "dp" in splt[0] and "(2)" in splt[0]:
        # bmode
        addon = ''
        cancopy = True

    output= out_dir+casename+addon+out_ext

    # shutil.copy(file_i, output)

    # print(file_i)
    # print(output)

    if not cancopy:
        c = c + 1
        print(file_i)
        print(cancopy)
        print(base_noext)
        print(tmp[1])
        print(casename)
        print(output)
        print('\n')

print("couldnt do "+str(c)+" out of "+str(len(files)))