'''
    reorder.py
Reorder a WL output .csv.

This version uses suggestions from Gaby regarding the formatting.

To be worked into the to_csv.py process...

J. Hills
'''

import pandas as pd
import os, re
from add_ga import get_wl_df
import numpy as np

PATH_COL= "kretzpath"
TAG1 = "WL"
TAG2 = "IMG"

def reorderWL(df):
    '''
        reorderWL
    Reorder a DataFrame of WL paths. 

    File names have generally variable structure e.g.,
    - WL97Kidney_3.vol
    - wl19_6.vol
    - WL38_KIDNEY_2.vol
    - ...

    We take the first appearing number to be the Wellcome Leap patient ID.
    We take the second appearing number to be the scan number for a particular patient.
    Rows are ordered accordingly.
    '''

    tags1, tags2 = [], []
    for i in range(len(df)):
        path = df[PATH_COL][i]
        try:
            tag1, tag2 = get_WL_tags(path)
        except:
            print("Could not extract WL tags from path "+path)
            tag1 = -1
            tag2 = -1

        tags1.append(tag1)
        tags2.append(tag2)

    df[TAG1] = tags1
    df[TAG2] = tags2

    df = df.sort_values(by=[TAG1, TAG2])

    return df

def get_WL_tags(path):
    path = path.replace('\\', '/')
    basename = os.path.basename(path)
    extract_nums = re.findall(r'\d+', basename)

    return int(extract_nums[0]), int(extract_nums[-1])

if __name__ == "__main__":
    
    # in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Brain/output.csv'
    # in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Brain/output.csv'
    # in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Data Analysis/GABY FMBV DATA/20_02_2024/brain_raw.csv'
    in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Data Analysis/GABY FMBV DATA/20_02_2024/output_liver_20022024.csv'
    # in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Kidney/output.csv'
    # in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Sphere placenta segmentations/output.csv'

    
    in_csv = in_csv.replace('\\', '/')

    # out_csv = os.path.dirname(in_csv)+"/output_reordered_new.csv"

    df = pd.read_csv(in_csv)

    df_reordered = reorderWL(df)

    wl_df = get_wl_df()

    gas = []
    for ind, row in df_reordered.iterrows():
        wl_ind = row[TAG1]
        try:
            ga = wl_df["GA"][wl_df["WL"] == int(wl_ind)].values[0]
        except:
            0
        # print(ga.values[0])
        gas.append(ga)

    df_reordered["GA"] = gas

    print(df_reordered)

    # df_reordered.to_csv(out_csv, index = False)
    # print(out_csv)

    # alter formatting to row per WL number
    # add patient ID
    df_final = pd.DataFrame()
    wl_numbers = df_reordered["WL"].unique()
    
    for wl in range(1, np.max(wl_df["WL"])+1):
        try:
            df_sub = df_reordered[df_reordered["WL"] == wl]

            # df_final.at[wl,"kretzpath"] = df_sub["kretzpath"].iloc(0)
            df_final.at[wl,"WL"] = int(wl)
            df_final.at[wl,"ID"] = wl_df["DEPERSONAL_ID"][wl_df["WL"] == int(wl)].values[0]
            df_final.at[wl,"GA"] = wl_df["GA"][wl_df["WL"] == int(wl)].values[0]
            df_final.at[wl,"GROUP"] = wl_df["GROUP"][wl_df["WL"] == int(wl)].values[0]
            df_final.at[wl,"POSITION"] = wl_df["POSITION"][wl_df["WL"] == int(wl)].values[0]
        except:
            continue
        
        # print(wl_numbers)
        # print(wl)
        # print(wl_df["WL"][wl_df["WL"] == int(wl)].values[0])
        # df_final.at[wl,"kretzpath"] = df_sub["kretzpath"].iloc[0]
        # df_final.at[wl,"dopplerpath"] = df_sub["dopplerpath"].iloc[0]

        if wl in wl_numbers: 

            for i in range(3):
                kretz_path = ''
                doppler_path = ''
                seg_path = ''
                fmbv = np.nan
                mpi = np.nan
                fmbv_dc = np.nan
                volume_mm3 = np.nan
                start_mm = np.nan
                end_mm = np.nan


                if i < len(df_sub):
                    kretz_path = df_sub["kretzpath"].iloc[i]
                    doppler_path = df_sub["dopplerpath"].iloc[i]
                    seg_path = df_sub["segpath"].iloc[i]
                    fmbv = df_sub["FMBV"].iloc[i]
                    mpi = df_sub["MPI"].iloc[i]
                    fmbv_dc = df_sub["FMBV Depth Corrected"].iloc[i]
                    # fmbv_dc = df_sub["FMBV_DD"].iloc[i]
                    

                    try:
                        volume_mm3 = df_sub["volume_mm3"].iloc[i]
                        start_mm = df_sub["start_mm"].iloc[i]
                        end_mm = df_sub["end_mm"].iloc[i]
                    except:
                        volume_mm3 = np.nan
                    
                df_final.at[wl,"kretzpath_"+str(i+1)] = kretz_path
                df_final.at[wl,"dopplerpath_"+str(i+1)] = doppler_path
                df_final.at[wl,"segpath_"+str(i+1)] = seg_path
                df_final.at[wl,"FMBV_"+str(i+1)] = fmbv
                df_final.at[wl,"MPI_"+str(i+1)] = mpi
                df_final.at[wl,"FMBV-DC_"+str(i+1)] = fmbv_dc
                df_final.at[wl,"volume-mm3_"+str(i+1)] = volume_mm3
                df_final.at[wl,"start-mm_"+str(i+1)] = start_mm
                df_final.at[wl,"end-mm_"+str(i+1)] = end_mm
            


            # df_sub["kretzpath"].iloc(0)
            print(df_sub)

    # tup = []
    # for c in df_final.columns:
    #     spl = c.split('_')
    #     if len(spl) > 1:
    #         tup.append((spl[0], spl[1]))
    #     else:
    #         tup.append(('',spl[0]))

    # df_final.columns = pd.MultiIndex.from_tuples(tup)
    # # print(wl_numbers)
    # print(df_final)
    df_final.to_csv('test_final.csv', index = False)
    

    



    