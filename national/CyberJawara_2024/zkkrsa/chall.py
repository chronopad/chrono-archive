from sympy.crypto import *
from Crypto.Util.number import getPrime
from libnum import n2s, s2n
import signal

FLAG = open('flag.txt', 'rb').read()

params = [getPrime(1024) for _ in range(3)] + [s2n(FLAG)]
pub = kid_rsa_public_key(*params)

a, b, A, B = params
M = a*b - 1
e = A*M + a 
d = B*M + b 
n = (e*d - 1) // M 

print(e.bit_length())
print(d.bit_length())
print(n.bit_length())
print(M.bit_length())

def main():
    print("--------Another baby RSA--------")
    print("1. Encrypt")
    print("2. Decrypt")
    print("--------------------------------")
    
    choice = int(input(">>> "))
    if choice == 1:
        pt = bytes.fromhex(input("Data: "))
        pt = s2n(pt)
        ct = pt
        for _ in range(pt.bit_length() + 1):
            ct = encipher_kid_rsa(ct, pub)
        print(f"Result: {n2s(ct).hex()}")
    # elif choice == 2:
    #     ct = bytes.fromhex(input("Data: "))
    #     ct = s2n(ct)
    #     pt: int = decipher_kid_rsa(ct, priv)
    #     print(f"Result: {n2s(pt).hex()}")
    else: raise NotImplementedError()
    
if __name__ == '__main__':
    signal.alarm(120)
    try:
        while True: main()
    except:
        exit(1)