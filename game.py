import random
import screeninfo
import tkinter as tk

class Game(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill=tk.BOTH)
        self.create_start_widgets()
        self.height = (self.getscreensize()[1] // 2)
        self.width = (self.getscreensize()[0] // 2)
        self.master.geometry(str(self.width) + "x" + str(self.height))
        self.master.title("Missing Letter Game")
        self.master.minsize(800, 600)
        # self.bind("<Return>", lambda x: self.check_answer()) # This will be used as a short cut to submit the answer Currently not working
        self.bind("<Configure>", lambda x: self.resize())
        
    def getscreensize(self):
        """
        This function will return the size of the screen
        """
        screen = screeninfo.get_monitors()[0]
        return screen.width, screen.height
    
    def resize(self):
        """
        Gets new window size when window is resized
        """
        self.scale = ((self.winfo_width() / self.width) * (self.winfo_height() / self.height)) ** 0.5
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.scale_objects()

    def scale_objects(self):
        """
        Scales all ojects in the canvas size
        """
        try:
            self.story_box.config(height=(self.height // 50), width=(self.width // 20), font=("Courier", int(self.story_box_font_size * self.scale)))
            self.story_box_font_size = self.story_box_font_size * self.scale
            self.story_box.update()
        except (AttributeError, tk.TclError):
            pass
        try:
            self.barrier.config(font=("Courier", int(self.barrier_font_size * self.scale)))
            self.barrier_font_size = self.barrier_font_size * self.scale
            self.barrier.update()
        except (AttributeError, tk.TclError):
            pass
        try:
            self.start_button.config(font=("Courier", int(self.start_button_size * self.scale)))
            self.start_button_size = self.start_button_size * self.scale
            self.start_button.update()
        except (AttributeError, tk.TclError):
            pass
        try:
            self.difficulty_scale.config(font=("Courier", int(self.difficulty_scale_size * self.scale)), length=(self.difficulty_scale_size * 4 * self.scale))
            self.difficulty_scale_size = self.difficulty_scale_size * self.scale
            self.difficulty_scale.update()
        except (AttributeError, tk.TclError):
            pass
        try:
            self.quit_button.config(font=("Courier", int(self.quit_button_size * self.scale)))
            self.quit_button_size = self.quit_button_size * self.scale
            self.quit_button.update()
        except (AttributeError, tk.TclError):
            pass
        try:
            self.answer_box.config(font=("Courier", int(self.awnser_box_size * self.scale)), width=round(self.awnser_box_size / 7 * self.scale))
            self.awnser_box_size = self.awnser_box_size * self.scale
            self.answer_box.update()
        except (AttributeError, tk.TclError):
            pass
        try:
            self.submit.config(font=("Courier", int(self.submit_size * self.scale)))
            self.submit_size = self.submit_size * self.scale
            self.submit.update()
        except (AttributeError, tk.TclError):
            pass
        

    def game(self, difficulty):
        """This is a simple game to guess a letter from the alphabet"""
        letters = []
        self.guesses = 3
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
        width = self.getscreensize()[0]
        height = self.getscreensize()[1]
        self.barrier_font_size = (((width / 100) * (height / 100)) ** 0.5) * 2 # This is a formula to scale the font size based on the screen size
        self.barrier = tk.Label(self, text="Welcome to the Missing Letter Game!", font=("Courier", int(self.barrier_font_size)))
        self.barrier.pack(side="top")
        self.start_button_size = (((width / 200) * (height / 200)) ** 0.5) * 2 # This is a formula to scale the font size based on the screen size
        self.start_button = tk.Button(self, font=("Courier", int(self.start_button_size)))
        self.start_button["text"] = "Play Game\n(click me)"
        self.start_button["command"] = lambda : self.game(self.difficulty_scale.get()) #Grabs difficulty from the slider
        self.start_button.pack(side="top")
        self.difficulty_scale_size = (((width / 100) * (height / 100)) ** 0.5) * 2 # This is a formula to scale the font size based on the screen size
        self.difficulty_scale = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL, font=("Courier", int(self.difficulty_scale_size)), length=(self.difficulty_scale_size * 4))
        self.difficulty_scale.pack(side="top")

        self.quit_button_size = (((width / 100) * (height / 100)) ** 0.5) # This is a formula to scale the font size based on the screen size
        self.quit_button = tk.Button(self, text="QUIT", fg="red",font=("Courier", int(self.quit_button_size)),
                            command=self.master.destroy)
        self.quit_button.pack(side="top")

    def create_game_widgets(self, letters, replacement):
        width = self.getscreensize()[0]
        height = self.getscreensize()[1]
        self.story_box_font_size = (((width / 100) * (height / 100)) ** 0.5) # This is a formula to scale the font size based on the screen size
        self.remove_start_widgets()
        self.barrier.config(text="Remaining Letters:" + str(len(letters)))
        self.barrier.pack(side="top") 
        self.story_box = tk.Text(self, height=((self.height // 50)), width=((self.width // 20)), font=("Courier", int(self.story_box_font_size)), wrap=tk.WORD)
        self.story_box.pack(side="top")
        self.scroll = tk.Scrollbar(self, command=self.story_box.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.story_box.config(yscrollcommand=self.scroll.set)
        # self.smooth_story_insert()
        self.story_box.config(state=tk.DISABLED)
        self.awnser_box_size = (((width / 100) * (height / 100)) ** 0.5) # This is a formula to scale the font size based on the screen size
        self.answer_box = tk.Entry(self, width=round(self.awnser_box_size / 7,), font=("Courier", int(self.awnser_box_size)))
        self.answer_box.pack(side="top")
        self.submit_size = (((width / 100) * (height / 100)) ** 0.5) # This is a formula to scale the font size based on the screen size
        self.submit = tk.Button(self, text="Submit", fg="green", command=lambda: self.check_answer(letters, replacement), font=("Courier", int(self.submit_size)))
        self.submit.pack(side="top")

    def check_answer(self, letters, replacement):
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
        self.guesses -= 1
        if self.guesses == 0:
            self.barrier.config(text="You lost!")
            self.answer_box.destroy()
            self.submit.destroy()
            self.quit_button = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
            self.quit_button.pack(side="top")

    def update_game(self, answer, letters, replacement):
        letters.remove(answer)
        self.replace_letters(letters, replacement)
        story = self.story
        self.story_box.config(state=tk.NORMAL)
        self.story_box.delete("1.0", tk.END)
        self.story_box.insert(tk.END, story)
        self.story_box.config(state=tk.DISABLED)
        print(len(letters))
        if len(letters) == 0:
            self.barrier.config(text="You won!")
            self.answer_box.destroy()
            self.submit.destroy()
            self.quit_button = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
            self.quit_button.pack(side="top")


    def remove_start_widgets(self):
        self.start_button.destroy()
        self.difficulty_scale.destroy()
        self.quit_button.destroy()

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