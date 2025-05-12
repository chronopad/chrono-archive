from Crypto.Util.number import getRandomRange, getStrongPrime

class SkillException(Exception): pass

FLAG = open("flag.txt").read()

p = getStrongPrime(512)
q = getStrongPrime(512)
N = p * q
o = (p - 1) * (q - 1)

g = 2
x = getRandomRange(2, o)
h = pow(g, x, N)
pw = getRandomRange(2, N)

def encrypt(msg: int):
    y = getRandomRange(2, o)
    s = pow(h, y, N)
    c1 = pow(g, y, N)
    c2 = msg * s % N
    return (c1, c2)

def decrypt(c1: int, c2: int):
    s = pow(c1, x, N)
    msg = pow(s, -1, N) * c2 % N
    return msg

def leak():
    c1, c2 = encrypt(pw)
    
    print("Gacha gacha gacha: ")
    print(f"N: {hex(N)}")
    print(f"c1: {hex(c1)}")
    print(f"c2: {hex(c2)}")

def main():
    print("You know the drill")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Win")
    print("==================")
    
    choice = int(input("> "))
    if choice == 1:
        msg = int(input("msg > "), 16)
        c1, c2 = encrypt(msg)
        print(f"c1: {hex(c1)}")
        print(f"c2: {hex(c2)}")
        
    elif choice == 2:
        c1 = int(input("c1 > "), 16)
        c2 = int(input("c2 > "), 16)
        pt = decrypt(c1, c2) % 5
        print(f"pt: {hex(pt)}")
    
    elif choice == 3:
        guess = int(input("guess > "), 16)
        # It doesn't have to be perfect
        if abs(guess - pw) < 256:
            print("Gratz, you win!")
            print(FLAG)
            exit(0)
        else:
            raise SkillException("404 skill not found")
        
if __name__ == '__main__':
    leak()
    try:
        for _ in range(444):
            main()
    except Exception as e:
        print("Eyy stop!")
        print(f"Exception triggered: {e.__class__}")