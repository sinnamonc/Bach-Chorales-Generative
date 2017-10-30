# TO DO: Have phrases not go between different chorales - preprocessing.

'''Create chorale melody lines in the style of Bach based on his compositions using a recurrant 
neural network.
This project is based on the keras lstm example for text prediction.
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import pandas as pd
import numpy as np
import random

from utilities import sample
from data_preprocessing import preprocess_notes_as_array
from data_preprocessing import array_is_nan
from chorale_player import play_chorale

# Set keysig to True to include the key signature information in the data, and False to ignore it. 
# Default is False.
keysig = True
# Get the preprocessed data
df = preprocess_notes_as_array(keysig = keysig)
# Convert the dataframe into an array
data_array = df.values
# Reshape the data into a single array
data_array = data_array.reshape(1,data_array.size)[0]
# Identify all of the (nan, nan) entries
index = np.argwhere(array_is_nan(data_array))
# Convert the corpus into a list and delete the (nan,nan) entries
corpus = np.ndarray.tolist(np.delete(data_array, index))

notes = sorted(list(set(corpus)))
print('total notes:', len(notes))
note_indices = dict((n, i) for i, n in enumerate(notes))
indices_note = dict((i, n) for i, n in enumerate(notes))

# cut the corpus in semi-redundant sequences of maxlen notes
maxlen = 10
step = 3
phrases = []
next_notes = []
for i in range(0, len(corpus) - maxlen, step):
    phrases.append(corpus[i: i + maxlen])
    next_notes.append(corpus[i + maxlen])
print('nb sequences:', len(phrases))

print('Vectorization...')
x = np.zeros((len(phrases), maxlen, len(notes)), dtype=np.bool)
y = np.zeros((len(phrases), len(notes)), dtype=np.bool)
for i, phrase in enumerate(phrases):
    for t, note in enumerate(phrase):
        x[i, t, note_indices[note]] = 1
    y[i, note_indices[next_notes[i]]] = 1

# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(notes))))
model.add(Dense(len(notes)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)



# train the model, output generated corpus after each iteration
for iteration in range(1, 60):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(x, y,
              batch_size=128,
              epochs=1)

    start_index = random.randint(0, len(corpus) - maxlen - 1)

    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print()
        print('----- diversity:', diversity)

        generated = []
        phrase = corpus[start_index: start_index + maxlen]
        generated = generated + phrase
        print('----- Generating with seed: "{}"'.format( phrase ))
        
        print('Generated: {}'.format(generated))
        
        for i in range(40):
            z = np.zeros((1, maxlen, len(notes)))
            for t, note in enumerate(phrase):
                #print('note_indices[note]={}'.format(note_indices[note]))
                z[0, t, note_indices[note]] = 1.

            preds = model.predict(z, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_note = indices_note[next_index]
            
            generated = generated + [next_note]

            phrase.append(next_note)
            phrase = phrase[1:]
            #print('phrase {}'.format(phrase))
            
            #sys.stdout.write(next_note)
            #sys.stdout.flush()
        
        file = open('outputs/texts/chorale_iter-{}_diversity-{}.txt'.format(iteration, diversity), 'w')
        try:
            for note in generated:
                file.write('{}\n'.format(note))
        finally:
            file.close()
            
model.save('models/chorales_generation_model_maxlen-{}_keysig-{}.h5'.format(maxlen, keysig))
        