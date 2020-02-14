import  pickle
import os


def checknote(note,nota):
    i = 0
    while i < len(note) and note[i] != nota:
        i += 1
    return i

def compute(list, part):

    for k in list:
        key = k[0] + ',' + k[1] + ',' + k[2] + ',' + k[3]
        if key not in part:
            part[key] = [[k[4]], k[5], [k[6]]]
        else:
            part[key][1] += k[5]
            index=checknote(part[key][0],k[4])
            if index>=len(part[key][0]):
                part[key][0].append(k[4])
                part[key][2].append(k[6])
            else:
                part[key][2][index]+=k[6]
    return part


Soprano =  Alto = Tenore = Basso = dict()

for file in os.listdir("../resultProb"):
    fout = pickle.load(open("../resultProb" + '/' + file, 'rb'))
    for part in fout:
        if part == "Soprano":
            Soprano = compute(fout[part], Soprano)
        elif part == "Alto":
            Alto = compute(fout[part], Alto)
        elif part == "Tenore":
            Tenore = compute(fout[part], Tenore)
        elif part == "Basso":
            Basso = compute(fout[part], Basso)

pickle.dump(Soprano, open("../finalProb" + '/Soprano.pickle', 'wb'))
pickle.dump(Alto, open("..r/finalProb" + '/Alto.pickle', 'wb'))
pickle.dump(Tenore, open("../finalProb" + '/Tenore.pickle', 'wb'))
pickle.dump(Basso, open("../finalProb" + '/Basso.pickle', 'wb'))







