#===============================================================================
# GUI - Version 14
#
# final version of commented and cleaned up code
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
import v26 as processingCode
import tkMessageBox
import tkFileDialog
import os
import copy


#-------------------------------------------------------------------------------
# Global variables
#-------------------------------------------------------------------------------

#image height is used to make sure the window displays at a sensible and consistant size
imageHeight = 500

mapNames = ['Main','North']

#makes dictionary for the images
images = {} 
images[mapNames[0]] = Image.open("main.png")
images[mapNames[1]] = Image.open("north.png")

#when the program is launched, the main map will be the current map
globalMapName = mapNames[0] 
#sets the current image using a global variable
globalMapImage = resizeimage.resize_height(images[globalMapName], imageHeight)

#when the program is launched, it will be in the designing state.
designingCarPark = True

#constants
radiusOfCarParkVertices = 4
pixelsPerMeter = float(1.75)
#large font used for when the label in the top right of the window is added.
LARGE_FONT= ("Verdana", 12)

#the main global variable is obvously the car park shape, which is an instance of a shape class
carParkShape = processingCode.shape()


#-------------------------------------------------------------------------------
# Frames defined
#
#       mainFrame, majorityFrame, leftFrame, bottomLeftFrame, mapOptionsFrame,
#       tileScrollBoxFrame, tileOptionsFrame
#
#-------------------------------------------------------------------------------


#everything is within the main frame.
class mainFrame(tk.Frame): 
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        #add frames and items
        #self.items['navBar'] = navBar(self)
        self.frames['majorityFrame'] = majorityFrame(self)
        #pack frames and items
        #self.items['navBar'].pack(side="top", fill="both", expand=True)
        self.frames['majorityFrame'].pack(side="top", fill="both", expand=True)

#everything is also within the majority frame.
class majorityFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        #add frames and items
        self.frames['leftFrame'] = leftFrame(self)
        self.frames['rightFrame'] = rightFrame(self)
        #pack frames and items
        self.frames['leftFrame'].pack(side="left", fill="both")
        self.frames['rightFrame'].pack(side="left", fill="both", expand=True)

#the left frame is the frame for all the suff on the left of the window.
class leftFrame(tk.Frame): 
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        #add frames and items
        self.frames['mapFrame'] = mapFrame(self)
        self.frames['bottomLeftFrame'] = bottomLeftFrame(self)
        #pack frames and items
        self.frames['mapFrame'].pack(side="top")
        self.frames['bottomLeftFrame'].pack(side="top", fill="both", expand=True)

#the map frame contains the map image.
class mapFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.items = {}
        #add the map item and pack it
        self.items['mapImage'] = mapImage(self)
        self.items['mapImage'].pack(side="top", fill="both", expand=True)

#the bottom left frame contains the map options and the go button
class bottomLeftFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        self.frames['mapOptionsFrame'] = mapOptionsFrame(self)
        self.items['goButton'] = goButton(self)
        #pack frames and items
        self.items['goButton'].pack(side="right", fill="y")
        self.frames['mapOptionsFrame'].pack(side="right", fill="both", expand=True)


#the map options fram contains the buttons in the bottom left of the window
class mapOptionsFrame(tk.Frame): 
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.items = {}
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



#the right frame contains the space queue options
class rightFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        #the '\n' on the next line adds the text folling it to a new line so that the program window is slimmer.
        self.items['tileLabel'] = tk.Label(self, text="Spaces to be added\nto the car park:", font=LARGE_FONT)
        self.items['tileScrollBox'] = tileScrollBox(self)
        self.frames['tileOptionsFrame'] = tileOptionsFrame(self)
        self.items['tileResetButton'] = tileResetButton(self)
        #pack frames and items
        self.items['tileLabel'].pack(side="top", fill="x")
        self.items['tileScrollBox'].pack(side="top", fill="both", expand=True)
        self.frames['tileOptionsFrame'].pack(side="top", fill="x")
        self.items['tileResetButton'].pack(side="top", fill="x")


#the tile options frame is for the elements packed to the right in the bottom right of the window
class tileOptionsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
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
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add image to a canvas
        myFrame = tk.Frame(self)
        myFrame.pack()
        self.image = globalMapImage
        #image.size gives you the width and depth
        self.canvas = tk.Canvas(myFrame, width=self.image.size[0], height=self.image.size[1]) 
        #packs the canvas so it shows up
        self.canvas.pack() 
        self.image_tk = ImageTk.PhotoImage(self.image)
        #on the next line, //2 is needed in order to center the image
        self.canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.image_tk) #//2 needed in order to center the image
        #binds clicking on image to a procedure calls mapClicked
        self.canvas.bind("<Button-1>", self.mapClicked) #<Button-1> is the left mouse button

    def mapClicked(self,event):
        #when the map is clicked and if the window is in designing mode, it will add a vertex to the car park shape then refresh just the map, not the entire window
        if designingCarPark:
            if len(carParkShape.getVerticesCoordinates()) > 0:
                if carParkShape.getVerticesCoordinates()[len(carParkShape.getVerticesCoordinates())-1] != [event.x,event.y]: #tests if vertex was already just added, then it will not add a duplicate vertex, but if it isnt the same as the most recent vertex it will add it.
                    carParkShape.addVertex(processingCode.vertex(event.x,event.y))
            else:
                #if there is only one vertex then it will add the vertex.
                carParkShape.addVertex(processingCode.vertex(event.x,event.y))
            drawMapImage()
            refreshMap()



class mapTypeComboBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        self.comboBox = ttk.Combobox(self, values = mapNames, state="readonly") #through setting the state to read only the user can only choose the values that are in the list.
        #I have tidied up my code by only adding the different state if the car park is not in the designing mode, instead of redefining the button
        if not designingCarPark:
            self.comboBox.config(state = 'disabled')
        self.comboBox.set(globalMapName)
        #pack items
        self.comboBox.pack(side="left")


class shapeVertexRemoveButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        button = tk.Button(self, text="Remove last vertex", command = self.buttonClicked)
        if not designingCarPark:
            button.config(state = 'disabled')
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
        button = tk.Button(self, text="Reset car park shape and update map", bg='red', command=self.buttonClicked)
        if not designingCarPark:
            button.config(state = 'disabled')
        #pack items
        button.pack(side="left")

    def buttonClicked(self):
        global globalMapName,globalMapImage, carParkShape
        globalMapName = self.parent.items['mapTypeComboBox'].comboBox.get()
        globalMapImage = resizeimage.resize_height(images[globalMapName], imageHeight)
        #sets the car park shape to a new blank shape
        carParkShape = processingCode.shape()
        refreshMap()

class mapPerimeterRoadCheckBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.addPerimeterRoad = tk.BooleanVar()
        checkBox = tk.Checkbutton(self, text="Add Perimeter Road", variable=self.addPerimeterRoad, onvalue = True, offvalue = False)
        if not designingCarPark:
            checkBox.config(state = 'disabled')
        #pack items
        checkBox.pack(side="left")

class hideParkingLayoutButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        button = tk.Button(self, text="Hide car park spaces layout",bg = "green", command = self.buttonClicked)
        if designingCarPark:
            #if the button is disabled I need to change its colour back to the default colour
            button.config(bg = "SystemButtonFace", state = 'disabled')
        #pack items
        button.pack(side="left")

    def buttonClicked(self):
        global designingCarPark
        designingCarPark = True
        drawMapImage()
        refreshWindow()


class goButton(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        button = tk.Button(self, text="GO!\nGenerate the\ncar park", bg = "green", command = self.buttonClicked)
        if not designingCarPark:
            button.config(bg = "SystemButtonFace", state = 'disabled')
        #pack items
        button.pack(side="right", fill="y", expand=True)

    def buttonClicked(self):
        #when this button is clicked, it will generate the car park design, pulling together the values from other areas from the gui
        #I also include validation here.
        global designingCarPark, globalMapImage
        if len(carParkShape.getVertices()) < 3: #a valid shape can't have less than three vertices
            tkMessageBox.showerror("Report","Error: Your car park shape must have more than 2 vertices")
        elif len(processingCode.spaceQueue) < 1:
            tkMessageBox.showerror("Report","Your space(s) queue must contain at least one type of car park to be added")
        else:
            #if the car park shape is okay, it will now generate the car park layout in the processing code
            globalMapImage = resizeimage.resize_height(images[globalMapName], imageHeight)
            designingCarPark = False
            carParkShapeForUseInProcessing = copy.deepcopy(carParkShape) #because it would otherwise pass my shape instance by referance, I make a copy of it to be passed to the processing code.
            listOfGroupsOfCoordinatesForLines,messageToPrint = processingCode.GetCarParkPixelLinesToDrawFromPixelShape(carParkShapeForUseInProcessing,pixelsPerMeter,getAddPerimeterRoad())     
            #it will now draw the car park layout with the lines that were passed back.
            draw = ImageDraw.Draw(globalMapImage)
            listOfCoordinates = carParkShape.getVerticesCoordinates()
            for eachGroupOfCoordinatesForLines in listOfGroupsOfCoordinatesForLines:
                draw.line(eachGroupOfCoordinatesForLines)
            del draw #this needs to be deleted to keep memory clean.
            refreshWindow()
            tkMessageBox.showinfo("Report",messageToPrint)


class tileScrollBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
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
            button = tk.Button(self, text="Add to space(s) queue", state='disabled')
        #pack items
        button.pack(side = "right")

    def buttonClicked(self):
        #print "tileAddButton clicked"
        try:
            if int(self.parent.items['tileNumericStepper'].stepper.get()) < 1: #will check if it is below the lower limit of 1
                tkMessageBox.showerror("Report","Error: To add some spaces to the queue, the number must be greater than 0")
            elif int(self.parent.items['tileNumericStepper'].stepper.get()) > 1000000: #will check if it is above the upper limit of 1 million
                if tkMessageBox.askyesno("Report","Error: To add some spaces to the queue, the number must be less than 1,000,000. Do you want me to add 1,000,000 spaces to the queue instead?"):
                    processingCode.spaceQueue.append((self.parent.items['tileTypeComboBox'].comboBox.get(), 1000000)) #if the user wanted, it will add 1 million spaces to the queue
                    refreshWindow()
            else: #if the integer value is okay then it will add it to the queue.
                processingCode.spaceQueue.append((self.parent.items['tileTypeComboBox'].comboBox.get(), int(self.parent.items['tileNumericStepper'].stepper.get())))
                refreshWindow()
        except:
            tkMessageBox.showerror("Report","Error: To add some spaces to the queue, the number must be an integer.")


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
    #destroys the frame, then creates it again, then packs it.
    godFrame.destroy()
    godFrame = mainFrame(window)
    godFrame.pack(side="top", fill="both", expand=True)

def refreshMap():
    global godFrame
    #destroys the frame, then creates it again, then packs it.
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
        draw.line((listOfCoordinates[count][0],listOfCoordinates[count][1],listOfCoordinates[(count+1)%len(listOfCoordinates)][0],listOfCoordinates[(count+1)%len(listOfCoordinates)][1]))        
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
    window.config(menu=menubar) #adds menubar to the window
    

def testProcedure():
    print getAddPerimeterRoad()

def getAddPerimeterRoad():
    return godFrame.frames['majorityFrame'].frames['leftFrame'].frames['bottomLeftFrame'].frames['mapOptionsFrame'].items['mapPerimeterRoadCheckBox'].addPerimeterRoad.get()
    
def saveImageToFile():
    #print "stub for saving image to file"
    try:
        filepath = tkFileDialog.asksaveasfilename(defaultextension = "bmp", title = "Choose where to save the image", filetypes=[("Bitmap Image", ".bmp")])
        if len(filepath) == 0:
            tkMessageBox.showinfo("Report","The image was not saved as you either didnt enter a file name or cancelled the save process.")
        else:
            if filepath[len(filepath)-4:] != ".bmp":
                filepath = filepath + ".bmp"
            globalMapImage.save(filepath,"bmp")
            tkMessageBox.showinfo("Report","Successfully saved image to:\n" + str(filepath))
    except:
        tkMessageBox.showinfo("Report","There was an error saving the image")
    
def emailCarParkImage():
    #gets the filepath to save the image in. I use \\ to escape the \ modifier so that I can add just a \
    filepath =  os.getcwd() + "\\" +"tempImageForEmail.bmp"
    globalMapImage.save("tempImageForEmail.bmp","bmp")
    #gets the required module
    import win32com.client as win32   

    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.Subject = "Car Park Image Email"
    #I then add the attachment
    mail.Attachments.Add(filepath)
    mail.Display(False)

def showHelpMessageBox():
    #opens the text file, reads it, closes the file connection, then shows the text in a info dialog
    helpFile = open('Help.txt','r')
    helpMessage = helpFile.read()
    helpFile.close()
    tkMessageBox.showinfo("Here's some help",helpMessage) 




#-------------------------------------------------------------------------------
# Window created and mainloop started.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    #the window is a global instance of a tk window
    window = tk.Tk()
    window.title("Car Park Layout Generator")
    #made it so you cannot scale the window any smaller than it should be
    window.minsize(width=1050, height=imageHeight+125)
    #adds the menubar using my menubar procedure
    addMenubar()
    #godFrame is the name of the mainFrame instance
    godFrame = mainFrame(window)
    #then packs the godFrame
    godFrame.pack(side="top", fill="both", expand=True)
    #starts the window running.
    window.mainloop()
