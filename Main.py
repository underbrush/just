import wave
import math
from Note import *
from Functions import *
from Instrument import *
from NoteUI import *
from InstUI import *

import random

## grey
## timb(sin, [1, 1.25, 1.125, 1.25, 1.3])
## timb(tri, [1, 0.5, 0.3, 0.25, 0.2]) -> 0.6, 0.5, 0.4
## timb(sin, [1, 2, 1, 0.5, 0.25]) -> 0.5, 0.25, 0.125

class MainUI:
    def __init__(self):
        self.root = Tk()
        self.frames = [[Frame(self.root, highlightbackground = "black", highlightthickness = 1) for i in range(2)] for i in range(3)]
        for row in range(len(self.frames)):
            for col in range(len(self.frames[row])):
                self.frames[row][col].grid(row = row, column = col)
        self.uis = [InstUI(self.frames[int(i/2)][i%2], 16, 4410) for i in range(1, 6)]
        for i in range(len(self.uis)):
            self.uis[i].name['text'] = str(i)
        self.masterSetup()
        self.time = 16
        self.speed = 4410

    def masterSetup(self):
        self.nameLabel = Label(self.frames[0][0], text = "Filename:")
        self.nameLabel.grid()
        self.nameEntry = Entry(self.frames[0][0])
        self.nameEntry.grid()
        self.startLabel = Label(self.frames[0][0], text = "Start:")
        self.startLabel.grid()
        self.startEntry = Entry(self.frames[0][0])
        self.startEntry.grid()
        self.endLabel = Label(self.frames[0][0], text = "End:")
        self.endLabel.grid()
        self.endEntry = Entry(self.frames[0][0])
        self.endEntry.grid()
        
        self.renderButton = Button(self.frames[0][0], text = "render (same file)", command = lambda: self.renderSame(self.nameEntry.get(), int(self.startEntry.get()), int(self.endEntry.get())))
        self.renderButton.grid()
        self.renderButton2 = Button(self.frames[0][0], text = "render (different files)", command = lambda: self.renderDiff(self.nameEntry.get(), int(self.startEntry.get()), int(self.endEntry.get())))
        self.renderButton2.grid()
        self.saveButton = Button(self.frames[0][0], text = "save", command = lambda: self.save(self.nameEntry.get()))
        self.saveButton.grid(row = 6, column = 1)
        self.loadButton = Button(self.frames[0][0], text = "load", command = lambda: self.load(self.nameEntry.get()))
        self.loadButton.grid(row = 7, column = 1)
        
        self.tlabel = Label(self.frames[0][0], text = "Time (subdivisions/measure):")
        self.tlabel.grid(row = 0, column = 1)
        self.tentry = Entry(self.frames[0][0])
        self.tentry.grid(row = 1, column = 1)
        self.slabel = Label(self.frames[0][0], text = "Speed (samples/note):")
        self.slabel.grid(row = 2, column = 1)
        self.sentry = Entry(self.frames[0][0])
        self.sentry.grid(row = 3, column = 1)
        self.confirmation = Button(self.frames[0][0], text = "Confirm", command = lambda: self.setMaster())
        self.confirmation.grid(row = 4, column = 1)

    def setMaster(self):
        if self.tentry.get():
            self.time = int(self.tentry.get())
            for i in self.uis:
                i.inst.set_time(int(self.tentry.get()))
        if self.sentry.get():
            self.speed = int(self.sentry.get())
            for i in self.uis:
                i.inst.set_speed(int(self.sentry.get()))

    def renderSame(self, filename, start, end):
        f = wave.open("_Music/" + filename + ".wav", "w")

        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)

        l = []

        v = 0
        for i in self.uis:
            if i.volume.get() > 0:
                v += 1
                i.updateInst()
                l.append(i.inst.quick_render(start, end))

        for i in l[1:]:
            for j in range(len(i)):
                l[0][j] += i[j]

        sfactor = 1/v
        l[0] = [i*sfactor for i in l[0]]

        b = bytearray()

        for s in l[0]:
            n = min(max(-32768, s), 32767)
            y = n if n >= 0 else n+65536
            a = round(min(max(y, 0), 65535))
            g = a%256
            c = a>>8
            b.append(g)
            b.append(c)

        f.writeframes(b)
        f.close()

    def renderDiff(self, filename, start, end):
        for i in range(len(self.uis)):
            self.uis[i].updateInst()
            if self.uis[i].volume.get() > 0:
                f = wave.open("_Music/" + filename + str(i) + ".wav", "w")

                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(44100)

                l = self.uis[i].inst.quick_render(start, end)

                b = bytearray()

                for s in l:
                    n = min(max(-32768, s), 32768)
                    y = n if n >= 0 else n+65536
                    a = round(min(max(y, 0), 65535))
                    g = a%256
                    c = a>>8
                    b.append(g)
                    b.append(c)

                f.writeframes(b)
                f.close()

    def save(self, filename):
        f = open("_Data/" + filename + ".txt", "w")
        f.write(str(self.time) + ',' + str(self.speed) + '\n\n')
        for i in self.uis:
            if i.volume.get() > 0:
                f.write(i.wavtype.get() + '-' + i.he.get() + '~' + str(i.pslider.get()) + '~' + str(i.overtones) + '~' + str(i.volume.get()) + '~' + i.artype.get() + "\n")
                x = i.inst.save()
                for j in x:
                    f.write(j)
                f.write("\n")
        f.close()

    def load(self, filename):
        f = open("_Data/" + filename + ".txt", "r")
        l = f.read()
        l = l.split('\n\n')
        main = l[0].split(',')
        self.time = int(main[0])
        self.tentry.delete(0, 'end')
        self.tentry.insert(0, main[0])
        self.speed = int(main[1])
        self.sentry.delete(0, 'end')
        self.sentry.insert(0, main[1])
        l = l[1:]
        for i in range(len(self.uis)):
            self.uis[i].inst.time = int(main[0])
            self.uis[i].inst.speed = int(main[1])
        for i in range(len(l[:-1])):
            x = l[i].splitlines()
            setup, notes = x[0].split('~'), x[1:]
            self.uis[i].wavtype.set(setup[0].split('-')[0])
            if setup[0].split('-')[0] in ['hxg', 'cus']:
                self.uis[i].showH()
            else:
                self.uis[i].hideH()
            for j in setup[0].split('-')[1:]:
                self.uis[i].he.delete(0, 'end')
                self.uis[i].he.insert(0, j)
            self.uis[i].volume.set(int(setup[3]))
            self.uis[i].overtones = [float(o) for o in setup[2][1:-1].split(',')]
            self.uis[i].pslider.set(int(setup[1]))
            self.uis[i].artype.set(setup[4])
            self.uis[i].inst.clear_notes()
            for j in notes:
                a = [n.split(",") for n in j.split(" ")]
                self.uis[i].inst.add_note(math.floor(int(a[0][0])/self.time), \
                                          int(a[0][0])%self.time, \
                                          int(a[0][1]), \
                                          length = int(a[2][0]), \
                                          acclist = [int(i) for i in a[1]])
        

#root = Tk()


##i = Instrument(timb(tri, [1, 0.2, 0.8]), wedge, 0, 0.15, 16, speed = 8820)
##u = NoteUI(i, "tri")

#i = InstUI(root, 16, 4410, tri, const, 0, 0.2)
m = MainUI()
