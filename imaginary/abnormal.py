#more constraint solving on verilog constants
import sys
from z3 import *

s = Solver()

def nor(b,c):
    a = (b | c) ^ 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    return a

def normal():
    c1 = 0x44940e8301e14fb33ba0da63cd5d2739ad079d571d9f5b987a1c3db2b60c92a3
    c2 = 0xd208851a855f817d9b3744bd03fdacae61a70c9b953fca57f78e9d2379814c21
    flag = 0x696374667b00000000000000000000000000000000000000000000000000007d
    #w1, w2, w3, w4, w5, w6, w7, w8, out = b''
    

    w1 = nor(flag, c1)
    w2 = nor(flag, w1)
    w3 = nor(c1, w1)
    w4 = nor(w2, w3)
    w5 = nor(w4, w4)
    w6 = nor(w5, c2)
    w7 = nor(w5, w6)
    w8 = nor(c2, w6)
    out = nor(w7, w8)
    return out

def norz(b,c):
    f = BitVecVal(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 256)
    a = (b | c) ^ f
    return a

def normalz():
    #may skip using norz b/c not sure if z3 can reach inside py funcs
    #but try it first
    flag = BitVec('flag', 256)
    c1 = BitVecVal(0x44940e8301e14fb33ba0da63cd5d2739ad079d571d9f5b987a1c3db2b60c92a3,256)
    c2 = BitVecVal(0xd208851a855f817d9b3744bd03fdacae61a70c9b953fca57f78e9d2379814c21,256) 
    
    w1 = norz(flag, c1)
    w2 = norz(flag, w1)
    w3 = norz(c1, w1)
    w4 = norz(w2, w3)
    w5 = norz(w4, w4)
    w6 = norz(w5, c2)
    w7 = norz(w5, w6)
    w8 = norz(c2, w6)
    out = norz(w7, w8)

    s.add(out == 0)
    stat = s.check()
    assert stat.r == 1
    return s.model()


#note: BitVecVal(int(bin(a)[2+i:j],2), j-i) gets sub bitvec of bvv
#may only need to be bitvec as callstack is being popped? 
#so not necessary to go in and out of bitvec type, just pass length through the nor funcs and set it at the end
#nvm flag is taken in, but z3 should?? be able to handle it, find out
#got the interface wrong, s/bin(a)[2+i:j]/a.get_binary_string()[i:j]
#but python int can be assigned to Int() so try that interface instead
#or im completetly misunderstanding how z3 works


# bitvecval -> bitvecval[i:j]
def subbv(a, i, j=0):
    a = BitVecVal()
    if j == 0:
        j = i+1
    return BitVecVal(int(a.as_binary_string()[i:j],2), j-i) 

# [bitvecval ... bitvecval] -> bitvecval
def catbv(a):
    b = ''
    for bvv in a:
        b += bvv.as_binary_string()
    return BitVecVal(int(b,2), len(b))


def noraz(o,i):
    pass

def abnormal():
    d1 = BitVec('d1',16)
    d2 = BitVec('d2',256)
    s.add(d2 == 0xd208851a855f817d9b3744bd03fdacae61a70c9b953fca57f78e9d2379814c21)
    wtest = norz(subbv(d2,0,16), d1)
    s.add(wtest == 0)
    print(s.check().r)

def main():
    abnormal()
    #then int.to_bytes(32,'big')

main()