"""
AudioCraft Resources:
https://huggingface.co/facebook/musicgen-small
https://github.com/facebookresearch/audiocraft

"""

import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import os
import sounddevice as sd
import soundfile as sf


class music:

    def __init__(self, testing_mode=False, duration=10):

        self.model = None
        self.music_descriptions = []
        self.wav = None # variable storing generated music
        self.music_path = None

        if not testing_mode:
            self.setupModelandDirectory(duration=duration)

    def setupModelandDirectory(self, duration):
        # AudioCraft Model setup
        self.model = MusicGen.get_pretrained("small")
        self.model.set_generation_params(duration=duration)  # generate X seconds of music

        # AudioCraft Directory Setup:
        # set a directory to save AudioCraft music to
        self.image_dir_full = os.path.join(os.curdir, "generatedMusic")

        # create the directory if it doesn't yet exist
        if not os.path.isdir(self.image_dir_full):
            os.mkdir(self.image_dir_full)

        # print the directory to save to
        print("music_dir="+self.image_dir_full)

    def getUserInput(self):
        
        print("Provide your music request: ")
        userPrompt = input()
        self.music_descriptions.append(userPrompt)

    def generateMusic(self):
        
        if len(self.music_descriptions) == 0:
            print("Prompt has not been inputted.")
            self.getUserInput()
        
        self.wav = self.model.generate(self.music_descriptions, progress=True)


    def saveMusic(self):

        for idx, one_wav in enumerate(self.wav):
            # Will save under {description}.wav, with loudness normalization at -14 db LUFS.
            description = self.music_descriptions[idx][:10]
            self.music_path = audio_write(f'generatedMusic\{description}', one_wav.cpu(), self.model.sample_rate, strategy="loudness", loudness_compressor=True)

            print("Path to generated music:", self.music_path)


    def playMusic(self):
        # How do i open a wav file in python?
        # Use sounddevice and soundfile

        if not self.music_path:
            print("No music has been generated. Exiting program...")
            return
        
        # Extract data and sampling rate from file
        data, fs = sf.read(self.music_path, dtype='float32')

        # play music indefinitely
        while True:  
            sd.play(data, fs)
            sd.wait()  # Wait until file is done playing

    """
    Getters and Testing Methods
    """
    def getMusicPath(self) -> str:
        return self.music_path

    def getPrecreatedMusic(self, path: str):
        self.music_path = path


if __name__ == "__main__":

    testing_mode = False

    mus = music(testing_mode, duration=10)

    if testing_mode:
        mus.getPrecreatedMusic("generatedMusic\\high_tempo.wav")

    else:
        mus.getUserInput()
        mus.generateMusic()
        mus.saveMusic()
    
    mus.playMusic()


