#global vars
from itertools import combinations, permutations
dict = [1,2,3,4]
guesses = 0

#when calling function, use idx = 0, curr = "", and layer = 1
def checker256(layer):
    for perm in permutations(dict, layer):
        guesses = guesses + 1
        if hash256(perm) == hashed_target:
            return [True, guesses]
    checker256(layer + 1)

#print(check256())
#not finished yet
count = 0
def permute():
    count = 0
    for perm in permutations(dict, 2):
        count = count + 1
        print(perm)
    print(count)

permute()


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