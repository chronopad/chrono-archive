from Crypto.Util.number import *

flag = open('flag.txt', 'rb').read()
hbits = 543
pbits = 468
p = getPrime(1024)
q = getPrime(1024)
n = p*q
c = pow(bytes_to_long(flag), 65537, n)
tot = (p-1) * (q-1)
d = int(pow(65537, -1, tot))
dinv = int(pow(d, -1, n))

h = int(dinv >> hbits)
hp = (int(p & (2**pbits - 1)))

with open('out.txt', 'w+') as f:
    f.write(f'{n=}\n')
    f.write(f'{h=}\n')
    f.write(f'{hp=}\n')
    f.write(f'{c=}\n')
