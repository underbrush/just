from tkinter import *
from fInfo import note_list, accidental_list, accidental_names
import math
import wave

class NoteUI:
    def __init__(self, inst, title, width = 48, height = 36, spacing = 16):
        self.w, self.h = width, height
        self.s = spacing
        self.inst = inst
        self.time = self.inst.time
        self.pos = (0, 0)

        self.selected = []
        self.clipboard = []
        self.ms = None
        self.labels = [[], []]
        self.buttons = [0] * 4

        self.window = Tk()
        self.window.title(title)
        self.tk_setup()

        self.visible = []
        self.visobj = {}

        self.draw_grid()
        self.reset_screen()

    def tk_setup(self):
        self.frames = (Frame(self.window), Frame(self.window))
        for i in range(len(self.frames)):
            self.frames[i].grid(row = 0, column = i)

        self.canvas = Canvas(self.frames[0], bg = "black", height = self.h * self.s, width = self.w * self.s)
        self.canvas.pack()
        self.canvas.focus_set()
        
        self.canvas.bind("<Right>", lambda x: self.get_input(x), True)
        self.canvas.bind("<Left>", lambda x: self.get_input(x), True)
        self.canvas.bind("<Up>", lambda x: self.get_input(x), True)
        self.canvas.bind("<Down>", lambda x: self.get_input(x), True)
        self.canvas.bind("<q>", lambda x: self.get_input(x), True)

        self.canvas.bind("<w>", lambda x: self.get_input(x), True)
        self.canvas.bind("<a>", lambda x: self.get_input(x), True)
        self.canvas.bind("<s>", lambda x: self.get_input(x), True)
        self.canvas.bind("<d>", lambda x: self.get_input(x), True)
        self.canvas.bind("<z>", lambda x: self.get_input(x), True)
        self.canvas.bind("<x>", lambda x: self.get_input(x), True)
        self.canvas.bind("<c>", lambda x: self.get_input(x), True)
        self.canvas.bind("<v>", lambda x: self.get_input(x), True)
        self.canvas.bind("<BackSpace>", lambda x: self.get_input(x), True)

        for k in range(10):
            self.canvas.bind(str(k), lambda x: self.add_accidentals(x), True)

        for k in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]:
            self.canvas.bind("<" + k + ">", lambda x: self.add_accidentals(x), True)

        self.canvas.bind("<Button-1>", lambda x: self.get_click(x), True)

    def height(self, note):
        return 7*int(note[1:]) + note_list.index(note[0])

    def note(self, height):
        """
        Converts a y-value to a note string
        """
        return note_list[height%7] + str(math.floor(height/7))

    def draw_grid(self):
        """
        Draws the note grid
        """
        for i in range(self.h):
            y = i*self.s
            self.canvas.create_line(self.s, y, self.w * self.s, y, width = 1, fill = "grey20")
            self.labels[1].append(self.canvas.create_text(5, y+5, text = self.note(int(self.h - (self.pos[1] + i) - 1)), fill = "white", font = ("Nunito", 10), anchor = "nw"))
        for i in range(int(self.w/self.time)+1):
            for j in range(self.time):
                x = (i*self.time + j + 1)*self.s
                if j == 0:
                    self.canvas.create_line(x, 0, x, self.h * self.s, width = 2, fill = "white")
                    self.labels[0].append(self.canvas.create_text(x+5, 5, text = str(i + int(self.pos[0]/self.time)), fill = "white", font = ("Nunito", 15), anchor = "nw"))
                else:
                    self.canvas.create_line(x, 0, x, self.h * self.s, width = 1, fill = "grey20")

    def check_visible(self):
        """
        Removes offscreen notes
        """
        m = []
        for i in self.visible:
            if i[0] < (self.pos[0] - 1)*self.time or i[0] > (self.pos[0] + 1)*self.time + self.w:
                m.append(i)
            elif i[1] < self.pos[1] - 1 or i[1] > self.pos[1] + self.h:
                m.append(i)
        for i in m:
            self.visible.remove(i)
            r = self.visobj.pop(i)
            self.canvas.delete(r[0])
            self.canvas.delete(r[1])

    def draw_note(self, pos):
        """
        Adds a note to the screen
        """
        x = pos[0] - self.pos[0]*self.time + 1
        y = self.h - (pos[1] - self.pos[1]) - 1
        if pos in self.inst.notes.keys() and pos not in self.visible:
            note = self.inst.notes[pos]
            accs = note.get_acc()
            s = ""
            for i in range(len(accs)):
                inverses = {'#':'b', '+':'-', '7':'L', '^':'v', '13':'t', '17':'Ll', '19':'6l', '23':'T', '29':'N', '31':'O'}
                if accs[i] > 0:
                    s += str(accidental_names[accidental_list[i]]) + (":" + str(accs[i]) if accs[i] > 1 else "") + " "
                elif accs[i] < 0:
                    s += inverses[str(accidental_names[accidental_list[i]])] + (":" + str(-accs[i]) if -accs[i] > 1 else "") + " "
            self.visible.append(pos)
            if pos in self.selected:
                self.visobj[pos] = [self.canvas.create_rectangle(x*self.s, y*self.s, (x + note.length)*self.s, (y+1)*self.s,
                                                                 fill = "#9944ff", outline = 'black')]
                self.visobj[pos].append(self.canvas.create_text(int((x + 0.25)*self.s), y*self.s, text = s,
                                                                anchor = "nw", fill = "white", font = ("Nunito", 12)))
            else:
                self.visobj[pos] = [self.canvas.create_rectangle(x*self.s, y*self.s, (x + note.length)*self.s, (y+1)*self.s,
                                                                 fill = "#443399", outline = 'black')]
                self.visobj[pos].append(self.canvas.create_text(int((x + 0.25)*self.s), y*self.s, text = s,
                                                                anchor = "nw", fill = "grey", font = ("Nunito", 12)))

    def add_visible(self, l):
        """
        Adds a set of notes to the screen
        """
        for i in l:
            self.draw_note(i)

    def move(self, x, y):
        """
        Moves the screen by (x, y)
        """
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        for i in self.labels[0]:
            xl = int(self.canvas.itemcget(i, "text"))
            xl += x
            self.canvas.itemconfig(i, text = str(xl))
        for i in range(len(self.labels[1])):
            self.canvas.itemconfig(self.labels[1][i], text = self.note(self.pos[1] - i + self.h - 1))
        for i in self.visible:
            self.canvas.move(self.visobj[i][0], -x*self.time*self.s, y*self.s)
            self.canvas.move(self.visobj[i][1], -x*self.time*self.s, y*self.s)
                       
        new = []
        if x > 0:
            new += self.inst.get_notes(self.pos[0]*self.time + self.w - x*self.time, self.pos[0]*self.time + self.w, self.pos[1], self.pos[1] + self.h)
        elif x < 0:
            new += self.inst.get_notes(self.pos[0]*self.time, self.pos[0]*self.time - x*self.time, self.pos[1], self.pos[1] + self.h)
        if y > 0:
            new += self.inst.get_notes(self.pos[0]*self.time, self.pos[0]*self.time + self.w, self.pos[1] + self.h - y, self.pos[1] + self.h)
        elif y < 0:
            new += self.inst.get_notes(self.pos[0]*self.time, self.pos[0]*self.time + self.w, self.pos[1], self.pos[1] - y)
        self.add_visible(new)
        self.check_visible()          

    def reset_screen(self):
        """
        Clears and refills the screen
        """
        for i in self.visible:
            self.canvas.delete(self.visobj[i][0])
            self.canvas.delete(self.visobj[i][1])
        self.visible = []
        self.visobj = {}
        new = self.inst.get_notes(self.pos[0] * self.time, self.pos[0] * self.time + self.w, self.pos[1], self.pos[1] + self.h)
        self.add_visible(new)
        self.check_visible()

    def move_selected(self, x, y):
        """
        Moves the notes that are selected by (x, y)
        """
        de = []
        new = {}
        newvo = {}
        x, y = -x, -y
        for i in self.selected:
            if i in self.visible:
                self.visible.remove(i)
            if i[0] + x >= 0:
                new[(i[0] + x, i[1] + y)] = self.inst.notes.pop(i)
                if (i[0], i[1]) in self.visobj.keys():
                    m = self.visobj.pop(i)
                    self.canvas.move(m[0], x*self.s, -y*self.s)
                    self.canvas.move(m[1], x*self.s, -y*self.s)
                    newvo[(i[0] + x, i[1] + y)] = m
            else:
                new[(i[0], i[1] + y)] = self.inst.notes.pop(i)
                if (i[0], i[1]) in self.visobj.keys():
                    m = self.visobj.pop(i)
                    self.canvas.move(m[0], 0, -y*self.s)
                    self.canvas.move(m[1], 0, -y*self.s)
                    newvo[(i[0], i[1] + y)] = m
        for i in new.keys():
            self.visible.append(i)
            if i in self.inst.notes.keys():
                self.inst.notes.pop(i)
            if i in self.visobj.keys():
                for j in self.visobj[i]:
                    self.canvas.delete(j)
                self.visobj.pop(i)
            self.inst.notes[i] = new[i]
            if i in newvo.keys():
                self.visobj[i] = newvo[i]
        self.visible = list(self.visobj.keys())
        self.selected = list(new.keys())

    def delete_selected(self):
        """
        Delete all selected notes
        """
        for i in self.selected:
            self.inst.notes.pop(i)
            if i in self.visible:
                m = self.visobj.pop(i)
                self.canvas.delete(m[0])
                self.canvas.delete(m[1])
                self.visible.remove(i)
        self.selected = []

    def size_selected(self, x):
        """
        Resizes all selected notes
        """
        for i in self.selected:
            if self.inst.notes[i].length > 1 or x >= 1:
                self.inst.notes[i].change_length(self.inst.notes[i].get_length() + x)
                c = self.canvas.coords(self.visobj[i][0])
                self.canvas.coords(self.visobj[i][0], c[0], c[1], c[2]+x*self.s, c[3])

    def add_note(self, x, y, acc = None, length = 1):
        """
        Adds a note to the score
        """
        if (x, y) not in self.inst.notes.keys():
            if acc:
                self.inst.add_note(int(x/self.time) + self.pos[0], x%self.time, y + self.pos[1], acclist = acc, length = length)
            else:
                self.inst.add_note(int(x/self.time) + self.pos[0], x%self.time, y + self.pos[1], length = length)
            self.draw_note((x + self.pos[0]*self.time, y + self.pos[1]))
            self.check_visible()
            self.select((x + self.pos[0]*self.time, y + self.pos[1]))

    def add_accidentals(self, key):
        """
        Adds accidentals to all selected notes
        """
        add= True
        if key.keysym in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            accnum = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].index(key.keysym)
            add = True
        elif key.keysym in ['exclam', 'at', 'numbersign', 'dollar', 'percent', 'asciicircum', 'ampersand', 'asterisk', 'parenleft', 'parenright']:
            accnum = ['exclam', 'at', 'numbersign', 'dollar', 'percent', 'asciicircum', 'ampersand', 'asterisk', 'parenleft', 'parenright'].index(key.keysym)
            add = False
        inverses = {'#':'b', '+':'-', '7':'L', '^':'v', '13':'t', '17':'Ll', '19':'6l', '23':'T', '29':'N', '31':'O'}
        for i in self.selected:
            if add:
                self.inst.notes[i].add_acc(accnum)
            else:
                self.inst.notes[i].remove_acc(accnum)
            if i in self.visible:
                note = self.inst.notes[i]
                accs = note.get_acc()
                s = ""
                for j in range(len(accs)):
                    if accs[j] > 0:
                        s += str(accidental_names[accidental_list[j]]) + (":" + str(accs[j]) if accs[j] > 1 else "") + " "
                    elif accs[j] < 0:
                        s += inverses[str(accidental_names[accidental_list[j]])] + (":" + str(-accs[j]) if -accs[j] > 1 else "") + " "
                self.canvas.itemconfig(self.visobj[i][1], text = s)

    def de_select(self):
        """
        Removes all notes from the selection
        """
        for i in self.selected:
            if i in self.visible:
                self.canvas.itemconfig(self.visobj[i][0], fill = "#443399")
                self.canvas.itemconfig(self.visobj[i][1], fill = "grey")
        self.selected = []

    def select(self, note, add = False):
        """
        Selects the note at a location
        """
        x, y = note
        if note not in self.selected:
            if not add:
                self.de_select()
            self.selected.append(note)
            if note in self.visible:
                self.canvas.itemconfig(self.visobj[note][0], fill = "#9944ff")
                self.canvas.itemconfig(self.visobj[note][1], fill = "white")

    def group_select(self, x1, x2, y1, y2):
        for x in range(x1, x2):
            for y in range(y1, y2):
                if (x, y) in self.inst.notes:
                    self.select((x, y), add = True)

    def copy(self):
        self.clipboard = {i:self.inst.notes[i] for i in self.selected}

    def paste(self):
        offset = int(min([i[0] for i in self.clipboard.keys()])/self.time)*self.time
        placement = {(i[0] - offset, i[1] - self.pos[1]):self.clipboard[i] for i in self.clipboard.keys()}
        for i in placement.keys():
            self.add_note(i[0], i[1], placement[i].get_acc(), length = placement[i].get_length())
        self.de_select()

    def get_input(self, key):
        """
        Handles keypress inputs
        """
        if key.keysym == "Right":
            self.move(1, 0)
        elif key.keysym == "Left":
            if self.pos[0] > 0:
                self.move(-1, 0)
        elif key.keysym == "Up":
            if self.pos[1] < 56 - self.h:
                self.move(0, 1)
        elif key.keysym == "Down":
            if self.pos[1] > 0:
                self.move(0, -1)
        elif key.keysym == "q":
            self.de_select()
        elif key.keysym == "w":
            self.move_selected(0, -1)
        elif key.keysym == "a":
            self.move_selected(1, 0)
        elif key.keysym == "s":
            self.move_selected(0, 1)
        elif key.keysym == "d":
            self.move_selected(-1, 0)
        elif key.keysym == "BackSpace":
            self.delete_selected()
        elif key.keysym == "z":
            self.size_selected(-1)
        elif key.keysym == "x":
            self.size_selected(1)
        elif key.keysym == "c":
            self.copy()
        elif key.keysym == "v":
            self.paste()

    def get_click(self, key):
        """
        Handles click events
        """
        x, y = int(key.x/self.s) - 1, self.h - int(key.y/self.s) - 1
        if key.state == 4:
            if self.ms == None:
                self.ms = (x+(self.pos[0]*self.time), y + self.pos[1])
            else:
                self.group_select(self.ms[0], x+(self.pos[0]*self.time), y + self.pos[1], self.ms[1])
                self.ms = None
        elif key.state == 8:
            if self.ms:
                self.ms = None
            self.add_note(x, y)
        elif key.state == 1:
            if self.ms:
                self.ms = None
            if (x+(self.pos[0]*self.time), y + self.pos[1]) in self.visible:
                self.select((x+(self.pos[0]*self.time), y + self.pos[1]), add = True)
        else:
            if self.ms:
                self.ms = None
            if (x+(self.pos[0]*self.time), y + self.pos[1]) in self.visible:
                self.select((x+(self.pos[0]*self.time), y + self.pos[1]))

    def save(self, filename):
        write = []
        for i in self.inst.notes.keys():
            write.append(str(i[0]) + "," + str(i[1]) + " " + ",".join([str(i) for i in self.inst.notes[i].get_acc()]) + " " + str(self.inst.notes[i].length) + "\n")
        self.canvas.focus_set()

    def load(self, filename):
        self.inst.clear_notes()
        for i in self.visobj.keys():
            self.canvas.delete(i[0])
            self.canvas.delete(i[1])
        self.visible = []
        self.visobj = {}
        g = open("_Data/" + filename + ".txt", "r")
        f = g.read()
        g.close()
        for i in f.splitlines():
            a = [n.split(",") for n in i.split(" ")]
            self.inst.add_note(math.floor(int(a[0][0])/self.time), \
                               int(a[0][0])%self.time, \
                               int(a[0][1]), \
                               length = int(a[2][0]), \
                               acclist = [int(i) for i in a[1]])
        self.reset_screen()
        self.canvas.focus_set()

    def render(self, filename):
        f = wave.open("_Music/" + filename + ".wav", "w")

        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)

        l = self.inst.quick_render(int(input("start: ")), int(input("end: "))) #change
        b = bytearray()

        for n in l:
            y = n if n >= 0 else n+65536
            a = round(min(max(y, 0), 65535))
            g = a%256
            c = a>>8
            b.append(g)
            b.append(c)

        f.writeframes(b)
        f.close()
        
        self.canvas.focus_set()

