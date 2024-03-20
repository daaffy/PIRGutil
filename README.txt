## PIRGutil
Some useful programs for the PIRG team.

## Install Overview

git clone
cd 
pip install virtualenv
python -m virtualenv venv
cd venv/Scripts
./activate
pip install -r requirements.txt

## Example Procedure
1. to_csv.py to create input.csv file for a large batch of files.
2. safe_run.py to run a batch FMBV on the files supplied in input.csv.
3. reorder.py to order output.csv according to WL scan number and add the gestational ages.