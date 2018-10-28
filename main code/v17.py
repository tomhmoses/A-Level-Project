#===============================================================================
# Main Processing - Version 17
#
# Adding final support for GUI
# including translating pixels to meters and back
#
#===============================================================================



#-------------------------------------------------------------------------------
# Importing required modules
#     PIL: For opening and editing image (will use this in a later version)
# Tkinter: Provides UI framework (will use this in a later version)
#    Math: Allows me to easily use trigonometry to rotate the vertices
# Shapely: Allows me to easily have a way to test if a point is outside a shape
#    copy: Allows me to duplicate a class instance easily rather than creating another referance to the same instance
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk, ImageDraw
from Tkinter import *
import math
from shapely.geometry import Point, Polygon #this imports the required classes from shapely
import copy

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

tileNames = ['standard','minibus','disabled','motorcycle']

tiles = {'standard':tile(sizes['standardW'],sizes['standardD']*2+sizes['roadWidth']), #standard tile should be fine for making the tile and trim and testing at first
         'minibus':tile(sizes['minibusW'],sizes['minibusD']*2+sizes['roadWidth']), #need to fix these tiles
         'disabled':tile((sizes['standardW']+sizes['gapBetweenDisabledSpaces']),sizes['standardD']*2+sizes['roadWidth']),
         'motorcycle':tile(sizes['motorcycleW'],sizes['standardD']*2+sizes['roadWidth'])}
         
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
    bottomLeftVertex = vertex(carParkShape.getFurthestLeftVertex().getX(),carParkShape.getFurthestDownVertex().getY())
    print bottomLeftVertex.getCoordinates()
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
                bottomLeftVertex.setX(carParkShape.getFurthestLeftVertex().getX())
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
# Main Menu definition - removed
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Testing procedures - removed
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
# code that will be executed - removed
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# code to convert pixel values to meters and back again
#-------------------------------------------------------------------------------

def convertShapePixelToMeter(shape,pixelsPerMeter):
    shape.stretchShape(float(1/float(pixelsPerMeter)))

def convertShapeMeterToPixel(shape,pixelsPerMeter):
    shape.stretchShape(float(pixelsPerMeter))

    
#-------------------------------------------------------------------------------
# get tuples of coordinates of edged of a shape ready for printing
#-------------------------------------------------------------------------------

def getEdgesOfShapes(shape):
    listOfGroupsOfCoordinatesForLines = [] #eg: [[x1,y1,x2,y2],[x3,y3,x4,y4]...]
    listOfCoordinates = shape.getVerticesCoordinates()
    for count in range(len(listOfCoordinates)):#  each in carParkShape.getVerticesCoordinates():
        listOfGroupsOfCoordinatesForLines.append([listOfCoordinates[count][0],listOfCoordinates[count][1],listOfCoordinates[(count+1)%len(listOfCoordinates)][0],listOfCoordinates[(count+1)%len(listOfCoordinates)][1]])
    return listOfGroupsOfCoordinatesForLines

#-------------------------------------------------------------------------------
# code that will be run by the GUI
#-------------------------------------------------------------------------------

def GetCarParkPixelLinesToDrawFromPixelShape(shape,pixelsPerMeter):
    listOfGroupsOfCoordinatesForLines = [] #eg: [[x1,y1,x2,y2],[x3,y3,x4,y4]...]
    originalShape = copy.deepcopy(shape)
    print shape.getVerticesCoordinates()
    print pixelsPerMeter
    convertShapePixelToMeter(shape,pixelsPerMeter)
    print shape.getVerticesCoordinates()
    parkingTilesMade = tileAndTrim(shape,tiles,listOFTuplesOfNamesOfTilesInListAndHowManyOfEach) #a list of tile shapes generated, currently in meters
    #print parkingTilesMade
    for eachCarParkTile in parkingTilesMade: #adds edges of each tile to lines to be drawn
        convertShapeMeterToPixel(eachCarParkTile,pixelsPerMeter) #converts the meters unit back to pixels unit.
        edgesList = getEdgesOfShapes(eachCarParkTile) #gets lines of edges of each tile
        #print "edges"
        #print edgesList
        listOfGroupsOfCoordinatesForLines.extend(edgesList) #concatinates the two lists
        #print "all"
        #print listOfGroupsOfCoordinatesForLines
    listOfGroupsOfCoordinatesForLines = listOfGroupsOfCoordinatesForLines + getEdgesOfShapes(originalShape) #adds edge of car park shape to be printed
    #print listOfGroupsOfCoordinatesForLines
    return listOfGroupsOfCoordinatesForLines
    

