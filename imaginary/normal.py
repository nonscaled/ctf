#exercise in processing Verilog logic with contraint solvers
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

    
    

def main():
    print(normalz())
    #then int.to_bytes(32,'big')

main()