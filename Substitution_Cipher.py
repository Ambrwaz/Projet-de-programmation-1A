# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 17:52:21 2018

@author: Navigateur_2
"""

import random
import _string_ as s
import _statistics_ as stat
import math

##We define the normal frequencies of each letter, in percentage.
#normal_frequencies = {'a': 7.636, 'b': 0.901, 'c': 3.260, 'd': 3.669, 
#                      'e': 14.715, 'f': 1.066, 'g': 0.866, 'h': 0.737, 
#                      'i': 7.529, 'j': 0.545, 'k': 0.049, 'l': 5.456, 
#                      'm': 2.968, 'n': 7.095, 'o': 5.378, 'p': 3.021, 
#                      'q': 1.362, 'r': 6.553, 's': 7.948, 't': 7.244, 
#                      'u': 6.311, 'v': 1.628, 'w': 0.114, 'x': 0.387, 
#                      'y': 0.308, 'z': 0.136}

Bigram_statistics = stat.Bigram_statistics
Alphabet = s.Alphabet

def generatePermutation():
    """
    Returns a dictionary that matches each letter with the one it is permuted with.
    """
    permuted_Alphabet = list(s.Alphabet).copy()
    random.shuffle(permuted_Alphabet)
    
    permutation = {}
    
    numberOfCharacters = len(s.Alphabet)
    for i in range(numberOfCharacters):
        permutation[s.Alphabet[i]] = permuted_Alphabet[i]
    
    return permutation


def distanceBetweenPermutations(permutation1, permutation2, isPermutation2Reverse = False):
    """
    This function takes as argument two permutations and returns the number of
    points where they differ.
    """
    
    assert permutation1.keys() == permutation2.keys()
    
    if (isPermutation2Reverse == True):
        new_perm = dict((v,k) for (k,v) in permutation2.items())
        permutation2 = new_perm
    
    differences = 0
    for key in permutation1.keys():
        if permutation1[key] != permutation2[key]:
            differences += 1
    
    return differences

def encrypt(message, permutation):
    
    """
    Encrypts the given message with the given permutation.
    """
    
    encrypted_text = ""
    cleared_text = s.clear(message) #We remove all accented characters.
    for char in cleared_text:
        
        if char in s.Alphabet:
            encrypted_char = permutation[char]
        else:
            encrypted_char = char
        
        encrypted_text += encrypted_char
    
    return encrypted_text


def decrypt(message, key=False, cleared=True):
    
    global Alphabet
    global Bigram_statistics
    
    #If the key is not given, we have to crack it. For this purpose, we use 
    #the method of simulated annealing.
    if key == False:
        
        permutation = dict([(char, char) for char in Alphabet]) #We initialize the permutation to the identity.
        energy = abs(s.logvraisemblance(message, Bigram_statistics) - s.frenchLogVraisemblance) #We initialize the energy.
        
        count = 0
        
        #Our goal is now to minimize the energy, i.e to obtain a message with logvraisemblance the closest to french logvraisemblance.
        while energy > 0.03 and count < 10000:
            #We try a random modification of the permutation.
            charsToPermute1, charsToPermute2 = random.choices(Alphabet, k=2)
            permutation[charsToPermute1], permutation[charsToPermute2] = permutation[charsToPermute2], permutation[charsToPermute1]

            #We check whether this new permutation is 'better' or not.
            new_energy = abs(s.logvraisemblance(encrypt(message, permutation), Bigram_statistics) - s.frenchLogVraisemblance)
            delta_Of_energy = new_energy - energy

            if delta_Of_energy < 0:
                energy = new_energy
            
            else: #If the permutation is worse than the previous one, we refuse it.
                permutation[charsToPermute1], permutation[charsToPermute2] = permutation[charsToPermute2], permutation[charsToPermute1]
        
            count += 1
            
            if count % 1000 == 0:
                print(energy)
            
        return encrypt(message, permutation), permutation
    
    
    #If the key is given, we have to reverse it.
    else:
        permutation = dict([(v, k) for k, v in key.items()])
        return encrypt(message, permutation), permutation




















































