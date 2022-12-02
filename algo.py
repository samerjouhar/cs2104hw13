#global vars
from itertools import combinations, permutations
dict = ['a','b','c','d']
guesses = 0

#when calling function, use layer = 1
#returns if pass is cracked as bool, number of guesses as int, difficulty of password (layer) as int

def checker256(layer):
    for perm in permutations(layer):
        guesses = guesses + 1
        temp = ''
        for i in range(len(perm)):
            temp = temp + perm[i]
        if hash256(temp) == hashed256_target:
            return [True, guesses, layer]
    checker256(layer + 1)
    if layer > len(dict):
        return [False]

def checker512(layer):
    for perm in permutations(layer):
        guesses = guesses + 1
        temp = ''
        for i in range(len(perm)):
            temp = temp + perm[i]
        if hash512(temp) == hashed512_target:
            return [True, guesses, layer]
    checker256(layer + 1)
    if layer > len(dict):
        return [False]

"""
def perm():
    count = 0
    temp = ''
    for perms in permutations(dict, 3):
        for i in range(len(perms)):
            temp = temp + perms[i]
            #print(perms[i])
        print(temp)
        temp = ''
        count=count+1
    print(count)
perm()
"""


"""
hash256 is the function to convert str --> hash256 with salt
hash512 is the function to convert str --> hash512 with salt
"""


"""
sample_dict = [a,b,c,d]
guesses:
a
b
c
d
aa
ab
ac
ad
ba
bb
bc
bd
ca
cb
cc
cd
da
db
dc
dd
"""