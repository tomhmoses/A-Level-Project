#===============================================================================
# GUI - Version 3
# 
# Adding image element
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
from resizeimage import resizeimage

LARGE_FONT= ("Verdana", 12)
imageHeight = 500

images = {} #makes dictionary for the images
images['main'] = Image.open("main.png")
images['north'] = Image.open("north.png")

images['main'] = resizeimage.resize_height(images['main'], imageHeight) #resizes the images so they fit on the screen
images['north'] = resizeimage.resize_height(images['north'], imageHeight)

globalImage = images['main'] #sets the current image using a global variable
frameBorderWidth = 5

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
        self.items['shapeResetButton']
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
# Items defined (all are actually just frames with things inside of them)
#
#       mapImage, mapTypeComboBox, shapeVertexRemoveButton,
#       shapeResetButton, hideParkingLayoutButton, goButton, tileScrollBox,
#       tileScrollBar, tileTypeComboBox, tileNumericStepper, tileAddButton,
#       tileResetButton
#
#-------------------------------------------------------------------------------

class mapImage(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add image to a canvas
        myFrame = tk.Frame(self)
        myFrame.pack()
        self.image = globalImage
        canvas = tk.Canvas(myFrame, width=self.image.size[0], height=self.image.size[1]) #image.size gives you the width and depth
        canvas.pack() #packs the canvas so it shows up
        self.image_tk = ImageTk.PhotoImage(self.image)
        canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.image_tk) #//2 needed in order to center the image
        #binds clicking on image to a procedure called clickedOnImage
        canvas.bind("<Button-1>", clickedOnImage) #<Button-1> is the left mouse button


class mapTypeComboBox(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="mapTypeComboBox", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items  


class shapeVertexRemoveButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Remove last vertex")
        #pack frames and items  
        button.pack(pady=10,padx=10)  


class shapeResetButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Reset car park shape")
        #pack frames and items  
        button.pack(pady=10,padx=10)  


class hideParkingLayoutButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Remove last vertex")
        #pack frames and items  
        button.pack(pady=10,padx=10)  


class goButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="goButton")
        #pack frames and items  
        button.pack(pady=10,padx=10)


class tileScrollBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="tileScrollBox", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items


class tileScrollBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="tileScrollBar", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items


class tileTypeComboBox(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="tileTypeComboBox", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items


class tileNumericStepper(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="tileNumericStepper", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items


class tileAddButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Remove last vertex")
        #pack frames and items  
        button.pack(pady=10,padx=10)  


class tileResetButton(tk.Frame):
    def __init__(self, parent, designingCarPark):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        if designingCarPark:
            button = tk.Button(self, text="tileResetButton")
        else:
            button = tk.Button(self, text="tileResetButton", state='disabled')
        #pack frames and items  
        button.pack(pady=10,padx=10)


        
#-------------------------------------------------------------------------------
# Functions for certain button clicks
#-------------------------------------------------------------------------------

def clickedOnImage(event):
  print "coords: " + str(event.x) + "," + str(event.y)

def callback():
    print "button pressed"
        
#-------------------------------------------------------------------------------
# Window created and mainloop started.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    window = tk.Tk()
    mainFrame(window,True).pack(side="top", fill="both", expand=True)
    window.mainloop()
