# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 17:45:22 2018

@author: Navigateur_2
"""

import _string_ as s
import Caesar_Cipher as caesar

Alphabet = s.Alphabet


def encrypt(message, key, cleared=False):
    
    """
    Encrypts the message by the vigenere cypher with the key.
    """

    assert type(message) == str
    assert type(key) == str
    assert type(cleared) == bool
    
    global Alphabet

    #If the message is not cleared, we clear it.
    if (cleared == False):
        message = s.clear(message)
        key = s.clear(key)
    
    #To optimize the code, we immediatly len_key.
    len_key = len(key)
    
    #Now, we creat a string which in will be saved the encrypted message.
    encrypted_message = ''
    key_index = 0
    #Then we encrypt the message.
    for character in message:
        
        #If the character is in the alphabet, then we encrypt it, otherwise
        #we don't touch it.
        if character in Alphabet:
            
            #Because the key is not as long as the message, we have to precize
            #which character will be used.
            key_index = key_index % len_key
            
            #And we save the index of this character in the alphabet.
            letter_key_index = Alphabet.index(key[key_index])
            
            #Now, we save the index of the message's character in the alphabet.
            Alphabet_index = Alphabet.index(character)
            
            #Then we add the two to know the index of the encrypted character.
            encrypted_index = (letter_key_index + Alphabet_index) % 26
            encrypted_character = Alphabet[encrypted_index]
            
            #Finally, we add it to the message.
            encrypted_message += encrypted_character
            
            key_index += 1
        
        else:
            encrypted_message += character
        
    return encrypted_message


def decrypt(message, key=False, cleared=False):
    
    """
    Decrypts the message by the vigenere cypher with or without the key.
    """

    assert type(message) == str
    assert type(key) == str or key == False
    assert type(cleared) == bool
    
    global Alphabet

    #If the message is not cleared, we clear it.
    if (cleared == False):
        message = s.clear(message)
    
    #If the key is not given, we will have to find it with the aim of
    #decrypting the message.
    if (key == False):
        
        #Firstly, we try to guess the lenght of the key, using the IC of each
        #substring.
        coincidence_index_list = [0]*100
        
        for lenght in range(1, 100):
            
            #We divide the message into lenght substrings.
            substrings = ['']*lenght
            character_substrings = 0
            for index, character in enumerate(message):
                if character in Alphabet:

                    substrings[character_substrings] += character
                    character_substrings += 1
                    character_substrings %= lenght
                    
                    
            #Now, we verify if the average of the IC of each substring belongs
            #to the language.
            IC = 0
            for substring in substrings:
                IC_substring = s.index_of_coincidence(substring, cleared = True)
                IC += IC_substring
            IC /= lenght
            
            is_likely_lenght = s.is_language(IC=IC, mode='is', language='French')
            
            coincidence_index_list[lenght] = IC
            
            #If the IC is right, it means that the key has this lenght, and we
            #can directly decrypt each substring.
            if (is_likely_lenght == True):
                key = ''
                count = 0
                for substring in substrings:
                    substring_key = caesar.decrypt(substring, cleared=True)[1]
                    character = Alphabet[substring_key]
                    key += character
                    count += 1
                
                
                break
            

    #If the key is given, we have to reverse it.
    else:
        key_list_index = []
        for character in key:
            key_list_index += [(26 - Alphabet.index(character))%26]
        
        key = ''
        for index in key_list_index:
            key += Alphabet[index]
        
    decrypted_message = encrypt(message, key, cleared=True)

    return decrypted_message, key
