#===============================================================================
# Version 10
# Starting over from scratch
#
# I plan to just do it mathmatically for now
#===============================================================================


#-------------------------------------------------------------------------------
# Importing required modules
#     PIL: For opening and editing image (will use this in a later version)
# Tkinter: provides UI framework (will use this in a later version)
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk, ImageDraw
from Tkinter import *

#-------------------------------------------------------------------------------
# Defining the space I will work within
#-------------------------------------------------------------------------------
minX = 0
minY = 0
maxX = 1
maxY = 1


#-------------------------------------------------------------------------------
# Defining a vertex class. This is just a point. (Plural = vertices)
#-------------------------------------------------------------------------------
class vertex():
    def __init__(self):
        self.x = None
        self.y = None
        
    def getX(self):
        return self.X

    def getY(self):
        return self.Y
    
    def coordinates(self):
        return [self.X,self.Y]

    def setX(self,X):
        self.X = X
    
    def setY(self,Y):
        self.Y = Y
    
    def setXY(self,both):
        self.X = both[0]
        self.Y = both[1]


#-------------------------------------------------------------------------------
# Defining a shape class.
# This is just a collection of vertices in a specific order.
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
# I will here define the sizes of  spaces and make it as a shape
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# I need to make the standard tile of parking spaces
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# I need a way to test if any points of a shape are outside the other shape.
#-------------------------------------------------------------------------------



