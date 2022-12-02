#global vars
from itertools import combinations, permutations
dict = [1,2,3,4]
guesses = 0

#when calling function, use idx = 0, curr = "", and layer = 1
def checker256(layer):
    for perm in permutations(layer):
        guesses = guesses + 1
        if hash256(perm) == hashed_target:
            return [True, guesses]
    checker256(layer + 1)
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