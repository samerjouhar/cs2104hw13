#global vars
dict = []
hashed_target = ""
guesses = 0

#when calling function, use idx = 0, curr = "", and layer = 0
def checker256(idx, curr, layer):
    guesses = guesses + 1
    if hash256(curr + dict(idx)) == hashed_target:
        return [True, guesses]
    if idx == len(dict-1):
        checker256(0, dict[layer], layer + 1)
        *


#not finished yet


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