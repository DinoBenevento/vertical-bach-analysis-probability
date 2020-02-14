import os
import pickle


def scanDict(nameVoice):
    fin = pickle.load(open("C:/Users/io/PycharmProjects/SoMusicHelpComposer/finalProb/" + nameVoice + ".pickle", 'rb'))
    fout = open("C:/Users/io/PycharmProjects/SoMusicHelpComposer/saveProb/" + nameVoice + ".txt", 'w')
    fout.write('Accordo;Nota;Prob\n')

    for k in fin:
        for i in range(len(fin[k][0])):
            s = k + ';'
            s += fin[k][0][i]
            s += ';' + str(float(fin[k][2][i]) / float(fin[k][1]))
            fout.write(s + '\n')
    fout.close()



scanDict("Soprano")
scanDict("Alto")
scanDict("Tenore")
scanDict("Basso")