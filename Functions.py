from math import gcd, pi, floor, ceil
from math import sin as sine
import random

# Ratio Functions #

def cancel(r):
    a, b = r
    return (int(a/gcd(a, b)), int(b/gcd(a, b)))

# Volume Functions #

def wedge(l, p):
    f = l[:round(len(l)*p)]
    b = l[round(len(l)*p):]
    return f + [b[i] * (1-(i/len(b))) for i in range(len(b))]

def ramp(l, p):
    f = l[:round(len(l)*p)]
    b = l[round(len(l)*p):]
    return [f[i] * (i/len(f)) for i in range(len(f))] + b

def swell(l, p):
    f = l[:round(len(l)*p)]
    b = l[round(len(l)*p):]
    return ([f[i] * (i/len(f)) for i in range(len(f))] +
            [b[i] * (1-(i/len(b))) for i in range(len(b))])

def const(l, p):
    return l

def bevel(l, p):
    sindx = round(len(l) * (p / 2))
    eindx = len(l) - round(len(l) * (p / 2)) - 1
    
    f = l[:sindx]
    m = l[sindx:eindx]
    b = l[eindx:]
    return ([f[i] * (i/len(f)) for i in range(len(f))] +
            m +
            [b[i] * (1-(i/len(b))) for i in range(len(b))])

# Wavefrom Functions #

def tri(freq, samples):
    b, a = freq
    l = []
    for i in range(samples):
        m = i/44100
        x = m*b
        x -= (a/4)
        x = x%(a)
        if x >= a/2:
            l.append(-32767 + (131072*(x-(a/2))/a))
        else:
            l.append(+32767 - (131072*x/a))
    # Cutting off wave at a zero, to avoid clicks at the ends of notes #
    for i in range(len(l)-1, -1, -1):
        if l[i] == 0:
            l = l[:i]
            break
        elif i+1 < len(l) and l[i+1] != 0 and l[i]/abs(l[i]) != l[i+1]/abs(l[i+1]):
            l = l[:i]
            break
        
    return l

def get_tri2(v):
    def w(freq, samples):
        b, a = freq
        #print(b, a)
        l = []
        for i in range(samples):
            m = i/44100
            x = m*b
            x -= (a - a*v/100)/4
            x = x%(a)
            if x >= (a/2) + (a*v/200):
                rise = 65534
                run = a - (a/2) - (a*v/200)
                #print(x , a , run, rise, (-32767 + (rise/run)*(x - (a/2) - (a*v/200))))
                l.append(-32767 + (rise/run)*(x - (a/2) - (a*v/200)))
            else:
                #print('\t', x , a , run, rise, (+32767 + (rise/run)*(x)))
                rise = -65534
                run = (a/2) + (a*v/200)
                l.append(+32767 + (rise/run)*(x))
        # Cutting off wave at a zero, to avoid clicks at the ends of notes #
        for i in range(len(l)-1, -1, -1):
            if l[i] == 0:
                l = l[:i]
                break
            elif i+1 < len(l) and l[i+1] != 0 and l[i]/abs(l[i]) != l[i+1]/abs(l[i+1]):
                l = l[:i]
                break
        #print(l[0:int(44100*a/b)])
        return l
    return w

def sqr(freq, samples):
    b, a = freq
    l = []
    for i in range(samples):
        m = i/44100
        x = m*b
        x -= (a/4)
        x = x%(a)
        if x >= a/2:
            l.append(-32767)
        else:
            l.append(+32767)
    return l

def hxg(freq, samples, v = 2):
    b, a = freq
    l = []
    for i in range(samples):
        m = i/44100
        x = m*b
        x -= (a/4)
        x = x%(a)
        if x >= a/2:
            y = -32767 + (131072*(x-(a/2))/a)
            l.append(min(max(y * v, -32767), 32767))
        else:
            y = +32767 - (131072*x/a)
            l.append(min(max(y * v, -32767), 32767))
    # Cutting off wave at a zero, to avoid clicks at the ends of notes #
    for i in range(len(l)-1, -1, -1):
        if l[i] == 0:
            l = l[:i]
            break
        elif i+1 < len(l) and l[i+1] != 0 and l[i]/abs(l[i]) != l[i+1]/abs(l[i+1]):
            l = l[:i]
            break
        
    return l

def get_hxg(v):
    def hxg(freq, samples):
        b, a = freq
        l = []
        for i in range(samples):
            m = i/44100
            x = m*b
            x -= (a/4)
            x = x%(a)
            if x >= a/2:
                y = -32767 + (131072*(x-(a/2))/a)
                l.append(min(max(y * v, -32767), 32767))
            else:
                y = +32767 - (131072*x/a)
                l.append(min(max(y * v, -32767), 32767))
        # Cutting off wave at a zero, to avoid clicks at the ends of notes #
        for i in range(len(l)-1, -1, -1):
            if l[i] == 0:
                l = l[:i]
                break
            elif i+1 < len(l) and l[i+1] != 0 and l[i]/abs(l[i]) != l[i+1]/abs(l[i+1]):
                l = l[:i]
                break
        return l
    return hxg
        
def pls(freq, samples):
    b, a = freq
    l = []
    for i in range(samples):
        m = i/44100
        x = m*b
        x -= (a/4)
        x = x%(a)
        if x >= a/2:
            l.append(-32767 + (65534*(x-(a/2))/a))
        else:
            l.append(+32767 - (65534*x/a))
    return l

def saw(freq, samples):
    b, a = freq
    l = []
    for i in range(samples):
        m = i/44100
        x = m*b
        x -= (a/4)
        x = x%(a)
        l.append(-32767 + (65534*x/a))
    return l

def sin(freq, samples):
    b, a = freq
    l = []
    for i in range(samples):
        m = i/44100
        x = m*b
        x = x%(a)
        l.append(sine(x*2*pi/a) * 32767)
    return l

def timb(func, ovt, detune = None):
    #print(ovt, detune)
    def w(freq, samples):
        l = func(freq, samples)
        l = [i*ovt[0]/sum(ovt) for i in l]
        for i in range(len(ovt[1:])):
            if ovt[i] != 0:
                if not detune:
                    #print(freq, cancel((freq[0] * (i+2), freq[1])))
                    x = func(cancel((freq[0] * (i+2), freq[1])), samples+(10*i))
                else:
                    x = func((freq[0] * (i+2) * (1.0005 ** detune[i]), freq[1]), samples+(10*i))
                x = [j*ovt[i]/sum(ovt) for j in x]
                for j in range(min(len(l), len(x))):
                    l[j] += x[j]*((-1)**i)
        for i in range(len(l)-1, -1, -1):
            if l[i] == 0:
                l = l[:i]
                break
            elif i+1 < len(l) and l[i+1] != 0 and l[i]/abs(l[i]) != l[i+1]/abs(l[i+1]):
                l = l[:i]
                break
        return l
    return w

def custom(inst, default = 440):
    print(inst)
    def w(freq, samp):
        import wave
        stop = False
        uinst = inst
        if inst[-1] == "|":
            uinst = inst[:-1]
            stop = True
        try:
            file = wave.open("_Instruments/" + uinst, "rb")
        except:
            raise "This instrument does not exist"
        frames = file.readframes(file.getnframes())
        x = file.getsampwidth()
        file.close()
        if x != 2:
            raise "Please use a 16-bit depth audio file"
        l = []
        for i in range(0, len(frames), 2):
            l.append(frames[i] + frames[i+1]*256)
        l = [i if i <= 32767 else i-65536 for i in l]
        ret = []
        for i in range(samp):
            x = i*freq[0]/default/freq[1]
            if not stop or x<=len(l):
                x = x%len(l)
                before = floor(x)%len(l)
                after = ceil(x)%len(l)
                if before == after:
                    ret.append(l[before])
                else:
                    ret.append(int((l[after] - l[before])*(x%1) + l[before]))
            else:
                ret.append(0)
        # Cutting off wave at a zero, to avoid clicks at the ends of notes #
        for i in range(len(ret)-1, -1, -1):
            if ret[i] == 0:
                ret = ret[:i]
                break
            elif i+1 < len(ret) and ret[i+1] != 0 and ret[i]/abs(ret[i]) != ret[i+1]/abs(ret[i+1]):
                ret = ret[:i]
                break
        return ret
    return w

def custom2(inst):
    file = open("_Instruments/" + inst, 'r')
    x = file.read()
    ins = eval(x.splitlines()[0])
    ovt, cents = [float(i.split(', ')[0]) for i in x.splitlines()[1:]], [float(i.split(', ')[1]) for i in x.splitlines()[1:]]
    file.close()
    return timb(ins, ovt, detune = cents)
        

        
