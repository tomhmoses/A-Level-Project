#===============================================================================
# GUI - Version 12
#
# changed listOFTuplesOfNamesOfTilesInListAndHowManyOfEach to spaceQueue
#
#===============================================================================



#-------------------------------------------------------------------------------
# Importing required modules
#          PIL: For opening and editing image
#      Tkinter: Provides UI framework
#  resizeimage: For resizing the images.
# tkMessageBox: For easily displaying progress or error messages
# tkFileDialog: For getting where to save the image file.
#           os: For finding current filepath for sending the image.
#         copy: For 
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk, ImageDraw
import Tkinter as tk
import ttk as ttk
from resizeimage import resizeimage
import v24 as processingCode
import tkMessageBox
import tkFileDialog
import os
import copy


#-------------------------------------------------------------------------------
# Global variables
#-------------------------------------------------------------------------------

LARGE_FONT= ("Verdana", 12)
imageHeight = 500

mapNames = ['Main','North']

images = {} #makes dictionary for the images
images[mapNames[0]] = Image.open("main.png")
images[mapNames[1]] = Image.open("north.png")

globalMapName = mapNames[0] #images[mapNames[globalMapCount]] #sets the current image using a global variable

globalMapImage = resizeimage.resize_height(images[globalMapName], imageHeight)

frameBorderWidth = 0
labelBorderWidth = 0

designingCarPark = True
radiusOfCarParkVertices = 4

carParkShape = processingCode.shape()

pixelsPerMeter = float(1.75)

colour = 'blue'

showLabels = False

#-------------------------------------------------------------------------------
# Frames defined
#
#       mainFrame, majorityFrame, leftFrame, bottomLeftFrame, mapOptionsFrame,
#       tileScrollBoxFrame, tileOptionsFrame
#
#-------------------------------------------------------------------------------


class templateFrame(tk.Frame): #progress
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="templateFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        #pack frames and items



class mainFrame(tk.Frame): #need to add navbar
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='green', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="mainFame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        #self.items['navBar'] = navBar(self)
        self.frames['majorityFrame'] = majorityFrame(self)
        #pack frames and items
        #self.items['navBar'].pack(side="top", fill="both", expand=True)
        self.frames['majorityFrame'].pack(side="top", fill="both", expand=True)


class majorityFrame(tk.Frame): #done
    def __init__(self,parent):
        tk.Frame.__init__(self, parent, bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="majorityFame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        self.frames['leftFrame'] = leftFrame(self)
        self.frames['rightFrame'] = rightFrame(self)
        #pack frames and items
        self.frames['leftFrame'].pack(side="left", fill="both")
        self.frames['rightFrame'].pack(side="left", fill="both", expand=True)


class leftFrame(tk.Frame): #done
    def __init__(self,parent):
        tk.Frame.__init__(self, parent, bg='red', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="leftFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        self.frames['mapFrame'] = mapFrame(self)
        self.frames['bottomLeftFrame'] = bottomLeftFrame(self)
        #pack frames and items
        self.frames['mapFrame'].pack(side="top")
        self.frames['bottomLeftFrame'].pack(side="top", fill="both", expand=True)

class mapFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent, bg='pink', bd = frameBorderWidth)
        self.parent = parent
        self.items = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="mapFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        self.items['mapImage'] = mapImage(self)
        self.items['mapImage'].pack(side="top", fill="both", expand=True)

class bottomLeftFrame(tk.Frame): #done
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='pink', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="bottomLeftFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        self.frames['mapOptionsFrame'] = mapOptionsFrame(self)
        self.items['goButton'] = goButton(self)
        #pack frames and items
        self.items['goButton'].pack(side="right", fill="y")
        self.frames['mapOptionsFrame'].pack(side="right", fill="both", expand=True)


class mapOptionsFrame(tk.Frame): #need to find how to pack hideParkingLayoutButton to bottom.
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="mapOptionsFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        self.items['mapTypeComboBox'] = mapTypeComboBox(self)
        self.items['shapeVertexRemoveButton'] = shapeVertexRemoveButton(self)
        self.items['shapeResetButton'] = shapeResetButton(self)
        self.items['mapPerimeterRoadCheckBox'] = mapPerimeterRoadCheckBox(self)
        self.items['hideParkingLayoutButton'] = hideParkingLayoutButton(self)
        #pack frames and items
        self.items['mapTypeComboBox'].pack(side="top", fill="x")
        self.items['shapeVertexRemoveButton'].pack(side="top", fill="x")
        self.items['shapeResetButton'].pack(side="top", fill="x")
        self.items['mapPerimeterRoadCheckBox'].pack(side="top", fill="x")
        self.items['hideParkingLayoutButton'].pack(side="top", fill="x") 




class rightFrame(tk.Frame): #done
    def __init__(self,parent):
        tk.Frame.__init__(self, parent, bg='orange', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="rightFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        self.items['tileLabel'] = tk.Label(self, text="Spaces to be added\nto the car park:", font=LARGE_FONT)
        self.frames['tileScrollBoxFrame'] = tileScrollBoxFrame(self)
        self.frames['tileOptionsFrame'] = tileOptionsFrame(self)
        self.items['tileResetButton'] = tileResetButton(self)
        #pack frames and items
        self.items['tileLabel'].pack(side="top", fill="x")#, expand=True)
        self.frames['tileScrollBoxFrame'].pack(side="top", fill="both",expand = True)#, expand=True)
        self.frames['tileOptionsFrame'].pack(side="top", fill="x")#, expand=True)
        self.items['tileResetButton'].pack(side="top", fill="x")



class tileScrollBoxFrame(tk.Frame): #done
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='grey', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="tileScrollBoxFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        self.items['tileScrollBox'] = tileScrollBox(self)
        #pack frames and items
        self.items['tileScrollBox'].pack(side="left", fill="both", expand=True)


class tileOptionsFrame(tk.Frame): #progress
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='blue', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        if showLabels:
            label = tk.Label(self, text="tileOptionsFrame", font=LARGE_FONT)
            label.pack(pady=labelBorderWidth,padx=labelBorderWidth)
        #add frames and items
        self.items['tileTypeComboBox'] = tileTypeComboBox(self)
        self.items['tileNumericStepper'] = tileNumericStepper(self)
        self.items['tileAddButton'] = tileAddButton(self)
        #pack frames and items
        self.items['tileTypeComboBox'].pack(side="top", fill="both", expand=True)
        self.items['tileNumericStepper'].pack(side="top", fill="both", expand=True)
        self.items['tileAddButton'].pack(side="top", fill="both", expand=True)


#-------------------------------------------------------------------------------
# Elements defined (all are actually just frames with things inside of them)
#
#       mapImage, mapTypeComboBox, shapeVertexRemoveButton,
#       shapeResetButton, hideParkingLayoutButton, goButton, tileScrollBox,
#       tileScrollBar, tileTypeComboBox, tileNumericStepper, tileAddButton,
#       tileResetButton
#
#-------------------------------------------------------------------------------

class mapImage(tk.Frame):
    def __init__(self, parent): #done
        #print "map drawn"
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add image to a canvas
        myFrame = tk.Frame(self)
        myFrame.pack()
        self.image = globalMapImage
        self.canvas = tk.Canvas(myFrame, width=self.image.size[0], height=self.image.size[1]) #image.size gives you the width and depth
        self.canvas.pack() #packs the canvas so it shows up
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.image_tk) #//2 needed in order to center the image
        #binds clicking on image to a procedure calls mapClicked
        self.canvas.bind("<Button-1>", self.mapClicked) #<Button-1> is the left mouse button

    def mapClicked(self,event):
        if designingCarPark:
            carParkShape.addVertex(processingCode.vertex(event.x,event.y))
            #print "coords: " + str(event.x) + "," + str(event.y)
            drawMapImage()
            refreshMap()
        else:
             print "clicking the map did nothing because you're looking at the finished car park"



class mapTypeComboBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            self.comboBox = ttk.Combobox(self, values = mapNames, state="readonly") #through setting the state to read only the user can only choose the values that are in the list.
        else:
            self.comboBox = ttk.Combobox(self, values = mapNames, state = 'disabled')
        self.comboBox.set(globalMapName)
        #pack items
        self.comboBox.pack(side="left")


class shapeVertexRemoveButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="Remove last vertex", command = self.buttonClicked)
        else:
            button = tk.Button(self, text="Remove last vertex", state='disabled')
        #pack items
        button.pack(side="left")

    def buttonClicked(self):
        #print "shapeVertexRemoveButton clicked"
        carParkShape.removeLastVertex() #removes last added vertex from the shape
        drawMapImage()
        refreshMap()


class shapeResetButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="Reset car park shape and update map", bg='red', command=self.buttonClicked)
        else:
            button = tk.Button(self, text="Reset car park shape and update map", bg='red', state='disabled')
        #pack items
        button.pack(side="left")

    def buttonClicked(self):
        global globalMapName,globalMapImage, carParkShape
        globalMapName = self.parent.items['mapTypeComboBox'].comboBox.get()
        globalMapImage = resizeimage.resize_height(images[globalMapName], imageHeight)
        carParkShape = processingCode.shape()
        #print "shapeResetButton clicked"
        #print self.parent.items['mapTypeComboBox'].comboBox.get()
        refreshMap()

class mapPerimeterRoadCheckBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.addPerimeterRoad = tk.BooleanVar()
        if designingCarPark:
            checkBox = tk.Checkbutton(self, text="Add Perimeter Road", variable=self.addPerimeterRoad, onvalue = True, offvalue = False)
        else:
            checkBox = tk.Checkbutton(self, text="Add Perimeter Road", variable=self.addPerimeterRoad, onvalue = True, offvalue = False, state='disabled')
        #pack items
        checkBox.pack(side="left")

class hideParkingLayoutButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if not designingCarPark:
            button = tk.Button(self, text="Hide car park spaces layout",bg = "green", command = self.buttonClicked)
        else:
            button = tk.Button(self, text="Hide car park spaces layout", state='disabled')
        #pack items
        button.pack(side="left")

    def buttonClicked(self):
        #print "hideParkingLayoutButton clicked"
        global designingCarPark
        designingCarPark = True
        drawMapImage()
        refreshWindow()


class goButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="GO!\nGenerate the\ncar park", bg = "green", command = self.buttonClicked)
        else:
            button = tk.Button(self, text="GO!\nGenerate the\ncar park", state='disabled')
        #pack items
        button.pack(side="right", fill="y", expand=True)

    def buttonClicked(self):
        #print "goButton clicked"
        global designingCarPark, globalMapImage
        if len(carParkShape.getVertices()) < 3: #a valid shape can't have less than three vertices
            tkMessageBox.showerror("Report","Error: Your car park shape must have more than 2 vertices")
        else:
            globalMapImage = resizeimage.resize_height(images[globalMapName], imageHeight)
            designingCarPark = False
            carParkShapeForUseInProcessing = copy.deepcopy(carParkShape) #because it would otherwise pass my shape instance by referance, I make a copy of it to be passed to the processing code.
            listOfGroupsOfCoordinatesForLines,messageToPrint = processingCode.GetCarParkPixelLinesToDrawFromPixelShape(carParkShapeForUseInProcessing,pixelsPerMeter,getAddPerimeterRoad())     
            draw = ImageDraw.Draw(globalMapImage)
            listOfCoordinates = carParkShape.getVerticesCoordinates()
            for eachGroupOfCoordinatesForLines in listOfGroupsOfCoordinatesForLines:
                #print "eachGroupOfCoordinatesForLines:"
                #print eachGroupOfCoordinatesForLines
                draw.line(eachGroupOfCoordinatesForLines)
            del draw
            refreshWindow()
            tkMessageBox.showinfo("Report",messageToPrint)
            #print messageToPrint


class tileScrollBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add label
        #add items
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(self)#, values = processingCode.spaceQueue)
        for each in processingCode.spaceQueue:
            self.listbox.insert('end', str(each))
        self.listbox.pack(side="right", fill="both", expand=True)

        # attach listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)


class tileTypeComboBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            self.comboBox = ttk.Combobox(self, values = processingCode.tileNames, state="readonly")
        else:
            self.comboBox = ttk.Combobox(self, values = processingCode.tileNames, state = 'disabled')
        self.comboBox.set(processingCode.tileNames[0])
        #pack items
        self.comboBox.pack(side="right")


class tileNumericStepper(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        self.stepper = tk.Spinbox(self, from_=1, to_=1000000000)
        self.stepper.pack(side = 'right')
        #pack items


class tileAddButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="Add to space(s) queue", command = self.buttonClicked)
        else:
            button = tk.Button(self, text="Add to tile queue", state='disabled')
        #pack items
        button.pack(side = "right")

    def buttonClicked(self):
        #print "tileAddButton clicked"
        processingCode.spaceQueue.append((self.parent.items['tileTypeComboBox'].comboBox.get(), int(self.parent.items['tileNumericStepper'].stepper.get())))
        refreshWindow()


class tileResetButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="\nReset queue\n",bg='red', command =  self.buttonClicked)
        else:
            button = tk.Button(self, text="\nReset queue\n",bg='red', state='disabled')
        #pack items
        button.pack(fill="both", expand=True)

    def buttonClicked(self):
        #print "tileResetButton clicked"
        processingCode.spaceQueue = []
        refreshWindow()





#-------------------------------------------------------------------------------
# Functions for refreshing the window
#-------------------------------------------------------------------------------

def refreshWindow():
    global godFrame
    godFrame.destroy()
    godFrame = mainFrame(window)
    godFrame.pack(side="top", fill="both", expand=True)

def refreshMap():
    global godFrame
    godFrame.frames['majorityFrame'].frames['leftFrame'].frames['mapFrame'].items['mapImage'].destroy()
    godFrame.frames['majorityFrame'].frames['leftFrame'].frames['mapFrame'].items['mapImage'] = mapImage(godFrame.frames['majorityFrame'].frames['leftFrame'].frames['mapFrame'])
    godFrame.frames['majorityFrame'].frames['leftFrame'].frames['mapFrame'].items['mapImage'].pack()


def drawMapImage():
    global globalMapImage
    globalMapImage = resizeimage.resize_height(images[globalMapName], imageHeight)
    draw = ImageDraw.Draw(globalMapImage)
    listOfCoordinates = carParkShape.getVerticesCoordinates()
    for count in range(len(listOfCoordinates)):#  each in carParkShape.getVerticesCoordinates():
        draw.ellipse((listOfCoordinates[count][0]-radiusOfCarParkVertices,listOfCoordinates[count][1]-radiusOfCarParkVertices,listOfCoordinates[count][0]+radiusOfCarParkVertices,listOfCoordinates[count][1]+radiusOfCarParkVertices))#,fill = colour)
        draw.line((listOfCoordinates[count][0],listOfCoordinates[count][1],listOfCoordinates[(count+1)%len(listOfCoordinates)][0],listOfCoordinates[(count+1)%len(listOfCoordinates)][1]))#,fill = colour)
        #print (listOfCoordinates[count][0],listOfCoordinates[count][1],listOfCoordinates[(count+1)%len(listOfCoordinates)][0],listOfCoordinates[(count+1)%len(listOfCoordinates)][1],)
    del draw


#-------------------------------------------------------------------------------
# Procedures for the menu bar
#-------------------------------------------------------------------------------

def addMenubar():
    menubar = tk.Menu(window) #creates menubar
    shareMenu = tk.Menu(menubar, tearoff = 0) #adds option to menu bar
    shareMenu.add_command(label = 'Save image to file', command = saveImageToFile) #adds option to save image to file
    shareMenu.add_command(label = 'Email car park image', command = emailCarParkImage) #adds option to save image to file
    menubar.add_cascade(label="Share", menu=shareMenu) #adds share menu to menubar
    menubar.add_command(label = "Help", command = showHelpMessageBox)
    #menubar.add_command(label = "Test Button", command = testProcedure)
    window.config(menu=menubar) #adds menubar to the window
    

def testProcedure():
    print getAddPerimeterRoad()

def getAddPerimeterRoad():
    return godFrame.frames['majorityFrame'].frames['leftFrame'].frames['bottomLeftFrame'].frames['mapOptionsFrame'].items['mapPerimeterRoadCheckBox'].addPerimeterRoad.get()
    
def saveImageToFile():
    #print "stub for saving image to file"
    try:
        filepath = tkFileDialog.asksaveasfilename(defaultextension = "bmp", title = "Choose where to save the image")
        globalMapImage.save(filepath,"bmp")
        tkMessageBox.showinfo("Report","Successfully saved image to: " + str(filepath))
    except:
        tkMessageBox.showinfo("Report","There was an error saving the image")
    
def emailCarParkImage():
    #print "stub for emailing car park image"
    filepath =  os.getcwd() + "\\" +"tempImageForEmail.bmp"
    globalMapImage.save("tempImageForEmail.bmp","bmp")
    import win32com.client as win32   

    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    #mail.To = ""
    mail.Subject = "Car Park Image Email"
    #mail.HtmlBody = "some text"
    print filepath
    
    mail.Attachments.Add(filepath)
    mail.Display(False)

def showHelpMessageBox():
    helpFile = open('Help.txt','r')
    helpMessage = helpFile.read()
    helpFile.close()
    tkMessageBox.showinfo("Here's some help",helpMessage) 




#-------------------------------------------------------------------------------
# Window created and mainloop started.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Designing Car Park")
    window.minsize(width=1050, height=imageHeight+125) #made it so you cannot scale the window any smaller than it should be
    addMenubar()
    godFrame = mainFrame(window) #the godFrame is the name of the mainFrame instance
    godFrame.pack(side="top", fill="both", expand=True)
    window.mainloop()
