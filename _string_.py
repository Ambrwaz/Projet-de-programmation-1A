# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 17:47:27 2018

@author: Navigateur_2
"""

import math

Alphabet = 'abcdefghijklmnopqrstuvwxyz'
 
frenchLogVraisemblance = -2.173238905072561 #This has been calculted using the file 'French_language.txt'.

def index_of_coincidence(message, cleared = False):
    
    """
    Calculates the index of coincidence of the message.
    """
    
    assert type(message) == str
    assert type(cleared) == bool
    
    global Alphabet
    
    #If the message is not cleared, we clear it.
    if (cleared == False):
        message = clear(message)
    
    #Then we calculate the index of coincidence.
    number_Of_Characters = 0
    coincidence_index = 0
    for letter in Alphabet:
        counter = message.count(letter)
        letter_probability = (counter*(counter-1))
        coincidence_index += letter_probability
        number_Of_Characters += counter
    coincidence_index /= (number_Of_Characters*(number_Of_Characters-1))
    
    return coincidence_index
    

def is_language(message='', IC=0.0, mode='is', language='French', cleared = False):
    
    """
    If mode = is, verifies if the message belongs to the given language.
    If mode = which, checks whose the language of the given message.
    """
    
    assert type(message) == str
    assert type(mode) == str and mode in ['is', 'which']
    assert type(language) == str
    assert type(cleared) == bool
    assert type(IC) == float
    
    #If the message is not cleared, we clear it.
    if (cleared == False):
        message = clear(message)
    
    #Firstly, we define the list of each IC by language and we calculate the IC
    #of the message.
    list_of_IC = {'French':0.0778, 'English':0.0667, 'German':0.0762}
    
    #We also take into account the fact that the message is given, or if the IC
    #is given.
    if (message == ''):
        message_IC = IC
    else:
        message_IC = index_of_coincidence(message, cleared = False)
    
    #If the mode is 'is', we verify if the message belongs to the language by 
    #looking at its IC.
    if (mode == 'is'):
        language_IC = list_of_IC[language]
        min_born = language_IC - 0.008
        max_born = language_IC + 0.008
        if (message_IC >= min_born and message_IC <= max_born):
            return True
        else:
            return False
    
    #If the mode is 'which', we check which language has the nearest IC and 
    #return it.
    if (mode == 'which'):
        deviation = 10
        message_language = ''
        for key, value in list_of_IC.items():
               deviation_value = abs(value-message_IC)
               
               if (deviation_value < deviation):
                   deviation = deviation_value
                   message_language = key
        
        return message_language




def clear(message, doWeRemovePonctuation = False, doWeRemoveMultipleSpaces = False):
    
    """
    Replaces each accented character by a non-accented character.
    """
    
    global Alphabet
    
    assert type(message) == str
    
    #List of each accented character and their associated non-accented 
    #character.
    accented_characters = 'âäàáéèêëíìïîùúûüôöòóýÿçœñ'
    linked_characters_list = {'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a',
                              'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                              'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
                              'ò': 'o', 'ó': 'o', 'ô': 'o', 'ö': 'o',
                              'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
                              'ý': 'y', 'ÿ': 'y',
                              'ç': 'c',
                              'œ': 'oe',
                              'ñ': 'n'}

    
    #Firstly, we transform the message into lowercase message.
    message = message.lower()
    
    #Cleared message
    cleared_message = ''
    
    #Secondly, we clear the message.
    for character in message:
        
        #If the character is non-accented, then we saved it, otherwise we
        #clear it.
        new_character = character
        if character in accented_characters:
            new_character = linked_characters_list[character]
            
        #If the option doWeRemovePonctuation is True, then we replace each ponctuation mark by a space.
        if (doWeRemovePonctuation == True):
            if new_character not in Alphabet:
                new_character = " "
                
        #Finally, if doWeRemoveMultipleSpaces is True, then we do so.
        if (doWeRemoveMultipleSpaces == True):
            if (new_character == " ") and len(cleared_message)>0 and cleared_message[-1] == " ":
                new_character = ""
                
        #Then we add the new_character into the cleared message.
        cleared_message += new_character
    
    return cleared_message


#The next function determines the degree of "frenchness" of a text.
def logvraisemblance(text, langage_bigram_stats):
    """
    This function returns an indicator of how much the given text is french (or english or german, 
    etc., depending on the data given in langage_bigram_stats).
    
    
    For a genuine french text, the result will average ENTERVALUE
    
    Examples: text = "pomme de terre", N = length of text = 24, so we return:
         -> 1/N * (log(proba('po')) + log(proba('om')) + log(proba('mm')) + ... + log(proba('re')))
         
    """
    
    #We first clear the text.
    cleared_text = clear(text, True, True)
    result = math.log(langage_bigram_stats[" "][cleared_text[0]]) #We initiate the result with the probability of starting with the first character.
    N = len(cleared_text)
    for i in range(N-1):
        firstLetter = cleared_text[i]
        secondLetter = cleared_text[i+1]
        result += math.log(langage_bigram_stats[firstLetter][secondLetter])
    
    #At last we normalize the result and return it.
    return result/N

    
    




















