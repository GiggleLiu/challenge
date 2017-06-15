#-*-coding:utf-8-*-

import pdb,numpy,time
import xlrd

def load_data(sheet=0):
    t0=time.time()
    wb = xlrd.open_workbook("data.xlsx")
    ws = wb.sheet_by_index(which)
    pdb.set_trace()
    data=numpy.array([[col for col in ws.row(irow)] for irow in xrange(ws.nrows)])
    t1=time.time()
    print data,t1-t0
    pdb.set_trace()

test_read()
