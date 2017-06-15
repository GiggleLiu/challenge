#-*-coding:utf-8-*-
import numpy as np
import pdb
from openpyxl import load_workbook

__all__=['load_data']

def load_data(filename,which):
    '''Load data from xlsx file to numpy array.'''
    wb=load_workbook(filename)
    if which==0:
        ws=wb.active
        pdb.set_trace()
    else:
        pdb.set_trace()
    data=np.array([[col.value for col in row] for row in ws.rows])
    return data

load_data('data.xlsx',which=0)
