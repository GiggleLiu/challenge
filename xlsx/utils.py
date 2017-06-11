import numpy as np
from openpyxl import load_workbook

__all__=['load_data']

def load_data(filename):
    '''Load data from xlsx file to numpy array.'''
    wb=load_workbook(filename)
    ws=wb.active
    data=np.array([[col.value for col in row] for row in ws.rows])
    return data
