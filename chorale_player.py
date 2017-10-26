# Library to play the chorales

import numpy as np
import pyaudio
import math

# Function to return the hertz of a given midi number 
# args midi number and optional value for a
def midi_to_hertz(midi,a=440):
    
    ''' Returns the frequency of a tone given the midi number. 
    
    Arguments: midi - the midi number of the tone (integer).
               a (optional) - declare the frequency of a for tuning, default 440.
    '''
    
    if 11<midi<128:
        hertz = (a / 32) * (2 ** ((midi - 9) / 12))
        return np.float16(hertz)
    else:
        print('midi value must be between 12 and 127 inclusive')
# Example:                
# print('hertz(25) = {}'.format(midi_to_hertz(25)))



# plays a chorale of the form [[note1,dur1],[note2,dur2],...] where the notes are in midi and the dur's 
# are in 16th notes based on the optional argument tempo in bpm
# This sounds pretty terrible. Combine write_chorale and play_chorale_midi for much better results
def play_chorale( chorale , tempo = 66): 
    
    ''' Play a chorale.
    
    Play a chorale of the form [ note1, note2, note3, ... ] where notei = (pitchi, durationi, optionalsi).
    Any entries in notei after the first two are ignored by this function. A note may contain, for example, 
    key signature information, used in training of the chorales_generation net, but that information will be 
    ignored here.
    
    Arguments: chorale -- the chorale as [ note1, note2, note3, ... ]
               tempo -- the tempo at which to play the chorale in beats per minute (bpm) (int) 
    '''
    
    bit_rate = 16000 #number of frames per second/frameset.      
    
    #chorale = np.array(chorale)
    wave_info = ''    
    #print('chorale={}'.format(chorale))
    for note in chorale:
        midi = note[0]
        dur = note[1]
        # print('note={}'.format(note))
        # print('midi={}'.format(midi))
        # print('dur={}'.format(dur))
        if math.isnan(midi) == False:
            frequency = midi_to_hertz(midi) #in Hz, waves per second
            play_time = dur*60/(tempo*4) #in seconds to play sound
        
            if frequency > bit_rate:
                bit_rate = frequency+100

            num_frames = int(bit_rate * play_time)
            total_frames = num_frames % bit_rate
        
            for x in np.arange(num_frames):
                wave_info = wave_info+chr(int(math.sin(x/((bit_rate/frequency)/math.pi))*127+128))    
        else:
            break
    for x in np.arange(total_frames): 
        wave_info = wave_info+chr(128)

    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = bit_rate, 
                    output = True)

    stream.write(wave_info)
    stream.stop_stream()
    stream.close()
    p.terminate()
    
#TO DO: Add support for rests
def write_chorale(chorale, track_title, tempo = 120 , extra_last_note = False):
    
    '''Write a chorale to a midi file. 
    
    Write a chorale of the form [ note1, note2, note3, ... ] where notei = (pitchi, durationi, optionalsi).
    Any entries in notei after the first two are ignored by this function. A note may contain, for example, 
    key signature information, used in training of the chorales_generation net, but that information will be 
    ignored here.
    
    Arguments: chorale -- the chorale as [ note1, note2, note3, ... ]
               track_title -- the name of the track used by the midi file metadata (string)
               tempo -- the tempo at which to save the chorale in beats per minute (bpm) (int)
               extra_last_note (optional) -- if True, repeat the last pitch of the chorale with a whole note (sounds nicer)
                                             if False (default), do not add any extra notes at the end
    '''
    
    
    from midiutil.MidiFile import MIDIFile
    
    
    # create your MIDI object
    mf = MIDIFile(1, adjust_origin = False)  # only 1 track
    track = 0  # the only track

    time = 0  # start at the beginning
    mf.addTrackName(track, time, track_title)
    mf.addTempo(track, time, tempo)

    # add some notes
    channel = 0
    volume = 100
    time = 0
    for note in chorale:
        pitch = np.int(note[0]) #pitch in midi
        dur = np.int(note[1]) #duration in 16th notes
        duration = dur/4  
        
        mf.addNote(track, channel, pitch, time, duration, volume)

        time = time + duration
    # Adds a whole note at the end repeating the previous last note - gives it a nicer ending
    if extra_last_note == True:
        mf.addNote(track, channel, pitch, time, 8, volume)
    # write it to disk
    with open("C:/Users/Craig/eclipse-workspace/test_keras/chorales_generation/outputs/midis/{}.mid".format(track_title), 'wb') as outf:
        mf.writeFile(outf)
    
    return track_title
        
def play_chorale_midi(filename):
    
    '''Play a chorale saved as a midi file.'''
    
    import pygame
    pygame.init()

    pygame.mixer.music.load("outputs/midis/{}.mid".format(filename))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(1000)
