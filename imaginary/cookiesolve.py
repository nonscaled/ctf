#insecure web-based cryptosystem
import requests
from binascii import hexlify, unhexlify
from Crypto.Util.Padding import pad, unpad
#import asyncio


def xorb(a, b, c):
    a = bin(int(a, 16))[2:]
    b = bin(int(b, 16))[2:]
    c = bin(int(c, 16))[2:]
    xor1 = ''.join([str(int(a[i-1]) ^ int(b[i-1])) for i in range(len(a))])
    xor2 = ''.join([str(int(xor1[i-1]) ^ int(c[i-1])) for i in range(len(c))])
    print(a)
    print(b)
    print(xor1)
    print(xor2)
    return int(xor2, 2).to_bytes((len(xor2) + 7 ) // 8, byteorder='big') 

def cookiesolve():
    username = pad('firepwny'.encode(), 16).hex()
    admin_username = pad('admin'.encode(), 16).hex()
    auth = 'a64fe4cb8c85d2d23d416bedb2953c7447df2112c0c59c0c'
    nonce = unhexlify(auth[:16])
    ctext1 = unhexlify(auth[16:]).hex()
    ptext1 = username
    ptext2 = admin_username
    #print(bin(int(ctext1, 16))[2:])
    #print(ptext1)
    #print(ptext2)
    print(nonce)
    admin_auth = hexlify(nonce) + hexlify(xorb(ctext1, ptext1, ptext2))

    #admin_auth = hexlify(nonce) + hexlify()
    print(admin_auth)

def main():
    cookiesolve()

main()