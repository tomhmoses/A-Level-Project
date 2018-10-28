#===============================================================================
# Version 11
# Adding Shaps class with ability to rotate and translate
#
#
#===============================================================================



#-------------------------------------------------------------------------------
# Importing required modules
#     PIL: For opening and editing image (will use this in a later version)
# Tkinter: Provides UI framework (will use this in a later version)
#    Math: Allows me to easily use trigonometry to rotate the vertices
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk, ImageDraw
from Tkinter import *
import math

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
        return self.x

    def getY(self):
        return self.y

    def coordinates(self):
        return [self.x,self.y]

    def setX(self,x):
        self.y = x

    def setY(self,Y):
        self.y = y

    def setXY(self,both): #both with become the standard name for a tuple of an X and Y coordinate
        self.x = both[0]
        self.y = both[1]

    def rotateAboutAnotherVertex(self,about,angle): #the position it rotates clockwise about will be passed in as a vertex class.
                                                    #the angle will be given in radians
        print "angle", angle
        angle = -angle #I realised the matrix i used was to rotate anticlockwise, so this fixes that problem.
        newX = (self.x-about.x)*(math.cos(angle)) - (self.y-about.y)*(math.sin(angle)) + about.x
        newY = (self.y-about.y)*(math.cos(angle)) + (self.x-about.x)*(math.sin(angle)) + about.y
        self.setXY([newX,newY])

    def translateXY(self,translationXY): #translation should be passed in the form [X,Y]
        self.x = (self.x + translationXY[0])
        self.y = (self.y + translationXY[1])


def toRadians(degrees):
    return degrees*((2*math.pi)/360)


#-------------------------------------------------------------------------------
# Defining a shape class.
# This is just a collection of vertices in a specific order.
#-------------------------------------------------------------------------------

class shape():
    def __init__(self):
        self.vertices = []

    def addVertex(self,vertex):
        self.vertices.append(vertex)

    def addVerticesXY(self,vertices): #vertices should be as lists within lists
        for each in vertices:
            temp = vertex()
            temp.setXY(each)
            self.addVertex(temp)

    def getVertices(self):
        return self.vertices

    def getVerticesCoordinates(self):
        listOfCoordinates = []
        for eachVertex in self.vertices:
            listOfCoordinates.append(eachVertex.coordinates())
        return listOfCoordinates

    def getDistanceToNextVertex(self,vertexNumber): #will return the first vertex from the longest line.
        if len(self.vertices) < vertexNumber: #checks the vertex will exist
            print "Error, vertex does not exist"
        elif len(self.vertices) < 2:
            print "Error, not enough vertices to find distance"
        else:
            vertex1 = self.vertices[vertexNumber]
            vertex2 = self.vertices[(vertexNumber+1)%(len(self.vertices))]
            differenceInX = vertex1.getX() - vertex2.getX()
            differenceInY = vertex1.getY() - vertex2.getY()
            distance = math.sqrt( differenceInX**2 + differenceInY**2 )
            return distance
        return None #if the distance was not retuned it will return a null value


    def getLongestSide(self): #will return the first vertex from the longest line.
        longestVertextNumber = None
        if len(self.vertices) < 2:
            print "Error, not enough vertices to find distance"
        elif len(self.vertices) == 2:
            longestVertextNumber = 0
        else:
            longestVertextNumber = 0
            for count in range(len(self.vertices)):
                if self.getDistanceToNextVertex(count) > self.getDistanceToNextVertex(longestVertextNumber):
                    longestVertextNumber = count
        return longestVertextNumber #will return the number of the first vertex of the longest edge of the shape.

    def rotateAboutAVertex(self,about,angle):
        for eachVertex in self.vertices:
            eachVertex.rotateAboutAnotherVertex(self,about,angle)

    def translate(self,translationXY):
        for eachVertex in self.vertices:
            eachVertex.translateXY(translationXY)

    def makeLongestSideFlat(self):
        makeSideAfterVertexFlat(self.vertices[self.getLongestSide()])

    def makeSideAfterVertexFlat(self,vertex1):
        for count in range(len(self.vertices)):
            if self.vertices[count] == vertex1:
                vertex2 = self.vertices[(count+1)%(len(self.vertices))]
        differenceInX = vertex1.getX() - vertex2.getX()
        differenceInY = vertex1.getY() - vertex2.getY()
        angle = (math.atan((differenceInY)/(differenceInX)))    #this finds the angle from horizonal of the line connecting the first vertex to the next
                                                                #when we have this anlgle, we can turn the entire shape by the same angle rotating about
        self.rotateAboutAVertex(vertex1,angle)                  #the first vertex in order to make this side lay flat.











#-------------------------------------------------------------------------------
# I will here define the sizes of spaces and make it as a shape
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# I need to make the standard tile of parking spaces (they will be groups of spaces with a standard size)
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# I need a way to test if any points of a shape are outside the other shape.
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Testing procedures
#-------------------------------------------------------------------------------

def testingRotatingAVertex():
    print math.cos(math.pi/2)
    origin = vertex()
    origin.setXY([0,0])

    toRotate = vertex()
    toRotate.setXY([0,20])
    print toRotate.coordinates()

    angle = toRadians(90)
    print angle*2 #should be pi, just to check.

    toRotate.rotateAboutAnotherVertex(origin,angle)
    print toRotate.coordinates() #should return 20,0 (it does)


def testingDistances():
    myShape = shape()
    myCoords = [[0,0],[8,0],[8,9],[0,9],[-10,-10],[0,-5]]
    for each in myCoords:
        temp = vertex()
        temp.setXY(each)
        myShape.addVertex(temp)
    returnedCoords = myShape.getVerticesCoordinates() #should return the same coordinates as in myCoords (it does)
    print returnedCoords

    for each in [0,1,3,8]:
        print myShape.getDistanceToNextVertex(each) #should return correct distances three times,
                                                    #then an error that the vertex does not exist then None (it does)


def testingFindingLongestDistance():
    myTriangle = shape()
    for each in [[0,0],[0,5],[10,0]]: #vertex 1 (starting at 0) has longest distance after it
        temp = vertex()
        temp.setXY(each)
        myTriangle.addVertex(temp)
    print myTriangle.getLongestSide() #should print 1 (it does)

    myEmptyShape = shape()
    print myEmptyShape.getLongestSide() #should return an appropriate error then print None (it does)

    myTwoPointShape = shape()
    myTwoPointShape.addVerticesXY([[0,0],[0,1]])
    print myTwoPointShape.getLongestSide() #should return 0 (it does)



#-------------------------------------------------------------------------------
# code that will be executed
#-------------------------------------------------------------------------------
testingFindingLongestDistance()


