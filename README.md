# SimplePianoUI
## Introduction
A most simple piano UI, created merely due to my curiosity in musical theory. Including some basic functions like changing instrument, metre, tempo and octave. It is able to display tone features (experimental), save some short notes and features instant play or pause.

## Usage

- 25 keys pianoroll with alterable octave, playing notes when clicking or using keyboard. **Z to M** on keyboard map to _seven white keys on the left_. **S, D, G, H, J** map to _five black keys on the left_. **Q to I** on the keyboard map to _eight white keys on the right_, **2, 3, 5, 6, 7** map to _five black keys on the right_
![pianoroll](/display/gifs/pianoroll.gif) 

- You can change length per note(LPN), metre, tempo(BPM), root note, tonic modes and instrument using the option boxes above the pianoroll.
![options](/display/gifs/options.gif) 

- Display mode keys according to the tonic mode. In heptatonic modes, I note is yellow, III and V notes are red, other notes are green. In pentatonic modes, I note is yellow, III and IV notes are red, other notes are green.![options](/display/gifs/mode_display.gif) 

- Record notes and rests in a MusicSegment object, the length of the current note could be altered using LPN box. You can plot the notes in a new window, delete the last notes, play notes and save the current segment in a .json file.
![options](/display/gifs/new_segment_and_save.gif) 

- Open an existing segment file and continue.
![options](/display/gifs/open_existing.gif) 