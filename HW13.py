import asyncio
import binascii
import hashlib
import time
import sys
import concurrent.futures
from multiprocessing import cpu_count
from itertools import permutations

import matplotlib.pyplot as plt

def make_dictionary(file):
    dict_array = []
    dict_file = open(file, "r")

    for line in dict_file:
        dict_array.append(line.rstrip('\n'))
    
    return dict_array

async def hash256(password: str):
    hashed_pwd = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 'saltPhrase'.encode('utf-8'), 100000) 
    return binascii.hexlify(hashed_pwd)

async def hash512(password: str):
    hashed_pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 'saltPhrase'.encode('utf-8'), 100000)
    return binascii.hexlify(hashed_pwd)

async def main():
    #dict_array = make_dictionary("common-passwords-win.txt")
    #dict_array = make_dictionary("best1050.txt")
    dict_array = make_dictionary("common-full")
    NUM_CORES = cpu_count()

    hashes = await asyncio.gather(
        hash256(password),
        hash512(password)
    )

    print("\t256 SHA: ", hashes[0].decode("utf-8") )
    print("\t512 SHA: ", hashes[1].decode("utf-8"), "\n")

    layer = 1
    futures = []

    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
       
            new_future = executor.submit(
                crackers, # Function to perform
                # v Arguments v
                hashes[0],
                hashes[1],
                dict_array,
                layer
            )
            futures.append(new_future)

    concurrent.futures.wait(futures)

    



async def checker256(hashed_pwd_hex_256: bytes, hashed_pwd_hex_512: bytes, dict_array: list[str], layer:int):
        time256 = time.time()
        guesses = 0
        for perm in permutations(dict_array, layer):
            guesses = guesses + 1
            temp = ''
            for i in range(len(perm)):
                temp = temp + perm[i]
            if await hash256(temp) == hashed_pwd_hex_256:
                print("Cracked SHA256: ", temp)
                print("Time to crack: ", time.time() - time256, "\n")
                return [True, guesses, layer]
        await checker256(hashed_pwd_hex_256, hashed_pwd_hex_512, dict_array, layer + 1)
        if layer > len(dict_array):
            return [False]

async def checker512(hashed_pwd_hex_256: bytes, hashed_pwd_hex_512: bytes, dict_array: list[str], layer:int):
        time512 = time.time()
        guesses = 0
        for perm in permutations(dict_array, layer):
            guesses = guesses + 1
            temp = ''
            for i in range(len(perm)):
                temp = temp + perm[i]
            if await hash512(temp) == hashed_pwd_hex_512:
                print("Cracked SHA512: ", temp)
                print("Time to crack: ", time.time() - time512, "\n")
                return [True, guesses, layer]
        await checker512(hashed_pwd_hex_256, hashed_pwd_hex_512, dict_array, layer + 1)
        if layer > len(dict_array):
            return [False]

def crackers(hashed_pwd_hex_256: bytes, hashed_pwd_hex_512: bytes, dict_array: list[str], layer:int):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    results256 = asyncio.run( checker256(hashed_pwd_hex_256, hashed_pwd_hex_512, dict_array, layer) )
    results512 = asyncio.run( checker512(hashed_pwd_hex_256, hashed_pwd_hex_512, dict_array, layer) )

    if (not results256):
        print("No SHA256 Passwords Cracked")
    if (not results512):
        print("No SHA512 Passwords Cracked")

start = time.time()

if __name__ == '__main__':
    while (True):
        password = input("Enter password: ")
        while (password != 'q'):
            asyncio.run(main())
            password = input("Enter password: ")
        else:
            print("Elpased time: ", (time.time() - start), " seconds.")
            names = ['group_a', 'group_b', 'group_c']
            values = [1, 10, 100]

            plt.bar(names, values)
            plt.title('Password Difficulty vs. Number of Guesses\n' + r'Dictionary Size: 815')
            plt.legend(bbox_to_anchor = (1.25, 0.6), loc='center right')
            plt.show()
            quit()
    