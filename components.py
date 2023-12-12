import tkinter as tk
from time import time

from utils import get_accuracy, get_wpm

LARGEFONT = ("Century Gothic", 35)
SMALLFONT = ("Century Gothic", 18)
BUTTONFONT = ("Century Gothic", 12)
TEXTFONT = ("Lucida Console", 18)
SPECIAL = (' ', '.', ':', '\'', ';', ',')

class Window(tk.Tk):
    def __init__(self): 
        super().__init__()

        self.title("ASD")
        self.geometry("1200x600")
        self.resizable(width=False, height=False)
        self.tk_setPalette(background="#1a1a1f", foreground="white")

    __frames = []

    def define(self, page):
        self.__frames.append(page)
        page.place(x=0, y=0)

    def show(self, index):
        self.__frames[index].tkraise()
        self.current_frame = index

class Page(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, width=1200, height=900)
        self.fieldcount = 0

    def add_title(self, title):
        label = tk.Label(self, text=title, font=LARGEFONT, bg="#1a1a1f", fg="#e14646")
        label.place(relx=0.5, y=50, anchor="center")

    def add_field(self, title, value): 
        self.fieldcount += 1
        tk.Label(self, text=title, font=SMALLFONT, bg="#1a1a1f", fg="#e14646").place(x=self.fieldcount*100, y=150)
        tk.Label(self, text=value, font=LARGEFONT, bg="#1a1a1f", fg="#ffffff").place(x=self.fieldcount*100, y=185)

class ButtonPanel(tk.Frame):
    def __init__(self, parent, size): 
        width = sum(size)*80+(len(size)-1)*2
        super().__init__(parent, width=width, height=40, bg="#e14646")

        self.buttons = [[Button(self, text=i) for i in range(j)] for j in size]

        x = 0
        for i in self.buttons:
            if x: x+=2
            for j in i:
                j.place(height=40, width=80, x=x)
                x+=80


class Button(tk.Button):
    def __init__(self, frame, text="", type=0):
        super().__init__(frame, text=text, font=BUTTONFONT, bg="#111114", fg="#41414b", borderwidth=0, highlightthickness=0, 
                         relief="flat", disabledforeground="#ffffff", activebackground="#111114", 
                         activeforeground="#81818b")

    def disable(self): self.config(state="disabled")

    def enable(self): self.config(state="normal")

class Textbox(tk.Canvas):
    def __init__(self, frame): 
        super().__init__(frame, height=300, width=900)
        self.place(relx=0.5, y=400, anchor="center")
        self.root = self.master.master

    def display_text(self, text):
        self.test = test = TypingTest(text)
        x = 10
        y = 20

        for i in range(len(text)):
            char = text[i]
            if text[i-1]==' ': 
                test.word_index+=1
                word = test.words[test.word_index]
                word_width = (len(word))*13

                if word_width+x > 900:
                    x = 10
                    y += 30

            char_label = self.create_text(x, y, text=char, fill="#61616b", font=TEXTFONT, anchor = "nw")
            test.chars.append(char)
            test.labels.append(char_label)
            x += 13

    def ready(self):
        self.cursor = self.create_line(10, 20, 10, 42, fill='#e14646', width=2)
        self.current_index = 0
        self.cursor_pos = [10, 20]
        self.root.bind("<Key>", self.key_press)
        self.root.bind("<BackSpace>", self.backspace)

    def unready(self):
        test = self.test
        test.stats["stoptime"] = time()

        self.root.unbind("<Key>")
        self.root.unbind("<BackSpace>")
        self.delete(self.cursor)
        time_elapsed = (test.stats['stoptime'] - test.stats['starttime']) / 60 # in minutes

        test.evaluate(time_elapsed)
        self.end()

    def key_press(self, event):
        test = self.test
        if self.current_index == len(test.chars): return

        typed_char = event.char
        req_char = test.chars[self.current_index]
    
        if not (typed_char.isalnum() or typed_char in SPECIAL): return
    
        if not test.stats["starttime"]: test.stats["starttime"] = time()

        if typed_char == req_char: 
            self.itemconfig(test.labels[self.current_index], fill="#ffffff")
        else: 
            self.itemconfig(test.labels[self.current_index], fill="#e14646", text=typed_char)
        test.key_press(typed_char, req_char)
        if self.current_index+1 == len(test.chars): self.unready()
        self.current_index+=1

        if self.current_index < len(test.chars):
            x1, y1 = self.cursor_pos
            x2, y2 = self.coords(test.labels[self.current_index])

            self.move_cursor(x2-x1, y2-y1)

    def backspace(self, event):
        prev_index = self.current_index-1
        test = self.test
        if test.typed[prev_index]==test.chars[prev_index]: return
    
        self.current_index=prev_index
        self.itemconfig(test.labels[self.current_index], fill="#61616b", text=test.chars[self.current_index])
        del test.typed[self.current_index]
        test.stats["correct"] -= 1
        x1, y1 = self.coords(test.labels[self.current_index])
        x2, y2 = self.cursor_pos
        self.move_cursor(x1-x2, y1-y2)

    def move_cursor(self, x=0, y=0, lc=0):
        self.move(self.cursor, x/10, y/10)
        if lc<9: self.after(15, lambda: self.move_cursor(x, y, lc+1))
        if not lc:
            self.cursor_pos[0]+=x
            self.cursor_pos[1]+=y

    def bind(self, function): self.end = function


class TypingTest:
    def __init__(self, text):
        self.words = text.split()
        self.word_index = 0
        self.chars, self.typed, self.labels = [], [], []

        self.weak = {}
        self.stats = {"correct": 0, "incorrect": 0, "starttime": 0, "stoptime": 0}

    def key_press(self, typed_char, req_char):
        if typed_char==req_char:
            self.stats["correct"] += 1

        else:
            self.stats["incorrect"] += 1
            if typed_char not in self.weak: self.weak[typed_char] = 1
            else: self.weak[typed_char] += 1
        self.typed.append(typed_char)

    def evaluate(self, time):
        self.stats["acc"] = get_accuracy(self.stats)
        self.stats["raw"] = get_wpm(len(self.chars), time)
        self.stats["wpm"] = get_wpm(self.stats["correct"], time)

