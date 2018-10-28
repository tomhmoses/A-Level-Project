#===============================================================================
# Main Processing - Version 26
#
# final commented version
# I also removed any unnessesary code.
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
         'roadWidth':6.0,'perimeterRoadWidth':6.0}


#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

#meters (1mm should fix some problems where the tiles would not be placed)
placementBufferForFirstTiles = 0.001





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

#it will not matter what the limit of the last item in the list is as this will be what the car park is then filled with.
spaceQueue = [('standard',1)] 


#-------------------------------------------------------------------------------
# tile and trim
#-------------------------------------------------------------------------------

def tileAndTrim(carParkShape,tiles,spaceQueue):
    messageToPrint = ""
    #Fill will be set to true when all the spaces from the space queue have been placed, then the car park will be filled with the last item from the queue
    fill = False
    carParkFull = False
    #will rotate car park to make longest side sit flat, then will later rotate everything back
    #this should line the spaces up with the longest side.
    angle = carParkShape.getAngleForLongestSide()
    origin = vertex(0,0)
    carParkShape.rotateAboutAVertex(origin,angle)
    #after rotating the shape to have the longest line sit horizontal, I check if it is at the bottom of the car park, if it isnt I will rotate the car park a further 180 degrees.
    if not carParkShape.getVertices()[carParkShape.getLongestSide()].getY() == carParkShape.getFurthestDownVertex().getY():
        carParkShape.rotateAboutAVertex(origin,(math.pi))
        angle = angle + math.pi
    #the bottom left vertex is a vertex that moves through the car park and the tiles are placed from this point.
    bottomLeftVertex = vertex(carParkShape.getFurthestLeftVertex().getX(),carParkShape.getFurthestDownVertex().getY()+placementBufferForFirstTiles)
    #I initialise the list that placed valid tiles will be added to.
    placedTiles = []
    furthestRightVertex = carParkShape.getFurthestRightVertex()
    furthestUpVertex = carParkShape.getFurthestUpVertex()
    currentMaxRowHeight = float(0)
    #will now try placing tiles by iterating through the queue of spaces to be added.
    for count in range(len(spaceQueue)): 
        tileLabel = spaceQueue[count][0]
        singleTileLabel = tileLabel + "_single"
        currentTile = tiles[tileLabel]
        if float(currentTile.getDepth()) > float(currentMaxRowHeight):
            #updates the hight to move the row for the next row.
            currentMaxRowHeight = currentTile.getDepth()
        howMany = spaceQueue[count][1]
        howManyLeft = howMany
        if count == (len(spaceQueue) -1):
            #if it is final item i will fill car park with this tile
            fill = True

        while (howManyLeft > 0 or fill == True) and (carParkFull == False): #places number of current type of tile
            #we will start testing at 0,0 then move right, then move onto a new row up when the current layer has been filled.
            #makeShapeFromTile
            tileShape = makeShapeFromTile(bottomLeftVertex,tileLabel,tiles)
            #then tests if it is a valid tile placement
            validTilePlacement = testIfOneShapeIsWithinAnotherShape(tileShape,carParkShape)
            if validTilePlacement:
                #it places a full tile so I remove two spaces from the queue
                howManyLeft = howManyLeft - 2 
                placedTiles.append(tileShape)
            else:
                #will now try and place a single space tile
                tileShape = makeShapeFromTile(bottomLeftVertex,singleTileLabel,tiles)
                validTilePlacement = testIfOneShapeIsWithinAnotherShape(tileShape,carParkShape)
                if validTilePlacement:
                    #it places a single tile so I remove just one spaces from the queue
                    howManyLeft = howManyLeft - 1 
                    placedTiles.append(tileShape)
            #moved bottom left vertex to the right after placing the tile.   
            bottomLeftVertex.translateXY([ tiles[tileLabel].getWidth() , 0 ]) 
            #will see if bottom left vertex needs resetting
            if bottomLeftVertex.getX() > furthestRightVertex.getX():
                bottomLeftVertex.setX(carParkShape.getFurthestLeftVertex().getX())
                bottomLeftVertex.translateXY([ 0 , currentMaxRowHeight ]) #moved bottom left vertex up and moves it up the amount of the highest tile for the current row.
                if (howManyLeft > 0 or fill == True):
                    currentMaxRowHeight = tiles[tileLabel].getDepth()
                else:
                    currentMaxRowHeight = 0
                if bottomLeftVertex.getY() > furthestUpVertex.getY():
                    #If the bottom left vertex started in the bottom left of the program and then finished over the top right then it has tried to place a car parking place everywhere it can, so we can assume the car park is full.
                    carParkFull = True

                
        if howManyLeft < 1:
            #if it sucessfully placed all of this type of tile then it will add this to the message to print.
            messageToPrint = messageToPrint + "Placed all " + str(howMany) + " of " + str(tileLabel) + " spaces sucessfully\n"
            if carParkFull:
                #If the car park is also full, then it will say how many extra spaces it added.
                messageToPrint = messageToPrint + "Car park was filled. I filled it up with " + str(-howManyLeft) + " extra " + str(tileLabel) + " spaces."
        else:
            #If there was still items left to be added then it exited the previous lop because the car park was full, so we can explain to the user how many of the space we were able to add, but that we then ran out of room to place the rest of their spaces.
            messageToPrint = messageToPrint + "Placed only " + str(howMany-howManyLeft) + " of " + str(howMany) + " " +  str(tileLabel) + " spaces sucessfully\n"
            messageToPrint = messageToPrint + "Car park was full and ran out of space to place the rest of what you wanted you wanted"

    #finishes by rotating all tiles back so that they will display back in the original shape.
    for eachTile in placedTiles: 
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
    #creates an instance of a Shapely Polygon that is identicle to the shape inputted
    shapelyShape = Polygon(shape.getVerticesCoordinates())
    #creates an instance of a Shapely Point which is identicle to the vertex inputted
    shapelyPoint = Point(vertex.getCoordinates())
    #tests and returns if the Point is within or on the boundary of the Polygon
    return shapelyShape.intersects(shapelyPoint) 

def testIfOneShapeIsWithinAnotherShape(oneShape,anotherShape):
    #This will be useful for testing if the places tile is within the carpark shape.
    shapelyPoints = []
    for eachVertex in oneShape.getVertices():
        shapelyPoints.append( Point(eachVertex.getCoordinates()) ) #creates an instance of a Shapely Point which is identicle to the vertices in the shape that needs to within the other one.
    shapelyShape = Polygon(anotherShape.getVerticesCoordinates()) #creates an instance of a Shapely Polygon that is identicle to the shape inputted
    #for each vertex it will test if it is within the other shape.
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

def getAreaOfShape(myShape):
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


#for next subroutine, it gets the fractions of sides of a tile to be drawn for one car parking place.
fractionOfLongestLengthWhichIsNotRoad = {'standard':float((sizes['standardD'])/(tiles['standard'].getDepth())), #gets the fraction of the side of the tile to be drawn as the car park space
                                        'minibus':float((sizes['minibusD'])/(tiles['minibus'].getDepth())),      #depth of space divided by depth of tile
                                        'disabled':float((sizes['standardD'])/(tiles['disabled'].getDepth())),
                                        'motorcycle':float((sizes['motorcycleD'])/(tiles['motorcycle'].getDepth())),
                                        'standard_single':float((sizes['standardD'])/(tiles['standard_single'].getDepth())),
                                        'minibus_single':float((sizes['minibusD'])/(tiles['minibus_single'].getDepth())),
                                        'disabled_single':float((sizes['standardD'])/(tiles['disabled_single'].getDepth())),
                                        'motorcycle_single':float((sizes['motorcycleD'])/(tiles['motorcycle_single'].getDepth()))}

def getLinesToDrawFromTiles(tileInstance):
    listOfGroupsOfCoordinatesForLines = []
    if tileInstance.getLabel() in ['standard','minibus','disabled','motorcycle','standard_single','minibus_single','disabled_single','motorcycle_single']:
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
    #makes a new empty shape that will become the inner shape.
    newShape = shape()
    verticesCoordinates = oldShape.getVerticesCoordinates()
    vertices = oldShape.getVertices()
    noOfCoordinates = len(verticesCoordinates)
    #for each vertex of the old shape, it will find the new vertex
    for count in range(noOfCoordinates):
        #get angle of the three vertices
        angle = getAngleBetweenThreeVertices(vertices[(count-1)%noOfCoordinates],vertices[(count)%noOfCoordinates],vertices[(count+1)%noOfCoordinates])
        #halfs the angle
        halfAngle = angle/2
        #gets the angle to be moved away from the original point from the horizontal
        angleFromHorizontal = halfAngle + oldShape.getAngleOflineAfterVertexFromHorizontal(count)
        #gets the length to be moved away from the original point along the angle using trigonometry
        lengthBetweenNewAndOldVertex = width/(math.sin(halfAngle))
        #gets the x and y to be added in both directions using trigonometry
        extraX = (math.cos(angleFromHorizontal)*lengthBetweenNewAndOldVertex)
        extraY = (math.sin(angleFromHorizontal)*lengthBetweenNewAndOldVertex)
        newX = vertices[count].getX() + extraX
        newY = vertices[count].getY() + extraY
        #adds the new vertex to the inner border shape.
        newShape.addVerticesXY([[newX,newY]])
    return newShape
        
def getDistanceBetweenTwoVertices(vertex2,vertex1):
    #uses The Pythagorean Theorem to find the distance between two vertices.
    differenceInX = vertex1.getX() - vertex2.getX()
    differenceInY = vertex1.getY() - vertex2.getY()
    distance = math.sqrt( differenceInX**2 + differenceInY**2 )
    return distance

def getAngleBetweenThreeVertices(vertexC,vertexA,vertexB):
    #will return angle at vertexA of a triangle made up of the three vertices, using the cosine rule 
    a = getDistanceBetweenTwoVertices(vertexB,vertexC)
    b = getDistanceBetweenTwoVertices(vertexA,vertexC)
    c = getDistanceBetweenTwoVertices(vertexA,vertexB)
    angle = math.acos(((b*b+c*c-a*a)/(2*b*c)))
    return angle


#-------------------------------------------------------------------------------
# code that will be run by the GUI
#-------------------------------------------------------------------------------

def GetCarParkPixelLinesToDrawFromPixelShape(carParkShape,pixelsPerMeter,addPerimeterRoad):
    listOfGroupsOfCoordinatesForLines = [] #eg: [[x1,y1,x2,y2],[x3,y3,x4,y4]...]
    #makes a copy of the shape for later use when getting the original perimeter of the shape to be drawn
    originalShape = copy.deepcopy(carParkShape)
    if addPerimeterRoad == True:
        #makes a copy of the shape for later use when getting the original perimeter of the shape to be drawn
        #If the shape needs a perimeter road then  the new shape will be generated
        newShape = getInsideBorderFromShape(originalShape,sizes['perimeterRoadWidth'])
        #makes a copy of the shape for later use when getting the original perimeter of the inner shape to be drawn
        origInsideShape = copy.deepcopy(newShape)
    else:
        #otherwise the new shape is just set to a copy of the original shape.
        newShape = copy.deepcopy(originalShape)
    convertShapePixelToMeter(newShape,pixelsPerMeter)
    #I then work out the area of the car park
    shapeForWorkingOutArea = copy.deepcopy(carParkShape)
    convertShapePixelToMeter(shapeForWorkingOutArea,pixelsPerMeter)
    #I add the area of the car park to the message to be printed.
    messageToPrint = "Your car park shape has an area of: " +str(round(getAreaOfShape(shapeForWorkingOutArea),1))+ " square metres.\n"
    parkingTilesMade,extraMessageToPrint = tileAndTrim(newShape,tiles,spaceQueue) #a list of tile shapes generated, currently in meters
    messageToPrint = messageToPrint + extraMessageToPrint
    #I now get the lines to be drawn for each car parking space placed.
    for eachCarParkTile in parkingTilesMade: #adds edges of each tile to lines to be drawn
        convertShapeMeterToPixel(eachCarParkTile,pixelsPerMeter) #converts the meters unit back to pixels unit.
        edgesList = getLinesToDrawFromTiles(eachCarParkTile) #gets lines of edges of each tile
        listOfGroupsOfCoordinatesForLines.extend(edgesList) #concatinates the two lists
    listOfGroupsOfCoordinatesForLines = listOfGroupsOfCoordinatesForLines + getEdgesOfShape(originalShape) #adds edge of car park shape to be printed
    if addPerimeterRoad == True:
        #adds edges of inner shape (so you can see the perimeter road), if a perimeter road was made.
        listOfGroupsOfCoordinatesForLines = listOfGroupsOfCoordinatesForLines + getEdgesOfShape(origInsideShape)
    return listOfGroupsOfCoordinatesForLines,messageToPrint


