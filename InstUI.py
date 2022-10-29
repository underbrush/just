from tkinter import *
from Instrument import *
from Functions import *
from NoteUI import *

class InstUI:
    def __init__(self, root, time, speed):
        self.inst = Instrument(tri, const, 0, 0, time, speed = speed)
        self.wavtype = StringVar()
        self.baseframe = Frame(root)
        self.baseframe.grid()
        self.mframes = [Frame(self.baseframe), Frame(self.baseframe), Frame(self.baseframe)]
        for i in range(len(self.mframes)):
            self.mframes[i].grid(row = 1, column = i)
        self.name = Label(self.baseframe, text = "Name")
        self.name.grid(row = 0, column = 1)
        self.volume = Scale(self.baseframe, from_ = 0, to = 100, orient = HORIZONTAL, length = 150)
        self.volume.grid(row = 2, column = 1)
        self.mUI = Button(self.baseframe, text = "Edit Notes", command = lambda:self.makeUI())
        self.mUI.grid(row = 3, column = 1)
        self.rButtonSetup()
        self.tSetup()
        self.aSetup()
        self.u = None

    def rButtonSetup(self):
        self.rb = []
        self.rb.append(Radiobutton(self.mframes[0], text = "Triangle wave", variable = self.wavtype, value = "tri", command = self.hideH))
        self.rb.append(Radiobutton(self.mframes[0], text = "CSaw wave", variable = self.wavtype, value = "tri2", command = self.showH))
        self.rb.append(Radiobutton(self.mframes[0], text = "Square wave", variable = self.wavtype, value = "sqr", command = self.hideH))
        self.rb.append(Radiobutton(self.mframes[0], text = "Sine wave", variable = self.wavtype, value = "sin", command = self.hideH))
        self.rb.append(Radiobutton(self.mframes[0], text = "Sawtooth wave", variable = self.wavtype, value = "saw", command = self.hideH))
        self.rb.append(Radiobutton(self.mframes[0], text = "Hexagon wave", variable = self.wavtype, value = "hxg", command = self.showH))
        self.rb.append(Radiobutton(self.mframes[0], text = "Custom wave", variable = self.wavtype, value = "cus", command = self.showH))
        for i in range(len(self.rb)):
            self.rb[i].grid(row = i, column = 0)
        self.rb[0].select()
        self.he = Entry(self.mframes[0])

    def showH(self):
        self.he.grid(row = 7, column = 0)

    def hideH(self):
        self.he.grid_forget()
        self.mframes[0].update()

    def tSetup(self):
        self.overtones = [1]
        self.ovtlabels = [Label(self.mframes[1], text = "Fundamental: 1"),\
                          Label(self.mframes[1], text = "Current Timbre:"),\
                          Label(self.mframes[1], text = "Higher partials, spaced by commas:")]
        for i in self.ovtlabels:
            i.pack()
        self.ovt = Entry(self.mframes[1])
        self.ovt.pack()
        self.confirmovt = Button(self.mframes[1], text = "Confirm", command = self.confOvt)
        self.confirmovt.pack()
 
    def confOvt(self):
        if self.ovt.get():
            self.overtones = [1]
            for i in self.ovt.get().split(","):
                v = float(i)
                self.overtones.append(v)
            self.ovtlabels[1]["text"] = "Current Timbre: " + self.ovt.get()

    def aSetup(self):
        self.artype = StringVar()
        self.arb = []
        self.arb.append(Radiobutton(self.mframes[2], text = "Constant", variable = self.artype, value = "const"))
        self.arb.append(Radiobutton(self.mframes[2], text = "Wedge", variable = self.artype, value = "wedge"))
        self.arb.append(Radiobutton(self.mframes[2], text = "Ramp", variable = self.artype, value = "ramp"))
        self.arb.append(Radiobutton(self.mframes[2], text = "Swell", variable = self.artype, value = "swell"))
        self.arb.append(Radiobutton(self.mframes[2], text = "Bevel", variable = self.artype, value = "bevel"))
        for i in self.arb:
            i.pack()
        self.arb[0].select()
        self.pslider = Scale(self.mframes[2], from_ = 0, to = 100, orient = HORIZONTAL, length = 150)
        self.pslider.pack()

    def updateInst(self):
        typ = self.wavtype.get()
        if typ != "cus":
            if typ == "tri":
                atyp = tri
            elif typ == "sqr":
                atyp = sqr
            elif typ == "sin":
                atyp = sin
            elif typ == "hxg":
                atyp = get_hxg((float(self.he.get()) if self.he.get() else 1))
            elif typ == "tri2":
                atyp = get_tri2((float(self.he.get()) if self.he.get() else 0))
            elif typ == "saw":
                atyp = saw
            else:
                print(typ)
            self.inst.set_wave(timb(atyp, self.overtones))
        else:
            instrument = self.he.get()
            d = 440
            if instrument[-1] in [str(i) for i in range(0, 10)]:
                d = int(instrument[-3:])
                instrument = instrument[:-3]
                #print(instrument)
            if instrument[-1] in ["v", "|"]:
                self.inst.set_wave(custom(instrument, default = d))
            else:
                self.inst.set_wave(custom2(instrument))
        artyp = self.artype.get()
        if artyp == 'const':
            self.inst.set_art(const)
        elif artyp == 'wedge':
            self.inst.set_art(wedge)
        elif artyp == 'ramp':
            self.inst.set_art(ramp)
        elif artyp == 'swell':
            self.inst.set_art(swell)
        elif artyp == 'bevel':
            self.inst.set_art(bevel)
        self.inst.set_volume(self.volume.get()/100)
        self.inst.set_point(self.pslider.get()/100)
        
    def makeUI(self):
        if self.u:
            try:
                self.u.window.destroy()
            except TclError:
                pass
            del self.u
        self.u = NoteUI(self.inst, self.name["text"])
