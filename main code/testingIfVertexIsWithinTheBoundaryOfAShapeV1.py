#===============================================================================
# Testing if a Vertex is within the boundary of a Shape
# 
# v1
#
#===============================================================================
import math
from myVertexandShapeClasses import * #this imports my vertex and shape classes
from shapely.geometry import Point, Polygon #this imports the required classes from shapely

#-------------------------------------------------------------------------------
# Defining the test to see if the Vertex is with the Shape
# I will be using the Shapely module
#-------------------------------------------------------------------------------

def testIfVertexIsWithinShape(shape,vertex):
    shapelyShape = Polygon(shape.getVerticesCoordinates()) #creates an instance of a Shapely Polygon that is identicle to the shape inputted
    shapelyPoint = Point(vertex.getCoordinates()) #creates an instance of a Shapely Point which is identicle to the vertex inputted
    return shapelyShape.intersects(shapelyPoint) #tests and returns if the Point is within or on the boundary of the Polygon
    


