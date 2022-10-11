import random
import string
import codecs

random.seed(123) 
f = codecs.open("pg3300.txt", "r", "utf-8")
par = f.read()
f.close()
par = par.split(' \n')
print(par[14])

def gut(p):
    return "gutenberg" not in p.lower()

def tokenize(p):
    s = string.punctuation+"\n\r\t"
    for c in s:
        # print(c)
        p.replace(c,"")
    return p

filtered_par = list(filter(gut, par))

# filtered_par = list(map(lambda p: tokenize(p), filtered_par)) # litt usikker på om vi trenger denne
# print(filtered_par[4])

def empty(p):
    return len(p) > 0 

tokens = list(map(lambda p: p.split(" "), filtered_par))
# for item in tokens :
#     print(item) 
#     item = list(filter(empty, item))

# print(tokens[0])

# table = p.maketrans(string.punctuation+"\n\r\t","!"*35)
# p =p.translate(table)