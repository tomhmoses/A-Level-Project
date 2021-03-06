#===============================================================================
# Main Processing - Version 24
#
# will output area of car park.
#
#===============================================================================


displayJustTiles = False
placementBufferForFirstTiles = 0.001#meters (1mm should fix some problems where the tiles would not be placed)

printProgress = False

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
         'roadWidth':6.0,'perimeterRoadWidth':6.0}




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
         'minibus':tile(sizes['minibusW'],sizes['minibusD']*2+sizes['roadWidth']), 
         'disabled':tile((sizes['standardW']+sizes['gapBetweenDisabledSpaces']),sizes['standardD']*2+sizes['roadWidth']),
         'motorcycle':tile(sizes['motorcycleW'],sizes['standardD']*2+sizes['roadWidth']),
         'standard_single':tile(sizes['standardW'],sizes['standardD']+sizes['roadWidth']), #single tiles do not have the *2 in them for the double space.
         'minibus_single':tile(sizes['minibusW'],sizes['minibusD']+sizes['roadWidth']), 
         'disabled_single':tile((sizes['standardW']+sizes['gapBetweenDisabledSpaces']),sizes['standardD']+sizes['roadWidth']),
         'motorcycle_single':tile(sizes['motorcycleW'],sizes['standardD']+sizes['roadWidth'])}

spaceQueue = [('standard',1)] #it will not matter what the limit of the last item in the list is as this will be what the car park is then filled with.
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

def tileAndTrim(carParkShape,tiles,spaceQueue,pixelsPerMeter):
    messageToPrint = "Your car park shape has an area of: " +str(round(getAreaOfShape(copy.deepcopy(carParkShape),pixelsPerMeter),1))+ " square metres.\n"
    
    if printProgress:
        print "Starting tile and trim"
    fill = False
    carParkFull = False
    #will rotate car park to make longest side sit flat, then will later rotate everything back
    #this should line the spaces up with the longest side.
    angle = carParkShape.getAngleForLongestSide()
    origin = vertex(0,0)
    carParkShape.rotateAboutAVertex(origin,angle)
    if carParkShape.getVertices()[carParkShape.getLongestSide()].getY() == carParkShape.getFurthestDownVertex().getY():
        if printProgress:
            print "successfully rotated first time"
    else:
        if printProgress:
            print "car park rotated another 180 degrees, so that longest side was on bottom."
        carParkShape.rotateAboutAVertex(origin,(math.pi))
        if printProgress:
            print "angle changed"
        angle = angle + math.pi
        if printProgress:
            if carParkShape.getVertices()[carParkShape.getLongestSide()].getY() == carParkShape.getFurthestDownVertex().getY():
                print "longest line is now on bottom"
            else:
                print "longest line still not on bottom apparrently :("
    bottomLeftVertex = vertex(carParkShape.getFurthestLeftVertex().getX(),carParkShape.getFurthestDownVertex().getY()+placementBufferForFirstTiles)
    if printProgress:
        print "bottom left coords"
        print bottomLeftVertex.getCoordinates()
    placedTiles = []
    furthestRightVertex = carParkShape.getFurthestRightVertex()
    if printProgress:
        print "furthest right: " + str(furthestRightVertex.getCoordinates())
    furthestUpVertex = carParkShape.getFurthestUpVertex()
    if printProgress:
        print "furthest up: " + str(furthestUpVertex.getCoordinates())
    currentMaxRowHeight = float(0)
    for count in range(len(spaceQueue)): #will now try placing tiles
        tileLabel = spaceQueue[count][0]
        singleTileLabel = tileLabel + "_single"
        currentTile = tiles[tileLabel]
        if float(currentTile.getDepth()) > float(currentMaxRowHeight):
            currentMaxRowHeight = currentTile.getDepth()
            if printProgress:
                print str(currentMaxRowHeight) + " was bigger than " +str(currentMaxRowHeight)
        howMany = spaceQueue[count][1]
        howManyLeft = howMany
        if count == (len(spaceQueue) -1): #if it is final item i will fill car park with this tile
            fill = True

        while (howManyLeft > 0 or fill == True) and (carParkFull == False): #places number of current type of tile
            #print "-------"
            #print bottomLeftVertex.getCoordinates()
            #we will start testing at 0,0 then move right, then move onto a new row up when the current layer has been filled.
            #print "stub for placing the tile as a shape and testing if all of its vertices are within the car park shape"
            #makeShapeFromTile
            tileShape = makeShapeFromTile(bottomLeftVertex,tileLabel,tiles)
            validTilePlacement = testIfOneShapeIsWithinAnotherShape(tileShape,carParkShape)
            #print "stub for if tile was placed and is in boundary, add this shape to a list of car parking tiles created. Then reduce howManyLeft by 1."
            if validTilePlacement:
                if printProgress:
                    print "valid " + tileLabel + " tile placement."
                howManyLeft = howManyLeft - 2 #it places a full tile so I remove two spaces from the queue
                placedTiles.append(tileShape)
            else:
                if printProgress:
                    print "failed to place double space tile, trying to place single tile..."
                #will now try and place a single space tile
                tileShape = makeShapeFromTile(bottomLeftVertex,singleTileLabel,tiles)
                validTilePlacement = testIfOneShapeIsWithinAnotherShape(tileShape,carParkShape)
                if validTilePlacement:
                    if printProgress:
                        print "valid " + singleTileLabel + " tile placement."
                    howManyLeft = howManyLeft - 1 #it places a single tile so I remove just one spaces from the queue
                    placedTiles.append(tileShape)
                
            bottomLeftVertex.translateXY([ tiles[tileLabel].getWidth() , 0 ]) #moved bottom left vertex to the right
            #will see if bottom left vertex needs resetting
            #print "stub for testing if placing x is out of range, will then move y up the right height and reset x"
            if bottomLeftVertex.getX() > furthestRightVertex.getX():
                if printProgress:
                    print "out of range, moving onto next row"
                bottomLeftVertex.setX(carParkShape.getFurthestLeftVertex().getX())
                #print bottomLeftVertex.getCoordinates()
                bottomLeftVertex.translateXY([ 0 , tiles[tileLabel].getDepth() ]) #moved bottom left vertex up
                #print "stub for testing if placing y is out of range, if y was just change, if it is filledCarPark will be set to True"
                if (howManyLeft > 0 or fill == True):
                    currentMaxRowHeight = tiles[tileLabel].getDepth()
                else:
                    currentMaxRowHeight = 0
                if bottomLeftVertex.getY() > furthestUpVertex.getY():
                    #print "Tried placing tiles in all spaces = true"
                    carParkFull = True

                #print "in range: " + str(furthestRightVertex.getX())
        if howManyLeft < 1:
            #was sucessful
            #print "got to here"
            messageToPrint = messageToPrint + "Placed all " + str(howMany) + " of " + str(tileLabel) + " spaces sucessfully\n"
            if carParkFull:
                messageToPrint = messageToPrint + "Car park was filled. I filled it up with " + str(-howManyLeft) + " extra " + str(tileLabel) + " spaces."
        else:
            messageToPrint = messageToPrint + "Placed only " + str(howMany-howManyLeft) + " of " + str(howMany) + " " +  str(tileLabel) + " spaces sucessfully\n"
            messageToPrint = messageToPrint + "Car park was full and ran out of space to place the rest of what you wanted you wanted"

    for eachTile in placedTiles: #finishes by rotating all tiles back so that they will display back in the original shape.
        eachTile.rotateAboutAVertex(origin,-angle)

    return placedTiles,messageToPrint

 
#-------------------------------------------------------------------------------
# Making a shape from a tile and a position to place the
#-------------------------------------------------------------------------------

def makeShapeFromTile(bottomLeftVertex,tileLabel,tiles):
    tileShape = shape(tileLabel)
    bottomLeftCoords = bottomLeftVertex.getCoordinates()
    bottomLeftX = bottomLeftCoords[0]
    bottomLeftY = bottomLeftCoords[1]
    width = tiles[tileLabel].getWidth()
    depth = tiles[tileLabel].getDepth()
    #works clockwise starting at bottom left vertex
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
# code to convert pixel values to meters and back again
#-------------------------------------------------------------------------------

def convertShapePixelToMeter(carParkShape,pixelsPerMeter):
    carParkShape.stretchShape(float(1/float(pixelsPerMeter)))

def convertShapeMeterToPixel(carParkShape,pixelsPerMeter):
    carParkShape.stretchShape(float(pixelsPerMeter))

def getAreaOfShape(myShape,pixelsPerMeter):
    convertShapePixelToMeter(myShape,pixelsPerMeter)
    shapelyShape = Polygon(myShape.getVerticesCoordinates()) #creates an instance of a Shapely Polygon that is identicle to the shape inputted
    return shapelyShape.area

#-------------------------------------------------------------------------------
# get tuples of coordinates of edged of a shape ready for printing
#-------------------------------------------------------------------------------

def getEdgesOfShape(shape):
    listOfGroupsOfCoordinatesForLines = [] #eg: [[x1,y1,x2,y2],[x3,y3,x4,y4]...]
    listOfCoordinates = shape.getVerticesCoordinates()
    for count in range(len(listOfCoordinates)):#  each in carParkShape.getVerticesCoordinates():
        listOfGroupsOfCoordinatesForLines.append([listOfCoordinates[count][0],listOfCoordinates[count][1],listOfCoordinates[(count+1)%len(listOfCoordinates)][0],listOfCoordinates[(count+1)%len(listOfCoordinates)][1]])
    return listOfGroupsOfCoordinatesForLines


#for next subroutine
fractionOfLongestLengthWhichIsNotRoad = {'standard':float((sizes['standardD'])/(tiles['standard'].getDepth())), #gets the fraction of the side of the tile to be drawn as the car park space
                                        'minibus':float((sizes['minibusD'])/(tiles['minibus'].getDepth())),      #depth of space divided by depth of tile
                                        'disabled':float((sizes['standardD'])/(tiles['disabled'].getDepth())),
                                        'motorcycle':float((sizes['motorcycleD'])/(tiles['motorcycle'].getDepth())),
                                        'standard_single':float((sizes['standardD'])/(tiles['standard_single'].getDepth())),
                                        'minibus_single':float((sizes['minibusD'])/(tiles['minibus_single'].getDepth())),
                                        'disabled_single':float((sizes['standardD'])/(tiles['minibus'].getDepth())),
                                        'motorcycle_single':float((sizes['motorcycleD'])/(tiles['disabled_single'].getDepth()))}

def getLinesToDrawFromTiles(tileInstance):
    listOfGroupsOfCoordinatesForLines = []
    if tileInstance.getLabel() in ['standard','minibus','disabled','motorcycle','standard_single','minibus_single','disabled_single','motorcycle_single'] and displayJustTiles == False:
        #print "standard tile... making space lines"
        #will draw boxes where the car park should be"
        
        #fractionOfLongestLengthWhichIsNotRoad = float((sizes['standardD'])/(sizes['standardD']*2+sizes['roadWidth']))
        #first will draw the short lengths (the ends)
        tempList = copy.deepcopy(tileInstance.getVerticesCoordinates()[0])
        tempList.extend(tileInstance.getVerticesCoordinates()[3])
        listOfGroupsOfCoordinatesForLines.append(copy.deepcopy(tempList))
        tempList = copy.deepcopy(tileInstance.getVerticesCoordinates()[1])
        tempList.extend(tileInstance.getVerticesCoordinates()[2])
        listOfGroupsOfCoordinatesForLines.append(copy.deepcopy(tempList))
        #will now get the 4 points at the edge of the roads, from bottom left and working clockwise
        #will need to move the fraction of each side which is not a road along each of the longest edges in both directions
        #makes referancing these numbers shorter and easier to read next
        a  = fractionOfLongestLengthWhichIsNotRoad[tileInstance.getLabel()]
        v0 = tileInstance.getVerticesCoordinates()[0] #vertex coords 0,1,2,3 from tile corners
        v1 = tileInstance.getVerticesCoordinates()[1]
        v2 = tileInstance.getVerticesCoordinates()[2]
        v3 = tileInstance.getVerticesCoordinates()[3]
        #x coords
        x0 = v0[0] 
        x1 = v1[0]
        x2 = v2[0]
        x3 = v3[0]
        #y coords
        y0 = v0[1] 
        y1 = v1[1]
        y2 = v2[1]
        y3 = v3[1]
        #gets middle points of parking place for drawing
        #new coordinate points that lines need drawing to from corners
        p0 = [(x1-x0)*a+x0,(y1-y0)*a+y0] 
        p1 = [(x0-x1)*a+x1,(y0-y1)*a+y1]
        p2 = [(x3-x2)*a+x2,(y3-y2)*a+y2]
        p3 = [(x2-x3)*a+x3,(y2-y3)*a+y3]
        #makes the groups of coords ready for drawing the lines
        line0 = v0
        line0.extend(p0)
        line1 = v1
        line1.extend(p1)
        line2 = v2
        line2.extend(p2)
        line3 = v3
        line3.extend(p3)
        #appends a copy of the list (what the '[:]' is for)
        if "_single" not in tileInstance.getLabel(): #if it is a full tile add all 4 lines for the 2 parking spaces (one at each side of each space)
            listOfGroupsOfCoordinatesForLines.append(line0[:])
            listOfGroupsOfCoordinatesForLines.append(line1[:])
            listOfGroupsOfCoordinatesForLines.append(line2[:])
            listOfGroupsOfCoordinatesForLines.append(line3[:])
        else: #if it is a single tile only add two lines
            listOfGroupsOfCoordinatesForLines.append(line0[:])
            listOfGroupsOfCoordinatesForLines.append(line3[:])
    else:
        print "tile type not supported yet, using standard edge of tile instead"
        listOfGroupsOfCoordinatesForLines = getEdgesOfShape(tileInstance)
    return listOfGroupsOfCoordinatesForLines



#-------------------------------------------------------------------------------
# get inside border shape
#-------------------------------------------------------------------------------

def getInsideBorderFromShape(carParkShape,width):
    oldShape = carParkShape
    newShape = shape()
    verticesCoordinates = oldShape.getVerticesCoordinates()
    vertices = oldShape.getVertices()
    noOfCoordinates = len(verticesCoordinates)
    for count in range(noOfCoordinates):
        #get angle of the three vertices
        angle = getAngleBetweenThreeVertices(vertices[(count-1)%noOfCoordinates],vertices[(count)%noOfCoordinates],vertices[(count+1)%noOfCoordinates])
        halfAngle = angle/2
        angleFromHorizontal = halfAngle + oldShape.getAngleOflineAfterVertexFromHorizontal(count)
        lengthBetweenNewAndOldVertex = width/(math.sin(halfAngle))
        extraX = (math.cos(angleFromHorizontal)*lengthBetweenNewAndOldVertex)
        extraY = (math.sin(angleFromHorizontal)*lengthBetweenNewAndOldVertex)
        newX = vertices[count].getX() + extraX
        newY = vertices[count].getY() + extraY
        newShape.addVerticesXY([[newX,newY]])
    return newShape
        
def getDistanceBetweenTwoVertices(vertex2,vertex1):
    #vertex1 = self.vertices[vertexNumber]
    #vertex2 = self.vertices[(vertexNumber+1)%(len(self.vertices))]
    differenceInX = vertex1.getX() - vertex2.getX()
    differenceInY = vertex1.getY() - vertex2.getY()
    distance = math.sqrt( differenceInX**2 + differenceInY**2 )
    return distance

def getAngleBetweenThreeVertices(vertexC,vertexA,vertexB): #will return angle at vertexA using cosine rule
    a = getDistanceBetweenTwoVertices(vertexB,vertexC)
    b = getDistanceBetweenTwoVertices(vertexA,vertexC)
    c = getDistanceBetweenTwoVertices(vertexA,vertexB)
    #print a,b,c
    angle = math.acos(((b*b+c*c-a*a)/(2*b*c)))
    return angle


#-------------------------------------------------------------------------------
# code that will be run by the GUI
#-------------------------------------------------------------------------------

def GetCarParkPixelLinesToDrawFromPixelShape(carParkShape,pixelsPerMeter,addPerimeterRoad):
    listOfGroupsOfCoordinatesForLines = [] #eg: [[x1,y1,x2,y2],[x3,y3,x4,y4]...]
    originalShape = copy.deepcopy(carParkShape)
    if addPerimeterRoad == True:
        newShape = getInsideBorderFromShape(originalShape,sizes['perimeterRoadWidth'])
        origInsideShape = copy.deepcopy(newShape)
    else:
        newShape = copy.deepcopy(originalShape)
    #print shape.getVerticesCoordinates()
    #print pixelsPerMeter
    convertShapePixelToMeter(newShape,pixelsPerMeter)
    #print shape.getVerticesCoordinates()
    parkingTilesMade,messageToPrint = tileAndTrim(newShape,tiles,spaceQueue,pixelsPerMeter) #a list of tile shapes generated, currently in meters
    #print parkingTilesMade
    for eachCarParkTile in parkingTilesMade: #adds edges of each tile to lines to be drawn
        convertShapeMeterToPixel(eachCarParkTile,pixelsPerMeter) #converts the meters unit back to pixels unit.
        edgesList = getLinesToDrawFromTiles(eachCarParkTile) #gets lines of edges of each tile
        #print""
        #print "edges being appended: should be in form [[x1,y1],[x2,y2]]"
        #print edgesList
        #print "edges"
        #print edgesList
        listOfGroupsOfCoordinatesForLines.extend(edgesList) #concatinates the two lists
        #print "all"
        #print listOfGroupsOfCoordinatesForLines
    listOfGroupsOfCoordinatesForLines = listOfGroupsOfCoordinatesForLines + getEdgesOfShape(originalShape) #adds edge of car park shape to be printed
    if addPerimeterRoad == True:
        listOfGroupsOfCoordinatesForLines = listOfGroupsOfCoordinatesForLines + getEdgesOfShape(origInsideShape)
    #print listOfGroupsOfCoordinatesForLines
    return listOfGroupsOfCoordinatesForLines,messageToPrint


