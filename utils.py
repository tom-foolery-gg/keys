from random import randint

def get_quote():
    with open("quotes.txt") as f:
        l = f.readlines()
        return l[randint(0, len(l)-1)].strip()       

def get_wpm(c, t): return round((c/5)/t, 1)

def get_accuracy(s): return str(s['correct']*100//(s['incorrect']+s['correct']))+"%"

def get_hex_range(start, end):
    
    s = [int(start[i+1:i+3], 16) for i in range(0, 6, 2)]
    e = [int(end[i+1:i+3], 16) for i in range(0, 6, 2)]
    
    l = []
    for i in range(1, 11):
        h = '#'
        for j in range(3):
            d = (e[j]-s[j])*i//10
            x = hex(s[j]+d)
            if len(x)==3: r = '0'+x[2:]
            else: 
                r = x[2:]
            h += r
        l.append(h)
    return l

