# # 
# # import pandas as pd
# # import numpy as np
# # import random
# # import sys
# # import math
# # 
# # 
# # from data_preprocessing import preprocess_notes_as_array
# # 
# # # Get the preprocessed data
# # df = preprocess_notes_as_array()
# # # Convert the dataframe into an array
# # data_array = df.values
# # # Reshape the data into a single array
# # data_array = data_array.reshape(1,data_array.size)[0]
# # # Remove all of the (nan, nan) entries
# # index = np.argwhere(array_is_nan(data_array))
# # data_array = np.delete(data_array, index)
# 
# import numpy as np
# # from chorale_player import play_chorale
# from ast import literal_eval
# # # read the chorale from file and play
# # file = open('outputs/texts/chorale_iter-59_diversity-1.0.txt', 'r')
# # z = file.readlines()
# # # print(z)
# # chorale = [x.strip('\n') for x in z] 
# # 
# # chorale = [literal_eval(x) for x in chorale]
# # play_chorale(chorale,144)
# 
# from chorale_player import write_chorale
# 
# file = open('outputs/texts/chorale_playground_diversity-0.2.txt', 'r')
# z = file.readlines()
# # print(z)
# chorale = [x.strip('\n') for x in z] 
#  
# chorale = [literal_eval(x) for x in chorale]
# 
# track_name = write_chorale(chorale, track_title = "test_name", extra_last_note = True)
# 
# from chorale_player import play_chorale_midi
# 
# play_chorale_midi(track_name)
# 
# from chorale_player import write_chorale
# from ast import literal_eval
# 
# 
# for diversity in [0.2, 0.5, 1.0, 1.2]:
#     file = open('outputs/texts/chorale_iter-56_diversity-{}.txt'.format(diversity), 'r')
#     z = file.readlines()
# # print(z)
#     chorale = [x.strip('\n') for x in z] 
#  
#     chorale = [literal_eval(x) for x in chorale]
# 
#     track_name = write_chorale(chorale, track_title = "test_name", extra_last_note = True)
# 
#     from chorale_player import play_chorale_midi
# 
#     play_chorale_midi(track_name)

from data_preprocessing import preprocess_notes_as_array
from data_preprocessing import array_is_nan
from data_preprocessing import chorale_intro
from data_preprocessing import midi_transpose
from data_preprocessing import get_chorales_as_list_with_transpositions
from chorale_player import play_chorale
import numpy as np

data = get_chorales_as_list_with_transpositions()
for chorale in data:
    print(chorale)
