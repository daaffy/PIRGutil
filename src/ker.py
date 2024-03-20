
'''
    ker.py

This kernel maintains the research data pipeline as a whole.

It is designed to be run periodically, hopefully on an external system (e.g., Katana).
'''

from organ import Organ

METHOD_ID = 'fmbv_20022024'

temp_org = Organ(
    NAME = "Temp",
    METHOD_ID=METHOD_ID
)

