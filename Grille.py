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
		return ((pcoords[0] - self.origine[0]) / self.definition, (pcoords[1] - self.origine[1]) / self.definition / 2)

	def convertGrilleCoords(self,pcoords):
		"""
		Convertit des coordonnees du referentiel tkinter
		vers des coordonnees de la Grille (2D)
		"""
		return (pcoords[0] * self.definition, (pcoords[1] * self.definition)*2)

	def __init__(self,pcanvas):
		self.definition = 26 # taille des cotes d'un carre
		self.taille_x = 3 # nombre de cases suivant l'axe x (qui va en bas à droite)
		self.taille_y = 3 # nombre de cases suivant l'axe y (qui va en bas à gauche)

		self.origine = (int(pcanvas.cget("width")) / 2,int(pcanvas.cget("height")) / 4) # coordonnees de l'origine (dans le referentiel tkinter)
		print("origine :",self.origine,"; definition :",self.definition)
		# pcanvas.create_line(self.origine,self.convertGrilleCoords((self.origine[0],self.origine[1]+10)))
		# dessin de la grille
		self.dessineGrille(pcanvas)
