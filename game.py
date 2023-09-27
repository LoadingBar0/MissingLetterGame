import random
import screeninfo
import tkinter as tk

guesses = 3

class Game(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill=tk.BOTH)
        self.create_start_widgets()
        self.height = self.getscreensize()[1]
        self.width = self.getscreensize()[0]
        self.master.geometry(str(self.width) + "x" + str(self.height))
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.master.title("Missing Letter Game")
        self.bind("<Return>", lambda x: self.check_answer())
        self.bind("<Configure>", lambda x: self.resize())
        
    def getscreensize(self):
        """
        This function will return the size of the screen
        """
        screen = screeninfo.get_monitors()[0]
        return screen.width, screen.height
    
    def resize(self):
        """
        
        """

        


    def scale(self, object, x1, y1, x2, y2):
        """
        Scales all ojects in the canvas
        """

    def game(self, difficulty):
        """This is a simple game to guess a letter from the alphabet"""
        letters = []
        self.pick_story()

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
        
        self.replace_letters(letters, replacement)

        self.create_game_widgets(letters, replacement)
        
    def replace_letters(self, letters, replacement):
        """
        This function replaces all letters in the story with the replacement character
        """
        story = self.story

        if not letters:
            self.story = self.orignal_story
            return
        
        for letter in letters:
            story = story.replace(letter, replacement)
            story = story.replace(letter.upper(), replacement)

        
        self.story = story

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

    def create_game_widgets(self, letters, replacement):
        self.remove_start_widgets()
        self.barrier = tk.Label(self, text="Guess a letter!")
        self.remaining = tk.Label(self, text="Remaining letters: " + str(len(letters)))
        self.remaining.pack(side="top")
        self.story_box = tk.Text(self, height=12, width=95) #Sets the box to
        self.story_box.pack(side="top")
        self.scroll = tk.Scrollbar(self, command=self.story_box.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.story_box.config(yscrollcommand=self.scroll.set)
        self.smooth_story_insert()
        self.story_box.config(state=tk.DISABLED)
        self.answer_box = tk.Entry(self, width=2)
        self.answer_box.pack(side="top")
        self.submit = tk.Button(self, text="Submit", fg="green", command=lambda: self.check_answer(letters, replacement))
        self.submit.pack(side="top")

    def check_answer(self, letters, replacement):
        global guesses #This is the number of guesses the player has left I need to find a way to do this without using a global variable but for now this will do
        answer = self.answer_box.get().lower()
        if len(answer) > 1:
            self.barrier.config(text="Please enter only one letter at a time!", fg="red")
            self.answer_box.delete(0, tk.END)
            return
        if answer in letters:
            self.barrier.config(text="You guessed it right!", fg="green")
            self.update_game(answer, letters, replacement)
            try:
                self.answer_box.delete(0, tk.END)
            except tk.TclError:
                pass
        else:
            self.barrier.config(text="Try again!", fg="red")
            self.answer_box.delete(0, tk.END)
            self.update_guesses()
    
    def smooth_story_insert(self):
        """
        This function will insert the story into the text box one character at a time
        """
        story = self.story
        for i in range(len(story)):
            self.story_box.insert(tk.END, story[i])
            self.story_box.after(2)
            self.story_box.update()

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

    def update_game(self, answer, letters, replacement):
        letters.remove(answer)
        self.replace_letters(letters, replacement)
        story = self.story
        self.remaining.config(text="Remaining letters: " + str(len(letters)))
        self.story_box.config(state=tk.NORMAL)
        self.story_box.delete("1.0", tk.END)
        self.story_box.insert(tk.END, story)
        self.story_box.config(state=tk.DISABLED)
        print(len(letters))
        if len(letters) == 0:
            self.barrier.config(text="You won!")
            self.answer_box.destroy()
            self.submit.destroy()
            self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
            self.quit.pack(side="top")


    def remove_start_widgets(self):
        self.barrier.config(text="")
        self.start_button.destroy()
        self.difficulty.destroy()
        self.quit.destroy()

    def pick_story(self):
        """
        This function will pick a story from a list of stories sotrored in a file
        """
        story_number = random.randrange(0, 101, 2)
        story_file = open("stories", "r")
        for i, line in enumerate(story_file):
            if i == story_number:
                story = line
        story_file.close()
        self.story = story.replace("\\n", "\n")
        self.orignal_story = self.story

def main():
    root = tk.Tk()
    app = Game(master=root)
    app.mainloop()

if __name__ == "__main__":
    main() 