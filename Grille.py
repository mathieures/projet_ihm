import tkinter as tk
class Grille:

	def dessineGrille(self,pcanvas):
		x = self.origine[0]
		y = self.origine[1]
		d = self.definition
		for i in range(self.taille_y+1):
			pcanvas.create_line(x,y,x+d*self.taille_y,y+(d*self.taille_y/2))
			x -= d
			y += d/2
		x = self.origine[0]
		y = self.origine[1]
		for j in range(self.taille_x+1):
			pcanvas.create_line(x,y,x-d*self.taille_x,y+(d*self.taille_x/2))
			x += d
			y += d/2

	def convertTkCoords(self,pcoords):
		"""
		Convertit des coordonnees du referentiel tkinter
		vers des coordonnees de la Grille (2D)
		"""
		x = pcoords[0]
		y = pcoords[1]
		return (self.dico[(x,y)])

	def convertGrilleCoords(self,pcoords):
		"""
		Convertit des coordonnees de la Grille (2D)
		vers des coordonnees du referentiel tkinter
		"""
		x = pcoords[0]
		y = pcoords[1]
		if(x >= self.taille_x or y >= self.taille_y or x < 0 or y < 0):
			print("Mauvaises coordonnees")
			exit(1)
		d = self.definition
		return(self.origine[0]-d*x + d * y, self.origine[1] + d * y/2 + d * x/2)

	def createDico(self):
		d = {}
		for i in range(self.taille_x):
			for j in range(self.taille_y):
				d[self.convertGrilleCoords((i,j))] = (i,j)
		return(d)


	def __init__(self,pcanvas,pdefinition=20,ptaille_x=10,ptaille_y=10):
		self.definition = pdefinition # taille des cotes d'un carre
		self.taille_x = ptaille_x # nombre de cases suivant l'axe x (qui va en bas à droite)
		self.taille_y = ptaille_y # nombre de cases suivant l'axe y (qui va en bas à gauche)
		self.origine = (int(pcanvas.cget("width")) / 2,int(pcanvas.cget("height")) / 4) # coordonnees de l'origine (dans le referentiel tkinter)
		self.dico = self.createDico()
		print("origine :",self.origine,"; definition :",self.definition)
		# pcanvas.create_line(self.origine,self.convertGrilleCoords((self.origine[0],self.origine[1]+10)))
		# dessin de la grille
		self.dessineGrille(pcanvas)
