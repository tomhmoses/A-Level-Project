#===============================================================================
# GUI - Version 4
# 
# Adding other buttons with the designing true/false support
# Removed padding when packing elements inside their original classes
#
#===============================================================================



#-------------------------------------------------------------------------------
# Importing required modules
#         PIL: For opening and editing image (will use this in a later version)
#     Tkinter: Provides UI framework (will use this in a later version)
# resizeimage: For resizing the images.
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk, ImageDraw
import Tkinter as tk
import ttk as ttk
from resizeimage import resizeimage

LARGE_FONT= ("Verdana", 12)
imageHeight = 500

mapNames = ['Main','North']

images = {} #makes dictionary for the images
images[mapNames[0]] = Image.open("main.png")
images[mapNames[1]] = Image.open("north.png")

images[mapNames[0]] = resizeimage.resize_height(images[mapNames[0]], imageHeight) #resizes the images so they fit on the screen
images[mapNames[1]] = resizeimage.resize_height(images[mapNames[1]], imageHeight)

globalMapName = mapNames[0] #images[mapNames[globalMapCount]] #sets the current image using a global variable
frameBorderWidth = 5

print "recent"

#-------------------------------------------------------------------------------
# Frames defined
#
#       mainFrame, majorityFrame, leftFrame, bottomLeftFrame, mapOptionsFrame,
#       tileScrollBoxFrame, tileOptionsFrame
#
#-------------------------------------------------------------------------------


class templateFrame(tk.Frame): #progress
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="templateFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items   



class mainFrame(tk.Frame): #need to add navbar
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent, bg='green', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="mainFame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #self.items['navBar'] = navBar(self)
        self.frames['majoirtyFrame'] = majorityFrame(self, designingCarPark)
        #pack frames and items
        #self.items['navBar'].pack(side="top", fill="both", expand=True)
        self.frames['majoirtyFrame'].pack(side="top", fill="both", expand=True)     


class majorityFrame(tk.Frame): #done
    def __init__(self,parent, designingCarPark):
        tk.Frame.__init__(self, parent, bg='blue', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="majorityFame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.frames['leftFrame'] = leftFrame(self, designingCarPark)
        self.frames['rightFrame'] = rightFrame(self, designingCarPark)
        #pack frames and items
        self.frames['leftFrame'].pack(side="left", fill="both", expand=True)
        self.frames['rightFrame'].pack(side="left", fill="both", expand=True)  


class leftFrame(tk.Frame): #done
    def __init__(self,parent, designingCarPark):
        tk.Frame.__init__(self, parent, bg='red', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="leftFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['mapImage'] = mapImage(self, designingCarPark)
        self.frames['bottomLeftFrame'] = bottomLeftFrame(self, designingCarPark)
        #pack frames and items
        self.items['mapImage'].pack(side="top", fill="both", expand=True) 
        self.frames['bottomLeftFrame'].pack(side="top", fill="both", expand=True)

    def refreshMap(self):
        self.items['mapImage'].destroy()
        self.items['mapImage'] = mapImage(self, designingCarPark)
        self.items['mapImage'].pack(side="top", fill="both", expand=True)


class bottomLeftFrame(tk.Frame): #done
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent, bg='pink', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="bottomLeftFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.frames['mapOptionsFrame'] = mapOptionsFrame(self, designingCarPark)
        self.items['goButton'] = goButton(self, designingCarPark)
        #pack frames and items
        self.frames['mapOptionsFrame'].pack(side="left", fill="both", expand=True)
        self.items['goButton'].pack(side="left", fill="both", expand=True)


class mapOptionsFrame(tk.Frame): #need to find how to pack hideParkingLayoutButton to bottom.
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent, bg='blue', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="mapOptionsFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['mapTypeComboBox'] = mapTypeComboBox(self, designingCarPark)
        self.items['shapeVertexRemoveButton'] = shapeVertexRemoveButton(self, designingCarPark)
        self.items['shapeResetButton'] = shapeResetButton(self, designingCarPark)
        self.items['hideParkingLayoutButton'] = hideParkingLayoutButton(self, designingCarPark)
        #pack frames and items
        self.items['mapTypeComboBox'].pack(side="top", fill="both", expand=True)
        self.items['shapeVertexRemoveButton'].pack(side="top", fill="both", expand=True)
        self.items['shapeResetButton'].pack(side="top", fill="both", expand=True)
        self.items['hideParkingLayoutButton'].pack(side="bottom", fill="both", expand=True)


        

class rightFrame(tk.Frame): #done
    def __init__(self,parent, designingCarPark):
        tk.Frame.__init__(self, parent, bg='orange', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="rightFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['tileLabel'] = tk.Label(self, text="Tiles to be added to the car park:", font=LARGE_FONT)
        self.frames['tileScrollBoxFrame'] = tileScrollBoxFrame(self)
        self.frames['tileOptionsFrame'] = tileOptionsFrame(self, designingCarPark)
        self.items['tileResetButton'] = tileResetButton(self, designingCarPark)
        #pack frames and items
        self.items['tileLabel'].pack(side="top", fill="both", expand=True)
        self.frames['tileScrollBoxFrame'].pack(side="top", fill="both", expand=True)
        self.frames['tileOptionsFrame'].pack(side="top", fill="both", expand=True)
        self.items['tileResetButton'].pack(side="top", fill="both", expand=True)
        
        

class tileScrollBoxFrame(tk.Frame): #done
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='grey', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="tileScrollBoxFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['tileScrollBox'] = tileScrollBox(self)
        self.items['tileScrollBar'] = tileScrollBar(self)
        #pack frames and items
        self.items['tileScrollBox'].pack(side="left", fill="both", expand=True)
        self.items['tileScrollBar'].pack(side="left", fill="both", expand=True)


class tileOptionsFrame(tk.Frame): #progress
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent, bg='blue', bd = frameBorderWidth)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="tileOptionsFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['tileTypeComboBox'] = tileTypeComboBox(self, designingCarPark)
        self.items['tileNumericStepper'] = tileNumericStepper(self, designingCarPark)
        self.items['tileAddButton'] = tileAddButton(self, designingCarPark)
        #pack frames and items
        self.items['tileTypeComboBox'].pack(side="top", fill="both", expand=True)
        self.items['tileNumericStepper'].pack(side="top", fill="both", expand=True)
        self.items['tileTypeComboBox'].pack(side="top", fill="both", expand=True)          


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
    def __init__(self, parent, designingCarPark): #done
        print "map drawn"
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add image to a canvas
        myFrame = tk.Frame(self)
        myFrame.pack()
        self.image = images[globalMapName]
        self.canvas = tk.Canvas(myFrame, width=self.image.size[0], height=self.image.size[1]) #image.size gives you the width and depth
        self.canvas.pack() #packs the canvas so it shows up
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.image_tk) #//2 needed in order to center the image
        #binds clicking on image to a procedure calls mapClicked
        self.canvas.bind("<Button-1>", self.mapClicked) #<Button-1> is the left mouse button

    def mapClicked(self,event):
        print "coords: " + str(event.x) + "," + str(event.y)


class mapTypeComboBox(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            self.comboBox = ttk.Combobox(self, values = mapNames)
        else:
            self.comboBox = ttk.Combobox(self, values = mapNames, state = 'disabled')
        self.comboBox.set(globalMapName)
        #pack items
        self.comboBox.pack(side="left")


class shapeVertexRemoveButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
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
        print "shapeVertexRemoveButton clicked"


class shapeResetButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="Reset car park shape and update map", bg='red', command=self.buttonClicked)
        else:
            button = tk.Button(self, text="Reset car park shape", bg='red', state='disabled')
        #pack items
        button.pack(side="left")

    def buttonClicked(self):
        global globalMapName
        globalMapName = self.parent.items['mapTypeComboBox'].comboBox.get()
        print "shapeResetButton clicked"
        print self.parent.items['mapTypeComboBox'].comboBox.get()
        refreshWindow()


class hideParkingLayoutButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if not designingCarPark:
            button = tk.Button(self, text="Hide car park tile layout", command = self.buttonClicked)
        else:
            button = tk.Button(self, text="Hide car park tile layout", state='disabled')
        #pack items
        button.pack(side="left")

    def buttonClicked(self):
        print "hideParkingLayoutButton clicked"


class goButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="GO!\nGenerate the\ncar park", bg = "green", command = self.buttonClicked)
        else:
            button = tk.Button(self, text="GO!\nGenerate the\ncar park", bg = "green", state='disabled')
        #pack items
        button.pack(fill="both", expand=True)

    def buttonClicked(self):
        print "goButton clicked"


class tileScrollBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add label  
        label = tk.Label(self, text="tileScrollBox", font=LARGE_FONT)
        label.pack()
        #add items
        #pack items


class tileScrollBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add label  
        label = tk.Label(self, text="tileScrollBar", font=LARGE_FONT)
        label.pack()
        #add items
        #pack items


class tileTypeComboBox(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add label  
        label = tk.Label(self, text="tileTypeComboBox", font=LARGE_FONT)
        label.pack()
        #add items
        #pack items


class tileNumericStepper(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add label  
        label = tk.Label(self, text="tileNumericStepper", font=LARGE_FONT)
        label.pack()
        #add items
        #pack items


class tileAddButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="Add to tile queue", command = self.buttonClicked)
        else:
            button = tk.Button(self, text="Add to tile queue", state='disabled')
        #pack items 
        button.pack(side = "right")

    def buttonClicked(self):
        print "tileAddButton clicked"


class tileResetButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add items
        if designingCarPark:
            button = tk.Button(self, text="Reset queue", command = refreshMap)#self.buttonClicked)
        else:
            button = tk.Button(self, text="Reset queue", state='disabled')
        #pack items  
        button.pack()

    def buttonClicked(self):
        print "tileResetButton clicked"


        
#-------------------------------------------------------------------------------
# Functions for certain button clicks
#-------------------------------------------------------------------------------

def refreshWindow():
    global godFrame
    godFrame.destroy()
    godFrame = mainFrame(window,True)
    godFrame.pack(side="top", fill="both", expand=True)

def refreshMap():
    global godFrame
    godFrame.frames['majoirtyFrame'].frames['leftFrame'].refreshMap()

def callback():
    print "button pressed"
        
#-------------------------------------------------------------------------------
# Window created and mainloop started.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    window = tk.Tk()
    godFrame = mainFrame(window,True)
    godFrame.pack(side="top", fill="both", expand=True)
    window.mainloop()
