import json
import os
import shutil

class Slideshow():

    def __init__(self):
        self.ROOT_PATH = './static/slideshows/'
        self.SLIDESHOWPATH = './subsections/slideshow/data/slideshow_data.json'

    def setRoot(self, root):
        self.ROOT_PATH = root

    def slideshowExists(self, slideshow):
        for i in self.getSlideshows():
            if i["name"] == slideshow:
                return True
        return False

    def getSlideshows(self) -> list:
        with open(self.SLIDESHOWPATH, 'r') as f:
            return json.loads(f.read())

    def writeSlideshows(self, data: list) -> None:
        with open(self.SLIDESHOWPATH, 'w') as a:
            a.write(json.dumps(data, indent=2, sort_keys=True))

    def deleteSlideshow(self, slideshow: str) -> None:
        slideshows = self.getSlideshows()
        for i in slideshows:
            if i["name"] == slideshow:
                slideshows.pop(slideshows.index(i))
        self.writeSlideshows(slideshows)
        shutil.rmtree(self.ROOT_PATH + f'{slideshow}')

    def addSlideshow(self, slideshow: str) -> None:
        slideshows = self.getSlideshows()
        slideshows.append({ "name": slideshow})
        if not self.slideshowExists(slideshow):
            self.writeSlideshows(slideshows)
            try:
                os.makedirs(self.ROOT_PATH + f'{slideshow}')
            except:
                None