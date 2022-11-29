import hashlib, binascii
import time
import os

start = time.time()
dict_array = []
dict_file = open("common-passwords-win.txt", "r")

for line in dict_file:
  dict_array.append(line.rstrip('\n'))
  # rstrip('\n') removes newline characters from the words, you might not need this.

password = input("Enter password: ")

def hash256(password):
    hashed_pwd = hashlib.pbkdf2_hmac('sha256', #later you will changes this to sha512
                         password.encode('utf-8'),# password is encoded into binary
                         'saltPhrase'.encode('utf-8'),# 'salt' is an extra bit of 
#info added to the password. When using randomized 'salt' dictionary attacks becomes
#nealry impossible. For this project keep 'salt' static. In the real world 'salt' is
#randomized and later exctracted from the hashed password during the verififcation 
#process. Essentially, the 'salt' portion of the hash can be separated from the 
#password portion.
                         100000) # number of iterations ('resolution') of the hashing computation)
    return binascii.hexlify(hashed_pwd)# converting binary to hex

def hash512(password):
    hashed_pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 'saltPhrase'.encode('utf-8'), 100000)
    return binascii.hexlify(hashed_pwd)

hashed_pwd_hex_256 = hash256(password)
hashed_pwd_hex_512 = hash512(password)

print("\t256 SHA: ", hashed_pwd_hex_256)
print("\t512 SHA: ", hashed_pwd_hex_512)

print("Cracked SHA256: ", )


print("Pwd is:" + password + " Length is: ", len(password))

# print(dict_array)

for word in dict_array:
    if hash256(word) == hashed_pwd_hex_256:
        print("Guessed it! " + word)
        print("Time to crack: ")
    #else:
        # print("Wrong:" + word)

print("Elpased time: ", (time.time() - start), " seconds.")