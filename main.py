from components import Window, Page, Textbox, ButtonPanel, Button, ToolTip

from utils import get_quote, get_words, get_chars, format_time

def practice_page(title):
# Creates a page for practicing typing 

    page = Page(window)
    page.add_title(f"practice {title}")

    # Creates main button panel
    buttons = ButtonPanel(page, 3)
    buttons.place(relx=0.5, y=110, anchor="center")

    for index, name in enumerate(["quotes", "words", "chars"]):

        # Sets up each button's command and name
        button = buttons.buttons[index]
        button.config(text=name, command=lambda mode=index: change_mode(mode)) 

        ToolTip(button, f"Practice typing {name}")

        if name == title: # If button is for current page, it is highlighted
            button["fg"] = "#a1a1ab"

    # Create and bind textbox for user input and display practice text
    textbox = Textbox(page)
    textbox.bind(lambda: end_page(textbox.test.stats))

    return page

def quotes_page():
    # Typing test with random quotes

    page = practice_page("quotes")
    textbox = page.textbox

    textbox.display_text(get_quote())

    return page

def words_page():
    # Typing test with random words

    page = practice_page("words")
    textbox = page.textbox

    textbox.display_text(get_words(length_words))

    secondary_buttons(page, change_words)
    
    return page

def chars_page():
    # Typing test with random characters

    page = practice_page("chars")
    textbox = page.textbox

    textbox.display_text(get_chars(length_chars))

    secondary_buttons(page, change_chars)
    
    return page

def end_page(results):
    # Page to be displayed when a test is completed
    page = Page(window)

    page.add_field("wpm", results["wpm"], "Considers only correctly typed characters")

    page.add_field("accuracy", results["acc"], "Ratio of correct characters to total characters")

    if results["incorrect"]:
        page.add_field("raw wpm", results["raw"], "Includes incorrectly typed characters")

        weak = "Your weak keys are {}, and {}".format(", ".join(results["weak"][:-1]), results["weak"][-1])
        page.add_field("mistakes", results["incorrect"], weak)
    
    time = format_time(round(results["stoptime"]-results["starttime"], 1))
    page.add_field("time taken", time, "Time between first key press and last")

    restart = Button(page)
    restart.config(text="restart", command=restart_test)
    restart.place(relx=0.5, y=400, height=50, width=100, anchor="center")
    ToolTip(restart, 'Restart the test')

    window.register_page(page)

def secondary_buttons(page, function):
    # Creates button panel for adjusting number of words
    
    title = page.title.split()[-1]
    buttons = ButtonPanel(page, 3, 40)
    buttons.place(relx=0.5, y=160, anchor="center")
    ToolTip(buttons, 'Adjust the number of words')
    count = 0

    for button in buttons.buttons:
        count+=10
        button.config(text=count)
        
        if title == "words":
            button["command"] = lambda c=count: change_words(c) 
            length = length_words
        
        elif title == "chars":
            button["command"] = lambda c=count: change_chars(c) 
            length = length_chars

        if count==length: button["fg"] = "#a1a1ab"

def start_test():

    page = window.pages[current_mode]
    page.textbox.ready()
    window.show_page(current_mode)

def restart_test():

    window.register_page(modes[current_mode](), current_mode)
    start_test()


def change_mode(mode):

    global current_mode
    if current_mode != mode:    

        window.register_page(modes[current_mode](), current_mode)                                       
        current_mode = mode

    restart_test()

    window.show_page(current_mode)

def change_words(new):

    global length_words
    length_words = new

    restart_test()

def change_chars(new):

    global length_chars
    length_chars = new

    restart_test()

window = Window()

# Variables
current_mode = 0
length_chars = 30
length_words = 30

# Sets up all typing pages
modes = (quotes_page, words_page, chars_page)
for mode in modes:

    window.register_page(mode())    

start_test()

# Starts the program
window.mainloop()
