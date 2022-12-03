import binascii
import hashlib
import time
from multiprocessing import Process
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np

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
    crackers( hash_256, hash_512, dict_array, layer, len_password, 0)

def checker256(hashed_pwd_hex_256: bytes, dict_array: list[str], layer:int, len_password:int, timer:float, guesses256:int):
        for perm in permutations(dict_array, layer):
            guesses256 = guesses256 + 1
            temp = ''
            for i in range(len(perm)):
                temp = temp + perm[i]
            if (len(temp) != len_password or len(temp) > len_password):
                continue
            if hash256(temp) == hashed_pwd_hex_256:
                print("Cracked SHA256: ", temp)
                timetaken = time.time() - timer
                print("Time to crack: ", timetaken, "\n")
                print(guesses256)
                return [True, guesses256, timetaken]
        if layer > len_password:
            return [False, -1]
        if(checker256(hashed_pwd_hex_256, dict_array, layer + 1, len_password, timer, guesses256)):
            guesses256 = checker256(hashed_pwd_hex_256, dict_array, layer + 1, len_password, timer, guesses256)[1]
            return [True, guesses256, time.time() - timer]
        

def checker512(hashed_pwd_hex_512: bytes, dict_array: list[str], layer:int, len_password:int, timer:float, guesses512:int):
        for perm in permutations(dict_array, layer):
            guesses512 = guesses512 + 1
            temp = ''
            for i in range(len(perm)):
                temp = temp + perm[i]
            if (len(temp) != len_password or len(temp) > len_password):
                continue
            if hash512(temp) == hashed_pwd_hex_512:
                print("Cracked SHA512: ", temp)
                timetaken = time.time() - timer
                print("Time to crack: ", timetaken, "\n")
                return [True, guesses512, timetaken]
        if layer > len_password:
            return [False, -1]
        if(checker512(hashed_pwd_hex_512, dict_array, layer + 1, len_password, timer, guesses512)):
            return [True, guesses512, time.time() - timer]

def crackers(hashed_pwd_hex_256: bytes, hashed_pwd_hex_512: bytes, dict_array, layer:int, len_password:int, guesses:int):
    time256 = time.time()
    data256 = checker256(hashed_pwd_hex_256, dict_array, layer, len_password, time256, guesses)
    guesses256_list.append(data256[1])
    times256_list.append(data256[2])
    time512 = time.time()
    data512 = checker512(hashed_pwd_hex_512, dict_array, layer, len_password, time512, guesses)
    times512_list.append(data512[2])

start = time.time()

if __name__ == '__main__':
    while (True):
        password = input("Enter password: ")
        guesses256_list = []
        times256_list = []
        times512_list = []
        while (password != 'q'):
            main()
            passwords.append(password)
            password = input("Enter password: ")
        else:
            xticks = []
            for i in range(len(passwords)):
                xticks.append(passwords[i] + " (" + str(round(guesses256_list[i],2)) + ")")
            print("Elpased time: ", (time.time() - start), " seconds.")
            #print(guesses_list)
            #print(times_list)
            #plt.bar(passwords, guesses_list)
            X_axis = np.arange(len(passwords))
            plt.bar(X_axis - 0.2, times256_list, 0.4, label = "SHA256")
            plt.bar(X_axis + 0.2, times512_list, 0.4, label = "SHA512")
            plt.title('Passwords (SHA256) vs. Time Taken to Crack\n' + r'Dictionary Size: 104')
            plt.xticks(range(len(passwords)), xticks)
            plt.xlabel("Entered Password (# of guesses)")
            plt.ylabel("Time Taken to Crack")
            plt.legend()
            plt.show()
            quit()
    