import os, random
from Crypto.Util.strxor import strxor
from itertools import product
from aes import AES
from utils import *

def decrypt(ciphertext, key):
    aes = AES(key, 2)
    key_expand = aes._key_matrices
    state = bytes2matrix(ciphertext)
    add_round_key(state, key_expand[-1])
    inv_mix_columns(state)
    add_round_key(state, key_expand[-1])

    return aes.decrypt_block(matrix2bytes(state))

def generate_sbox_different_distribution_table():
    table = {}
    for i in range(256):
        for j in range(256):
            diff = i ^ j
            diff_sbox = sbox[i] ^ sbox[j]

            if diff in table:
                if diff_sbox not in table[diff]:
                    table[diff].append(diff_sbox)
            else:
                table[diff] = [diff_sbox]

    return table

def inv_last_round(s, k):
    state = bytes2matrix(s)
    round_key = bytes2matrix(k)
    inv_mix_columns(state)
    add_round_key(state, round_key)
    inv_shift_rows(state)
    inv_sub_bytes(state)

    return matrix2bytes(state)

def mix_columns_key(round_key):
    state = bytes2matrix(round_key)
    mix_columns(state)

    return matrix2bytes(state)

def generate_impossible_state(differential):
    impossible = []
    for i in range(4):
        impossible.append([])
        for j in range(256):
            if j not in sbox_ddt[differential[i]]:
                impossible[i].append(j)

    impossible_state = []
    for i in range(4):
        
        for j in impossible[i]:
            state = bytes2matrix(b'\x00'*(i) + bytes([j]) + b'\x00'*(15-i))
            shift_rows(state)
            mix_columns(state)
            impossible_state.append(matrix2bytes(state))
            
    return impossible_state

def generate_256_list():
    result = []
    for i in range(256):
        result.append(i)

    return result

shifted_round1 = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
sbox_ddt = generate_sbox_different_distribution_table()

print("[+] Retrieve 5 plaintext-ciphertext pairs from encryption oracle...")
test_pair = [[bytes.fromhex(block) for block in pair.split("\n")] for pair in open("../pairs.txt").read().split("\n\n")[:-1]]
impossible_key = [None] * 16

for plaintext1, plaintext2, ciphertext1, ciphertext2 in test_pair:

    print("[+] Checking impossible state from differential pair...")
    plain_diff = xor(plaintext1, plaintext2)
    enc_diff = xor(ciphertext1, ciphertext2)

    impossible_state = generate_impossible_state(plain_diff)
    for i in range(16):
        if impossible_key[i] is None:
            impossible_key[i] = []

        shifted_index = shifted_round1[i]
        for j in range(256):
            if j in impossible_key[i]:
                continue

            guess_key = b'\x00'*(i) + bytes([j]) + b'\x00'*(15-i)
            inv_a = inv_last_round(ciphertext1, guess_key)
            inv_b = inv_last_round(ciphertext2, guess_key)
            inv_diff = xor(inv_a, inv_b)
            
            for k in impossible_state:
                if inv_diff[shifted_index] == k[shifted_index]:
                    impossible_key[i].append(j)

list_256 = generate_256_list()
possible_key = []
for imp_key in impossible_key:
    possible_key.append(list(set(list_256) - set(imp_key)))

all_possible_key = product(*possible_key)

ciphertext_check = ciphertext1
for possible_round_key in all_possible_key:
    
    mixed_key = mix_columns_key(possible_round_key)
    master_key = inv_key_expansion(list(mixed_key), 2)
    
    decrypt_check = decrypt(ciphertext_check, master_key)
    if decrypt_check == test_pair[-1][0]:
        print('[+] Possible Master Key:', master_key)

        encs = [bytes.fromhex(enc) for enc in open("../out.txt").read().split("\n")]
        pts = [decrypt(enc, master_key) for enc in encs]
        print("[+] Flag:", b''.join(pts))
