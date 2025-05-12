from Crypto.Util.number import getStrongPrime
m = int.from_bytes("IFEST13{???}".encode())
p = getStrongPrime(1024)
q = getStrongPrime(1024)
n = p * q
print(f'{pow(m, 0x10001, n)}\n{n}\n{p >> 40}')
