import math
import fInfo

class Note:
    def __init__(self, length, acclist = [0]*10):
        self.length = length
        self.accidentals = acclist[:]

    def add_acc(self, num):
        self.accidentals[num] += 1

    def remove_acc(self, num):
        self.accidentals[num] -= 1

    def clear_acc(self):
        self.accidentals = [0]*10

    def get_acc(self):
        return self.accidentals

    def change_length(self, newl):
        if newl > 0:
            self.length = newl

    def get_length(self):
        return self.length

    def multiply_acc(self):
        r = [1, 1]
        for i in range(len(self.accidentals)):
            if self.accidentals[i] < 0:
                for j in range(-self.accidentals[i]):
                    r[1] *= fInfo.accidental_list[i][0]
                    r[0] *= fInfo.accidental_list[i][1]
            elif self.accidentals[i] > 0:
                for j in range(self.accidentals[i]):
                    r[0] *= fInfo.accidental_list[i][0]
                    r[1] *= fInfo.accidental_list[i][1]
        return r

