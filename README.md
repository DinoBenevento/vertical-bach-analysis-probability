# **Vertical Bach Analysis Probability**
This project was born on the idea to calculate the probability of all possible note repetitions after each single chord in the 4-voice Bach chorales.

All Bach 4-voice chorales are scanned with the library **music21** and for each chorale, a .pickle file is generated. In such files there are several features: the vertical chord, the numbers of occurences of the chord, its occurances, and the relationship between each note played after the chord for every voice.

- VerticalAnalysis: Source code for Bach's chorales analysis.

## Result
The folder **saveProb** contains four .txt files, one for each voice.
Each file contains every chord that is played, and for each chord the probability to find a certain note.

The files are formatted as the following:

[Chord]; [Note]; [Probability to find Note after Chord]
