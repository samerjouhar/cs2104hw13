import binascii
import hashlib
import time
from multiprocessing import Process
from itertools import permutations
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

passwords = []

def make_dictionary(file) -> list[str]:
    dict_array = []
    dict_file = open(file, "r")

    for line in dict_file:
        dict_array.append(line.rstrip('\n'))
    
    return dict_array

def hash256(password: str):
    hashed_pwd = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 'saltPhrase'.encode('utf-8'), 100000) 
    return binascii.hexlify(hashed_pwd)

def hash512(password: str):
    hashed_pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 'saltPhrase'.encode('utf-8'), 100000)
    return binascii.hexlify(hashed_pwd)

def main():
    dict_array = make_dictionary("common-passwords-win.txt")
    #dict_array = make_dictionary("best1050.txt")
    #dict_array = make_dictionary("common-full")

    hash_256 = hash256(password)
    hash_512 = hash512(password)
    len_password = len(password)

    print("\t256 SHA: ", hash_256.decode("utf-8") )
    print("\t512 SHA: ", hash_512.decode("utf-8"), "\n")

    layer = 1
    crackers( hash_256, hash_512, dict_array, layer, len_password)

def checker256(hashed_pwd_hex_256: bytes, dict_array: list[str], layer:int, len_password:int, timer:float):
        guesses = 0
        for perm in permutations(dict_array, layer):
            if (len(perm) > len_password):
                continue
            guesses = guesses + 1
            temp = ''
            for i in range(len(perm)):
                temp = temp + perm[i]
            if hash256(temp) == hashed_pwd_hex_256:
                print("Cracked SHA256: ", temp)
                timetaken = time.time() - timer
                print("Time to crack: ", timetaken, "\n")
                return [True, guesses, timetaken]
        if layer > len_password:
            return [False, -1]
        if(checker256(hashed_pwd_hex_256, dict_array, layer + 1, len_password, timer)):
            return [True, guesses, time.time() - timer]
        

def checker512(hashed_pwd_hex_512: bytes, dict_array: list[str], layer:int, len_password:int, timer:float):
        guesses = 0
        for perm in  permutations(dict_array, layer):
            if (len(perm) > len_password):
                continue
            guesses = guesses + 1
            temp = ''
            for i in range(len(perm)):
                temp = temp + perm[i]
            if hash512(temp) == hashed_pwd_hex_512:
                print("Cracked SHA512: ", temp)
                timetaken = time.time() - timer
                print("Time to crack: ", timetaken, "\n")
                return [True, guesses, layer, timetaken]
        if layer > len_password:
            return [False, -1]
        checker512(hashed_pwd_hex_512, dict_array, layer + 1, len_password, timer)

def crackers(hashed_pwd_hex_256: bytes, hashed_pwd_hex_512: bytes, dict_array, layer:int, len_password:int):
    time256 = time.time()
    data256 = checker256(hashed_pwd_hex_256, dict_array, layer, len_password, time256)
    guesses_list.append(data256[1])
    times_list.append(data256[2])
    time512 = time.time()
    checker512(hashed_pwd_hex_512, dict_array, layer, len_password, time512)

start = time.time()

if __name__ == '__main__':
    while (True):
        password = input("Enter password: ")
        guesses_list = []
        times_list = []
        while (password != 'q'):
            main()
            passwords.append(password)
            password = input("Enter password: ")
        else:
            print("Elpased time: ", (time.time() - start), " seconds.")
            #print(guesses_list)
            #print(times_list)
            plt.bar(passwords, guesses_list)
            plt.title('Password Difficulty vs. Number of Guesses\n' + r'Dictionary Size: 104')
            plt.legend(bbox_to_anchor = (1.25, 0.6), loc='upper left', borderaxespad=0.)
            plt.show()
            quit()
    