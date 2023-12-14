from components import Window, Page, Textbox, ButtonPanel, Button, ToolTip

from utils import get_quote, format_time

def quotes_page():
    page1 = Page(window)
    page1.add_title("practice quotes")

    buttons = ButtonPanel(page1, [2, 3])
    buttons.place(relx=0.5, y=110, anchor="center")

    profile = buttons.buttons[0][0]
    profile.config(text="profile", command=lambda: window.show_page(1))
    ToolTip(profile, 'Check your statistics')

    options = buttons.buttons[0][1]
    options.config(text="config", command=lambda: window.show_page(1))
    ToolTip(options, 'Customize the application')

    textbox = Textbox(page1)

    textbox.display_text(get_quote())
    #textbox.display_text("asd")
    textbox.bind(lambda: end_page(textbox.test.stats))
    textbox.ready()

    window.register_page(page1)

def end_page(results):
    end_page = Page(window)

    end_page.add_field("wpm", results["wpm"], "Considers only correctly typed characters")

    end_page.add_field("accuracy", results["acc"])

    time = format_time(round(results["stoptime"]-results["starttime"], 1))
    end_page.add_field("time taken", time)

    if results["incorrect"]:
        end_page.add_field("raw wpm", results["raw"], "Includes incorrectly typed characters")

        weak = "Your weak keys are {}, and {}".format(", ".join(results["weak"][:-1]), results["weak"][-1])
        end_page.add_field("mistakes", results["incorrect"], weak)

    window.register_page(end_page)

window = Window()

quotes_page()

page2 = Page(window)
window.register_page(page2)
window.show_page(0)


window.mainloop()
