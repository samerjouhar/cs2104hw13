import hashlib, binascii
import time
import asyncio

def make_dictionary(file):
    dict_array = []
    dict_file = open(file, "r")

    for line in dict_file:
        dict_array.append(line.rstrip('\n'))
    
    return dict_array

async def hash256(password):
    hashed_pwd = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 'saltPhrase'.encode('utf-8'), 100000) 
    return binascii.hexlify(hashed_pwd)

async def hash512(password):
    hashed_pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 'saltPhrase'.encode('utf-8'), 100000)
    return binascii.hexlify(hashed_pwd)

async def main():
    dict_array = make_dictionary("common-passwords-win.txt")

    hashes = await asyncio.gather(
        hash256(password),
        hash512(password)
    )

    print("\t256 SHA: ", hashes[0].decode("utf-8") )
    print("\t512 SHA: ", hashes[1].decode("utf-8"), "\n")

    cracked_words = await asyncio.gather(
        crack_array(hashes[0], hashes[1], dict_array)
    )


async def crack_array(hashed_pwd_hex_256, hashed_pwd_hex_512, dict_array):
    start256 = time.time()
    for word in dict_array:
        hash256_word = await hash256(word)
        if hash256_word == hashed_pwd_hex_256:
            print("Cracked SHA256: " + word)
            print("Time to crack: ", time.time() - start256, "\n")
            break

    start512 = time.time()
    for word in dict_array:
        hash512_word = await hash512(word)
        if hash512_word == hashed_pwd_hex_512:
            print("Cracked SHA512: " + word)
            print("Time to crack: ", time.time() - start512, "\n")
            break

start = time.time()

if __name__ == '__main__':
    while (True):
        password = input("Enter password: ")
        while (password != 'q'):
            asyncio.run(main())
            password = input("Enter password: ")
        else:
            print("Elpased time: ", (time.time() - start), " seconds.")
            break