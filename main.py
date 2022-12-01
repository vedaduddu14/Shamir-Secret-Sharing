#by Veda D
#import packages
from cryptography.fernet import Fernet
import IDA
import sys
import random
import functools

from numpy import short

prime = 2 ** 521 - 1

#simple encryption algorithm
def encrypt(filename1,filename2,key):
    f = Fernet(key)
    with open(filename1, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename2, "wb") as file:
        file.write(encrypted_data)
#simple decryption algorithm
def decrypt(filename1,filename2,key):
    f = Fernet(key)
    with open(filename2, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename1, "wb") as file:
        file.write(decrypted_data)
#secret sharing functions
#random generator function
random_generator = functools.partial(random.SystemRandom().randint, 0)
#function to generate shares. returning shares in the tuple
def make_random_shares(secret, minimum_shares, no_shares, prime=prime):
    if minimum_shares > no_shares:
        print("can't reconstruct the shares umm")
        sys.exit()
    polynomial = [secret] 
    for i in range(minimum_shares -1):
        polynomial = polynomial+ [random_generator(prime - 1)]
    shares = []
    for i in range(1,no_shares+1):
        accumalator = 0
        for coeff in reversed(polynomial):
            accumalator = accumalator*i
            accumalator = accumalator+coeff
            accumalator = accumalator % prime
        shares.append([i,accumalator])
    return shares
#lagrange interpolation for polynomials in the Z_p world
def lagrange_interpolation(j, x_shares, y_shares, prime):
    def product(values):  
        counter = 1
        for v in values:
            counter = counter*v
        return counter
    def division_modulus(numerator,denominator,prime):
        variable1 = 0
        last_x = 1
        variable2 = 1
        last_y = 0
        while prime != 0:
            quotient = denominator // prime
            denominator, prime = prime, denominator % prime
            variable1, last_x = last_x - quotient * variable1, variable1
            variable2, last_y = last_y - quotient * variable2, variable2
        return last_x*numerator
    numerator = []
    denominator = []
    for i in range(len(x_shares)):
        x_list = list(x_shares)
        current = x_list.pop(i)
        numerator_product =[]
        denominator_product = []
        for x in x_list:
            numerator_product.append(j-x)
        numerator.append(product(numerator_product))
        for x in x_list:
            denominator_product.append(current - x)
        denominator.append(product(denominator_product))
    denominator_product = product(denominator)
    div_mod = []
    for i in range(len(x_shares)):
        div_mod.append(division_modulus(numerator[i] * denominator_product * y_shares[i] % prime, denominator[i], prime))
    numerator_sum = sum(div_mod)
    return (division_modulus(numerator_sum, denominator_product, prime) + prime) % prime
#recover secrets
def recover_secret(x_shares,y_shares,minimum_shares, prime=prime):
    if len(x_shares) < minimum_shares:
        print("Wrong number of shares, rerun the program")
        sys.exit()
    return lagrange_interpolation(0, x_shares, y_shares, prime)


#generate shares containing both fragment of key and file
def shortshare(file,minimum_shares,no_shares):
    key = Fernet.generate_key()
    file1 = "encrypted.txt"
    encrypt(file,file1,key)
    keyy = str(key)
    key1 = ' '.join([ str(ord(c)) for c in keyy])
    binary = int(''.join([str(x) for x in key1.split()]))
    if (minimum_shares>no_shares):
        print("System error!")
        sys.exit()
    fragments = IDA.split("encrypted.txt",no_shares,minimum_shares)
    shares = make_random_shares(binary, minimum_shares, no_shares)
    def combinefile(shares,fragments):
        combined_files = []
        for i in range(no_shares):
            combined_files.append([shares[i],fragments[i]])
        return combined_files
    combined_files = combinefile(shares,fragments)
    return combined_files

#reconstruct using the shares
def reconstructshortshare(combined_files,minimum_shares):
    if len(combined_files)<minimum_shares:
        print("Incorrect number of shares given")
        sys.exit()
    subset = []
    assemble = []
    for i in range (minimum_shares):
        subset.append(combined_files[i][0])
        assemble.append(combined_files[i][1])
    x_shares = []
    y_shares = []
    for i in range(len(subset)):
        x_shares.append(subset[i][0])
        y_shares.append(subset[i][1])
    recovered = str(recover_secret(x_shares,y_shares,minimum_shares))
    str1 = ''
    i = 0
    while i<len(recovered):
        if (recovered[i] == '1'):
            str1 = str1 + recovered[i]+recovered[i+1]+recovered[i+2] + ' '
            i = i+3
        else:
            str1 = str1 + recovered[i]+recovered[i+1] + ' '
            i = i+2
    str1 = str1[:-1]
    a = str1.split()
    res = ''
    for i in a:
        res = res + chr(int(i))
    res = res[:-1]
    res = res[2:]
    res = bytes(res,"utf-8")
    IDA.assemble(assemble,"decrypted1.txt")
    file2 = "decrypted1.txt"
    file3 = "decrypted.txt"
    decrypt(file3,file2,res)
    return file3
