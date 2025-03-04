from pwn import *

def repeatingXor(ct, key):
    print(len(ct), len(key))
    res = [ct[i] ^ key[i % len(key)] for i in range(len(ct))]
    return bytes(res)

io = remote("20.6.89.33", 8040)
# io = process(["python3", "chall.py"])

io.recvuntil(b"Encrypted password: ")
ct = io.recvline().strip().decode()
io.recvuntil(b"IV: ")
iv = io.recvline().strip().decode()

print("ct:", ct)
print("iv:", iv)

# CBC mode for the first two blocks
io.sendlineafter(b">>> ", b"1")
data = b"00" * 32
io.sendlineafter(b"Data: ", data)
params = '{"mode": 2, "iv": "' + iv + '"}'
io.sendlineafter(b"Params: ", params.encode())
io.recvuntil(b"Result: ")
first_part = io.recvline().strip().decode()

# CFB mode for the last two blocks
io.sendlineafter(b">>> ", b"1")
data = b"00" * 32
io.sendlineafter(b"Data: ", data)
params = '{"mode": 3, "iv": "' + first_part[32:] + '", "segment_size": 128}'
io.sendlineafter(b"Params: ", params.encode())
io.recvuntil(b"Result: ")
second_part = io.recvline().strip().decode()

fullkey = first_part + second_part
password = repeatingXor(bytes.fromhex(ct), bytes.fromhex(fullkey))
print("Password:", password)

io.sendlineafter(b">>> ", b"3")
io.sendlineafter(b"Guess: ", password)
io.interactive()