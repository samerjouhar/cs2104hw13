#global vars
from itertools import combinations, permutations
dict = [1,2,3,4]
guesses = 0

#when calling function, use layer = 1
#returns if pass is cracked as bool, number of guesses as int, difficulty of password (layer) as int
def checker256(layer):
    for perm in permutations(layer):
        guesses = guesses + 1
        if hash256(perm) == hashed256_target:
            return [True, guesses, layer]
    checker256(layer + 1)
    if layer > len(dict):
        return [False]

def checker512(layer):
    for perm in permutations(layer):
        guesses = guesses + 1
        if hash512(perm) == hashed512_target:
            return [True, guesses, layer]
    checker512(layer + 1)
    if layer > len(dict):
        return [False]





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