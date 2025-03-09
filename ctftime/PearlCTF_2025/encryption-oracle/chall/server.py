#!/usr/local/bin/python
import random
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import math


p = getPrime(1024)
q = getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)


e = getPrime(20)
while math.gcd(e, phi) != 1:
    e = getPrime(20)

d = pow(e, -1, phi)  
leak = d % (p-1)

flag="pearl{fake_flag}"
flag_int = bytes_to_long(flag.encode())
encrypted_flag = pow(flag_int, e, n)

count = 0

while True:
    print("\n1. Encrypt message (3 times max)")
    print("2. Show encrypted flag")
    print("3. Show leak (d mod (p-1))")
    print("4. Exit")
    
    choice = input("> ")
    
    if choice == "1":
        if count >= 3:
            print("No more encryptions allowed")
            continue
        
        hex_msg = input("Enter hex message: ")
        try:
            msg = int(hex_msg, 16)
            if msg.bit_length() < 600:
                print(f"Message too short ({msg.bit_length()} bits, need 600+)")
                continue
            
            encrypted = pow(msg, e, n)
            count += 1
            print(f"Encrypted (hex): {encrypted:x}")
            print(f"Encryptions used: {count}/3")
        except:
            print("Invalid input")
    
    elif choice == "2":
        print(f"Encrypted flag: {encrypted_flag:x}")
    
    elif choice == "3":
        print(f"Leak (d mod (p-1)): {leak}")
    
    elif choice == "4":
        print("Exiting")
        break
    
    else:
        print("Invalid choice")
