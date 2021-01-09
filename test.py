import tkinter as tk
import Grille

class Cube:

	def __init__(self,pcanv,pgrille,pcoords):
		print(pcoords)
		self.coords = pgrille.convertGrilleCoords(pcoords)
		print(self.coords)
		self.canv = pcanv
		self.definition = pgrille.definition
		self.dessine()

	def dessine(self):
		x = self.coords[0]
		y = self.coords[1]
		d = self.definition
		AB = [x-d,y-d/2]
		EB = [x+d,y-d/2]
		AC = [x-d,y+d/2]
		EC = [x+d,y+d/2]
		xD = [x,y+d]
		xF = [x,y-d]
		haut = self.canv.create_polygon(x,y,EB,xF,AB,fill='#afafaf')
		gauche = self.canv.create_polygon(x,y,AB, AC, xD,fill='#414141')
		droite = self.canv.create_polygon(x,y,EB,EC, xD,fill='#808080')

def placer(event,grille):
	c = grille.convertTkCoords((event.x,event.y))
	x = c[0]
	y = c[1]
	print(x,y)
	Cube(pcanv=canv,pgrille=grille,pcoords=(x,y))


root = tk.Tk()
root.title("Test")
canv = tk.Canvas(root, width=800,height=800)

G = Grille.Grille(pcanvas=canv)
print(G.dico)
canv.bind("<Button-1>",lambda event: placer(event,grille=G))
canv.pack()
root.mainloop()
exit(0)
