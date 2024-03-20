'''
    reorder.py
Reorder a WL output .csv.

To be worked into the to_csv.py process...

J. Hills
'''

import pandas as pd
import os, re
from add_ga import get_wl_df

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
    in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Liver/output_temp.csv'
    # in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Kidney/output.csv'
    # in_csv = '/Volumes/PIRG_Research/Wellcome Leap/Sphere placenta segmentations/output.csv'

    
    in_csv = in_csv.replace('\\', '/')

    out_csv = os.path.dirname(in_csv)+"/output_reordered_new.csv"

    df = pd.read_csv(in_csv)

    df_reordered = reorderWL(df)

    wl_df = get_wl_df()

    gas = []
    for ind, row in df_reordered.iterrows():
        wl_ind = row[TAG1]
        ga = wl_df["GA"][wl_df["WL"] == int(wl_ind)].values[0]
        # print(ga.values[0])
        gas.append(ga)

    df_reordered["GA"] = gas

    print(df_reordered)

    df_reordered.to_csv(out_csv, index = False)
    print(out_csv)
    



    