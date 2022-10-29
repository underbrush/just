from Note import Note
import fInfo
from Functions import cancel

class Instrument:
    def __init__(self, wave, art, point, volume, time, speed = 4410):
        self.notes = {}
        self.wave = wave
        self.art = art
        self.point = point
        self.time = time
        self.volume = volume
        self.speed = speed

##    def add_note(self, measure, x, note, octave, length = 1, acclist = [0]*10):
##        dist = measure*self.time + x
##        height = octave*7 + fInfo.note_list.index(note)
##        n = Note(length, acclist = acclist)
##        self.notes[dist, height] = n
##        return dist, height

    def add_note(self, measure, x, y, length = 1, acclist = [0]*10):
        dist = measure*self.time + x
        height = y
        n = Note(length, acclist = acclist)
        self.notes[dist, height] = n
        return dist, height

    def clear_notes(self):
        for i in self.notes:
            del i
        self.notes = {}

    def get_notes(self, x1, x2, y1, y2):
        r = {}
        for x in range(x1, x2):
            for y in range(y1, y2):
                if (x, y) in self.notes.keys():
                    r[x, y] = self.notes[x, y]
        return r

    def quick_render(self, startx, endx):
        n = self.get_notes(startx, endx, 0, 56)
        r = [0]*(endx-startx)*self.speed
        for i in n.keys():
            a, b = i
            value = b%7
            octave = int((b-value)/7)-4
            freq = (fInfo.notes[fInfo.note_list[value]], 1)
            if octave < 0:
                freq = (freq[0], freq[1]*(2**-octave))
            else:
                freq = (freq[0]*(2**octave), freq[1])
            freq = cancel(freq)
            acc = n[i].multiply_acc()
            freq = cancel((freq[0]*acc[0], freq[1]*acc[1]))
            wav = self.art(self.wave(freq, n[i].length*self.speed), self.point)
            d = (a - startx)*self.speed
            for i in range(len(wav)):
                if i+d >= len(r):
                    break
                r[i+d] += wav[i]*self.volume
        return r

    def set_wave(self, wave):
        self.wave = wave

    def set_art(self, art):
        self.art = art

    def set_volume(self, volume):
        self.volume = volume

    def set_point(self, point):
        self.point = point

    def set_time(self, time):
        self.time = time

    def set_speed(self, speed):
        self.speed = speed

    def save(self):
        write = []
        for i in self.notes:
            write.append(str(i[0]) + "," + str(i[1]) + " " + ",".join([str(i) for i in self.notes[i].get_acc()]) + " " + str(self.notes[i].length) + "\n")
        return write
