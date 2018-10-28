class tile():
    def __init__(self,width = 0, depth = 0):
         self.width = width
         self.depth = depth
         
    def getWidth(self):
        return self.width

    def getDepth(self):
        return self.depth


tiles = {'a':tile(),'b':tile(4,5)}

