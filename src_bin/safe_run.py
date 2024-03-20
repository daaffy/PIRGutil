import sys
sys.path.insert(1, "/Users/jackh/Documents/FMBV_2023/gordon_original/")
sys.path.insert(1, "/Users/jackh/Documents/FMBV_2023/gordon_original/src/")


import fmbv_functions
import pandas as pd
import fmbv_refactor as fmbv
import load

# Hardcoded .csv column names
INDEX_COL_NAME = "index"
VOL_COL_NAME = "kretzpath"
PD_COL_NAME = "dopplerpath"
SEG_COL_NAME = "segpath"

# base = '/Volumes/PIRG_Research/Wellcome Leap/Sphere placenta segmentations/'
base = "/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Liver/"
# base = "/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Brain/"
# base = "/Volumes/PIRG_Research/Wellcome Leap/Placental Studies/segmented placentas/"
# base = "/Volumes/PIRG_Research/Wellcome Leap/Sphere Placental Segementations Renamed/"

input_path = base+"input.csv"
output_path = base+"output_20022024_3.csv"

# input_df = pd.read_csv(input_path)

# for ind, row in input_df.iterrows():
#     vol_path = row[VOL_COL_NAME]
#     pd_path = row[PD_COL_NAME]
#     seg_path = row[SEG_COL_NAME]
#     print(pd_path)

#     f = fmbv.FMBV(verbose = True)
#     f.load_pd(pd_path)
#     f.load_seg(seg_path)
#     f.load_kretz(vol_path)

#     f.global_method()

#     break

# fmbv_functions.run(input_path, output_path=output_path, verbose=True)
load.run(input_path, output_path=output_path, mode=1, verbose=True, mm = True, zoom = 0.5, start = 34)




