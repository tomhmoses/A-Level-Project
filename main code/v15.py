#===============================================================================
# Version 15
# Adding tiles
# Now imports vertex and shape from other python file
# Now with Tile and Trim basic functionality
#
#===============================================================================



#-------------------------------------------------------------------------------
# Importing required modules
#     PIL: For opening and editing image (will use this in a later version)
# Tkinter: Provides UI framework (will use this in a later version)
#    Math: Allows me to easily use trigonometry to rotate the vertices
# Shapely: Allows me to easily have a way to test if a point is outside a shape
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk, ImageDraw
from Tkinter import *
import math
from shapely.geometry import Point, Polygon #this imports the required classes from shapely

from myVertexandShapeClasses import *



#-------------------------------------------------------------------------------
# Here I will define the sizes of spaces, W (width) will be the side facing the road
# The real life sizes in this program are in metres
#-------------------------------------------------------------------------------

sizes = {'standardW':2.4,'standardD':4.8,
         'minibusW':2.4,'minibusD':6,
         'gapBetweenDisabledSpaces':1.2,
         'motorcycleW':1.2,'motorcycleD':4.8,
         'roadWidth':6.0}




#-------------------------------------------------------------------------------
# I need to make the standard tile of parking spaces (they will be groups of spaces with a standard size)
#-------------------------------------------------------------------------------

class tile():
    def __init__(self,width = 0, depth = 0):
         self.width = width
         self.depth = depth
         
    def getWidth(self):
        return self.width

    def getDepth(self):
        return self.depth

tiles = {'standard':tile(sizes['standardW'],sizes['standardD']*2+sizes['roadWidth']), #standard tile should be fine for making the tile and trim and testing at first
         'minibus':tile(sizes['minibusW'],sizes['minibusD']*2+sizes['roadWidth']), #need to fix these tiles
         'gapBetweenDisabledSpaces':tile(sizes['gapBetweenDisabledSpaces'],sizes['standardD']*2+sizes['roadWidth']),
         'motorcycle':1.2,'motorcycleD':tile(sizes['standardW'],sizes['standardD']*2+sizes['roadWidth'])}
         
listOFTuplesOfNamesOfTilesInListAndHowManyOfEach = [('standard',1)] #it will not matter what the limit of the last item in the list is as this will be what the car park is then filled with.
#-------------------------------------------------------------------------------
# Algorythm i will use
#-------------------------------------------------------------------------------

#get all points of edge of the car park
#rotate so longest side is flat
#translate so is closest to the origin but all positive coordinates
#row-by-row place tiles (by adding them to a list)
#then make sure road works


#-------------------------------------------------------------------------------
# tile and trim
#-------------------------------------------------------------------------------

def tileAndTrim(carParkShape,tiles,listOFTuplesOfNamesOfTilesInListAndHowManyOfEach):
    print "Starting tile and trim"
    fill = False
    carParkFull = False
    bottomLeftVertex = vertex(0,0)
    placedTiles = []
    furthestRightVertex = carParkShape.getFurthestRightVertex()
    print "furthest right: " + str(furthestRightVertex.getCoordinates())
    furthestUpVertex = carParkShape.getFurthestUpVertex()
    for count in range(len(listOFTuplesOfNamesOfTilesInListAndHowManyOfEach)):
        tileLabel = listOFTuplesOfNamesOfTilesInListAndHowManyOfEach[count][0]
        currentTile = tiles[tileLabel]
        howMany = listOFTuplesOfNamesOfTilesInListAndHowManyOfEach[count][1]
        howManyLeft = howMany
        if count == (len(listOFTuplesOfNamesOfTilesInListAndHowManyOfEach) -1): #if it is final item i will fill car park with this tile
            fill = True

        while (howManyLeft > 0 or fill == True) and (carParkFull == False):
            #print "-------"
            print bottomLeftVertex.getCoordinates()
            #we will start testing at 0,0 then move right, then move onto a new row up when the current layer has been filled.
            #print "stub for placing the tile as a shape and testing if all of its vertices are within the car park shape"
            #makeShapeFromTile
            tileShape = makeShapeFromTile(bottomLeftVertex,tileLabel,tiles)
            validTilePlacement = testIfOneShapeIsWithinAnotherShape(tileShape,carParkShape)
            #print "stub for if tile was placed and is in boundary, add this shape to a list of car parking tiles created. Then reduce howManyLeft by 1."
            if validTilePlacement:
                print "valid " + tileLabel + " tile placement."
                howManyLeft = howManyLeft - 1
                placedTiles.append(tileShape)
            bottomLeftVertex.translateXY([ tiles[tileLabel].getWidth() , 0 ]) #moved bottom left vertex to the right
            #will see if bottom left vertex needs resetting
            #print "stub for testing if placing x is out of range, will then move y up the right height and reset x"
            if bottomLeftVertex.getX() > furthestRightVertex.getX():
                #print "out of range"
                bottomLeftVertex.setX(0)
                #print bottomLeftVertex.getCoordinates()
                bottomLeftVertex.translateXY([ 0 , tiles[tileLabel].getDepth() ]) #moved bottom left vertex up
                #print "stub for testing if placing y is out of range, if y was just change, if it is filledCarPark will be set to True"
                if bottomLeftVertex.getY() > furthestUpVertex.getY():
                    #print "Tried placing tiles in all spaces = true"
                    carParkFull = True
            
                #print "in range: " + str(furthestRightVertex.getX())
        if howManyLeft == 0:
            #was sucessful
            print "Placed all " + tileLabel + " spaces sucessfully"
            if carParkFull:
                print "Car park was filled. I filled it up with " + str(-howManyLeft) + " extra " + tileLabel + " spaces."
        else:
            print "car park was full and ran out of space to place what you wanted"
    return placedTiles
        

#-------------------------------------------------------------------------------
# Making a shape from a tile and a position to place the 
#-------------------------------------------------------------------------------

def makeShapeFromTile(bottomLeftVertex,tileLabel,tiles):
    tileShape = shape()
    bottomLeftCoords = bottomLeftVertex.getCoordinates()
    bottomLeftX = bottomLeftCoords[0]
    bottomLeftY = bottomLeftCoords[1]
    width = tiles[tileLabel].getWidth()
    depth = tiles[tileLabel].getDepth()
    tileShape.addVerticesXY([bottomLeftCoords,[bottomLeftX,bottomLeftY+depth],[bottomLeftX+width,bottomLeftY+depth],[bottomLeftX+width,bottomLeftY]])
    return tileShape

#-------------------------------------------------------------------------------
# I need a way to test if any points of a shape are outside the other shape.
#-------------------------------------------------------------------------------

def testIfVertexIsWithinShape(shape,vertex):
    shapelyShape = Polygon(shape.getVerticesCoordinates()) #creates an instance of a Shapely Polygon that is identicle to the shape inputted
    shapelyPoint = Point(vertex.getCoordinates()) #creates an instance of a Shapely Point which is identicle to the vertex inputted
    return shapelyShape.intersects(shapelyPoint) #tests and returns if the Point is within or on the boundary of the Polygon
    
def testIfOneShapeIsWithinAnotherShape(oneShape,anotherShape):  
    shapelyPoints = []
    for eachVertex in oneShape.getVertices():
        shapelyPoints.append( Point(eachVertex.getCoordinates()) ) #creates an instance of a Shapely Point which is identicle to the vertices in the shape that needs to within the other one.
    shapelyShape = Polygon(anotherShape.getVerticesCoordinates()) #creates an instance of a Shapely Polygon that is identicle to the shape inputted
    
    allWithin = True
    for eachShapelyPoint in shapelyPoints:
        if not shapelyShape.intersects(eachShapelyPoint): #tests if the Point is within or on the boundary of the Polygon
            allWithin = False
    return allWithin 

#-------------------------------------------------------------------------------
# Main Menu definition
#-------------------------------------------------------------------------------

menuText ="""
Welcome to the car park layout generator program.
1. Make new empty shape
2. Add vertices to shape
3. Print shape vertices
4. Rotate shape about origin
5. Rotate shape about a vertex
6. Translate shape
7. Print longest side number of shape
8. Make longest side sit flat
9. translateShapeToFitNicely
10. getDistanceToNextVertex
11. set current shape as carParkShape
12. Tile and Trim!
20. Exit
"""

def mainMenu(menuText):
    repeatMenu = True
    myShape = shape()
    origin = vertex(0,0)
    while repeatMenu == True:
        print menuText
        menuChoice = askMenuChoice(["1","2","3","4","5","6","7","8","9","10","11","12","20"])
        if menuChoice == "1":
            myShape = shape()

        elif menuChoice == "2":
            try:
                myShape.addVerticesXY(getListOfListOfXY())
            except:
                print "there was an error adding those vertices"

        elif menuChoice == "3":
            print myShape.getVerticesCoordinates()

        elif menuChoice == "4":
            myShape.rotateAboutAVertex(origin,getAngle())

        elif menuChoice == "5":
            myShape.rotateAboutAVertex(myShape.getVertices()[getVertexNumber()],getAngle())

        elif menuChoice == "6":
            myShape.translateXY(getXY())

        elif menuChoice == "7":
            print myShape.getLongestSide()

        elif menuChoice == "8":
            myShape.makeLongestSideFlat()

        elif menuChoice == "9":
            myShape.translateShapeToFitNicely()

        elif menuChoice == "10":
            print myShape.getDistanceToNextVertex(getVertexNumber())

        elif menuChoice == "11":
            carParkShape = myShape

        elif menuChoice == "12":
            placedTiles =  tileAndTrim(carParkShape,tiles,listOFTuplesOfNamesOfTilesInListAndHowManyOfEach)
            print "carParkShape vertices: " + str(carParkShape.getVerticesCoordinates())
            print "car park places:"
            print ""
            for count in range(len(placedTiles)):
                print str(count + 1) + str(placedTiles[count].getVerticesCoordinates())
            
        elif menuChoice == "20":
            return 

        else:
            print "invalid menu choice"


def askMenuChoice(acceptedChoices,stringToAsk = "Please enter your menu choice: ",errorMessage  = "Sorry, that is not an accepted answer, please try again."):
    menuChoice = ""
    while menuChoice not in acceptedChoices or menuChoice == "":
        menuChoice = raw_input(stringToAsk)
        if menuChoice not in acceptedChoices:
            print errorMessage
    return menuChoice

def getXY():
    return [float(raw_input("Enter the value for x: ")),float(raw_input("Enter the value for y: "))]

def getAngle():
    return toRadians(float(raw_input("enter how many degrees to rotate the shape clockwise: ")))

def getVertexNumber():
    return int(raw_input("enter a vertex number (they start at 0): "))

def getListOfListOfXY():
    verticesXY = [[]]
    commaCount = 0
    stringOfVertices = raw_input("enter your coords in the following way 'x1,y1,x2,y2,x3,y3...': ")
    currentItem = ""
    for eachChar in stringOfVertices: #this will add anything but not including the last number to the list
        #print "char: " + eachChar
        if eachChar == ",":
            commaCount += 1
            #print commaCount
            #print (commaCount-1)/2
            #print verticesXY
            #print verticesXY[(commaCount-1)/2]
            verticesXY[(commaCount-1)/2].append(int(currentItem))
            if commaCount%2 == 0:
                verticesXY.append([])
                #print "new XY space added"
            #print verticesXY[(commaCount-1)/2]
            #print ""
            currentItem = ""
        else:
            currentItem = currentItem + eachChar
    verticesXY[(commaCount-1)/2].append(int(currentItem)) #this adds the final number, it was not added before as there is no comma after it
    #print verticesXY
    return verticesXY



#-------------------------------------------------------------------------------
# Testing procedures
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
# code that will be executed
#-------------------------------------------------------------------------------



mainMenu(menuText)

