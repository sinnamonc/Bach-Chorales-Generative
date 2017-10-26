''' A place to load a model and feel it different initial phrases to see what the model does! '''
from data_preprocessing import preprocess_notes_as_array
from data_preprocessing import array_is_nan
from chorales_generation import sample
from data_preprocessing import chorale_intro

import pandas as pd
import numpy as np
import random
from keras.models import load_model
from ast import literal_eval

# Get the preprocessed data
df = preprocess_notes_as_array(keysig = True)
# Convert the dataframe into an array
data_array = df.values
# Reshape the data into a single array
data_array = data_array.reshape(1,data_array.size)[0]
# Identify all of the (nan, nan) entries
index = np.argwhere(array_is_nan(data_array))
# Convert the corpus into a list and delete the (nan,nan) entries
corpus = np.ndarray.tolist(np.delete(data_array, index))

# path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/corpus-datasets/nietzsche.txt')
# corpus = open(path).read().lower()
print('corpus length:', len(corpus))


notes = sorted(list(set(corpus)))
print('total notes:', len(notes))
note_indices = dict((n, i) for i, n in enumerate(notes))
indices_note = dict((i, n) for i, n in enumerate(notes))



filename = 'models/chorales_generation_model_maxlen-10.h5'

model = load_model(filename)

maxlen = 10
# enter an initial phrase of length maxlen
# phrase = [(64, 4, 1), (67, 4, 1), (67, 4, 1), (69, 4, 1), (69, 4, 1), 
#             (71, 4, 1), (71, 4, 1), (71, 4, 1), (74, 4, 1), (72, 4, 1)]
phrase = chorale_intro(num_notes = maxlen, keysig = True)
phrase = np.ndarray.tolist(phrase)
for diversity in [0.2, 0.5, 1.0, 1.2]:
    print()
    print('----- diversity:', diversity)

    generated = []
    generated = generated + phrase
    print('----- Generating with seed: "{}"'.format(phrase))
        
    print('Generated: {}'.format(generated))
        
    for i in range(40):
        z = np.zeros((1, maxlen, len(notes)))
        for t, note in enumerate(phrase):
            z[0, t, note_indices[note]] = 1.

        preds = model.predict(z, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_note = indices_note[next_index]
            
        generated = generated + [next_note]

        phrase.append(next_note)
        phrase = phrase[1:]
        
    file = open('outputs/texts/chorale_playground_diversity-{}.txt'.format(diversity), 'w')
    try:
        for note in generated:
            file.write('{}\n'.format(note))
    finally:
        file.close()

from chorale_player import write_chorale

for diversity in [0.2, 0.5, 1.0, 1.2]:
    file = open('outputs/texts/chorale_playground_diversity-{}.txt'.format(diversity), 'r')
    z = file.readlines()
# print(z)
    chorale = [x.strip('\n') for x in z] 
 
    chorale = [literal_eval(x) for x in chorale]

    track_name = write_chorale(chorale, track_title = "test_name", extra_last_note = True)

    from chorale_player import play_chorale_midi

    play_chorale_midi(track_name)

# If you just save the weights, can you use that to predict without retraining?
