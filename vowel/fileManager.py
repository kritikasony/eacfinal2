from os import listdir
from os.path import isfile, join

path = "/Users/akash.gupta/Downloads/ForKritika/SoundFiles"

def get_files():
	return [f for f in listdir(path) if isfile(join(path, f))]
