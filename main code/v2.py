#########################################
#                                       #
#   Car Park Layout Program             #
#   Version 2                           #
#                                       #
#   Starting to add the draw            #
#   image functions                     #
#                                       #
#########################################



#########################################
######################################### Import libraries and modules
#Import PIL
from PIL import Image, ImageTk, ImageDraw #for opening file
#Import Tkinter
import Tkinter #for opening window



#########################################
######################################### Constants
#Background Image File
backgroundImageLocation = "test.jpg"
#Width of car park space

#Length of car park space

#Width of road



#########################################
######################################### Classes
###################
#Vertex Class - contains an x and y position
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



class shape(): #need to change this ordered list to work for a shape
    def __init__(self):
        self.vertices = []

    def isEmpty(self):
        return len(self.vertices) == 0

    def addCoordinatesToEnd(self,both):
        temp = vertex()
        temp.setXY(both)
        self.addVertexToEnd(temp)

    def addVertexToEnd(self,vertex):
        self.vertices += [vertex]

    def numberOfVertices(self):
        return len(self.vertices)

    def vertices(self):
        return self.vertices

    def coordinates(self):
        coordinateList = []
        for each in self.vertices:
            coordinateList += [each.coordinates()]
        return coordinateList

    def search(self,both):
        foundPositions = []
        for count in range(self.numberOfVertices()):
            if vertices[count].coordinates() == both:
                foundPositions += [count]
        return foundPositions

    def removeFromPosition(self,position):
        self.vertices =  self.vertices[:position] + self.vertices[position+1:]

    def removeFromEnd(self):
        self.removeFromPosition(self.numberOfVertices()-1)



#########################################
######################################### Sub-routines
def openImage(fileName):
    print #header


def openImageAndGetClickedLocations(backgroundImageLocation): #will return clicked locations as a list
    window = Tkinter.Tk() #creates window
    image = Image.open(backgroundImageLocation) #creates an instance of an image class
    canvas = Tkinter.Canvas(window, width=image.size[0], height=image.size[1]) #image.size gives you the width and depth
    canvas.pack()
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk) #//2 needed in order to center the image

    canvas.bind("<Button-1>", whenImageIsClicked) #<Button-1> is the left mouse button
    #print "image size: " + str(image.size)
    Tkinter.mainloop()


def whenImageIsClicked(event):
    print "coords: " + str(event.x) + "," + str(event.y)

    #carparkOutline.addCoordinatesToEnd([event.x,event.y])
    #print carparkOutline.coordinates()

    #newImage = drawLinesOnImage(backgroundImageLocation,carparkOutline.coordinates(),128)
    #canvas.itemconfig(self.image_on_canvas, image = ...)




def drawLinesOnImage(fileName,coordinates,colour): #will return edited image
    image = Image.open(fileName)

    imageToDrawOn = ImageDraw.Draw(image)
    imageToDrawOn.line(coordinates, fill=colour)
    del imageToDrawOn

    return image


#########################################
######################################### Stuff it will do


carparkOutline = shape()
openImageAndGetClickedLocations(backgroundImageLocation)
carparkOutline = shape()
carparkOutline.addCoordinatesToEnd([3,7])
print carparkOutline.coordinates()

