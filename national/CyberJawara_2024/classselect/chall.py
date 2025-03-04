import os
import signal
import json
from Crypto.Cipher import AES
from typing import Tuple

FLAG = open('flag.txt', 'r').read()
PASSWORD = os.urandom(32).hex()
KEY = os.urandom(16)
used = []

def check_mode(mode: int):
    mode = int(mode)
    global used
    if mode in used: raise ValueError("Value already used")
    used.append(mode)
    
def encrypt(data: bytes, params: dict) -> bytes:
    check_mode(params['mode'])    
    cipher = AES.new(KEY, **params)
    ct = cipher.encrypt(data)
    return ct

def decrypt(data: bytes, params: dict) -> bytes:
    check_mode(params['mode'])    
    cipher = AES.new(KEY, **params)
    ct = cipher.decrypt(data)
    return ct

def user_input() -> Tuple[bytes, dict]:
    data = bytes.fromhex(input("Data: ").strip())
    params = json.loads(input("Params: ").strip())
    if 'iv' in params:
        params['iv'] = bytes.fromhex(params['iv'])
    if 'nonce' in params:
        params['nonce'] = bytes.fromhex(params['nonce'])
     
    assert(len(data) < 41)
    
    return data, params
    
    
def main():
    IV = os.urandom(16)
    params = {'mode': 5, 'iv': IV}
    print("Guess my password and I gib flag")
    print(f"Encrypted password: {encrypt(PASSWORD.encode(), params).hex()}")
    print(f"IV: {IV.hex()}")
    print()
    
    for _ in range(3):
        print("="*50)
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Guess pw")
        print("="*50)
        
        choice = int(input(">>> "))
        
        if choice == 1:
            params = user_input()
            result = encrypt(*params)
            print(f'Result: {result.hex()}')
        elif choice == 2:
            params = user_input()
            result = decrypt(*params)
            print(f'Result: {result.hex()}')
        elif choice == 3:
            guess = input("Guess: ").strip()
            if guess == PASSWORD:
                print(f"Gratz: {FLAG}")
            else: print("Meh, try again.")
            
if __name__ == '__main__':
    signal.alarm(120)
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)