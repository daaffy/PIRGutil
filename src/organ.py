
class Organ():

    def __init__(self, NAME, METHOD_ID):
        '''
            Each organ is a data analysis case that uses similar internal methods.

            Running an organ case consists of the following operations:
            - Use METHOD_ID to sort data. If FMBV method is updated METHOD_ID must be updated and the data must be separated.
            - Check which scans need to be run against a running ledger.
            - Run scans to obtain new FMBV.
            - Add new FMBV to ledger.
            - Export a new reordered/reformatted results batch.
        '''
        
        self.NAME = ''
        self.METHOD_ID = ''

        # HARDCODED
        # sub-directories names.
        self.DATA = 'data'
        self.LOGS = 'logs'
        self.RESULTS = 'results'

        # misc.
        self.LEDGER = 'ledger'