# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 16:57:45 2022

@author: kerya
"""

import Caesar_Cipher as caesar
import Vigenere_Cipher as vigenere
import Substitution_Cipher as substitution
import _statistics_ as stat
import _string_ as s

###############################################################################
############################## Unit tests #####################################
###############################################################################

# This block gathers all the unit tests that check whether the program is working
# as wanted.

Message_test = "Mais, vous savez, moi je ne crois pas qu’il y ait de bonne ou de mauvaise situation. \
 Moi, si je devais résumer ma vie aujourd’hui avec vous, je dirais que c’est d’abord des rencontres, \
 des gens qui m’ont tendu la main, peut-être à un moment où je ne pouvais pas, où j’étais seul chez \
 moi. Et c’est assez curieux de se dire que les hasards, les rencontres forgent une destinée… \
 Parce que quand on a le goût de la chose, quand on a le goût de la chose bien faite, le beau geste, \
 parfois on ne trouve pas l’interlocuteur en face, je dirais, le miroir qui vous aide à avancer. \
 Alors ce n’est pas mon cas, comme je le disais là, puisque moi au contraire, j’ai pu ; \
 et je dis merci à la vie, je lui dis merci, je chante la vie, je danse la vie… \
 Je ne suis qu’amour ! Et finalement, quand beaucoup de gens aujourd’hui me disent : \
 « Mais comment fais-tu pour avoir cette humanité ? » Eh bien je leur réponds très simplement, \
 je leur dis que c’est ce goût de l’amour, ce goût donc qui m’a poussé aujourd’hui à entreprendre \
 une construction mécanique, mais demain, qui sait, peut-être simplement à me mettre au service de \
 la communauté, à faire le don, le don de soi…" #We use a very long text so that statistic-based methods converge.
Key_caesar = 13
Key_vigenere = "ensae"
Key_substitution = {'a': 't',  'b': 'x',  'c': 'u',  'd': 'c',  'e': 'd',
                    'f': 'q',  'g': 'i',  'h': 'h',  'i': 'r',  'j': 'w',
                    'k': 'j',  'l': 'z',  'm': 'f',  'n': 'y',  'o': 'v',
                    'p': 'b',  'q': 'm',  'r': 'k',  's': 'g',  't': 'n',
                    'u': 'e',  'v': 'o',  'w': 'l',  'x': 'p',  'y': 'a',
                    'z': 's'}

def unit_test_caesar():
    """
    This function checks whether the caesar_cipher is invertible and whether it is 
    breakable.
    """
    
    global Message_test
    global Key_caesar
    
    encrypted_message = caesar.encrypt(Message_test, Key_caesar)
    decrypted_message_with_key = caesar.decrypt(encrypted_message, Key_caesar)[0]
    decrypted_message_without_key, key_found = caesar.decrypt(encrypted_message)
    
    #We know that the decrypted_message may not contain accented characaters, 
    #so before asserting that decrypted_message == Message_test, we clear a bit
    #the Message_test.
    if decrypted_message_with_key != s.clear(Message_test):
        print(Message_test, Key_caesar, "\n")
        print(encrypted_message, "\n")
        print(decrypted_message_with_key)
        raise Exception("Le cryptage César n'est pas inversible lorsque l'on lui donne la clef.")
    
    #We know check whether or not we are able to decrypt without the key.
    if decrypted_message_without_key != s.clear(Message_test):
        print(Message_test, Key_caesar, "\n")
        print(encrypted_message, "\n")
        print(decrypted_message_without_key, key_found)
        raise Exception("Le programme n'arrive pas à craquer la clef du cryptage César.")
    else:
        print("Cryptage de César : RAS.\n")

def unit_test_vigenere():
    """
    This function checks whether the vigenere_cipher is invertible and whether it is 
    breakable.
    """
    
    global Message_test
    global Key_vigenere
    
    encrypted_message = vigenere.encrypt(Message_test, Key_vigenere)
    decrypted_message_with_key = vigenere.decrypt(encrypted_message, Key_vigenere)[0]
    decrypted_message_without_key, key_found = vigenere.decrypt(encrypted_message)
    
    #We know that the decrypted_message may not contain accented characaters, 
    #so before asserting that decrypted_message == Message_test, we clear a bit
    #the Message_test.
    if decrypted_message_with_key != s.clear(Message_test):
        print(Message_test, Key_vigenere, "\n")
        print(encrypted_message, "\n")
        print(decrypted_message_with_key)
        raise Exception("Le cryptage de Vigenere n'est pas inversible lorsque l'on lui donne la clef.")
    
    #We know check whether or not we are able to decrypt without the key.
    if decrypted_message_without_key != s.clear(Message_test):
        print(Message_test, Key_vigenere, "\n")
        print(encrypted_message, "\n")
        print(decrypted_message_without_key, key_found)
        raise Exception("Le programme n'arrive pas à craquer la clef du cryptage de Vigenere.")
    else:
        print("Cryptage de Vigenere : RAS.\n")

def unit_test_substitution():
    """
    This function checks whether the vigenere_cipher is invertible and whether it is 
    breakable.
    """
    
    global Message_test
    global Key_substitution
    
    encrypted_message = substitution.encrypt(Message_test, Key_substitution)
    decrypted_message_with_key = substitution.decrypt(encrypted_message, Key_substitution)[0]
    decrypted_message_without_key, key_found = substitution.decrypt(encrypted_message)
    differences = substitution.distanceBetweenPermutations(Key_substitution, key_found, True)
    
    #We know that the decrypted_message may not contain accented characaters, 
    #so before asserting that decrypted_message == Message_test, we clear a bit
    #the Message_test.
    if decrypted_message_with_key != s.clear(Message_test):
        print(Message_test, Key_substitution, "\n")
        print(encrypted_message, "\n")
        print(decrypted_message_with_key)
        raise Exception("Le cryptage par subsitution n'est pas inversible lorsque l'on lui donne la clef.")
    
    #We know check whether or not we are able to decrypt without the key.
    #In the case of the substitution Cipher, if the program finds "j'aime les grites" instead 
    #of "j'aime les frites", we still want to say that it works. 
    #In other word, what matters is the number of errors: if there are enough rightly deciphered
    #text, we humans understand the message, so it's okay to stop.
    if decrypted_message_without_key != s.clear(Message_test) and differences > 5:
        print(Message_test, Key_substitution, "\n")
        print(encrypted_message, "\n")
        print(decrypted_message_without_key, key_found, differences)
        raise Exception("Le programme n'arrive pas à craquer la clef du cryptage par substitution.")
    
    else:
        print("Cryptage de Vigenere : RAS.\n")
    
unit_test_caesar()
unit_test_vigenere()
unit_test_substitution()

