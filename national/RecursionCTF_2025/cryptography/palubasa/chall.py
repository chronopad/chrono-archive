from Crypto.Util.number import getRandomRange
import ecdsa
import hashlib
import string
import signal

FLAG = open("flag.txt", "rb").read().strip()

E = ecdsa.curves.SECP256k1
g = E.generator * 246
n = E.order
p = E.curve.p()

def keygen():
    x = getRandomRange(1, n - 1)
    y = g * -x
    return x, y

def sign(x, m: bytes):
    k = ecdsa.rfc6979.generate_k(g.x(), x % g.x(), hashlib.sha512, m) * p % n
    r = g * k
    r = r.x()
    e = int(hashlib.sha256(str(r).encode() + m).hexdigest(), 16)
    s = (k + x * e) % n
    return e, s

def verify(y, m: bytes, e, s):
    r = g * s + y * e
    r = r.x()
    ev = int(hashlib.sha256(str(r).encode() + m).hexdigest(), 16)
    return e == ev

def menu():
    print("Nnnnnnn~~ Vivi!!")
    print("1. Keygen")
    print("2. Sign")
    print("3. Verify")

def challenge():
    x, y = keygen()
    
    for _ in range(27):
        menu()
        choice = int(input(">> "))
        
        if choice == 1:
            x, y = keygen()
        elif choice == 2:
            m = bytes.fromhex(input("Message: "))
            if any(c.encode() in m for c in string.printable):
                print("Invalid message")
                continue
            e, s = sign(x, m)
            print(f"Signature: ({e}, {s})")
        elif choice == 3:
            m = bytes.fromhex(input("Message: "))
            e = int(input("e: "), 16)
            s = int(input("s: "), 16)
            
            if not verify(y, m, e, s):
                print("Invalid")
                exit(1)
                
            print("Valid")
            pt = m.decode('utf-8')
            
            if pt == '浮気したらあかんで..., うちがそばにいるのに....!':
                print(FLAG)
                exit(0)
        else:
            print("Bye bye")
            exit(1)
            
    print("Bye bye")
            
if __name__ == "__main__":
    try:
        signal.alarm(60)
        challenge()
    except Exception as e:
        print(f"Exception triggered: {e.__class__}")
        exit(1)
        
