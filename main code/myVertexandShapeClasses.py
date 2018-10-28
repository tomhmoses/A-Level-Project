import math

#-------------------------------------------------------------------------------
# Defining a vertex class. This is just a point. (Plural = vertices)
#-------------------------------------------------------------------------------
class vertex():
    def __init__(self,x = None, y = None):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getCoordinates(self):
        return [self.x,self.y]

    def setX(self,x):
        self.x = float(x)

    def setY(self,Y):
        self.y = float(y)

    def setXY(self,both): #both with become the standard name for a tuple of an X and Y coordinate
        self.x = both[0]
        self.y = both[1]

    def rotateAboutAnotherVertex(self,about,angle): #the position it rotates clockwise about will be passed in as a vertex class.
                                                    #the angle will be given in radians
        #print "angle", angle
        angle = -angle #I realised the matrix i used was to rotate anticlockwise, so this fixes that problem.
        newX = (self.x-about.x)*(math.cos(angle)) - (self.y-about.y)*(math.sin(angle)) + about.x
        newY = (self.y-about.y)*(math.cos(angle)) + (self.x-about.x)*(math.sin(angle)) + about.y
        self.setXY([newX,newY])

    def translateXY(self,translationXY): #translation should be passed in the form [X,Y]
        self.x = (self.x + translationXY[0])
        self.y = (self.y + translationXY[1])

    def stretchVertex(self,scale): #will stretch the position of the vertex about the origin
        self.x = (self.x * scale)
        self.y = (self.y * scale)
        


def toRadians(degrees):
    return degrees*((2*math.pi)/360)


#-------------------------------------------------------------------------------
# Defining a shape class.
# This is just a collection of vertices in a specific order.
#-------------------------------------------------------------------------------

class shape():
    def __init__(self,label = ""):
        self.vertices = []
        self.label = label

    def getLabel(self):
        return self.label

    def addVertex(self,vertex):
        self.vertices.append(vertex)

    def addVerticesXY(self,verticesXY): #vertices should be as lists within lists
        for each in verticesXY:
            temp = vertex()
            temp.setXY(each)
            self.addVertex(temp)

    def removeLastVertex(self):
        self.vertices = self.vertices[:-1] #removes last item from list

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
        #print "X:",differenceInX
        #print "Y:",differenceInY
        if differenceInX in [float(0),float(-0)]:
            angle = math.pi/2 #90 degrees
        else:
            angle = (math.atan((differenceInY)/(differenceInX)))    #this finds the angle from horizonal of the line connecting the first vertex to the next
                                                                    #when we have this anlgle, we can turn the entire shape by the same angle rotating about
        print "angle:",angle
        self.rotateAboutAVertex(vertex1,angle)                  #the first vertex in order to make this side lay flat.

    def getAngleForLongestSide(self):
        vertex1 = self.vertices[self.getLongestSide()]
        for count in range(len(self.vertices)):
            if self.vertices[count] == vertex1:
                vertex2 = self.vertices[(count+1)%(len(self.vertices))]
        differenceInX = float(float(vertex1.getX()) - float(vertex2.getX())) # I needed to add in these float bit so that the devision later is not floor devision.
        differenceInY = float(float(vertex1.getY()) - float(vertex2.getY()))
        #print "X:",differenceInX
        #print "Y:",differenceInY
        if differenceInX in [float(0),float(-0)]:
            angle = math.pi/2 #90 degrees if the difference in either x is 0
        else:
            angle = (math.atan((differenceInY)/(differenceInX)))    #this finds the angle from horizonal of the line connecting the first vertex to the next
                                                                    #when we have this anlgle, we can turn the entire shape by the same angle rotating about
                                                                    #the first vertex in order to make this side lay flat.
        return angle

    def getAngleOflineAfterVertexFromHorizontal(self,vertexNumber):
        vertex1 = self.vertices[vertexNumber]
        vertex2 = self.vertices[(vertexNumber+1)%(len(self.vertices))]
        differenceInX = float(float(vertex1.getX()) - float(vertex2.getX())) # I needed to add in these float bit so that the devision later is not floor devision.
        differenceInY = float(float(vertex1.getY()) - float(vertex2.getY()))
        #print "X:",differenceInX
        #print "Y:",differenceInY
        if differenceInX in [float(0),float(-0)]:
            angle = math.pi/2 #90 degrees if the difference in either x is 0
        else:
            angle = (math.atan((differenceInY)/(differenceInX)))    #this finds the angle from horizonal of the line connecting the first vertex to the next
                                                                    #when we have this anlgle, we can turn the entire shape by the same angle rotating about
                                                                    #the first vertex in order to make this side lay flat.
        #will now make sure its in the correct quadrant.
        if vertex2.getY > vertex1.getY() and vertex2.getX() < vertex1.getX():
            angle = angle + math.pi
                        
                
        return angle
        
    
    def translateShapeToFitNicely(self): #this will move the shape to the positive quardrant of a graph, on the axis.
        longestVertexNumber = self.getLongestSide()
        furthestLeftVertex = self.getFurthestLeftVertex()
        furthestDownVertex = self.getFurthestDownVertex()
        tranlationXY = [(-furthestLeftVertex.getX(),-furthestDownVertex.getY())] #now translates using negative of most extremely wrong values for X and Y
        self.translateXY(tranlationXY)

    def stretchShape(self,scale):
        for eachVertex in self.vertices:
            eachVertex.stretchVertex(scale)

    def getFurthestRightVertex(self): #returns vertex with lowest X value
        furthestRightVertexNumber = 0
        if len(self.vertices) > 1:
            for count in range(1,len(self.vertices)):
                if self.vertices[count].getX() > self.vertices[furthestRightVertexNumber].getX():
                    furthestRightVertexNumber = count
        return self.vertices[furthestRightVertexNumber]

    def getFurthestLeftVertex(self): #returns vertex with highest X value
        furthestNumber = 0
        if len(self.vertices) > 1:
            for count in range(1,len(self.vertices)):
                if self.vertices[count].getX() < self.vertices[furthestNumber].getX():
                    furthestNumber = count
        return self.vertices[furthestNumber]

    def getFurthestUpVertex(self): #returns vertex with lowest Y value
        furthestNumber = 0
        if len(self.vertices) > 1:
            for count in range(1,len(self.vertices)):
                if self.vertices[count].getY() > self.vertices[furthestNumber].getY():
                    furthestNumber = count
        return self.vertices[furthestNumber]

    def getFurthestDownVertex(self): #returns vertex with highest Y value
        furthestNumber = 0
        if len(self.vertices) > 1:
            for count in range(1,len(self.vertices)):
                if self.vertices[count].getY() < self.vertices[furthestNumber].getY():
                    furthestNumber = count
        return self.vertices[furthestNumber]
