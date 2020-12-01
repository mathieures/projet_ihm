import tkinter as tk
import Grille
import Cube

def placerCube(pcoordsGrille):
	"""Prend en parametre des coordonnes de grille (peut-etre a changer ?)"""
	print("		placed cube at :",grille.closestPoint(pcoordsGrille))
	return Cube.Cube(canv,grille,grille.closestPoint(pcoordsGrille))


def onClick(event):
    currentCoords = (event.x,event.y)
    convertedCoords = grille.canvasToGrille((currentCoords))
    print("click on :",currentCoords,"=>",convertedCoords)
    placerCube(convertedCoords)

# Root

root = tk.Tk()
# root.geometry("300x300")

# Canvas

canv = tk.Canvas(root,width=500,height=500,bg="white")
canv.bind("<1>",onClick)

grille = Grille.Grille(canv)

# cube1 = Cube.Cube(canv,grille,(1,1))


canv.pack()
# print("is ready :",isReadyToDraw)


# Fin

root.mainloop()

exit(0)
