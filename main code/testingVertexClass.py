import math

#-------------------------------------------------------------------------------
# Defining a vertex class. This is just a point. (Plural = vertices)
#-------------------------------------------------------------------------------
class vertex():
    def __init__(self,x = None, y = None):
        if (bool(x == None) != bool(y == None)): #if just one of them is a None value they will both be set as None values
            self.x = None
            self.y = None
            print "Both x and y were set as None, since only one was a None value"
        elif x == None and y == None:
            self.x = None
            self.y = None
        else:
            try:
                self.x = float(x)
                self.y = float(y)
            except:
                print "there was an error changing the x or y to float values, check what was inputted"
                print "they have both been set as None Values"
                self.x = None
                self.y = None

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getCoordinates(self):
        return [self.x,self.y]

    def setX(self,x):
        self.x = round(float(x),5)
        # the round function removes uneeded accuracy that could cause problems

    def setY(self,y):
        self.y = round(float(y),5)

    def setXY(self,both): #both will become the standard name for a tuple of an X and Y coordinate
        self.setX(both[0])
        self.setY(both[1])

    def rotateAboutAnotherVertex(self,about,angle): #the position it rotates clockwise about will be passed in as a vertex class.
                                                    #the angle will be given in radians
        #print "angle", angle
        angle = -angle #I realised the matrix i used was to rotate anticlockwise, so this fixes that problem.
        newX = (self.x-about.x)*(math.cos(angle)) - (self.y-about.y)*(math.sin(angle)) + about.x
        newY = (self.y-about.y)*(math.cos(angle)) + (self.x-about.x)*(math.sin(angle)) + about.y
        self.setXY([newX,newY])

    def translateXY(self,translationXY): #translation should be passed in the form [X,Y]
        self.setX(self.x + translationXY[0])
        self.setY(self.y + translationXY[1])

