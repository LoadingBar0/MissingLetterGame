import random
import tkinter as tk

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
        correct = 0
        letters = []
        original_story = self.gerneate_story()
        story = original_story
        story_lowercase = story.lower()
        if difficulty < 3:
            replacement = "_"
        elif difficulty < 5:
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

            for i in story_lowercase:
                if i in letters:
                    story = story.replace(i, replacement)
                    story = story.replace(i.upper(), replacement)

        self.create_game_widgets(story, letters, original_story)
        
    def create_start_widgets(self):
        self.barrier = tk.Label(self, text="Welcome to the Missing Letter Game!")
        self.barrier.pack(side="top")
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Play Game\n(click me)"
        self.hi_there["command"] = lambda : self.game(2) #Difficulty is currently set to 2 for testing purposes
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
        self.quit.pack(side="bottom")

    def create_game_widgets(self, story, letters, original_story):
        self.remove_start_widgets()
        self.story_box = tk.Text(self, height=12, width=95)
        self.story_box.pack(side="top")
        self.story_box.insert(tk.END, story)
        self.story_box.config(state=tk.DISABLED)
        self.answer_box = tk.Entry(self, width=95)
        self.answer_box.pack(side="top")
        self.submit = tk.Button(self, text="Submit", fg="green", command=lambda: self.check_answer(letters, original_story))
        self.submit.pack(side="top")

    def check_answer(self, letters, original_story):
        answer = self.answer_box.get()
        if answer in letters:
            self.update_story(answer, original_story)
            self.barrier.config(text="You guessed it right!")
            try:
                self.answer_box.delete(0, tk.END)
            except tk.TclError:
                pass
        else:
            self.barrier.config(text="Try again!")
            self.answer_box.delete(0, tk.END)

    def update_story(self, answer, original_story):
        story = self.story_box.get("1.0", tk.END)
        i = 0
        while i < len(story):
            if story[i] == "_" and original_story[i] == answer:
                story = story[:i] + answer + story[i+1:]
            if story[i] == "_" and original_story[i] == answer.upper():
                story = story[:i] + answer.upper() + story[i+1:]
            i += 1
        self.story_box.config(state=tk.NORMAL)
        self.story_box.delete("1.0", tk.END)
        self.story_box.insert(tk.END, story)
        self.story_box.config(state=tk.DISABLED)
        if "_" not in story:
            self.barrier.config(text="You won!")
            self.answer_box.destroy()
            self.submit.destroy()
            self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
            self.quit.pack(side="bottom")


    def remove_start_widgets(self):
        self.barrier.config(text="")
        self.hi_there.destroy()
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