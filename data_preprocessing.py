# Preprocess the chorales data to extract the note tone and durations only
# The csv has the data in the form name1, value1, name2, value2, etc. We will extract the values and put
# them into a panda dataframe with appropriate headers

# Data Set Information:
# https://archive.ics.uci.edu/ml/datasets/Bach+Chorales
# Sequential (time-series) domain. Single-line melodies of 100 Bach chorales (originally 4 voices). 
# The melody line can be studied independently of other voices. 
# The grand challenge is to learn a generative grammar for stylistically valid chorales 
# (see references and discussion in "Multiple Viewpoint Systems for Music Prediction"). 
# 
# 
# Attribute Information:
# 
# Number of Attributes: 6 (nominal) per event 
# 
# (a) start-time, measured in 16th notes from chorale beginning (time 0) 
# (b) pitch, MIDI number (60 = C4, 61 = C#4, 72 = C5, etc.) 
# (c) duration, measured in 16th notes 
# (d) key signature, number of sharps or flats, positive if key signature has sharps, negative if key signature has flats 
# (e) time signature, in 16th notes per bar 
# (f) fermata, true or false depending on whether event is under a fermata 
# 
# Attribute domains (all integers): 
# 
# (a) {0,1,2,...} 
# (b) {60,...,75} 
# (c) {1,...,16} 
# (d) {-4,...,+4} 
# (e) {12,16} 
# (f) {0,1} 
# 
# 
# Relevant Papers:
# 
# Conklin, Darrell and Witten, Ian. 1995. Multiple Viewpoint Systems for Music Prediction. 
# Journal of New Music Research. 24(1):51-73. 

import pandas as pd
# print("pandas Successfully Imported")
import numpy as np
# print("numpy Successfully Imported")

# Function to make notes of the form (pitch, dur) and return a dataframe containing the music in that format
def preprocess_notes_as_array(keysig = False):
    
    '''Imports the chorales.csv dataset, and returns a pandas dataframe containing the note information.
    
    Arguments: keysig -- tells the function whether to take the key signature information into account.
                            If keysig = False (which is the default), then notes will have the form (pitch, duration).
                            If keysig = True, then notes will have the form (pitch, duration, key signature)
    '''
    
    # Set the number of columns to be imported. This is based on the longest row. The dataframe will have many 
    # entries that are None or NaN.
    
    # Inputs: 
    numcols = 1034
    usecols = np.arange(numcols)
    
    # Read the data
    data = pd.read_table('data/chorales.csv',
                         sep=',', names=usecols, engine='python', header=None)
    # Remove the first column and every other column which contain attribute names. 
    # The first column is an unneeded index column.
    data = data.iloc[:,2::2]
    # print("data Successfully Read")
    
    
    # Create the desired column names using the attribute names. We make each one unique 
    # by adding a trailing number.
    colnames = []
    for i in range(((len(data.columns)) // 6)):
        colnames = colnames + ['st{}'.format(i + 1), 'pitch{}'.format(i + 1), 'dur{}'.format(i + 1), 'keysig{}'.format(i + 1)
                               , 'timesig{}'.format(i + 1), 'fermata{}'.format(i + 1)]
    # Set the new column names
    data.columns = colnames
    
    # Zip the pitchi and duri columns into a new column notei for each i
    # The entry in each not column will be of the form (pitch, dur).
    if keysig == False:
        for i in range((len(data.columns) // 6)):
           data['note{}'.format(i + 1)] = list(zip(data['pitch{}'.format(i + 1)], data['dur{}'.format(i + 1)]))
    else:
        for i in range((len(data.columns) // 6)):
           data['note{}'.format(i + 1)] = list(zip(data['pitch{}'.format(i + 1)], data['dur{}'.format(i + 1)], 
                                                   data['keysig{}'.format(i + 1)]))
    # Extract only the columns whose name starts with note and create our desired dataframe df containing only
    # those columns.
    filter_col = [col for col in data if col.startswith('note')]
    df = data[filter_col]
    # print("Created dataframe containing the notes successfully.")
    # print("Sample:\n{}".format(df.iloc(1)[50:]))
    return df

import math
# Function to make a mask indicating when the first element of a note is nan (i.e there is no note there)
def array_is_nan(array):
    
    '''Function to make a mask indicating when the first element of a note is nan (i.e there is no note there).'''
    
    mask = []
    for i in array:
        if math.isnan(np.float32(i[0])):
            mask = mask + [True]
        else:
            mask = mask + [False]
    return mask


# Function to return the first num_notes of chorale num_chorale, with or without the key signature information
def chorale_intro(num_notes = 10, num_chorale = 0, keysig = False):
    
    '''Return the first num_notes of chorale num_chorale, with or without the key signature information.
    
    Arguments: num_notes (optional) - the number of initial notes to take
               num_chorale (optional) - the number of the chorale to extract from
               keysig (optional) - whether or not to take the key signature information
    '''
       
    df = preprocess_notes_as_array(keysig = keysig)
    
    df = df.iloc[num_chorale,:]
    intro = df.values[0:num_notes]
    
    return intro

