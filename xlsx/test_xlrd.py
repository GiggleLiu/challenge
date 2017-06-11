#-*-coding:utf-8-*-

import pdb,numpy,time
import xlrd

def test_read():
    t0=time.time()
    wb = xlrd.open_workbook("sample.xlsx")
    ws = wb.sheet_by_index(0)
    data=numpy.array([[col for col in ws.row(irow)] for irow in xrange(ws.nrows)])
    t1=time.time()
    print data,t1-t0
    pdb.set_trace()

test_read()
