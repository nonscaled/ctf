#solve brief complex polynomials from the challenge server, with the occasional fork bomb thrown in to avoid passing to eval 
import re
import asyncio


test = '(55+42i) + (12+5i) - (124+15i)'
test2 = '(23+32i) + (3+500i) - (11+44i)'
test = test2

#check for the ol' fork bomb
def clean(t):
    if re.match(r'_',t):
        return False
    return True

#break up the problem and solve it
def solve(tst):
    if clean(tst):
        real = [int(a[1:]) for a in re.findall(r'\([0-9]+',tst)]
        ima = [int(b[:-1]) for b in re.findall(r'[0-9]+i', tst)]
        ops = [o[0] for o in re.findall(r'[\+\-] \(',tst)]
        racc = real[0]
        iacc = ima[0]
        for i in range(len(ops)):
            if ops[i] == '+':
                racc += real[i+1]
                iacc += ima[i+1]
            if ops[i] == '-':
                racc -= real[i+1]
                iacc -= ima[i+1]
        if iacc >= 0:
            return '{}+{}i'.format(racc, iacc)
        else:
            return '{}{}i'.format(racc,iacc)
    return 'fork'

async def connect():
    try:
        ncin, ncout = await asyncio.open_connection('chal.imaginaryctf.org', 42015)
        print('Connection opened.')
        for _ in range(300):
            await ncout.drain()
            b = await ncin.readuntil(b'\n> ')
            equ = b.decode('utf-8').split('\n')[-2]
            #print('Input: ' + equ)
            out = solve(equ)
            print('Output: ' + out)
            ncout.write(bytes(out,'utf-8')+b'\n')
        await ncout.drain()
        print('Calculation done.')
        c = await ncin.readuntil(b'}')
        print (c.decode('utf-8'))
        ncout.close()
        await ncout.wait_closed()
        print('Connection closed.')
    except Exception as ex:
        err = "Exception: {0}\nArgs: {1!r}".format(type(ex).__name__, ex.args)
        print(err)
    
    #print(solve(test))

def main():
    asyncio.run(connect())

main()