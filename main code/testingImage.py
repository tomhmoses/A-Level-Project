import Tkinter as tk
from PIL import Image, ImageTk

coordsClicked = []

def clickedOnImage(event):
  print "coords: " + str(event.x) + "," + str(event.y)

class mapImage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #add image to a canvas
        myFrame = tk.Frame(self)
        myFrame.pack()
        self.image = Image.open("test.jpg") #creates an instance of an image class
        canvas = tk.Canvas(myFrame, width=self.image.size[0], height=self.image.size[1]) #image.size gives you the width and depth
        canvas.pack()
        self.image_tk = ImageTk.PhotoImage(self.image)
        canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.image_tk) #//2 needed in order to center the image

        canvas.bind("<Button-1>", clickedOnImage) #<Button-1> is the left mouse button



window = tk.Tk()
mapImage(window).pack(side="top", fill="both", expand=True)
window.mainloop()


