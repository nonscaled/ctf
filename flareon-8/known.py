#known plaintext attack on ransomware encryption
from Crypto.Util.Padding import pad
import string
from itertools import permutations, combinations
from binascii import hexlify, unhexlify

#hardcoded vars
FILE_NAME = "./Files/latin_alphabet_u.txt"
ENC_FILE_NAME = "./Files/latin_alphabet.txt.encrypted"
MUT_FILE_NAME = "not yet"
CICERO_ENC = "./Files/cicero.txt.encrypted"
CICERO = "./Files/cicero_u.txt"
PNG = "./Files/capa.png.encrypted"

alpha = string.ascii_uppercase# + string.digits

# critical then context then boilerplate
def xor(x, y):
    return bytes(a ^ b for a, b in zip(x,y))

def xorb(a, b):
    return a ^ b

#ror and rol taken from based aldeid
def rol(inp, bits_to_rotate, max_rot=8):
    return (inp << bits_to_rotate % max_rot) & (2**max_rot-1) | \
    ((inp & (2**max_rot-1)) >> (max_rot - (bits_to_rotate % max_rot)))

def ror(inp, bits_to_rotate, max_rot=8):
    return ((inp & (2**max_rot-1)) >> bits_to_rotate % max_rot) | \
    (inp << (max_rot-(bits_to_rotate % max_rot)) & (2**max_rot-1))

# r and l are bitwise so need to make bytelist -> byte wrapper    
def rolb(x, y):
    c = b''
    for a in x:
        c += rol(a,y).to_bytes(1,'little')
    return c

def rorb(x,y):
    c = b''
    for a in x:
        c += ror(a,y).to_bytes(1,'little')
    return c

#also addition and subtraction need to be bitwise i think?
def badd(i, j):
    c = b''
    for a in i:
        c += ((a + j) % 0xff).to_bytes(1,'little')
    return c

def bsub(i, j):
    c = b''
    for a in i:
        c += ((a - j) % 0xff).to_bytes(1,'little')
    return c

#now the actual decryptor/encryptor
def decryptor(file_char, console_char, i, n=7):
    #i = 0
    #while i <= n:
    

    b = file_char[i] ^ console_char[i]
    c = rol(b,i)
    #file_char = bsub(file_char, i)
    d = (c - i)
    #i += 1 
    return d

def encryptor(file_char, console_char):
    i = 7
    while i >= 0:
        #file_char = badd(file_char, i)
        file_char = (file_char + i) 
        file_char = ror(file_char, i)
        file_char ^= console_char
        i -= 1
    return file_char

def file_reader(blok, console_inp, op='d', bloksize=8, n=7, mut_filename='notyet'):
    #only need one block for now, also skip mutation for just dumping to console
    if op == 'd':
        d = b''
        for i in range(bloksize):
            try:
                #if bloksize != 1:
                    d += decryptor(blok, console_inp, i, n).to_bytes(1, 'little')
                #else:
                #    d += decryptor(blok, console_inp, n).to_bytes(1, 'little')
            except OverflowError:
                d += b'\x00'
        return d
    elif op == 'e':
        e = b''
        for i in range(bloksize):
            if bloksize != 1:
                e += encryptor(blok[i], console_inp[i]).to_bytes(1, 'little')
            else:
                e += encryptor(blok, console_inp).to_bytes(1, 'little')
        return e
    else:
        raise Exception("not enc/dec")

def b(a):
    return a.to_bytes(1,'little')

def console_reader(inp='i'):
    f = open(ENC_FILE_NAME, "rb")
    g = open(FILE_NAME, "rb")
    c_plain = open(CICERO, "rb")
    c_enc = open(CICERO_ENC, "rb")
    p_enc = open(PNG, "rb")

    if inp == 'i':
        line = input("Key to test: ")
        #q = f.read(8)
        #print(hexlify(q))
        #o = file_reader(q,bytes(line,'utf-8'), 'e')
        #print(hexlify(o))
        o = f.read(8)
        p = file_reader(o, bytes(line, 'utf-8'), 'd')
        print(b'decryption: ' + p)
        o = f.read(8)
        p = file_reader(o, bytes(line, 'utf-8'), 'd')
        print(b'decryption: ' + p)
    if inp == 'b':
        #hellcode, doesn't really work as state space isn't reduced w/o certain plaintext
        by = bytes(range(0x7F))
        bloksize = 8
        #f.read(8)
        #f.read(8)
        u = f.read(bloksize)
        print(u)
        #print(bytes(alpha, 'utf-8'))
        # ABCDEFG\x00
        # 8: 01 8b ed (assuming 0x00: = 4 A)
        # 7: & /
        # 6: 5 D
        # 5:
        # 4:
        # 3:
        # 2:
        # 1:
        #
        #
        # final1 = b'xsQ"L5&\x01'
        # try2 = b'\mA'
        z = b'OGVGmJfBHqtJwTjh'
        zz = b'fdVtFGFizIgtWZTGnaLJ'
        zzz = b'DELT'
        zzzz = b'DYTENXKFRECGS' # FK
        zzzzz = b'CEP'
        bbeta = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        #for w in bbeta:
        for x in bbeta:
            for y in bbeta:
                for i in bbeta:
                    i = i.to_bytes(1, 'little')
                    i = b''.join([b'A']*2) + i + b(y) + b(x) + b'aj='
                    assert(len(i) == bloksize)
                    fr = file_reader(u,i,'d',bloksize, bloksize-1)
                    if b(fr[-1]) == b'\x00' and (b(fr[-2]) == b'T') and (b(fr[-3]) == b'I') and (b(fr[-4]) == b'E') \
                        and (b(fr[-5]) in bytes(alpha,'utf-8')) and (b(fr[-6]) in bytes(alpha,'utf-8')): #and (b(fr[-7]) in bytes(alpha,'utf-8')):# and (b(fr[-8]) in bytes(alpha,'utf-8')):

                        print(i + b' ' + fr)
    if inp == 'c':
        #more confident in cicero plaintext, now that i've found it
        #nvm haven't found it ig
        ptxt = c_plain.read(32)
        ctxt = c_enc.read(32)
        print("Checking Cicero")
        f = 0
        for i in bytes(range(0xFF)):
            key = b(i) + b''.join([b'C']*7)
            res = file_reader(ptxt[f:f+8], key,'e')
            #res2 = file_reader(res,key,'d')
            #print(ptxt[8:16])
            if res[f+8] == ctxt[f+8]:
                print(key + b'  ' + res + b'  ' + ptxt[f:f+8] + b'  ' + ctxt[f:f+8]) 
    if inp == 'p':
        #png file header 8 bytes baby dat twitter osint
        #this f*cking worked jesus f*ck holy sh*t absolutely wasting my time i legit despise this location the decryptor was even wrong the whole time and i just let it happen
        ptxt = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
        ctxt = p_enc.read(8)
        print("Checking pingas")
        n=0
        g=b''
        while n < 8:
            for i in bytes(range(0xFF)):
                key = g + b(i) + b''.join([b'A']*(7-n))
                res = file_reader(ctxt, key,'d')
                #res2 = file_reader(res,key,'d')
                #print(ptxt[8:16])
                if res[n] == ptxt[n]:
                    print(key + b'  ' + res + b'  ' + ptxt + b'  ' + ctxt) 
                    g += b(key[n])
                    n += 1


    else:  
        #line = "ffffffffffffffff"
        #inp_blok = unhexlify(line)[:8]
        #inp_blok = bytes(line,'utf-8')[:8]
        #print(hexlify(f.read(8)))
        j = 0
        while j < 3:
            h = f.read(8)
            inp_blok = g.read(8)
            print(hexlify(h))
            print(hexlify(inp_blok))
            #fr = file_reader(h, inp_blok, 'e')
            #print(hexlify(fr))
            fg = file_reader(h, inp_blok , 'd')
            print(hexlify(fg))
            print('\n')
            j += 1

def main():
    console_reader('p')

main()







#assuming latin alphabet is uppercase, key would be 

# 0f -> 07 -> 1F is +8 each time