# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 19:09:01 2018

@author: Navigateur_2
"""

import time
import _string_ as s



def encrypt(message, key, cleared=False):
    
    """
    Encrypts the message by the caesar cypher with the key, which corresponds 
    to the used shift.
    """
    
    assert type(message) == str
    assert type(key) == int
    assert type(cleared) == bool
    
    
    #If the message is not cleared, we clear it.
    if (cleared == False):
        message = s.clear(message)
    
    #Then we keep the modulo of the key, because it is a shift in the alphabet,
    #it shouldn't go beyond 26.
    key = key%26

    #Now, we creat a string which in will be saved the encrypted message.
    encrypted_message = ''
    
    #Then we encrypt the message.
    for character in message:
        
        #If the character is not a letter, then we just keep it, otherwise we
        #crypt it.
        new_character = character
        if character in s.Alphabet:
            index = s.Alphabet.index(character)
            new_character = s.Alphabet[(index+key)%26]
    
        encrypted_message += new_character
        
    return encrypted_message



def decrypt(message, key = False, cleared=False):
    
    """
    Decrypts the message crypted by the caesar cypher with or without the key.
    """

    assert type(message) == str
    assert type(key) == int or key == False
    assert type(cleared) == bool


    
    #If the message is not cleared, we clear it.
    if (cleared == False):
        message = s.clear(message)
        
    #Firstly, we assert if the key is known or not.
    if (key == False):
        
        #To know the key, we will see which letter come the more often in the
        #encrypted message.
        encrypted_e = ''
        encrypted_e_number = 0
        
        for character in s.Alphabet:
            counter = message.count(character)
            
            if (counter > encrypted_e_number):
                encrypted_e_number = counter
                encrypted_e = character
        
        key = (s.Alphabet.index('e') - s.Alphabet.index(encrypted_e))%26
        decrypted_message = encrypt(message, key, cleared=False)
        
        1
    else:
        key = 26 - key
    
        decrypted_message = encrypt(message, key, cleared=False)
        
    return decrypted_message, key











if __name__ == '__main__':
    
    tps1 = time.time()
    
    message = "Nous sommes bien arrivés, route sans problème. Mais j'aime les sardines à la banane. Et toi, est-ce que tu vas bien ? Si oui, dis-le moi. J'ai besoin de savoir, dis dis dis dis-moi si tu m'aimes."
    
    key = "bo"
    
    
    tps2 = time.time()
    elapsed_time = tps2 - tps1

