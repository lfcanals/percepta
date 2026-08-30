class MetaRectification:
    """
        Wraps all kind of rectifications and can change them
        in realtime.
    """
    def __init__(self):
        self.noRectifier = NoRectifier()
        self.enabledRectifier = self.noRectifier

    
    def set(self, rectifierName):
        if rectifierName is None or rectifierName == "":
            self.enabledRectifier = self.noRectifier
        else:
            # By the moment do not know what other names are available....
            pass


    def rectify(self, image):    
        return self.enabledRectifier.rectify(image)


class NoRectifier:
    def rectify(self, image):
        return image
