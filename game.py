import random
import tkinter as tk

guesses = 3

class Game(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_start_widgets()
        self.master.geometry("800x600") # Sets the window size to 800x600 
        self.master.title("Missing Letter Game")
        

    def game(self, difficulty):
        """This is a simple game to guess a letter from the alphabet"""
        letters = []
        original_story = self.gerneate_story()
        story = original_story
        if  difficulty <= 5:
            replacement = "_"
        elif difficulty <= 10:
            replacement = ""
        else:
            print("Invalid difficulty level. Please try again.")
            return

        for i in range(difficulty): # This loop generates a list of random letters for testing purposes we will use a and b
            ascii_x = random.randrange(97, 123)
            if chr(ascii_x) not in letters:
                letters += chr(ascii_x)
            else:
                i -= 1

        story = self.replace_letters(original_story, letters, replacement)

        self.create_game_widgets(story, original_story, letters, replacement)
        
    def replace_letters(self, orignal_story, letters, replacement):
        """
        This function replaces all letters in the story with the replacement character
        """
        story = orignal_story
        for letter in letters:
            story = story.replace(letter, replacement)
            story = story.replace(letter.upper(), replacement)

        if not letters:
            story = orignal_story
        
        return story

    def create_start_widgets(self):
        self.barrier = tk.Label(self, text="Welcome to the Missing Letter Game!")
        self.barrier.pack(side="top")
        self.start_button = tk.Button(self)
        self.start_button["text"] = "Play Game\n(click me)"
        self.start_button["command"] = lambda : self.game(self.difficulty.get()) #Grabs difficulty from the slider
        self.start_button.pack(side="top")
        self.difficulty = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL)
        self.difficulty.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
        self.quit.pack(side="bottom")

    def create_game_widgets(self, story, original_story, letters, replacement):
        self.remove_start_widgets()
        self.barrier = tk.Label(self, text="Guess a letter!")
        self.remaining = tk.Label(self, text="Remaining letters: " + str(len(letters)))
        self.remaining.pack(side="top")
        self.story_box = tk.Text(self, height=12, width=95)
        self.story_box.pack(side="top")
        self.story_box.insert(tk.END, story)
        self.story_box.config(state=tk.DISABLED)
        self.answer_box = tk.Entry(self, width=2)
        self.answer_box.pack(side="top")
        self.submit = tk.Button(self, text="Submit", fg="green", command=lambda: self.check_answer(original_story, letters, replacement))
        self.submit.pack(side="top")

    def check_answer(self, oringal_story, letters, replacement):
        global guesses #This is the number of guesses the player has left I need to find a way to do this without using a global variable but for now this will do
        answer = self.answer_box.get().lower()
        if len(answer) > 1:
            self.barrier.config(text="Please enter only one letter at a time!", fg="red")
            self.answer_box.delete(0, tk.END)
            return
        if answer in letters:
            self.barrier.config(text="You guessed it right!", fg="green")
            self.update_game(oringal_story, answer, letters, replacement)
            try:
                self.answer_box.delete(0, tk.END)
            except tk.TclError:
                pass
        else:
            self.barrier.config(text="Try again!", fg="red")
            self.answer_box.delete(0, tk.END)
            self.update_guesses()

    def update_guesses(self):
        global guesses #This is the number of guesses the player has left I need to find a way to do this without using a global variable but for now this will do
        guesses -= 1
        if guesses == 0:
            self.barrier.config(text="You lost!")
            self.answer_box.destroy()
            self.submit.destroy()
            self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
            self.quit.pack(side="bottom")

    def update_game(self, orignal_story, answer, letters, replacement):
        story = self.story_box.get("1.0", tk.END)
        letters.remove(answer)
        story = self.replace_letters(orignal_story, letters, replacement)
        self.remaining.config(text="Remaining letters: " + str(len(letters)))
        self.story_box.config(state=tk.NORMAL)
        self.story_box.delete("1.0", tk.END)
        self.story_box.insert(tk.END, story)
        self.story_box.config(state=tk.DISABLED)
        if len(letters) == 0:
            self.barrier.config(text="You won!")
            self.answer_box.destroy()
            self.submit.destroy()
            self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
            self.quit.pack(side="bottom")


    def remove_start_widgets(self):
        self.barrier.config(text="")
        self.start_button.destroy()
        self.difficulty.destroy()
        self.quit.destroy()

    def gerneate_story(self):
        """
        This function generates a story using Chat GTP api.
        """
        sample = "In the quaint village of Everwood, nestled beneath the towering mountains, lived a gifted inventor named Felix Whizbang. His workshop, a chaotic blend of gears and gizmos, was the heart of the town. One day, a mysterious portal materialized before him, revealing Zara, an adventurer with a glowing amulet.\n\nZara explained the amulet's purpose: to find the scattered ingredients for the legendary " + '"Elixir of Allure, "' + "a potion that bestowed irresistible charm. Together, they embarked on a whimsical quest through the Fantasylands, facing riddles and befriending fantastical creatures.\n\nTheir journey not only uncovered the elixir's secret but also revealed the true magic lay in the bonds of friendship forged along the way. In the end, they shared the elixir's charm with their village, making Everwood a place where even eccentric inventions found a warm welcome."
        return sample # For now we will use a sample story
        

def main():
    root = tk.Tk()
    app = Game(master=root)
    app.mainloop()

if __name__ == "__main__":
    main() 