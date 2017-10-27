# SharpestMinds-Application
A project for my SharpestMinds Application.

I implemented a long short term memory neural network using keras with tensorflow backend to generate chorales in the style of Bach. The structure was based on a keras example that uses a lstm network for character generation starting with a corpus of nietzche's writings. 

If you want to try it out, check out the testing_ground jupyter notebook! It allows you to load and compile the network and then enter your own initial segments of music and see what the network comes up with.

With a dataset of the melody lines from some of Bach's chorales (https://archive.ics.uci.edu/ml/datasets/Bach+Chorales) I extract the information into a convenient format (data_preprocessing.py) and use it to train a lstm network (chorales_generation.py). I wrote some functions to save the chorales in text files, and read the text files, write the chorales to midis and play them so you can listen to the generated chorales without an external player. The pygame package makes for nice sounding playback and that is what I use now, but there is an older function that uses pyaudio if you're a fan of music from 80's arcade games or don't have pygame installed!



Really, the dataset is two or three orders of magnitute too small for a lstm network to be particularly effective. The dataset that I used has about 8000 notes, while it would be desirable to have 100,000 or 1,000,000! Still, as a proof on concept it works, and it's fun to play with!

There is a large repository of music (http://kern.humdrum.org/) written in humdrum kern format. It would be great to write a script to read that file format and extract the information in a form that could be reasonably put into a lstm network. Then one would have access to a much larger set of data including many different musical styles and composers.


