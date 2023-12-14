from random import randint

def get_quote():
# Gets a random quote from quotes.txt

    with open("quotes.txt") as f:
        lines = f.readlines()
        random_index = randint(0, len(lines) - 1)
        return lines[random_index].strip()


def get_wpm(chars, time):
# Calculates the words per minute using character count and time taken

    return round((chars / 5) / time, 1)


def get_accuracy(stats):
# Calculates the typing accuracy percentage using stats

    correct = stats["correct"]
    incorrect = stats["incorrect"]
    accuracy = 0
    if correct + incorrect > 0:
        accuracy = round(correct * 100 / (correct + incorrect))
        
    # Returns accuracy as a string with %
    return f"{accuracy}%" 


def format_time(seconds):
    # Formats seconds into a human readable string

    if seconds < 60: # Less than a minute
        return f"{seconds}s" 
    
    elif seconds % 60 == 0: # Perfect minutes
        return f"{seconds // 60}m"
    
    else:
        return f"{seconds // 60}m {seconds % 60}s"