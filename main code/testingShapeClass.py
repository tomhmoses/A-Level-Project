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

        

#-------------------------------------------------------------------------------
# Defining a shape class.
# This is just a collection of vertices in a specific order.
#-------------------------------------------------------------------------------

class shape():
    def __init__(self):
        self.vertices = []

    def addVertex(self,vertex):
        self.vertices.append(vertex)

    def addVerticesXY(self,verticesXY): #vertices should be as lists within lists
        for each in verticesXY:
            temp = vertex()
            temp.setXY(each)
            self.addVertex(temp)

    def getVertices(self):
        return self.vertices

    def getVerticesCoordinates(self):
        listOfCoordinates = []
        for eachVertex in self.vertices:
            listOfCoordinates.append(eachVertex.getCoordinates())
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
            eachVertex.rotateAboutAnotherVertex(about,angle)

    def translateXY(self,translationXY):
        for eachVertex in self.vertices:
            eachVertex.translateXY(translationXY)

    def makeLongestSideFlat(self):
        self.makeSideAfterVertexFlat(self.vertices[self.getLongestSide()])

    def makeSideAfterVertexFlat(self,vertex1):
        for count in range(len(self.vertices)):
            if self.vertices[count] == vertex1:
                vertex2 = self.vertices[(count+1)%(len(self.vertices))]
        differenceInX = float(float(vertex1.getX()) - float(vertex2.getX())) # I needed to add in these float bit so that the devision later is not floor devision.
        differenceInY = float(float(vertex1.getY()) - float(vertex2.getY()))
        print "X:",differenceInX
        print "Y:",differenceInY
        if differenceInX in [float(0),float(-0)]:
            angle = math.pi/2 #90 degrees
        else:
            angle = (math.atan((differenceInY)/(differenceInX)))    #this finds the angle from horizonal of the line connecting the first vertex to the next
                                                                    #when we have this anlgle, we can turn the entire shape by the same angle rotating about
        print "angle:",angle
        self.rotateAboutAVertex(vertex1,angle) #the first vertex in order to make this side lay flat.

    def translateShapeToFitNicely(self): #this will get the longest side along the x axis after it has been rotated and the furthest left vertex to be on the y axis.
        longestVertexNumber = self.getLongestSide()
        furthestLeftVertex = self.getFurthestLeftVertex()
        tranlationXY = [(-(furthestLeftVertex.getX())),(-(self.vertices[longestVertexNumber].getY()))]
        self.translateXY(tranlationXY)

    def getFurthestLeftVertex(self):
        furthestLeftVertex = self.vertices[0]
        for each in self.vertices:
            if each.getX < furthestLeftVertex.getX:
                furthestLeftVertex = each
        #print furthestLeftVertex.getCoordinates()
        return furthestLeftVertex


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
11. exit
"""

def mainMenu(menuText):
    repeatMenu = True
    myShape = shape()
    origin = vertex(0,0)
    while repeatMenu == True:
        print menuText
        menuChoice = askMenuChoice(["1","2","3","4","5","6","7","8","9","10","11"])
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

def toRadians(degrees):
    return degrees*((2*math.pi)/360)

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
