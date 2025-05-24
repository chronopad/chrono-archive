import random
import signal

FLAG = open('flag.txt').read()

def temper(y):
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & (0x9d2c5680))
    y = y ^ ((y << 15) & (0xefc60000))
    y = y ^ (y >> 18)
    return y


def main():
    # Let's do more random shenanigans, with spices
    leak_mask = int(input("Enter leak mask: "), 16)
    if leak_mask.bit_count() > 8 or leak_mask <= 0:
        print("Skill issue")
        exit(0)
    
    for _ in range(50):
        for _ in range(random.getrandbits(32) & 15):
            random.getrandbits(32)
        secret = random.getrandbits(32)
        out = temper(secret)
        print(f'Your leak: {out & leak_mask}')
        
        res = int(input("Just gimme one bit: "))
        if res != secret & 1:
            print("Skill issue")
            exit(0)
        
        random.seed(random.getrandbits(32))
        
    print("Well played good sir")
    print(FLAG)
    
    
if __name__ == '__main__':
    try:
        signal.alarm(88)
        main()
    except Exception as e:
        print(e)
        exit(1)