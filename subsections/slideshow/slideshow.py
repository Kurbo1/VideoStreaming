import json

class Slideshow():

    def __init__(self):
        self.SLIDESHOWPATH = './subsections/slideshow/data/slideshow_data.json'

    def getSlideshows(self):
        with open(self.SLIDESHOWPATH, 'r') as f:
            return json.loads(f.read())