'''
    to_csv.py
Tool for sorting all cases in a directory to an appropriate .csv file to be read by FMBV GUI.

J. Hills
'''

import os, glob
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

print(" -------------------------------------------------------------------------------------")
print("to_csv.py...")
root = tk.Tk()
root.withdraw()
# look_dir = "C:/MyProjects/FMBV/gui/test/"
look_dir = filedialog.askdirectory()
# print(look_dir)

dat = []

c = 0
all_vols = glob.glob(look_dir+"/*"+VOL_TAG)
for i in range(len(all_vols)):
    proceed = True

    # Build expected file paths to look for.
    curr_vol = all_vols[i]
    noext = os.path.splitext(curr_vol)[0]
    curr_pd = noext+PD_TAG
    curr_seg = noext+SEG_TAG

    # Check that files exist.
    if not os.path.isfile(curr_pd):
        proceed = False
        print("The .vol file "+curr_vol+" exists, but the power Doppler file "+curr_pd+" does not exist!")

    if not os.path.isfile(curr_seg):
        proceed = False
        print("The .vol file "+curr_vol+" exists, but the segmentation file "+curr_seg+" does not exist!")

    if not proceed:
        print("Skipping "+curr_vol+"...\n")
        continue
    
    # Add files to list
    dat.append([c, curr_vol, curr_pd, curr_seg])
    c = c + 1
    
dat_df = pd.DataFrame(dat, columns = [INDEX_COL_NAME,
    VOL_COL_NAME,
    PD_COL_NAME,
    SEG_COL_NAME])

# out_path = "C:/MyProjects/FMBV/gui/test/"+"test_input.csv"
out_path = filedialog.asksaveasfile(defaultextension=".csv").name
print("Exporting to "+out_path)
dat_df.to_csv(out_path, index = False)

    

