#from sage.all import *
import random
import os
import signal
from ecdsa import ellipticcurve
from Crypto.Util.number import getPrime, inverse
from libnum import s2n, n2s

# Setup
FLAG = os.urandom(10) + open('flag.txt', 'rb').read() + os.urandom(10)
assert(len(FLAG) <= 120)
random.seed(s2n(os.urandom(12)))

# EC params
P = 93556643250795678718734474880013829509320385402690660619699653921022012489089
A = 66001598144012865876674115570268990806314506711104521036747533612798434904785
B = 25255205054024371783896605039267101837972419055969636393425590261926131199028
x = 1663255323649316187237502679180020234514169346773977936323045878120391437837
y = 84006750294604478804216697619398950537391904455312244388797990516611936533488
curve = ellipticcurve.CurveFp(P, A, B)
G = ellipticcurve.Point(curve, x, y)
# q = E.base_ring().order()
# n = G.order()
# for k in range(1, 10):
#     assert(power_mod(q, k, n) != 1)
# assert(E.trace_of_frobenius() != 1)

# RSA params
p = getPrime(512)
q = getPrime(512)
e = 0x10001
d = inverse(e, (p-1) * (q-1))
N = p * q
assert(pow(pow(1337, e, N), d, N) == 1337)


def main():
    print("Another RSA machine...")
    x = s2n(random.randbytes(16))
    Gx = G * x
    
    while True:
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Flag")
        
        choice = int(input(">>> "))
        
        if choice == 1:
            pt = bytes.fromhex(input("Plaintext (hex): ").strip())
            pt = s2n(pt)
            ct = pow(pt, e * (pt.bit_length() + 1), N)
            print(n2s(int(ct)).hex())
        if choice == 2:
            ct = bytes.fromhex(input("Ciphertext (hex): ").strip())
            pt = pow(s2n(ct), d, N)          
            y = s2n(random.randbytes(32))
            Gy = G * y * (x + 1)
            res = Gy + Gx * pt
            print(f"({res.x()}, {res.y()})")
        if choice == 3:
            pt = s2n(FLAG)
            ct = pow(pt, e, N)
            print(n2s(int(ct)).hex())
    
    
if __name__ == '__main__':
    try:
        signal.alarm(69)
        main()
    except Exception as e:
        print(e)
        exit(1)
    