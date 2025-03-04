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

io.sendlineafter(b">>> ", b"1")
data = b"0"*64
io.sendlineafter(b"Data: ", data)
params = '{"mode": 3, "iv": "' + iv + '", "segment_size": 128}'
io.sendlineafter(b"Params: ", params)
io.recvuntil(b"Result: ")
key1 = io.recvline().strip().decode()
print("key1:", key1)

io.sendlineafter(b">>> ", b"1")
data = (key1[32:] + "0" * 32).encode()
io.sendlineafter(b"Data: ", data)
params = '{"mode": 2, "iv": "' + "0"*32 + '"}'
io.sendlineafter(b"Params: ", params)
io.recvuntil(b"Result: ")
key2 = io.recvline().strip().decode()
print("key2:", key2)

fullkey = key1 + key2
password = repeatingXor(bytes.fromhex(ct), bytes.fromhex(fullkey))

io.sendlineafter(b">>> ", b"3")
io.sendlineafter(b"Guess: ", password)
io.interactive()
# 