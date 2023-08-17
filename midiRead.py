import mido
import math


def test(midi):
    print('reading...')
    allNotes = set()
    allDelay = set()
    for msg in midi.play():
        print(msg)
        if msg.type == 'note_on':
            allNotes.add(msg.note)
        elif msg.type == 'note_off':
            allDelay.add(msg.time)
    allNotes,allDelay = list(allNotes),list(allDelay)
    allNotes.sort()
    allDelay.sort()
    minP,maxP,minT = allNotes[0], allNotes[-1],allDelay[0]
    if minT == 0:
        idx = 1
        while minT == 0 :
            minT = allDelay[idx]
            idx += 1
    #pitchRange = max - min + 1
    return minP,minT



def createSequence(midiFileName,tick=1):
    midi = mido.MidiFile(midiFileName)
    minP,minT = test(midi)
    print(minP,minT)
    pitchDifference = minP
    for msg in midi.play():
        print(msg)
        if msg.type == 'note_on':
            yield msg.note - pitchDifference
        elif msg.type == 'note_off':
            if msg.time == 0 :
                continue
            t = msg.time/minT
            t = math.ceil(t)
            print(t)
            for i in range((tick * t)-1):
                yield None




if __name__ == '__main__':
    midi = mido.MidiFile('OMR.mid')
    for msg in midi.play():
        if msg.type == 'note_off':
            print(msg.time)

            print(msg.time / 0.116279)
    print()