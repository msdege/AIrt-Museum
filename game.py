# code to combine the image and music classes so they can be played in PyGame

import music
import image
import pygame

class game:

    def __init__(self) -> None:

        # Variables
        self.display_width = 800
        self.display_height = 600
        self.game_display = None
        self.art_image = None

        # create class objects of music and image
        self.img = image.image()
        self.msc = music.music()

        # initialize pygame
        pygame.init()

        self.setupDisplay()
        self.setupImage()
        self.setupMusic()

    def setupDisplay(self):
        
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("AI Art Museum")

    def setupImage(self):
        self.img.getUserInput()
        self.img.generateArt()
        self.img.saveTheImage()
        self.art_image = self.img.printImage()

    def setupMusic(self):
        self.msc.getUserInput()
        self.msc.generateMusic()
        self.msc.saveMusic()
        # we don't want to play the music right away

    def playGame(self):
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

            self.msc.playMusic()

            # Clear the screen
            # game_display.fill((255, 255, 255))

        pygame.quit()
        quit()    


if __name__ == "__main__":

    gm = game()
    gm.playGame()
