import tkinter as tk
from time import time

from utils import get_accuracy, get_wpm

# Define font constants
FONT_LARGE = ("Century Gothic", 35)
FONT_SMALL = ("Century Gothic", 18)
FONT_TOOLTIP = ("Century Gothic", 10)
FONT_BUTTON = ("Century Gothic", 12)
FONT_TEXT = ("Lucida Console", 18)

# Define special characters and their names
SPECIAL_CHARACTERS = {
    " ": "space",
    ".": "period",
    ":": "colon",
    "\'": "apostrophe",
    ";": "semicolon",
    ",": "comma",
}


class Window(tk.Tk):
# Template for main window

    def __init__(self): 

        super().__init__()

        # Configure window appearance
        self.title("ASD")
        self.geometry("1200x600")
        self.resizable(width=False, height=False)
        self.tk_setPalette(background="#1a1a1f", foreground="#ffffff")

        # Define a list to store page frames
        self.pages = []

    def register_page(self, page, index=None):
    # Adds a page frame to the list and places it on the window
        
        if index==None: 
            self.pages.append(page)
        else: self.pages[index] = page
        page.place(x=0, y=0)

    def show_page(self, index):
        # Raises a page to the top of the window to display it

        self.pages[index].tkraise()
        self.current_page = index

class Page(tk.Frame):
# Template for the window pages

    def __init__(self, parent):
    # Creates the Page object

        super().__init__(parent, width=1200, height=900)
        self.field_count = 0
        self.textbox = None

    def add_title(self, title):
        # Adds a title label to the top of the page
        self.title = title

        label = tk.Label(
            self,
            text=title,
            font=FONT_LARGE,
            bg="#1a1a1f",
            fg="#e14646"
        )
        label.place(relx=0.5, y=50, anchor="center")

    def add_field(self, title, value, desc=None):
        # Adds a field with a title, value, and optional tooltip to the page

        x = self.field_count * 200 + 100
        self.field_count += 1
        field = tk.Frame(self, height=100, width=200)

        # Field title label
        tk.Label(
            field,
            text=title,
            font=FONT_SMALL,
            bg="#1a1a1f",
            fg="#e14646"
        ).place(y=0)

        # Field value label
        tk.Label(
            field,
            text=value,
            font=FONT_LARGE,
            bg="#1a1a1f",
            fg="#ffffff"
        ).place(y=35)

        field.place(x=x, y=150)

        if desc: # If a description is given, then tooltip is added

            ToolTip(field, desc, offset=0)

class ButtonPanel(tk.Frame):
# Template for a button panel with configurable buttons

    def __init__(self, parent, buttons, size=80):

        # Calculate panel width based on button count
        width = buttons * size
        super().__init__(parent, width=width, height=40, bg="#111114")

        # Create a list of Button objects
        self.buttons = []
        for i in range(buttons):
            button = Button(self, text=i)

            self.buttons.append(button)

        x = 0
        # Place each button in panel
        for button in self.buttons:
            button.place(height=40, width=size, x=x)
            x += size

class Button(tk.Button):
    # Template for custom button

    def __init__(self, parent, text="", state="normal"):
        
        super().__init__(
            parent,
            text=text,
            font=FONT_BUTTON,
            bg="#111114",
            fg="#51515b",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            disabledforeground="#ffffff",
            activebackground="#111114",
            activeforeground="#a1a1ab",
            state=state
        )

class Textbox(tk.Canvas):
# Template for the area where the user can type in

    def __init__(self, frame): 

        super().__init__(frame, height=300, width=900)
        self.place(relx=0.5, y=400, anchor="center")
        self.root = self.master.master
        self.master.textbox = self

    def display_text(self, text):

        self.test = TypingTest(text)

        # Initial coordinates
        x, y = 10, 20

        # Loop through each character in the text
        for index in range(len(text)):
            char = text[index]
            
            # Check for textbox end and handle line breaks
            if text[index - 1] == " ":
                self.test.word_index += 1
                word = self.test.words[self.test.word_index]
                word_width = (len(word)) * 13

                if word_width + x > 900:
                    x = 10
                    y += 30

            # Create a label for each character
            char_label = self.create_text(
                x,
                y,
                text=char,
                fill="#61616b",
                font=FONT_TEXT,
                anchor="nw"
            )

            # Save char and labels to test object for tracking
            self.test.chars.append(char)
            self.test.labels.append(char_label)

            # Update position for next char
            x += 13

    def ready(self):
    # Prepares the Textbox by creating the cursor and binding key events

        # Create the cursor line
        self.cursor = self.create_line(
            10, 20, 10, 42, fill="#e14646", width=2
        )

        # Create tracking variables
        self.current_index = 0
        self.cursor_pos = [10, 20]

        # Bind key press events
        self.root.bind("<Key>", self.key_press)
        self.root.bind("<BackSpace>", self.backspace)

    def unready(self):
    # Stops the test, calculates stats, and calls the end function

        # Retrieve the test object
        test = self.test

        # Record the end time
        test.stats["stoptime"] = time()

        # Unbind key events to stop keypresses
        self.root.unbind("<Key>")
        self.root.unbind("<BackSpace>")

        # Calculate time taken
        time_elapsed = (test.stats["stoptime"] - test.stats["starttime"]) / 60

        # Evaluate test stats
        test.evaluate(time_elapsed)
        self.end()

        # Clear the canvas
        self.delete("all")

    def key_press(self, event):
    # Handles key presses and updates the Textbox based on user input

        test = self.test

        # Check if the user has already typed all chars
        if self.current_index == len(test.chars):
            return

        # Get typed and required chars
        typed_char = event.char
        required_char = test.chars[self.current_index]

        # Check if typed char is valid
        if not (typed_char.isalnum() or typed_char in SPECIAL_CHARACTERS):
            return

        # Start the timer on first key press
        if not test.stats["starttime"]:
            test.stats["starttime"] = time()

        # Update character label color based on correctness
        if typed_char == required_char:
            self.itemconfigure(test.labels[self.current_index], fill="#ffffff")
        else:
            self.itemconfigure(test.labels[self.current_index], fill="#e14646", text=typed_char)
            if required_char == ' ':
                self.itemconfigure(test.labels[self.current_index], text="_")
            if typed_char == ' ':
                self.itemconfigure(test.labels[self.current_index], text=required_char)

        # Update test stats
        test.key_press(typed_char, required_char)

        # Check if the test is complete
        if self.current_index + 1 == len(test.chars):
            self.unready()

        # Update current character index
        self.current_index += 1

        # Move the cursor if the test isn't finished
        if self.current_index < len(test.chars):
            x1, y1 = self.cursor_pos
            x2, y2 = self.coords(test.labels[self.current_index])
            self.move_cursor(x2 - x1, y2 - y1)

    def backspace(self, event):
    # Handles backspace events for deleting incorrectly typed chars

        test = self.test
        if not self.current_index: return
        prev_index = self.current_index - 1

        # Check if the previous character was typed correctly
        if test.typed[prev_index] == test.chars[prev_index]:
            return

        # Update current index and character label
        self.current_index = prev_index
        self.itemconfigure(
            test.labels[self.current_index], fill="#61616b", text=test.chars[self.current_index]
        )

        # Remove typed character and update statistics
        del test.typed[self.current_index]
        test.stats["correct"] -= 1

        # Update cursor position based on the deleted character
        x1, y1 = self.coords(test.labels[self.current_index])
        x2, y2 = self.cursor_pos
        self.move_cursor(x1 - x2, y1 - y2)

    def move_cursor(self, x=0, y=0, move_count=0):
    # Moves the cursor based on the given offset values

        self.move(self.cursor, x / 10, y / 10)

        # Animate the cursor movement
        if move_count < 9:
            self.after(15, lambda: self.move_cursor(x, y, move_count + 1))

        # Update cursor position
        if not move_count:
            self.cursor_pos[0] += x
            self.cursor_pos[1] += y

    def bind(self, function):
    # Binds a function to be called when the test ends

        self.end = function

class TypingTest:
# This class tracks stats and handles test data

    def __init__(self, text):

        self.words = text.split()  # Separate text into words
        self.word_index = 0  # Track current word index
        self.chars = []  # List of all chars
        self.typed = []  # List of typed chars
        self.labels = []  # List of labels of each chars

        self.weak = {}  # Dictionary to store incorrectly typed chars and their frequency
        self.stats = {  # Dictionary for storing test stats
            "correct": 0,  # Number of correctly typed chars
            "incorrect": 0,  # Number of incorrectly typed chars
            "starttime": 0,  # Start time of the test
        }

    def key_press(self, typed_char, req_char):
    # Updates stats based on the typed char and the required char

        if typed_char == req_char:
            self.stats["correct"] += 1
        else:
            self.stats["incorrect"] += 1
            if req_char not in self.weak:
                self.weak[req_char] = 1
            else:
                self.weak[req_char] += 1

        self.typed.append(typed_char)

    def evaluate(self, time):
    # Calculates and stores stats based on test results

        self.stats["acc"] = get_accuracy(self.stats)
        self.stats["raw"] = get_wpm(len(self.chars), time)
        self.stats["wpm"] = get_wpm(self.stats["correct"], time)

        # Sort and name weak characters for display
        weak = sorted(self.weak)
        for i, k in enumerate(weak):
            if k in SPECIAL_CHARACTERS:
                weak[i] = SPECIAL_CHARACTERS[k]
        self.stats["weak"] = weak

class ToolTip:

    def __init__(self, widget, text="info", offset=6):
        self.widget = widget  # Widget to which the tooltip is applied
        self.text = text  # Text displayed in the tooltip
        self.offset = offset  # Distance between tooltip and widget

        # Bind events to show and hide the tooltip
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

        self.schedule_id = None  # Variable for tracking schedule ID
        self.tooltip_window = None  # Variable for toplevel window

    def enter(self, event=None):
        # Schedules the display of the tooltip with 500ms delay
        self.schedule()

    def leave(self, event=None):
        # Unschedules the display and hides the tooltip if exists
        self.unschedule()
        self.hidetip()

    def schedule(self):
        # Cancels any existing scheduling and schedules the tooltip display with a 500ms delay
        self.unschedule()
        self.schedule_id = self.widget.after(500, self.showtip)

    def unschedule(self):
        # Cancels any pending tooltip display
        if self.schedule_id:
            self.widget.after_cancel(self.schedule_id)
            self.schedule_id = None

    def showtip(self, event=None):
        # Creates and displays the tooltip at the specified position

        # Get widget position relative to user's screen
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + self.offset

        # Create and configure the tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Disable window mode
        self.tooltip_window.geometry(f"+{x}+{y}")  # Set position

        border = tk.Frame(self.tooltip_window, bg="#111114", padx=6, pady=6)  # Create border frame
        label = tk.Label(border,  # Create label widget
                         text=self.text,
                         font=FONT_TOOLTIP,
                         bg="#111114",
                         wraplength=180)
        label.pack()  # Pack label inside border frame
        border.pack()  # Pack border frame in the toplevel window

    def hidetip(self):
        # Destroys the tooltip window if it exists.
        if self.tooltip_window:
            self.tooltip_window.destroy()