from components import Window, Page, Textbox, ButtonPanel, Button, ToolTip

from utils import get_quote

def quotes_page():
    page1 = Page(window)
    page1.add_title("practice quotes")

    buttons = ButtonPanel(page1, [2, 3])
    buttons.place(relx=0.5, y=110, anchor="center")
    profile = buttons.buttons[0][0]
    profile.config(text="profile", command=lambda: window.show(1))
    button1_tooltip = ToolTip(profile, 'asd')

    textbox = Textbox(page1)

    textbox.display_text(get_quote())
    #textbox.display_text("asd")
    textbox.bind(lambda: end_page(textbox.test.stats))
    textbox.ready()

    window.define(page1)

def end_page(results):
    end_page = Page(window)
    end_page.add_field("wpm", results["wpm"])
    end_page.add_field("raw wpm", results["raw"], "Includes incorrect characters as well.")
    end_page.add_field("accuracy", results["acc"])
    end_page.add_field("mistakes", results["incorrect"])
    window.define(end_page)

window = Window()

quotes_page()

page2 = Page(window)
window.define(page2)
window.show(0)


window.mainloop()
