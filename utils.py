from random import randint

def get_quote():
# Gets a random quote from quotes.txt
    
    f = open("quotes.txt")
    quotes = f.readlines()

    if not quotes: # If quotes file is empty, backup is returned
        return "Be the change that you wish to see in the world."

    random_index = randint(0, len(quotes) - 1)
    f.close()
    return quotes[random_index].strip()

def get_words(length):
# Gets a random word collection from words.txt

    f = open("words.txt")     
    words = f.readlines()

    if not words: # If words file is empty, backup is returned
        return "words file empty backup sentence displayed"

    collection = []
    while length:
        random_index = randint(0, len(words) - 1)
        collection.append(words[random_index].strip())
        length-=1
            
    return " ".join(collection)

def get_chars(length):
# Generates a random char collection

    chars = list(range(97, 123))
    collection = []

    while length: # Creates words with random chars and generates a sentence
        word_length = randint(2, 6)
        word = ""
        while word_length:
            random_index = randint(0, 25)
            word += chr(chars[random_index])
            word_length -= 1
        collection.append(word) 

        length -= 1
    return " ".join(collection)

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
        return f"{int(seconds / 60)}m"
    
    else:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"