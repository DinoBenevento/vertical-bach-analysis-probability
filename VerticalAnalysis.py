from music21 import *
from CompositionAndPositionStruct import *
import pickle

def verticalAnalysis(score, name_chorale):
    i = -1
    support_score_voice = []
    for entry in score.recurse():
        if isinstance(entry, stream.Part):
            score_voice = []
            i = i + 1
            support_score_voice.append(score_voice)
        if isinstance(entry, stream.note.Note) or isinstance(entry, stream.note.Rest) or isinstance(entry, stream.chord.Chord):
            score_voice.append(entry)

    #Sta parte di codice serve per scandire le note suonare per instante e messe nel dizionario, quindi le note delle voci suonate nell'instante 0 stanno come 0:[notes] ecc..
    dictNotes = dict()
    i = 0
    j = 0
    lenMin = shortest_voice(support_score_voice)
    while (j < lenMin):
        iNotes = get_notes(support_score_voice, i)
        for note in iNotes:
            dictNotes.setdefault(i, []).append(note)
        i += 1
        j += 1

    get_vertical_notes(dictNotes, name_chorale)

def shortest_voice(support_score_list):
    min = 100000000
    i = 0
    while i < len(support_score_list):
        if min > len(support_score_list[i]):
            min = len(support_score_list[i])
        i += 1
    return min

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
        save_dict = save_files(proc_notes, el, name_chorale, temp, save_dict)
    pickle.dump(save_dict, open("C:/Users/io/PycharmProjects/SoMusicHelpComposer/resultProb" + '/' + name_chorale + '.pickle', 'wb'))



def save_files(proc_notes, el, name_chorale, temp, save_dict):
    j = 0
    path = "C:/Users/io/Desktop/DatasetNotesStat"
    saved_list = []
    while j < len(proc_notes):
        cnt = proc_notes.count(proc_notes[j])
        #cnt is a count for the occurences of the notes (proc_notes[j]) after the chord (el.composition[0])
        #el.reps is the number of the occurences of the chord (composition[0]) into chorales
        saved_list.append([el.composition[0], proc_notes[j], el.reps, cnt])
        j += 1
    save_dict = split_file(saved_list, name_chorale, temp, save_dict)
    return save_dict



def split_file(saved_list, name_chorale, temp, save_dict):

    # fileSoprano = open(pathDir + '/' + 'Soprano' + name_chorale + '.txt', 'a')
    # fileAlto = open(pathDir + '/' + 'Alto' + name_chorale + '.txt', 'a')
    # fileTenore = open(pathDir + '/' + 'Tenore' + name_chorale + '.txt', 'a')
    # fileBasso = open(pathDir + '/' + 'Basso' + name_chorale + '.txt', 'a')


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
        # if elem[1][1] == 'A':
        #     fileSoprano.write(nomenota1 + ' ' + nomenota2 + ' ' + nomenota3 + ' ' + nomenota4 + ', ' + succ_note + ', ' + str(elem[2]) + ', ' + str(elem[3]) + "\n")
        # if elem[1][1] == 'B':
        #     fileAlto.write(nomenota1 + ' ' + nomenota2 + ' ' + nomenota3 + ' ' + nomenota4 + ', ' + succ_note + ', ' + str(elem[2]) + ', ' + str(elem[3]) + "\n")
        # if elem[1][1] == 'C':
        #     fileTenore.write(nomenota1 + ' ' + nomenota2 + ' ' + nomenota3 + ' ' + nomenota4 + ', ' + succ_note + ', ' + str(elem[2]) + ', ' + str(elem[3]) + "\n")
        # if elem[1][1] == 'D':
        #     fileBasso.write(nomenota1 + ' ' + nomenota2 + ' ' + nomenota3 + ' ' + nomenota4 + ', ' + succ_note + ', ' + str(elem[2]) + ', ' + str(elem[3]) + "\n")

    # fileSoprano.close()
    # fileAlto.close()
    # fileTenore.close()
    # fileBasso.close()


def set_files(pathDir, name_chorale):
    fileSoprano = open(pathDir + '/' + 'Soprano' + name_chorale + '.txt', 'w')
    fileSoprano.write('Accordo, Nota, Prob' + '\n')
    fileSoprano.close()
    fileAlto = open(pathDir + '/' + 'Alto' + name_chorale + '.txt', 'w')
    fileAlto.write('Accordo, Nota, Prob' + '\n')
    fileAlto.close()
    fileTenore = open(pathDir + '/' + 'Tenore' + name_chorale + '.txt', 'w')
    fileTenore.write('Accordo, Nota, Prob' + '\n')
    fileTenore.close()
    fileBasso = open(pathDir + '/' + 'Basso' + name_chorale + '.txt', 'w')
    fileBasso.write('Accordo, Nota, Prob' + '\n')
    fileBasso.close()



def checkIncmpP(cmpP_list, el):

    for el_cmpP in cmpP_list:
        if el_cmpP.composition[0] == el:
            return False
    return True



def setPosition(vertical_array, element):
    positions = []
    i = 0
    while i < len(vertical_array):
        if vertical_array[i] == element:
            positions.append(i)
        i += 1
    return positions


def dictionary_voice():
    import string
    d = dict(enumerate(string.ascii_uppercase, 0))
    return d

def check_part(chorale):
    i = 0
    for entry in chorale.recurse():
        if isinstance(entry, stream.Part):
            i = i + 1
    if i == 4:
        return True
    return False



for chorale, name in zip(corpus.chorales.Iterator(), corpus.chorales.Iterator(returnType='filename')):
    if check_part(chorale):
        verticalAnalysis(chorale, (name.replace("bach/", "")).replace(".", "-"))


