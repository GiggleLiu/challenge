#-*-coding:utf-8-*-
import numpy as np
import pdb

__all__=['get_testcase']

def get_testcase(which=0):
    if which==1:
        return _load_test_data(which)
    elif which==2:
        maxmin=np.loadtxt('maxmin1000.dat',dtype='int32')
        p0=np.loadtxt('p01000.dat',dtype='int32')
        table=np.loadtxt('table1000.dat',dtype='int32')
        return maxmin[:,0],maxmin[:,1],table,p0
    node_min=[10,5,-5,15,5,5,-5,-5,-5]
    node_max=[20,20,10,25,20,20,20,10,15]
    route_table=[[0,4,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [2,4,6],
            [0,1,2],
            [3,4,5],
            [6,7,8]]
    p0=[5,6,15,5,-15,8,4,-10]

    table=np.zeros([len(node_min),len(route_table)],dtype='int32')
    for i in xrange(len(route_table)):
        table[route_table[i],i]=1
    return node_min,node_max,table,p0

def _load_test_data(sheet=1):
    wb = xlrd.open_workbook("data2.xlsx")
    ws = wb.sheet_by_index(sheet)
    #pl=np.array([cell.value for cell in ws.row(1)[3:]])
    minmax=[cell.value.strip('[]').split(',') for cell in ws.col(1)[2:]]
    minval=np.array([int(val[0]) for val in minmax],dtype='int32')
    maxval=np.array([int(val[1]) for val in minmax],dtype='int32')
    data=np.array([[1 if col.value else 0 for col in ws.row(irow)[3:]] for irow in xrange(2,ws.nrows)],dtype='int32')
    data_val=np.array([[col.value if col.value else 0 for col in ws.row(irow)[3:]] for irow in xrange(2,ws.nrows)],dtype='int32')
    max_row=np.argmax(abs(data_val),axis=0)
    pl=data_val[max_row,np.arange(data_val.shape[1])]
    return minval,maxcal,data,pl


