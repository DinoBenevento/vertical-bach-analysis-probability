from music21 import *
from src.CompositionAndPositionStruct import *
import pickle

#function to read the 4 voices
def verticalAnalysis(score, name_chorale):
    i = -1
    #list for the notes played in a voice
    support_score_voice = []
    for entry in score.recurse():
        if isinstance(entry, stream.Part):
            #every time there is a new Part, there is a new instrument
            score_voice = []
            i = i + 1
            support_score_voice.append(score_voice)
        if isinstance(entry, stream.note.Note) or isinstance(entry, stream.note.Rest) or isinstance(entry, stream.chord.Chord):
            score_voice.append(entry)


    dictNotes = dict()
    i = 0
    j = 0
    lenMin = shortest_voice(support_score_voice)
    while (j < lenMin):
        iNotes = get_notes(support_score_voice, i)
        for note in iNotes:
            #append the note with the relative voice into the dictionary
            dictNotes.setdefault(i, []).append(note)
        i += 1
        j += 1

    get_vertical_notes(dictNotes, name_chorale)

#funtion to check the shortest voice in the composition
def shortest_voice(support_score_list):
    min = 100000000
    i = 0
    while i < len(support_score_list):
        if min > len(support_score_list[i]):
            min = len(support_score_list[i])
        i += 1
    return min

#funtion to get the vertical notes played in the instant i
def get_notes(support_score_voice, i):
    k = 0
    iNotes = []
    while k < len(support_score_voice):
        iNotes.append(support_score_voice[k][i])
        k += 1
    return iNotes


def get_vertical_notes(dictNotes, name_chorale):
    vertical_array = []
    vd = dictionary_voice()
    i = 0
    vl = voiceLeading.Verticality(dictNotes)
    while i < len(dictNotes):
        vertical_array.append(vl.getObjectsByPart(i)) #in vertical_array now every cel contains the notes play in the instant i
        i += 1
    i = 0
    cmpP_list = []
    while i < len(vertical_array):
        if(checkIncmpP(cmpP_list, vertical_array[i])):
            cmpP = CompositionPosition()
            cmpP.add_composition(vertical_array[i])
            cmpP.add_position(setPosition(vertical_array, vertical_array[i]))
            cmpP.set_reps(vertical_array.count(vertical_array[i]))
            cmpP_list.append(cmpP)
        i += 1

    i = 0
    index_vd = 0
    temp = {"A": "Soprano", "B": "Alto", "C": "Tenore", "D": "Basso"}
    save_dict = {"Soprano": [], "Alto": [], "Tenore": [], "Basso": []}
    while i < len(cmpP_list):
        el = cmpP_list[i]
        positions = el.positions
        proc_notes = []
        for index in positions:
            if len(vertical_array) > index + 1:
                for elem in vertical_array[index + 1]:
                    proc_notes.append([elem, vd[index_vd]])
                    index_vd += 1
                index_vd = 0
        i += 1
        save_dict = save_files(proc_notes, el, temp, save_dict)
    pickle.dump(save_dict, open("../resultProb" + '/' + name_chorale + '.pickle', 'wb'))



def save_files(proc_notes, el, temp, save_dict):
    j = 0
    saved_list = []
    while j < len(proc_notes):
        cnt = proc_notes.count(proc_notes[j])
        #cnt is a count for the occurences of the notes (proc_notes[j]) after the chord (el.composition[0])
        #el.reps is the number of the occurences of the chord (composition[0]) into chorales
        saved_list.append([el.composition[0], proc_notes[j], el.reps, cnt])
        j += 1
    save_dict = split_file(saved_list, temp, save_dict)
    return save_dict



def split_file(saved_list, temp, save_dict):

    for elem in saved_list:
        if isinstance(elem[0][0], note.Note):
            nomenota1 = str(elem[0][0].pitch)
        if isinstance(elem[0][0], note.Rest):
            nomenota1 = 'Rest'
        if isinstance(elem[0][1], note.Note):
            nomenota2 = str(elem[0][1].pitch)
        if isinstance(elem[0][1], stream.note.Rest):
            nomenota2 = 'Rest'
        if isinstance(elem[0][2], note.Note):
            nomenota3 = str(elem[0][2].pitch)
        if isinstance(elem[0][2], note.Rest):
            nomenota3 = 'Rest'
        if isinstance(elem[0][3], note.Note):
            nomenota4 = str(elem[0][3].pitch)
        if isinstance(elem[0][3], note.Rest):
            nomenota4 = 'Rest'
        if isinstance(elem[1][0], note.Note):
            succ_note = str(elem[1][0].pitch)
        if isinstance(elem[1][0], note.Rest):
            succ_note = 'Rest'
        save_dict[temp[elem[1][1]]].append([nomenota1, nomenota2, nomenota3, nomenota4, succ_note, elem[2], elem[3]])
    return save_dict

#funtion to check if
def checkIncmpP(cmpP_list, el):

    for el_cmpP in cmpP_list:
        if el_cmpP.composition[0] == el:
            return False
    return True

#funtion to check if a vertical chord is repeated into the composition and append the positions in witch is repeted
def setPosition(vertical_array, element):
    positions = []
    i = 0
    while i < len(vertical_array):
        if vertical_array[i] == element:
            positions.append(i)
        i += 1
    return positions

#function to create a dictionary to indicate with a letter the voices
def dictionary_voice():
    import string
    d = dict(enumerate(string.ascii_uppercase, 0))
    return d

#check if the chorale has only 4 voices
def check_part(chorale):
    i = 0
    for entry in chorale.recurse():
        if isinstance(entry, stream.Part):
            i = i + 1
    if i == 4:
        return True
    return False


#get all score and chorale name
for chorale, name in zip(corpus.chorales.Iterator(), corpus.chorales.Iterator(returnType='filename')):
    if check_part(chorale):
        verticalAnalysis(chorale, (name.replace("bach/", "")).replace(".", "-"))


