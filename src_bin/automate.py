'''
        automate.py
    Batch FMBV consists of multiple steps in series (see README.txt). This script is an attempt to pull together
    these separate parts into one process.

    Anticipating the need to run these scripts from the shell (e.g., on Katana) we will allow for the possibility
    of entering parameters as arguments.

    * Mount the research drive prior to running.
'''

import os, sys
import to_csv
import pandas as pd
import logging

sys.path.insert(1, "/Users/jackh/Documents/FMBV_2023/gordon_original/")
sys.path.insert(1, "/Users/jackh/Documents/FMBV_2023/gordon_original/src/")
import load

# Session specific parameters
session_name = "18_03_2024"
prev_session_name = ""

# Hardcoded parameters
INPUT_ROOT = "/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/"
EXPORT_ROOT = "/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Data Analysis/GABY FMBV DATA/"

BRAIN_PATH = INPUT_ROOT + "Brain/"

# Derived
SESSION_PATH = EXPORT_ROOT + session_name + "/"
LOG_PATH = SESSION_PATH+"/logs/"

class Organ():

    def __init__(
            self, 
            NAME,
            VOL_PATH='',
            PD_PATH='',
            SEG_PATH='',
            LOG_PATH=''):
        self.NAME = NAME
        self.VOL_PATH = VOL_PATH
        self.PD_PATH = PD_PATH
        self.SEG_PATH = SEG_PATH

        self.LOG_PATH = LOG_PATH

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=self.LOG_PATH+"/"+self.NAME+"_log.txt", encoding='utf-8', level=logging.DEBUG)

        self.logger.debug("Creating "+self.NAME+" organ.")
        print("Creating "+self.NAME+" organ.")

        # checks...

    def build_index(self):
        print("Building "+self.NAME+" index.")
        self.index_df, self.total_df, self.index_notices = to_csv.build_index(self.VOL_PATH, self.PD_PATH, self.SEG_PATH)

        print(self.index_df)

        if not self.LOG_PATH == '':
            print("Index to .csv...")
            self.index_df.to_csv(LOG_PATH+self.NAME+"_index.csv", index=False)
            self.total_df.to_csv(LOG_PATH+self.NAME+"_total_index.csv", index=False)
            self.list_to_file(LOG_PATH+self.NAME+"_index_notices.txt", self.index_notices)

    def mask_from_prev_session(self, prev_session_results=None):
        self.masked_index_df = self.index_df

        if prev_session_results == None:
            return

        if isinstance(prev_session_results, str):
            prev_df = pd.read_csv(prev_session_results)
            self.logger.debug("Masking index against file "+prev_session_results)
        
        drop_ind = []
        for i, row in self.index_df.iterrows():
            # print(sum(prev_df['kretzpath'].values == row['kretzpath']) == 1)
            if (sum(prev_df['kretzpath'].values == row['kretzpath']) == 1):
                drop_ind.append(i)

        self.masked_index_df = self.masked_index_df.drop(drop_ind, axis=0)

        self.logger.debug(str(len(self.masked_index_df))+" cases remain to be run!")
        self.logger.debug(self.masked_index_df)

        if not self.LOG_PATH == '':
            self.MASKED_PATH = LOG_PATH+self.NAME+"_masked_index.csv"
            self.masked_index_df.to_csv(self.MASKED_PATH, index=False)

    def safe_run(self):
        ''' 
            TO-DO:
        - Add parameter hardcodes
        - Log verbose to logger.
        - Use dataframe as input.
        '''
        load.run(self.MASKED_PATH, output_path=LOG_PATH+self.NAME+"_output_"+session_name+".csv", mode=1, verbose=True, mm = True, zoom = 0.5, start = 0)

        
    def list_to_file(self, path, list):
        with open(path, 'w') as fp:
            for item in list:
                # write each item on a new line
                fp.write("%s\n" % item)


if __name__ == "__main__":
    print(" -------------------------------------------------------------------------------------")
    print("automate.py...")

    # Repeat parameter values...

    # New case?
    if not os.path.isdir(SESSION_PATH):
        print("Session does not exist. Creating...")
        # create directories (/logs, /index, /results)
        os.mkdir(SESSION_PATH)
        os.mkdir(LOG_PATH)
        os.mkdir(SESSION_PATH+"/results")
    else:
        print("Session already created.")

    # * Do brain first (turn into a function)...
    brain = Organ("BRAIN",VOL_PATH=BRAIN_PATH,PD_PATH=BRAIN_PATH,SEG_PATH=BRAIN_PATH,LOG_PATH=LOG_PATH)
    
    # create index file
    brain.build_index() # log which files do not match (vol, pd, seg) for sam [total_index, might need better formatting]

    # create mask file to indicate which files to run (based on prev session for example or manual indication)
    # figure out how to drop
    PREV_PATH = "/Volumes/PIRG_Research/Wellcome Leap/Brain Kidney Liver Volumes/Data Analysis/GABY FMBV DATA/20_02_2024/"
    brain.mask_from_prev_session(PREV_PATH+"output_brain_20022024.csv")
    
    # Run FMBV on new index file
    brain.safe_run()

    # Reorder file appropriately 




