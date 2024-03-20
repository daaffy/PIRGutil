'''
    to_csv.py
Tool for sorting all cases in a directory to an appropriate .csv file to be read by FMBV GUI.

J. Hills
'''

import os, glob, re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QErrorMessage

# Hardcoded .csv column names
INDEX_COL_NAME = "index"
VOL_COL_NAME = "kretzpath"
PD_COL_NAME = "dopplerpath"
SEG_COL_NAME = "segpath"

# Hardcoded file tags
VOL_TAG = ".vol"
PD_TAG = "_dp.nii.gz"
SEG_TAG = "_seg.nii.gz"

VOL_CASE = {"name": "VOL", "tag": VOL_TAG, "col": VOL_COL_NAME}
PD_CASE = {"name": "PD", "tag": PD_TAG, "col": PD_COL_NAME}
SEG_CASE = {"name": "SEG", "tag": SEG_TAG, "col": SEG_COL_NAME}

PER_TAG = "PER"
CI_TAG = "CI"

# print(look_dir)

def collect(PATH, FILE_CASE):
    notice_log = ['Begin '+FILE_CASE["name"] +' index notices...']
    dat = []

    ext_tag = FILE_CASE["tag"]
    col_name = FILE_CASE["col"]

    all = glob.glob(PATH+"/*"+ext_tag)
    for i in range(len(all)):
        curr_path = all[i]
        curr_filename = os.path.basename(curr_path).split('/')[-1]
        # curr_no_ext = curr_filename.split('.')[0]

        nums = [int(s) for s in re.findall(r'\d+', curr_filename)]
        
        wl = 0
        scan = 0

        do_append = True
        
        if len(nums) == 1:
            wl = nums[0]
            scan = 1 
            notice_log.append("[NAMING CONVENTION] "+curr_filename+" has number content = 1. WL is set to number and SCAN is set to 1.")
        elif len(nums) == 2:
            wl = nums[0]
            scan = nums[1]
        elif len(nums) == 3:
            wl = nums[0]
            scan = nums[-1]
            notice_log.append("[NAMING CONVENTION] "+curr_filename+" has number content = 3. WL is first number and SCAN is last number.")
        else:
            notice_log.append("[NAMING CONVENTION] "+curr_filename+" has unclassified number content. FILE WILL BE IGNORED.")
            do_append = True # keep true for now just in case...

        if do_append:
            dat.append([wl, scan, curr_path])
    
    df = pd.DataFrame(dat, columns=['WL', 'SCAN', col_name])

    # print(df)

    return df, notice_log
        
def build_index(VOL_PATH, PD_PATH, SEG_PATH, LOG_PATH=''):
    '''
        build_index
    Creates an index data frame and various logs for batch system diagnostics.

    TO-DO:
    - Look for copies and log, since these copies automatically get dropped it would nice to know which ones are ignored.
    - Pass logger into the method and add debug messages.
    '''

    vol_dat = []
    dat = []

    vol_df, vol_notice_log = collect(VOL_PATH, VOL_CASE)
    pd_df, pd_notice_log = collect(PD_PATH, PD_CASE)
    seg_df, seg_notice_log = collect(SEG_PATH, SEG_CASE)

    # m = pd.merge(pd.merge(vol_df,pd_df,on='no_ext'),seg_df,on='no_ext')
    index = pd.merge(pd.merge(vol_df,pd_df,on=['WL', 'SCAN']),seg_df, on=['WL','SCAN'])
    total = pd.merge(pd.merge(vol_df,pd_df, on=['WL', 'SCAN'], how='outer'),seg_df, on=['WL', 'SCAN'], how='outer')
    # print(index)

    index = index.sort_values(by=['WL', 'SCAN'])
    total = total.sort_values(by=['WL', 'SCAN'])

    index.drop_duplicates(subset=['WL','SCAN'], inplace=True)

    notice_log = sum([vol_notice_log, pd_notice_log, seg_notice_log], [])

    return index, total, notice_log

    c = 0
    all_vols = glob.glob(VOL_PATH+"/*"+VOL_TAG)
    for i in range(len(all_vols)):
        # proceed = True

        # Build expected file paths to look for.
        curr_vol = all_vols[i]
        noext = os.path.splitext(curr_vol)[0]
        curr_pd = noext+PD_TAG
        curr_seg = noext+SEG_TAG

        # for placental (divide CI and PER)
        # if CI_TAG in curr_vol: # activate to obtain PER
        #     continue

        # if PER_TAG in curr_vol: # activate to obtain CI
        #     continue

        # Check that files exist.
        if not os.path.isfile(curr_pd):
            proceed = False
            print("The .vol file "+curr_vol+" exists, but the power Doppler file "+curr_pd+" does not exist!")
            curr_pd = ''

        if not os.path.isfile(curr_seg):
            proceed = False
            print("The .vol file "+curr_vol+" exists, but the segmentation file "+curr_seg+" does not exist!")
            curr_seg = ''

        # if not proceed:
        #     print("Skipping "+curr_vol+"...\n")
        #     continue
        
        # Add files to list
        dat.append([c, curr_vol, curr_pd, curr_seg])
        c = c + 1
    
    dat_df = pd.DataFrame(dat, columns = [INDEX_COL_NAME,
        VOL_COL_NAME,
        PD_COL_NAME,
        SEG_COL_NAME])
    
    return dat_df

# # temp: check leftoever segs
# l_segs = []
# all_segs = glob.glob(look_dir+"/*seg*")
# for i in range(len(all_segs)):
#     if not all_segs[i] in dat_df[SEG_COL_NAME].values:
#         l_segs.append(all_segs[i])

# print(l_segs)

# out_path = "C:/MyProjects/FMBV/gui/test/"+"test_input.csv"


if __name__ == "__main__":
    print(" -------------------------------------------------------------------------------------")
    print("to_csv.py...")
    root = tk.Tk()
    root.withdraw()
    # look_dir = "C:/MyProjects/FMBV/gui/test/"
    look_dir = filedialog.askdirectory()

    dat_df = build_index(look_dir, look_dir, look_dir)

    out_path = filedialog.asksaveasfile(defaultextension=".csv").name
    print("Exporting to "+out_path)
    dat_df.to_csv(out_path, index = False)

    

