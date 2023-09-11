"""
Class that combines the image and music classes so they can be played in PyGame
"""

"""
Resources:
    - threading in Python: https://www.geeksforgeeks.org/multithreading-python-set-1/
    - https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

"""

import threading
import music
import image
import pygame
from pygame import mixer

class game:

    def __init__(self) -> None:

        # Variables
        self.display_width = 800
        self.display_height = 600
        self.game_display = None
        self.art_image = None
        self.imagePrompt = None
        self.musicPrompt = None

        self.getUserInputs()

        # create objects of music and image
        self.img = image.image()
        self.setupImage()

        self.msc = music.music()
        self.setupMusic()

    """
    Instead of getting prompts in msc and img objects,
    get all prompts in this class to avoid waiting times.
    Provides base for future improvements
    """
    def getUserInputs(self):

        print("Prompt DALL-E with your art request: ")
        self.imagePrompt = input()

        print("Prompt AudioCraft with your music request: ")
        self.musicPrompt = input()
        

    def setupImage(self):
        #self.img.getUserInput()
        self.img.userPrompt = self.imagePrompt
        self.img.generateArt()
        self.img.saveTheImage()
        self.art_image = self.img.printImage()

    def setupMusic(self):
        # self.msc.getUserInput()
        self.msc.music_descriptions.append(self.musicPrompt)
        self.msc.generateMusic()
        self.msc.saveMusic()
        # we don't want to play the music right away

    def setupDisplay(self):
        
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("AI Art Museum")

    def setupPygameMusic(self):
        mixer.init() # Starting the mixer
        mixer.music.load(self.msc.getMusicPath()) # Loading the song
        mixer.music.set_volume(0.7) # Setting the volume
        mixer.music.play(loops=-1) # indefinitely play the song

    def playGame(self):
        # initialize pygame stuff
        pygame.init()
        self.setupDisplay()
        self.setupPygameMusic()

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Display AI-generated art on the wall
            # math for centered coords
            x = (self.display_width - 512) // 2
            y = (self.display_height - 512) // 2
            self.game_display.blit(self.art_image, (x, y))
            
            pygame.display.update()

            # Clear the screen
            # game_display.fill((255, 255, 255))

        pygame.quit()
        quit()    


if __name__ == "__main__":

    gm = game()
    gm.playGame()






"""
I had an idea to use multithreading to play the music in conjunction with game display,
but PyGame has a handy built-in "mixer" module which makes this much easier.
Old thread code for reference:
"""
# # Create two threads, one for PyGame (which includes art) and one for music
# t1 = threading.Thread(target=gm.msc.playMusic, args=())
# t2 = threading.Thread(target=gm.playGame, args=())

# t1.start()
# t2.start()

# # Once the threads start, the current program 
# # (you can think of it like a main thread) also keeps on executing. 
# # In order to stop the execution of the current program 
# # until a thread is complete, we use the join() method.
# t1.join()
# t2.join()