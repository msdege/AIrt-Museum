import pygame
import requests # used to download images
import io
import openai  # OpenAI Python library to make API calls
import os # used to access filepaths
from PIL import Image  # used to print and edit images


class image:

    def __init__(self):
        # set API key
        # openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        """
        Variables
        """
        self.showInGame = True
        self.userPrompt = None
        self.generated_image = None
        self.image_dir_name = "generatedImages"
        self.image_dir_full = None
        self.generated_image_filepath = None

        # initialize pygame
        pygame.init()

        self.setupDirectory()

    def setupDirectory(self):
        # DALL-E Directory Setup
        # set a directory to save DALL·E images to
        self.image_dir_full = os.path.join(os.curdir, self.image_dir_name)

        # create the directory if it doesn't yet exist
        if not os.path.isdir(self.image_dir_full):
            os.mkdir(self.image_dir_full)

        # print the directory to save to
        print("image_dir="+self.image_dir_full)


    def getUserInput(self):

        print("Prompt DALL-E with your request: ")
        self.userPrompt = input()


    # Load AI-generated art
    def generateArt(self):

        if not self.userPrompt:
            print("Prompt has not been inputted.")
            self.getUserInput()

        self.generated_image = openai.Image.create(
            prompt=self.userPrompt, 
            n=1, 
            size="512x512",
            response_format="url",
            )


    def saveTheImage(self):

        if not self.generated_image:
            print("Can not save. Image has not been generated.")
            self.generateArt()

        generated_image_name = self.userPrompt[:8] + ".png"  # any name you like; the filetype should be .png
        generated_image_filepath = os.path.join(self.image_dir_full, generated_image_name)
        generated_image_url = self.generated_image["data"][0]["url"]  # extract image URL from response
        generated_image = requests.get(generated_image_url).content  # download the image

        with open(generated_image_filepath, "wb") as image_file: # wb is binary format for writing
            image_file.write(generated_image)  # write the image to the file

        self.generated_image_filepath = generated_image_filepath


    def printImage(self):

        print("Printing image from filepath: " + self.generated_image_filepath)

        if self.showInGame:
            art_image = pygame.image.load(self.generated_image_filepath)
            return art_image
        
        else: # open image in Windows Image Viewer (or user's default choice)
            img = Image.open(self.generated_image_filepath)
            img.show()


    """ 
    TESTING METHODS 
    """

    def printModels(self):

        models = openai.Model.list()

        for val in range(len(models)):
            print(models.data[val].id)

    def getPremadeImage(self, image_name: str):

        # Retrieve pre-produced image from generateImages file
        self.generated_image_filepath = os.path.join(self.image_dir_full, image_name)

if __name__ == "__main__":

    img = image()

    testing_mode = False

    if testing_mode:
        img.getPremadeImage("a painti.png")

    else:
        img.getUserInput()
        img.generateArt()
        img.saveTheImage()
    
    art_image = img.printImage()

    # Set up display
    display_width = 800
    display_height = 600
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("AI Art Museum")

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Display AI-generated art on the wall
        # math for centered coords
        x = (display_width - 512) // 2
        y = (display_height - 512) // 2
        game_display.blit(art_image, (x, y))
        
        pygame.display.update()

        # Clear the screen
        # game_display.fill((255, 255, 255))

        pygame.display.flip()

    pygame.quit()
    quit()
