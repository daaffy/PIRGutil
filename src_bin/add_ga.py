'''
    Map the GA from the MRN and add to FMBV spreadsheet.
'''

import pandas as pd

in_xlsx = './files/Welcome Leap Patient Scanning 12052023.xlsx'
in_xlsx = in_xlsx.replace('\\', '/')
ex = pd.read_excel(in_xlsx)

def get_wl_number(input):
    wl = -1
    check = False

    if input[:2] == 'WL':
        check = True
        wl = int(input[2:])

    return wl, check

def get_wl_df():
    wls = []
    gas = []
    all = []
    for i in range(len(ex.columns)):
        col_i = ex.columns[i]
        ga_i = ex.loc[13-2,:].values[i]
        mrn_i = ex.loc[7-2,:].values[i]
        group_i = ex.loc[16-2,:].values[i]
        position_i = ex.loc[23-2,:].values[i]
        
        wl_i, check = get_wl_number(col_i)

        if check:
            wls.append(wl_i)
            gas.append(ga_i)
            all.append([wl_i, mrn_i, ga_i, group_i, position_i, ''])


        # print(ex.columns[i])
        # print(get_wl_number(col_i))
        # print(col_i[:2])

    df = pd.DataFrame(all, columns=['WL', 'MRN' ,'GA', 'GROUP', 'POSITION', 'DEPERSONAL_ID'])

    unique_mrns = df['MRN'].unique().tolist()
    print(unique_mrns)
    for ind, row in df.iterrows():
        # print(row['MRN'])
        # print()
        row['DEPERSONAL_ID'] = unique_mrns.index(row['MRN'])

    return df

if __name__ == "__main__":
    df = get_wl_df()

    print(df)