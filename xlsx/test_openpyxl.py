#-*-coding:utf-8-*-

import pdb,numpy,time
from utils import load_data

def test_read():
    t0=time.time()
    data=load_data('sample.xlsx')
    t1=time.time()
    print data,t1-t0
    pdb.set_trace()

test_read()
