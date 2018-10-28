#===============================================================================
# GUI - Version 1
# 
# Starting out adding basic frames
#
#===============================================================================



#-------------------------------------------------------------------------------
# Importing required modules
#     PIL: For opening and editing image (will use this in a later version)
# Tkinter: Provides UI framework (will use this in a later version)
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk, ImageDraw
import Tkinter as tk

LARGE_FONT= ("Verdana", 12)


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
        label = tk.Label(self, text="templateFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items   



class mainFrame(tk.Frame): #need to add navbar
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="mainFame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #self.items['navBar'] = navBar(self)
        self.frames['majoirtyFrame'] = majorityFrame(self)
        #pack frames and items
        #self.items['navBar'].pack(side="top", fill="both", expand=True)
        self.frames['majoirtyFrame'].pack(side="top", fill="both", expand=True)     


class majorityFrame(tk.Frame): #done
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="majorityFame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.frames['leftFrame'] = leftFrame(self)
        self.frames['rightFrame'] = rightFrame(self)
        #pack frames and items
        self.frames['leftFrame'].pack(side="left", fill="both", expand=True)
        self.frames['rightFrame'].pack(side="left", fill="both", expand=True)  


class leftFrame(tk.Frame): #done
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="leftFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['mapImage'] = mapImage(self)
        self.frames['bottomLeftFrame'] = bottomLeftFrame(self)
        #pack frames and items
        self.items['mapImage'].pack(side="top", fill="both", expand=True) 
        self.frames['bottomLeftFrame'].pack(side="top", fill="both", expand=True)


class bottomLeftFrame(tk.Frame): #done
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="bottomLeftFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.frames['mapOptionsFrame'] = mapOptionsFrame(self)
        self.items['goButton'] = goButton(self)
        #pack frames and items
        self.frames['mapOptionsFrame'].pack(side="left", fill="both", expand=True)
        self.items['goButton'].pack(side="left", fill="both", expand=True)


class mapOptionsFrame(tk.Frame): #need to find how to pack hideParkingLayoutButton to bottom.
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="mapOptionsFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['mapTypeComboBox'] = mapTypeComboBox(self) #needs making
        self.items['shapeVertexRemoveButton'] = tk.Button(self, text="Remove last vertex", command=callback)
        self.items['shapeResetButton'] = tk.Button(self, text="Reset car park shape", command=callback)
        self.items['hideParkingLayoutButton'] = tk.Button(self, text="Hide car park tile layout", state='disabled')
        #pack frames and items
        self.items['mapTypeComboBox'].pack(side="top", fill="both", expand=True)
        self.items['shapeVertexRemoveButton'].pack(side="top", fill="both", expand=True)
        self.items['shapeResetButton']
        self.items['hideParkingLayoutButton'].pack(side="bottom", fill="both", expand=True)


        

class rightFrame(tk.Frame): #done
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label
        label = tk.Label(self, text="rightFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['tileLabel'] = tileLabel(self)
        self.frames['tileScrollBoxFrame'] = tileScrollBoxFrame(self)
        self.frames['tileOptionsFrame'] = tileOptionsFrame(self)
        self.items['tileResetButton'] = tileResetButton(self)
        #pack frames and items
        self.items['tileLabel'].pack(side="top", fill="both", expand=True)
        self.frames['tileScrollBoxFrame'].pack(side="top", fill="both", expand=True)
        self.frames['tileOptionsFrame'].pack(side="top", fill="both", expand=True)
        self.items['tileResetButton'].pack(side="top", fill="both", expand=True)
        
        

class tileScrollBoxFrame(tk.Frame): #done
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
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
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="tileOptionsFrame", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        self.items['tileTypeComboBox'] = tileTypeComboBox(self)
        self.items['tileNumericStepper'] = tileTypeComboBox(self)
        self.items['tileTypeComboBox'] = tileTypeComboBox(self)
        #pack frames and items
        self.items['tileTypeComboBox'].pack(side="top", fill="both", expand=True)
        self.items['tileNumericStepper'].pack(side="top", fill="both", expand=True)
        self.items['tileTypeComboBox'].pack(side="top", fill="both", expand=True)          


#-------------------------------------------------------------------------------
# Items defined
#
#       mapImage, mapTypeComboBox, shapeVertexRemoveButton,
#       shapeResetButton, hideParkingLayoutButton, tileLabel, tileScrollBar,
#       tileScrollBox, tileTypeComboBox, tileNumericStepper, tileAddButton,
#       tileResetButton
#
#-------------------------------------------------------------------------------

class mapImage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add label  
        label = tk.Label(self, text="mapImage", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add frames and items
        #pack frames and items


class mapTypeComboBox(tk.Frame):
    def __init__(self, parent):
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
    def __init__(self, parent, state):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Remove last vertex", state=state)
        #pack frames and items  
        button.pack(pady=10,padx=10)  


class shapeResetButton(tk.Frame):
    def __init__(self, parent, enabled):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Reset car park shape", state=state)
        #pack frames and items  
        button.pack(pady=10,padx=10)  


class hideParkingLayoutButton(tk.Frame):
    def __init__(self, parent, enabled):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Remove last vertex", state=state)
        #pack frames and items  
        button.pack(pady=10,padx=10)  


class shapeVertexRemoveButton(tk.Frame):
    def __init__(self, parent, enabled):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frames = {}
        self.items = {}
        #add frames and items
        button = tk.Button(self, text="Hide car park tile layout", state=state)
        #pack frames and items  
        button.pack(pady=10,padx=10)


def callback():
    print "button clicked"


        
#-------------------------------------------------------------------------------
# Window created and mainloop started.
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    window = tk.Tk()
    mainFrame(window).pack(side="top", fill="both", expand=True)
    window.mainloop()
