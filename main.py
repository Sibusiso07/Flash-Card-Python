# Importing necessary libraries
from tkinter import *
import pandas
import random

# Global variables
current_card = ""
BACKGROUND_COLOR = "#B1DDC6"
learned_words = []

# Reading from the 'words_to_learn.csv' if it exists, else reading from the original file
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    words_to_learn = data.to_dict(orient="records")

# Function to display a flashcard
def show_card(button_clicked):
    global current_card, flip_timer
    # Resetting the timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(flip_card, image=front_flash_card)
    canvas.itemconfig(current_title, text="French", fill="black")
    canvas.itemconfig(current_word, text=current_card["French"], fill="black")
    # Change after 3 seconds
    flip_timer = window.after(3000, show_translation)

    if button_clicked == "right":
        learned()

# Function to display the English translation of the current card
def show_translation():
    global current_card
    # Flip the card to show the English translation
    canvas.itemconfig(flip_card, image=back_flash_card)
    canvas.itemconfig(current_title, text="English", fill="white")
    canvas.itemconfig(current_word, text=current_card["English"], fill="white")

# Function to handle learned words
def learned():
    global current_card, learned_words
    # Append the known words to the list of learned cards
    learned_words.append(current_card)
    # Saving the learned words to a new csv
    df = pandas.DataFrame(learned_words)
    df.to_csv("data/words_learned.csv", index=False)
    # Removing the learned cards from the list of cards to learn
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

# Creating the main window
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Setting up the timer for flipping the flashcard
flip_timer = window.after(3000, func=show_translation)

# Creating the canvas for displaying flashcards
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_flash_card = PhotoImage(file="images/card_front.png")
back_flash_card = PhotoImage(file="images/card_back.png")
flip_card = canvas.create_image(400, 263, image=front_flash_card)
current_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
current_word = canvas.create_text(400, 253, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Creating buttons for user interaction
right_image = PhotoImage(file="images/right.png")
right = Button(image=right_image, highlightthickness=0, command=lambda: show_card("right"))
right.grid(row=1, column=1)
wrong_image = PhotoImage(file="images/wrong.png")
wrong = Button(image=wrong_image, highlightthickness=0, command=lambda: show_card("wrong"))
wrong.grid(row=1, column=0)

# Displaying the initial flashcard
show_card("null")

# Running the application
window.mainloop()
