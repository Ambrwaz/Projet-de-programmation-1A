# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:22:15 2022

@author: kerya
"""


import re
import time
import random
import _string_ as s

#Le but de ce fichier est de générer des statistiques intéressantes sur la langue française.
#-----------VARIABLES----------------------------------------------------------


#Normal Paths
Dictionary_path = 'French_language.txt'
Statistics_path = 'Statistics.txt'
Archives_path = 'Archives.txt'

##Test Paths
#Dictionary_path = 'test_language.txt'
#Statistics_path = 'test_Statistics.txt'

#In this dictionary will be saved the needed probabilities which have been read
Bigram_statistics = {}
for letter1 in s.Alphabet:
    Bigram_statistics[letter1] = {}
    for letter2 in s.Alphabet:
        Bigram_statistics[letter1][letter2] = 1e-6 #We put this probability not equal to 0 because we sometimes like to take the log of it.

#-----------VARIABLES----------------------------------------------------------

#######################   BLOCK-0   ###########################################
#Useful functions

#This function transforms the values of a dictionary into probabilities.
def probabilities(dictionary):
    
    #We calculate the sum of the values
    values_sum = 0
    for value in dictionary.values():
        values_sum += value
        
    #Then we calculate the probabilities of every keys
    for key in dictionary.keys():
        dictionary[key] = float(dictionary[key])/values_sum
    
    return dictionary

#This function takes into account the weight of each keys in the random print
def weights_random_choice(dictionary):
    
    #We random a number between 0 and 1
    choice = random.random()
    cumulated_frequencies = 0
#    
#    print("APPEL DE LA FONCTION RANDOM")
#    print("[choice = {}][cumulated_frequencies = {}]".format(choice, cumulated_frequencies))
    
    for key in dictionary.keys():
        
        chosen_value = dictionary[key]
        cumulated_frequencies += dictionary[key]
#        print("[key = {}][chosen_value = {}][cumulated_frequencies = {}]".format(key, chosen_value, cumulated_frequencies))
        
        if (cumulated_frequencies >= choice):
            chosen_key = key
            break

    return chosen_key, chosen_value


#######################   BLOCK-0   ###########################################
    

#######################   BLOCK-1   ###########################################
#This block is only useful if the Statistics file is empty or does not exist


def generateStats():
    
    global Bigram_statistics
    
    with open(Dictionary_path, 'r', encoding = 'utf8') as file:
        source_text = file.read()
        source_text = source_text.replace("\n", " ")
        
        #We assert the text only contains letters and space without any ponctuation.
        cleared_text = s.clear(source_text, True, True)

        #We now count each occurence of each bigram in the source_text.
        for index, char in enumerate(cleared_text):
            
            if (index == 0):
                previous_char = ' '
            else:
                previous_char = cleared_text[index-1]
            
            #If the key 'previous_char' does not exist, we create it and increment it,
            #else we just increment.
            if previous_char not in Bigram_statistics.keys():
                Bigram_statistics[previous_char] = {}
            
            if char not in Bigram_statistics[previous_char].keys():
                Bigram_statistics[previous_char][char] = 0
            
            Bigram_statistics[previous_char][char] += 1
            
    #We change every counters into probabilities of occurrence
    for key in Bigram_statistics.keys():
        Bigram_statistics[key] = probabilities(Bigram_statistics[key])

    
    #In a new file, we save the results for next use
    with open(Statistics_path, 'w', encoding='utf8') as file:
        file.write("Statistics of each letter to occur after a specific letter.\n")
        for dico_key in Bigram_statistics.keys():
            allItems = sorted(Bigram_statistics[dico_key].items(), key = lambda item: item[1])
            for dico_key2, dico_value2 in allItems:
                file.write('\n[letter1 = {}][letter2 = {}][probability = {}]'.format(dico_key, dico_key2, dico_value2))

    return Bigram_statistics


#######################   BLOCK-1   ###########################################
            
            
#Now that we have calculated the needed probabilities, we have to open and read
#the file which contains these probabilities.


#######################   BLOCK-2   ###########################################

def readStats():
    
    global Bigram_statistics
    
    with open(Statistics_path, 'r', encoding='utf8') as statistics_file:
    
    
        #We define the regular expression we want to check
        expression = "(\[letter1 = )(?P<letter1>[\-'âäàáéèêëíìïîùúûüôöòóýÿç a-z]?[\-'âäàáéèêëíìïîùúûüôöòóýÿç a-z]?)\](\[letter2 = )(?P<letter2>[\-'âäàáéèêëíìïîùúûüôöòóýÿç a-z])\](\[probability = )(?P<probability>[0-9]\.[0-9e\-]*)\]"
        expression = re.compile(expression)
        
        #We examinate each line in the file
        for line in statistics_file.readlines():
            
            #If this expression is found, then we save the data
            is_line_right = expression.search(line)
            if is_line_right is not None:
                letter1 = expression.search(line)['letter1']
                letter2 = expression.search(line)['letter2']
                probability = expression.search(line)['probability']
                
                if letter1 not in Bigram_statistics:
                    Bigram_statistics[letter1] = {}

                Bigram_statistics[letter1][letter2] = float(probability)
    
    return Bigram_statistics

#We don't forget to update the first list.
readStats()
    

if __name__ == '__main__':
    generateStats()
    readStats()








