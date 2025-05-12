from math import gcd
import random
from flag import flag

class Verifier:
    def __init__(self, y, n):
        self.y = y
        self.n = n
        self.previous_ss = set()
        self.previous_zs = set()

    def spin_roulette(self) -> int:
        return random.randint(0, 115792089237316195423570985008687907853269984665640564039457584007913129639934)

    def verify(self, s, z, b) -> bool:
        if s in self.previous_ss or z in self.previous_zs:
            print("Bad: repeated s or z")
            return False

        self.previous_ss.add(s)
        self.previous_zs.add(z)

        n = self.n
        y = self.y
        if s == 0:
            print("Bad: s = 0")
            return False
        if gcd(s, n) != 1:
            print("Bad: gcd(s, n) != 1")
            return False
        return pow(z, 2, n) == (s * pow(y, 1 - b, n)) % n


def main():
    print("Welcome to the mind reading test! Let's see if you're worthy of becoming the Kwisatz Haderach")
    no = 0 
    passed = 0
    n_rounds = 256

    while no < 100:
        if passed >= 100:
            print("Paul Atreides, you've convinced me that you are worthy to be part of the Bene Gesserit")
            print(flag)
            return

        n = 10205316970729431639485797664559886873490701487420041461102004580735751585751742938892976099986403177553363193830393487376567969420541261258134979327616363126253347148610544049807204226284930907503420405166209168541128632688637445870726287383056390377377382107622861504746212131179321468457103686904634978985262225083923899729078173292553918759616384301941301278845655112236714906572052945789912210749004588396399367890793347769585000314877970596365280369362958611301633074434160115833714459835933860197771690614293763100020927442209269135680658111369923029908840001532934157556701107140402652365541506235916261071723
        print(f"n = {n}")

        x = random.randrange(1, n)
        y = pow(x, 2, n)
        print(f"y = {y}")

        print("\nCan you read my mind? I'm playing the secret message in my head now.")
        print("1) yes\n2) no, I can't read your mind at the moment")
        choice1 = input("Your choice [1/2]: ").strip()
        if choice1 == "2":
            no += 1
            continue 

        print("Now, there are many spies in this public place. Show me that you know the secret message without showing me the secret message")
        verifier = Verifier(y, n)

        for i in range(n_rounds):
            s = int(input("Give me an s: ")) % n

            print("Let's spin the gigantic roulette to determine your fate:")
            b = verifier.spin_roulette()
            print(b)

            print("Are you ready to show me?")
            print("1) yes\n2) no, I am not ready, I need to calm my mind\n3) no, I forgot the mind reading from earlier")
            choice2 = input("Your choice [1/2/3]: ").strip()
            if choice2 == "2":
                no += 1
                if no >= 100:
                    return
                continue
            elif choice2 == "3":
                no += 1
                if no >= 50:
                    return
                passed=0
                break

            z = int(input("Give me a z: ")) % n
            if verifier.verify(s, z, b % 2):
                print(f"Good, you are telling the truth, but I am still not convinced")
                passed += 1
            else:
                print("I am the Reverend Mother, I can see through your lies. Don't you dare lie to me!")
                return
    
    print("You're just wasting my time, Atreides. You will never be the Kwisatz Haderach")

if __name__ == "__main__":
    main()
